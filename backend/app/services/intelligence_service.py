from __future__ import annotations

import math
import statistics
from itertools import combinations

import numpy as np
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.analytics.clustering import compute_kmeans
from app.analytics.inferential import compute_spearman
from app.analytics.multiple_testing import adjust_pvalues_bh
from app.analytics.normality import compute_normality
from app.analytics.reliability import compute_reliability
from app.core.exceptions import NotFoundError, ValidationDomainError
from app.models.analysis import AnalysisRun
from app.models.censopas import ConstructScore
from app.models.construct import Construct
from app.models.project import Project
from app.models.response import Response
from app.models.study import Study


def _round(value: float | None, digits: int = 3) -> float | None:
    if value is None or not math.isfinite(value):
        return None
    return round(float(value), digits)


def _bootstrap_median_ci(values: list[float], seed: int) -> tuple[float | None, float | None]:
    if len(values) < 5:
        return None, None
    rng = np.random.default_rng(seed)
    data = np.asarray(values, dtype=float)
    samples = rng.choice(data, size=(400, len(data)), replace=True)
    medians = np.median(samples, axis=1)
    return float(np.quantile(medians, 0.025)), float(np.quantile(medians, 0.975))


def _robust_outliers(values: list[float]) -> list[int]:
    if len(values) < 5:
        return []
    data = np.asarray(values, dtype=float)
    median = float(np.median(data))
    mad = float(np.median(np.abs(data - median)))
    if mad > 0:
        robust_z = 0.6745 * (data - median) / mad
        return [index for index, value in enumerate(robust_z) if abs(value) > 3.5]
    q1, q3 = np.quantile(data, [0.25, 0.75])
    iqr = float(q3 - q1)
    if iqr <= 0:
        return []
    lower, upper = float(q1 - 1.5 * iqr), float(q3 + 1.5 * iqr)
    return [index for index, value in enumerate(data) if value < lower or value > upper]


def _silhouette(points: np.ndarray, labels: np.ndarray) -> float | None:
    if len(points) < 3 or len(set(labels.tolist())) < 2:
        return None
    distances = np.linalg.norm(points[:, None, :] - points[None, :, :], axis=2)
    values: list[float] = []
    for index, label in enumerate(labels):
        same = np.where(labels == label)[0]
        same = same[same != index]
        if not len(same):
            values.append(0.0)
            continue
        a = float(distances[index, same].mean())
        other_means = [float(distances[index, labels == other].mean()) for other in set(labels.tolist()) if other != label]
        b = min(other_means)
        values.append((b - a) / max(a, b) if max(a, b) else 0.0)
    return float(np.mean(values))


class IntelligenceService:
    """Resumen analítico de solo lectura sobre la última corrida de scoring.

    No persiste asignaciones de clúster ni devuelve filas individuales. Todas
    las salidas están agregadas y heredan el mínimo publicable del estudio.
    """

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def build(self, study_id: int) -> dict:
        study = await self.session.get(Study, study_id)
        if study is None:
            raise NotFoundError(f"Estudio {study_id} no encontrado")
        project = await self.session.get(Project, study.project_id)
        run_stmt = (
            select(AnalysisRun)
            .where(
                AnalysisRun.study_id == study_id,
                AnalysisRun.analysis_type.in_(("CENSOPAS_SCORING", "LIKERT_SCORING")),
                AnalysisRun.status == "COMPLETED",
            )
            .order_by(AnalysisRun.completed_at.desc(), AnalysisRun.id.desc())
        )
        scoring_run = (await self.session.execute(run_stmt)).scalars().first()
        if scoring_run is None:
            raise ValidationDomainError("El estudio todavía no tiene scoring completo.")

        construct_stmt = (
            select(Construct)
            .where(
                Construct.instrument_version_id == study.instrument_version_id,
                Construct.construct_type == "DIMENSION",
            )
            .options(selectinload(Construct.item_links))
            .order_by(Construct.sort_order, Construct.id)
        )
        dimensions = list((await self.session.execute(construct_stmt)).scalars().all())
        dimension_ids = [item.id for item in dimensions]
        score_stmt = select(ConstructScore).where(
            ConstructScore.analysis_run_id == scoring_run.id,
            ConstructScore.construct_id.in_(dimension_ids),
            ConstructScore.score_0_100.is_not(None),
        )
        scores = list((await self.session.execute(score_stmt)).scalars().all())
        series: dict[int, dict[int, float]] = {item.id: {} for item in dimensions}
        for score in scores:
            series[score.construct_id][score.response_session_id] = float(score.score_0_100)

        valid_session_ids = sorted({score.response_session_id for score in scores})
        response_rows = []
        all_item_ids = sorted({link.question_id for dimension in dimensions for link in dimension.item_links})
        if valid_session_ids and all_item_ids:
            response_stmt = select(
                Response.response_session_id,
                Response.question_id,
                Response.numeric_value,
            ).where(
                Response.study_id == study_id,
                Response.response_session_id.in_(valid_session_ids),
                Response.question_id.in_(all_item_ids),
                Response.numeric_value.is_not(None),
                Response.is_missing.is_(False),
            )
            response_rows = list((await self.session.execute(response_stmt)).all())
        answers: dict[int, dict[int, float]] = {}
        for session_id, question_id, numeric_value in response_rows:
            answers.setdefault(session_id, {})[question_id] = float(numeric_value)

        dimension_results = []
        total_outliers: set[int] = set()
        non_normal = 0
        for index, dimension in enumerate(dimensions):
            values_by_session = series.get(dimension.id, {})
            values = list(values_by_session.values())
            normality = compute_normality(values, histogram_bins=12)
            if normality["status"] == "NO_NORMAL":
                non_normal += 1
            outlier_indices = _robust_outliers(values)
            session_keys = list(values_by_session)
            total_outliers.update(session_keys[item] for item in outlier_indices)
            clean_values = [value for item, value in enumerate(values) if item not in set(outlier_indices)]
            median_ci = _bootstrap_median_ci(values, seed=2026 + index)

            item_ids = [link.question_id for link in dimension.item_links]
            item_matrix = [
                [answers[session_id][question_id] for question_id in item_ids]
                for session_id in valid_session_ids
                if item_ids and all(question_id in answers.get(session_id, {}) for question_id in item_ids)
            ]
            reliability = compute_reliability(item_matrix)
            alpha = reliability.get("cronbach_alpha")
            omega = reliability.get("mcdonald_omega")
            reliability_status = (
                "SÓLIDA" if alpha is not None and omega is not None and min(alpha, omega) >= 0.8
                else "ACEPTABLE" if alpha is not None and alpha >= 0.7
                else "REVISAR"
            )
            dimension_results.append({
                "construct_id": dimension.id,
                "code": dimension.code,
                "name": dimension.name,
                "n": len(values),
                "mean": _round(statistics.fmean(values) if values else None, 2),
                "median": _round(statistics.median(values) if values else None, 2),
                "median_ci_lower": _round(median_ci[0], 2),
                "median_ci_upper": _round(median_ci[1], 2),
                "standard_deviation": _round(normality["standard_deviation"], 2),
                "normality_test": normality["test"],
                "normality_p": _round(normality["p_value"], 4),
                "normality_status": normality["status"],
                "outlier_count": len(outlier_indices),
                "sensitivity_mean": _round(statistics.fmean(clean_values) if clean_values else None, 2),
                "sensitivity_delta": _round(
                    abs(statistics.fmean(values) - statistics.fmean(clean_values))
                    if values and clean_values else None,
                    2,
                ),
                "alpha": _round(alpha),
                "omega": _round(omega),
                "reliability_status": reliability_status,
                "n_items": reliability.get("n_items", 0),
            })

        correlation_rows = []
        raw_p_values = []
        pair_payloads = []
        for left, right in combinations(dimensions, 2):
            common = sorted(set(series[left.id]) & set(series[right.id]))
            if len(common) < study.min_publishable_n:
                continue
            computed = compute_spearman(
                [series[left.id][session_id] for session_id in common],
                [series[right.id][session_id] for session_id in common],
            )
            raw_p_values.append(computed["p_value"])
            pair_payloads.append((left, right, len(common), computed))
        adjusted = adjust_pvalues_bh(raw_p_values)
        for (left, right, n, computed), adjusted_p in zip(pair_payloads, adjusted, strict=True):
            rho = float(computed["statistic"])
            correlation_rows.append({
                "x": left.code,
                "x_name": left.name,
                "y": right.code,
                "y_name": right.name,
                "n": n,
                "rho": _round(rho),
                "p_value": _round(computed["p_value"], 4),
                "adjusted_p_value": _round(adjusted_p, 4),
                "significant": adjusted_p < 0.05,
                "magnitude": "FUERTE" if abs(rho) >= 0.5 else "MODERADA" if abs(rho) >= 0.3 else "DÉBIL" if abs(rho) >= 0.1 else "DESPRECIABLE",
            })
        correlation_rows.sort(key=lambda item: abs(item["rho"] or 0), reverse=True)

        common_sessions = sorted(set.intersection(*(set(series[item.id]) for item in dimensions))) if dimensions else []
        cluster_summary = {"status": "NO_DISPONIBLE", "reason": "Muestra o matriz insuficiente", "k": None, "silhouette": None, "profiles": []}
        if len(common_sessions) >= max(30, study.min_publishable_n * 3) and len(dimensions) >= 2:
            raw = np.asarray([[series[item.id][session_id] for item in dimensions] for session_id in common_sessions], dtype=float)
            medians = np.median(raw, axis=0)
            q1, q3 = np.quantile(raw, [0.25, 0.75], axis=0)
            scale = np.where((q3 - q1) > 0, q3 - q1, 1.0)
            standardized = (raw - medians) / scale
            clustering = compute_kmeans(standardized.tolist(), k=3, seed=2026)
            labels = np.asarray(clustering["labels"], dtype=int)
            profiles = []
            for cluster_id in range(3):
                cluster_rows = raw[labels == cluster_id]
                centroid = cluster_rows.mean(axis=0)
                risk_index = float(centroid.mean())
                profiles.append({
                    "cluster_id": cluster_id + 1,
                    "n": int(len(cluster_rows)),
                    "risk_index": _round(risk_index, 1),
                    "centroids": {dimension.code: _round(value, 1) for dimension, value in zip(dimensions, centroid, strict=True)},
                })
            ordered = sorted(profiles, key=lambda item: item["risk_index"])
            labels_by_id = {ordered[0]["cluster_id"]: "Perfil protector", ordered[1]["cluster_id"]: "Exposición intermedia", ordered[2]["cluster_id"]: "Prioridad preventiva"}
            for profile in profiles:
                profile["label"] = labels_by_id[profile["cluster_id"]]
            cluster_summary = {
                "status": "AVAILABLE",
                "reason": "K-means exploratorio sobre puntajes dimensionales robustamente escalados.",
                "k": 3,
                "silhouette": _round(_silhouette(standardized, labels)),
                "profiles": sorted(profiles, key=lambda item: item["risk_index"], reverse=True),
            }

        thresholds = {
            "coverage_target": 85,
            "coverage_critical": 65,
            "completion_target": 90,
            "risk_warning": 35,
            "risk_critical": 50,
            **(((project.metadata_ or {}).get("thresholds") or {}) if project else {}),
        }
        return {
            "study_id": study_id,
            "analysis_run_id": scoring_run.id,
            "algorithm_version": scoring_run.algorithm_version,
            "engine": "Python · NumPy · SciPy",
            "n": len(valid_session_ids),
            "min_publishable_n": study.min_publishable_n,
            "thresholds": thresholds,
            "dimensions": dimension_results,
            "correlations": correlation_rows,
            "clustering": cluster_summary,
            "quality": {
                "outlier_sessions": len(total_outliers),
                "outlier_pct": _round(len(total_outliers) / len(valid_session_ids) * 100 if valid_session_ids else 0, 1),
                "non_normal_dimensions": non_normal,
                "sensitivity_max_delta": _round(max((item["sensitivity_delta"] or 0) for item in dimension_results), 2) if dimension_results else None,
            },
            "decision": {
                "normality_summary": f"{non_normal} de {len(dimensions)} dimensiones no son compatibles con normalidad.",
                "recommended_comparison": "Mann–Whitney / Kruskal–Wallis" if non_normal else "Welch / ANOVA con verificación de varianzas",
                "recommended_correlation": "Spearman con ajuste Benjamini–Hochberg",
                "outlier_policy": "No excluir automáticamente; comparar estimadores clásicos y robustos.",
            },
            "limitations": [
                "Resultados sintéticos y exploratorios; no sustituyen el baremo oficial.",
                "Omega usa una aproximación unifactorial por componentes principales, no CFA robusto.",
                "Los clústeres describen perfiles agregados y no se usan para decisiones individuales.",
                "No se interpreta causalidad a partir de asociaciones transversales.",
            ],
        }
