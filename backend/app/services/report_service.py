"""ReportService (harness §39).

Ensambla un *bundle* (estudio + resultados de análisis ya persistidos +
resultados CENSOPAS con privacidad aplicada + `barem_results`/baremación) y
lo renderiza al formato pedido:
  - DOCX (default): Word con ficha técnica, tabla de baremación por
    dimensión y gráficas embebidas (`report_docx.py`).
  - JSON: el mismo bundle sin renderizar, para integraciones.
No se recalcula estadística durante la generación, sólo se ensamblan
resultados ya persistidos (`responses -> analysis_run -> analysis_results ->
report_run`, harness).
"""

from __future__ import annotations

import hashlib
import json
from datetime import UTC, datetime
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.action_plan_status import compute_effective_status
from app.core.config import get_settings
from app.core.exceptions import ConflictError, NotFoundError
from app.models.analysis import AnalysisResult, AnalysisRun
from app.models.bsc import ActionPlan, ActionPlanItem, Kpi
from app.models.censopas import Barem
from app.models.construct import Construct
from app.models.project import Project
from app.models.user import Organization, User
from app.repositories.analytics import AnalyticsRepository
from app.repositories.reports import ReportRepository
from app.repositories.studies import StudyRepository
from app.schemas.reports import ReportRunCreate, ReportTemplateCreate
from app.services.censopas_methodology import (
    resolve_censopas_methodological_status,
    resolve_official_equivalence_enabled,
)
from app.services.censopas_service import CensopasScoringService
from app.services.response_descriptive_service import ResponseDescriptiveService
from app.services.scoring_service import ScoringService
from app.services.telemetry_service import TelemetryService

# Fase 4: separar D1-D6 de S1-S20 en cualquier consumidor del bundle —
# nunca filtrar por posición en la lista, siempre por `construct_type` real.
_DIMENSION_TYPE = "DIMENSION"
_SUBDIMENSION_TYPE = "SUBDIMENSION"

_CONFIDENTIALITY_NOTICE = (
    "Documento de uso interno del Comité/Grupo de Trabajo de Seguridad y Salud en el "
    "Trabajo. Contiene resultados colectivos únicamente — no incluye identificadores "
    "de participantes ni registros individuales."
)


def _trichotomy_lines(results: list[dict], min_publishable_n: int | None) -> list[str]:
    """Fase 11: misma fuente y mismos campos que la tabla DOCX
    (`favorable/intermediate/unfavorable_pct` + n válido + clasificación
    colectiva) — antes el PDF usaba menos campos que el DOCX, esto cierra
    GAP-REPORT-PDF-PARITY para D1-D6/S1-S20."""
    lines = []
    for result in results:
        code = result.get("construct_code") or "—"
        name = result.get("construct_name") or "—"
        if result.get("suppressed"):
            hidden = f"Oculto (n<{min_publishable_n})" if min_publishable_n else "Oculto"
            lines.append(f"{code} · {name} · {hidden}")
            continue
        classification = _CLASSIFICATION_LABELS_PDF.get(
            result.get("collective_classification"), result.get("collective_classification") or "—"
        )
        lines.append(
            f"{code} · {name} · Favorable {result.get('favorable_n', '—')} "
            f"({_pct(result.get('favorable_pct'))}) · Intermedio {result.get('intermediate_n', '—')} "
            f"({_pct(result.get('intermediate_pct'))}) · Desfavorable {result.get('unfavorable_n', '—')} "
            f"({_pct(result.get('unfavorable_pct'))}) · n válido={result.get('n_valid', '—')} · "
            f"clasificación={classification}"
        )
    return lines


def _pct(value: float | None) -> str:
    return f"{value:.1f}%" if value is not None else "—"


_CLASSIFICATION_LABELS_PDF = {
    "RIESGO_ALTO": "Riesgo alto",
    "FACTOR_PROTECTOR": "Factor protector",
    "RIESGO_MEDIO": "Riesgo medio",
    "REVISION": "Requiere revisión",
}


def _render_report_pdf(bundle: dict) -> bytes:
    """Render PDF multipágina desde el mismo bundle, sin datos individuales.
    Fase 11: mismas secciones metodológicas que el DOCX — el layout es texto
    plano por página, pero el contenido (perfil sociolaboral, D1-D6/S1-S20
    separados, interpretación, priorización, plan preventivo completo,
    conclusiones) es semánticamente equivalente."""
    import io
    import textwrap

    import matplotlib.pyplot as plt
    from matplotlib.backends.backend_pdf import PdfPages

    output = io.BytesIO()
    selected_sections = set(bundle.get("sections") or [])
    pages_rendered = 0

    def add_page(pdf, title: str, lines: list[str], section_keys: set[str] | None) -> None:
        nonlocal pages_rendered
        if section_keys is not None and selected_sections and not selected_sections.intersection(section_keys):
            return
        pages_rendered += 1
        figure = plt.figure(figsize=(8.27, 11.69), dpi=120)
        figure.patch.set_facecolor("white")
        figure.text(0.08, 0.94, title, fontsize=18, fontweight="bold", color="#1C1F24")
        y = 0.89
        for line in lines:
            wrapped = textwrap.wrap(str(line), width=105) or [""]
            for part in wrapped:
                figure.text(0.08, y, part, fontsize=9.5, color="#374151")
                y -= 0.024
            y -= 0.008
            if y < 0.08:
                break
        figure.text(0.08, 0.035, "Colmena · CENSOPAS-COPSOQ", fontsize=8, color="#6B7280")
        pdf.savefig(figure, bbox_inches="tight")
        plt.close(figure)

    with PdfPages(output) as pdf:
        study = bundle.get("study") or {}
        cover = bundle.get("cover") or {}
        label = bundle.get("methodological_label") or {}
        equivalence_line = (
            "Equivalente al resultado oficial CENSOPAS-COPSOQ"
            if label.get("official_equivalence")
            else "No equivalente al resultado oficial CENSOPAS-COPSOQ"
        )
        add_page(
            pdf,
            study.get("name") or "Reporte",
            [
                f"{label.get('label', 'Baremo de referencia')} — {equivalence_line}",
                f"Instrumento: {cover.get('instrument_label') or 'CENSOPAS-COPSOQ'} · "
                f"Versión: {cover.get('version_kind') or 'UNKNOWN'}",
                f"Organización: {cover.get('organization_name') or '—'}",
                f"Código del estudio: {cover.get('study_code') or '—'}",
                f"Período: {cover.get('period_start') or '—'} – {cover.get('period_end') or '—'}",
                f"Evaluador/responsable: {cover.get('evaluator_label') or '—'}",
                f"Generado: {bundle.get('generated_at', '—')}",
                cover.get("confidentiality_notice") or "",
            ],
            {"portada"},
        )
        summary = bundle.get("executive_summary") or {}
        summary_lines = [summary.get("headline") or "Sin datos suficientes para un resumen."]
        if summary.get("n_valid") is not None:
            summary_lines.append(f"Respuestas válidas: {summary['n_valid']}")
        if summary.get("completion_rate") is not None:
            summary_lines.append(f"Tasa de finalización: {summary['completion_rate'] * 100:.1f}%")
        summary_lines.append(
            f"Baremo: {summary.get('barem_status') or '—'} · "
            f"Equivalencia oficial: {'sí' if summary.get('official_equivalence') else 'no'}"
        )
        for dimension in summary.get("priority_dimensions") or []:
            dim_label = dimension.get("construct_name") or dimension.get("construct_code") or "—"
            pct = dimension.get("unfavorable_pct")
            pct_label = f"{pct:.1f}%" if pct is not None else "—"
            summary_lines.append(
                f"Prioritaria: {dim_label} · {pct_label} desfavorable · {dimension.get('classification') or '—'}"
            )
        add_page(pdf, "Resumen ejecutivo", summary_lines, {"resumen_ejecutivo"})

        readiness = bundle.get("methodological_status") or {}
        add_page(
            pdf,
            "Estado metodológico",
            [
                f"Versión: {readiness.get('version_kind', 'UNKNOWN')}",
                f"Listo para scoring: {readiness.get('ready_for_scoring', False)}",
                f"Baremo: {label.get('label', 'Baremo de referencia')}. {equivalence_line}.",
                "Bloqueos: " + ", ".join(readiness.get("errors", [])),
                "Advertencias: " + ", ".join(readiness.get("warnings", [])),
            ],
            {"trazabilidad", "ficha_tecnica"},
        )

        data_quality = bundle.get("data_quality") or {}
        traceability = bundle.get("traceability") or {}
        min_publishable_n = (traceability.get("privacy") or {}).get("min_publishable_n")
        barem_trace = traceability.get("barem") or {}
        add_page(
            pdf,
            "Ficha técnica",
            [
                f"Instrumento: {study.get('instrument_name') or 'CENSOPAS-COPSOQ'}",
                f"Versión del instrumento: {study.get('instrument_version_code') or '—'}",
                "Población convocada: No disponible en el sistema (sin registro de convocatoria)",
                f"Respondieron (sesiones iniciadas): {data_quality.get('started_count', '—')}",
                f"Válidos: {data_quality.get('valid_count', '—')}",
                f"Excluidos: {data_quality.get('excluded_count', '—')}",
                "Tasa válida: " + _format_percentage_pdf(data_quality.get("completion_rate")),
                f"Baremo aplicado: {barem_trace.get('name') or '—'}",
                f"Equivalencia oficial: {'habilitada' if label.get('official_equivalence') else 'no habilitada'}",
                f"N mínimo publicable: {min_publishable_n if min_publishable_n is not None else '—'}",
            ],
            {"ficha_tecnica"},
        )

        add_page(
            pdf,
            "Calidad de datos",
            [
                f"Sesiones iniciadas: {data_quality.get('started_count', '—')}",
                f"Completadas: {data_quality.get('completed_count', '—')}",
                f"Válidas: {data_quality.get('valid_count', '—')}",
                f"Abandonadas: {data_quality.get('abandoned_count', '—')}",
                f"En revisión: {data_quality.get('review_count', '—')}",
                f"Excluidas: {data_quality.get('excluded_count', '—')}",
                "Tasa de finalización: " + _format_percentage_pdf(data_quality.get("completion_rate")),
            ]
            if data_quality
            else ["Todavía no hay telemetría persistida para este estudio."],
            {"calidad_datos"},
        )

        sociolaboral_lines = []
        for question in bundle.get("sociolaboral_profile") or []:
            for category in question.get("categories") or []:
                if category.get("suppressed"):
                    sociolaboral_lines.append(
                        f"{question.get('label')} · {category.get('label')} · Oculto (n<{min_publishable_n})"
                    )
                else:
                    sociolaboral_lines.append(
                        f"{question.get('label')} · {category.get('label')} · "
                        f"n={category.get('n')} ({_pct(category.get('percentage'))})"
                    )
        add_page(
            pdf,
            "Perfil sociolaboral",
            sociolaboral_lines
            or ["Este estudio no tiene variables sociolaborales descriptivas provisionadas."],
            {"variables_descriptivas"},
        )

        dimension_results = bundle.get("dimension_results") or []
        add_page(
            pdf,
            "Resultados por dimensión (D1-D6)",
            _trichotomy_lines(dimension_results, min_publishable_n)
            or ["Este estudio todavía no tiene resultados por dimensión calculados."],
            {"dimensiones", "resultados_globales"},
        )

        if cover.get("version_kind") == "MEDIUM":
            subdimension_results = bundle.get("subdimension_results") or []
            add_page(
                pdf,
                "Resultados por subdimensión (S1-S20)",
                _trichotomy_lines(subdimension_results, min_publishable_n)
                or ["Este estudio todavía no tiene resultados por subdimensión calculados."],
                {"subdimensiones"},
            )

        interpretation_lines = []
        for entry in bundle.get("interpretation") or []:
            interpretation_lines.append(
                f"{entry.get('construct_name') or entry.get('construct_code') or '—'} — "
                f"Hallazgo: {entry.get('finding') or '—'}"
            )
            if entry.get("classification"):
                interpretation_lines.append(f"  Clasificación: {entry['classification']}")
            hypotheses = entry.get("origin_hypothesis") or []
            interpretation_lines.append(
                "  Hipótesis de origen a contrastar: "
                + ("; ".join(hypotheses) if hypotheses else "sin registrar todavía.")
            )
            orientations = entry.get("preventive_orientation") or []
            interpretation_lines.append(
                "  Orientación preventiva: " + ("; ".join(orientations) if orientations else "—")
            )
            interpretation_lines.append(f"  Limitación: {entry.get('limitation') or '—'}")
        add_page(
            pdf,
            "Interpretación de resultados",
            interpretation_lines or ["Sin resultados publicables todavía para interpretar."],
            {"dimensiones", "resultados_globales", "subdimensiones"},
        )

        priority_lines = [
            "El siguiente orden es una ayuda de priorización preventiva calculada por el "
            "backend; no es una clasificación oficial adicional de CENSOPAS-COPSOQ."
        ]
        for row in bundle.get("priority_ranking") or []:
            priority_lines.append(
                f"#{row.get('priority_rank') or '—'} · {row.get('construct_code') or ''} "
                f"{row.get('construct_name') or '—'} · {_pct(row.get('unfavorable_pct'))} desfavorable · "
                f"n={row.get('n_valid') or '—'}"
            )
        add_page(
            pdf,
            "Priorización preventiva",
            priority_lines,
            {"dimensiones", "resultados_globales", "subdimensiones"},
        )

        analysis_lines = [
            f"{result.get('result_code') or '—'} · {result.get('result_type', '—')} · "
            f"n={result.get('n_valid', '—')} · p={result.get('p_value', '—')}"
            for result in (bundle.get("analysis_results") or [])[:50]
        ]
        if analysis_lines:
            add_page(pdf, "Resultados de análisis estadístico", analysis_lines, {"hallazgos_premium"})

        premium = bundle.get("premium_analytics") or {}
        premium_lines = [
            f"Estado: {premium.get('status') or 'NO_RESULTS'}",
            "Métodos: " + (", ".join(premium.get("methods") or []) or "—"),
            f"Resultados publicables: {premium.get('result_count', 0)}",
            f"Resultados significativos: {premium.get('significant_result_count', 0)}",
        ]
        for result in (premium.get("results") or [])[:50]:
            premium_lines.append(
                f"{result.get('result_code') or '—'} · {result.get('result_type') or '—'} · "
                f"n={result.get('n_valid') or '—'} · p={result.get('adjusted_p_value') or result.get('p_value') or '—'}"
            )
        premium_lines.extend(premium.get("limitations") or [])
        add_page(pdf, "Analítica premium", premium_lines, {"hallazgos_premium"})

        action_lines = []
        for plan in bundle.get("action_plans") or []:
            action_lines.append(
                f"{plan.get('name') or 'Plan de acción'} · estado={plan.get('status') or '—'} · "
                f"{'aprobado' if plan.get('approved') else 'pendiente de aprobación'}"
            )
            for item in plan.get("items") or []:
                action_lines.append(
                    f"P{item.get('priority') or '—'} · {item.get('construct_code') or '—'} · "
                    f"hallazgo={item.get('finding') or '—'} · "
                    f"hipótesis={item.get('origin_hypothesis') or '—'}"
                )
                action_lines.append(
                    f"  medida={item.get('action_description') or item.get('title') or '—'} · "
                    f"responsable={item.get('responsible_label') or '—'} · fecha={item.get('due_date') or '—'} · "
                    f"estado={item.get('effective_status') or item.get('status') or '—'}"
                )
                for kpi in item.get("kpis") or []:
                    current = kpi.get("current_value")
                    if current is None:
                        latest = kpi.get("latest_measurement") or {}
                        current = latest.get("text_value") or "sin medición"
                    action_lines.append(
                        f"  KPI {kpi.get('code') or '—'}: {kpi.get('name') or '—'} · "
                        f"línea base={kpi.get('baseline_value') if kpi.get('baseline_value') is not None else '—'} · "
                        f"actual={current} · meta={kpi.get('target_value') if kpi.get('target_value') is not None else '—'} · "
                        f"unidad={kpi.get('unit') or '—'}"
                    )
        add_page(
            pdf,
            "Plan de acción",
            action_lines or ["No hay planes de acción registrados para este estudio."],
            {"plan_accion"},
        )

        add_page(
            pdf,
            "Conclusiones",
            bundle.get("conclusions") or ["Sin datos suficientes para conclusiones todavía."],
            {"conclusiones", "resumen_ejecutivo"},
        )

        barem = traceability.get("barem") or {}
        trace_lines = [
            f"report_run_id: {traceability.get('report_run_id') or '—'}",
            f"study_id: {traceability.get('study_id') or '—'} · código: {traceability.get('study_code') or '—'}",
            f"analysis_run_id: {traceability.get('analysis_run_id') or '—'}",
            f"Versión: {traceability.get('version_kind') or '—'}",
            f"instrument_version_id: {traceability.get('instrument_version_id') or '—'}",
            f"Hash del manifiesto: {traceability.get('manifest_hash') or '—'}",
            "Linaje: " + " → ".join(traceability.get("lineage") or []),
            f"Baremo: {barem.get('name') or '—'} · versión {barem.get('version') or '—'} · "
            f"id={barem.get('id') or '—'} · estado={barem.get('type') or '—'}",
            f"Hash del baremo: {barem.get('content_hash') or '—'}",
            f"Equivalencia oficial: {'sí' if traceability.get('official_equivalence') else 'no'}",
            "Registros individuales incluidos: no",
        ]
        exclusions = traceability.get("exclusions") or {}
        if exclusions:
            trace_lines.append(
                f"Exclusiones: excluidas={exclusions.get('excluded_count') or 0} · "
                f"abandonadas={exclusions.get('abandoned_count') or 0} · "
                f"en revisión={exclusions.get('review_count') or 0} — {exclusions.get('criteria') or ''}"
            )
        for run in traceability.get("analysis_runs") or []:
            trace_lines.append(
                f"Ejecución {run.get('analysis_type') or '—'} · estado={run.get('status') or '—'} · "
                f"algoritmo={run.get('algorithm_version') or '—'} · hash={run.get('input_hash') or '—'}"
            )
        add_page(pdf, "Anexos y trazabilidad", trace_lines, {"anexos", "trazabilidad"})

        if pages_rendered == 0:
            add_page(
                pdf,
                "Secciones seleccionadas",
                [
                    "Las secciones solicitadas aún no tienen contenido disponible "
                    "para este estudio.",
                    "Selección: " + ", ".join(bundle.get("sections") or []),
                ],
                None,
            )

    return output.getvalue()


def _format_percentage_pdf(ratio: float | None) -> str:
    if ratio is None:
        return "—"
    return f"{ratio * 100:.1f}%"


class ReportService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.repo = ReportRepository(session)
        self.study_repo = StudyRepository(session)
        self.analytics_repo = AnalyticsRepository(session)

    async def create_template(self, payload: ReportTemplateCreate):
        from app.models.report import ReportTemplate

        template = ReportTemplate(
            code=payload.code,
            name=payload.name,
            report_type=payload.report_type,
            instrument_version_id=payload.instrument_version_id,
            template_config=payload.template_config,
        )
        template = await self.repo.add_template(template)
        await self.session.commit()
        return template

    async def get_run(self, run_id: int):
        run = await self.repo.get_run(run_id)
        if run is None:
            raise NotFoundError(f"Reporte {run_id} no encontrado")
        return run

    async def generate(self, study_id: int, payload: ReportRunCreate):
        from app.models.report import ReportRun

        study = await self.study_repo.get(study_id)
        if study is None:
            raise NotFoundError(f"Estudio {study_id} no encontrado")

        report_run = ReportRun(
            study_id=study_id,
            report_template_id=payload.report_template_id,
            analysis_run_id=payload.analysis_run_id,
            requested_by_user_id=payload.requested_by_user_id,
            output_format=payload.output_format,
            status="PENDING",
            metadata_={
                "report_mode": payload.report_mode,
                "sections": payload.sections,
            },
        )
        report_run = await self.repo.add_run(report_run)
        await self.session.flush()

        try:
            bundle = await self._build_bundle(
                study,
                payload.analysis_run_id,
                report_mode=payload.report_mode,
                sections=payload.sections,
                report_run=report_run,
            )

            storage_dir = Path(get_settings().export_storage_dir).parent / "reports_storage"
            storage_dir.mkdir(parents=True, exist_ok=True)

            if payload.output_format == "DOCX":
                from app.services.report_docx import render_report_docx

                file_bytes = render_report_docx(bundle)
                path = storage_dir / f"{report_run.public_id}.docx"
                path.write_bytes(file_bytes)
            elif payload.output_format == "PDF":
                file_bytes = _render_report_pdf(bundle)
                path = storage_dir / f"{report_run.public_id}.pdf"
                path.write_bytes(file_bytes)
            else:
                file_bytes = json.dumps(bundle, indent=2, default=str, ensure_ascii=False).encode("utf-8")
                path = storage_dir / f"{report_run.public_id}.json"
                path.write_bytes(file_bytes)

            data_hash = hashlib.sha256(file_bytes).hexdigest()
            report_run.storage_path = str(path)
            report_run.data_hash = data_hash
            report_run.status = "COMPLETED"
            report_run.generated_at = datetime.now(UTC)
        except Exception as exc:
            report_run.status = "FAILED"
            report_run.error_message = str(exc)
            await self.session.commit()
            raise

        await self.session.commit()
        await self.session.refresh(report_run)
        return report_run

    async def _build_bundle(
        self,
        study,
        analysis_run_id: int | None,
        *,
        report_mode: str = "PROVISIONAL",
        sections: list[str] | None = None,
        report_run=None,
    ) -> dict:
        bundle: dict = {
            "study": {
                "id": study.id,
                "public_id": str(study.public_id),
                "code": f"EST-{study.id:06d}",
                "name": study.name,
                "study_type": study.study_type,
                "status": study.status,
                "period_start": study.start_at.isoformat() if study.start_at else None,
                "period_end": study.end_at.isoformat() if study.end_at else None,
                "instrument_name": study.instrument_name,
                "instrument_version_code": study.instrument_version_code,
            },
            "generated_at": datetime.now(UTC).isoformat(),
            "report_mode": report_mode,
            "sections": sections or [],
            "methodological_status": None,
            "methodological_label": None,
            "cover": None,
            "sociolaboral_profile": [],
            "dimension_results": [],
            "subdimension_results": [],
            "interpretation": [],
            "priority_ranking": [],
            "conclusions": [],
            "analysis_results": [],
            "censopas_results": [],
            "barem_results": None,
            "action_plans": [],
            "premium_analytics": None,
            "traceability": None,
            "data_quality": None,
            "executive_summary": None,
        }

        if analysis_run_id is not None:
            run = await self.analytics_repo.get_run(analysis_run_id)
            if run is not None:
                bundle["analysis_results"] = [self._serialize_result(r) for r in run.results]
        else:
            stmt = (
                select(AnalysisResult)
                .join(AnalysisRun, AnalysisResult.analysis_run_id == AnalysisRun.id)
                .where(AnalysisRun.study_id == study.id)
                .order_by(AnalysisResult.created_at.desc())
                .limit(50)
            )
            results = list((await self.session.execute(stmt)).scalars().all())
            bundle["analysis_results"] = [self._serialize_result(r) for r in results]

        censopas_service = CensopasScoringService(self.session)
        construct_results = await censopas_service.get_results(study.id)
        official_equivalence_enabled = await resolve_official_equivalence_enabled(
            censopas_service.instrument_repo, study.instrument_version_id
        )
        barem = await censopas_service.repo.get_barem(study.barem_id) if study.barem_id else None
        # Fase 1/7 (harness §31): única autoridad para "oficial"/"referencia" —
        # nunca inferir localmente, siempre censopas_methodology.py.
        bundle["methodological_label"] = resolve_censopas_methodological_status(
            barem, official_equivalence_enabled
        )
        censopas_payload = [
            censopas_service.apply_privacy(
                r,
                study.min_publishable_n,
                barem=barem,
                official_equivalence_enabled=official_equivalence_enabled,
            )
            for r in construct_results
        ]
        bundle["censopas_results"] = censopas_service.attach_priority_ranks(censopas_payload)

        telemetry = await TelemetryService(self.session).get_study_telemetry(study.id)
        bundle["data_quality"] = telemetry.model_dump(mode="json")
        bundle["executive_summary"] = self._build_executive_summary(
            bundle["censopas_results"], bundle["data_quality"], bundle["methodological_label"]
        )

        if study.instrument_version_id is not None:
            readiness = await censopas_service.get_readiness(study.instrument_version_id)
            bundle["methodological_status"] = readiness
            if report_mode == "OFFICIAL" and not readiness["ready_for_official_reporting"]:
                raise ConflictError(
                    "El reporte oficial está bloqueado porque la versión CENSOPAS no cumple readiness.",
                    readiness=readiness,
                )
            overview = await ScoringService(self.session).get_overview(study.id)
            bundle["barem_results"] = overview.model_dump(mode="json")

        # Fase 4/5: D1-D6 y S1-S20 se construyen desde `censopas_results`
        # (trichotomy favorable/intermedio/desfavorable + clasificación
        # colectiva + priority_rank ya agrupado por construct_type en
        # `attach_priority_ranks`) — es la MISMA fuente que ya usaba el PDF,
        # y la que trae exactamente los campos que pide la tabla CENSOPAS
        # (antes el DOCX usaba `barem_results`, una fuente distinta con
        # bandas/media/mediana pero sin trichotomy — esa divergencia era
        # el origen de GAP-REPORT-PDF-PARITY). `barem_results` se conserva
        # en el bundle para compatibilidad JSON (media/mediana), pero deja
        # de ser la fuente de las secciones D1-D6/S1-S20/interpretación.
        bundle["dimension_results"] = [
            r for r in bundle["censopas_results"] if r.get("construct_type") == _DIMENSION_TYPE
        ]
        bundle["subdimension_results"] = [
            r for r in bundle["censopas_results"] if r.get("construct_type") == _SUBDIMENSION_TYPE
        ]

        bundle["sociolaboral_profile"] = await self._build_sociolaboral_profile(study)
        bundle["action_plans"] = await self._build_action_plans(study.id)
        bundle["priority_ranking"] = self._build_priority_ranking(bundle["dimension_results"])
        bundle["interpretation"] = self._build_interpretation(
            bundle["dimension_results"], bundle["action_plans"]
        )
        bundle["premium_analytics"] = self._build_premium_analytics(
            bundle["analysis_results"], study.min_publishable_n
        )
        bundle["cover"] = await self._build_cover(study, bundle, report_run)
        bundle["traceability"] = await self._build_traceability(
            study, bundle, report_run, analysis_run_id
        )
        bundle["conclusions"] = self._build_conclusions(bundle)
        return bundle

    async def _build_cover(self, study, bundle: dict, report_run) -> dict:
        organization_name = None
        project = await self.session.get(Project, study.project_id)
        if project is not None and project.organization_id is not None:
            organization = await self.session.get(Organization, project.organization_id)
            organization_name = organization.name if organization else None

        evaluator_label = None
        requested_by_user_id = getattr(report_run, "requested_by_user_id", None)
        if requested_by_user_id is not None:
            user = await self.session.get(User, requested_by_user_id)
            if user is not None:
                full_name = " ".join(filter(None, (user.first_name, user.last_name))).strip()
                evaluator_label = full_name or user.username or user.email

        readiness = bundle.get("methodological_status") or {}
        return {
            "organization_name": organization_name,
            "study_code": bundle["study"]["code"],
            "period_start": bundle["study"]["period_start"],
            "period_end": bundle["study"]["period_end"],
            "instrument_label": "CENSOPAS-COPSOQ",
            "version_kind": readiness.get("version_kind", "UNKNOWN"),
            "generated_at": bundle["generated_at"],
            "evaluator_label": evaluator_label,
            "confidentiality_notice": _CONFIDENTIALITY_NOTICE,
            "methodological_label": bundle["methodological_label"],
        }

    async def _build_sociolaboral_profile(self, study) -> list[dict]:
        """Fase 3: perfil sociolaboral (11 variables C-001..C-011, EXOGENOUS,
        nunca puntuables — harness §9). Reusa `ResponseDescriptiveService`
        (misma fuente que Resultados) y aplica supresión n<min_publishable_n
        por categoría aquí mismo, porque ese servicio no suprime por diseño
        (sirve también a vistas internas con otro umbral de exposición)."""
        try:
            descriptives = await ResponseDescriptiveService(self.session).get(study.id)
        except NotFoundError:
            return []

        profile = []
        for question in descriptives.questions:
            if question.research_role != "EXOGENOUS" or question.is_scored:
                continue
            categories = []
            for frequency in question.frequencies:
                suppressed = frequency.n < descriptives.min_publishable_n
                categories.append(
                    {
                        "label": frequency.label,
                        "n": None if suppressed else frequency.n,
                        "percentage": None if suppressed else frequency.percentage,
                        "suppressed": suppressed,
                    }
                )
            profile.append(
                {
                    "code": question.code,
                    "label": question.short_label or question.question_text,
                    "valid_n": question.valid_n,
                    "missing_n": question.missing_n,
                    "categories": categories,
                }
            )
        return profile

    @staticmethod
    def _build_priority_ranking(dimension_results: list[dict]) -> list[dict]:
        """Fase 7: reusa `priority_rank`/`unfavorable_pct` ya calculados por
        `CensopasScoringService.attach_priority_ranks` — no reordena con una
        regla nueva. El orden es una ayuda de priorización preventiva, nunca
        una clasificación oficial adicional (se deja explícito en el render)."""
        ranked = sorted(
            (r for r in dimension_results if not r.get("suppressed")),
            key=lambda r: (r.get("priority_rank") if r.get("priority_rank") is not None else 9999),
        )
        return [
            {
                "construct_code": r.get("construct_code"),
                "construct_name": r.get("construct_name"),
                "priority_rank": r.get("priority_rank"),
                "n_valid": r.get("n_valid"),
                "unfavorable_pct": r.get("unfavorable_pct"),
                "collective_classification": r.get("collective_classification"),
            }
            for r in ranked
        ]

    @staticmethod
    def _build_interpretation(dimension_results: list[dict], action_plans: list[dict]) -> list[dict]:
        """Fase 6: separa hallazgo / clasificación / prioridad / hipótesis a
        contrastar / orientación preventiva / limitación — nunca causalidad,
        nunca diagnóstico individual. La hipótesis y la orientación vienen de
        `ActionPlanItem.origin_hypothesis`/`action_description` cuando existe
        una acción vinculada al mismo constructo; si no hay acción registrada
        se deja constancia explícita de que aún no se contrastó."""
        hypotheses_by_construct: dict[str, list[str]] = {}
        actions_by_construct: dict[str, list[str]] = {}
        for plan in action_plans:
            for item in plan.get("items") or []:
                code = item.get("construct_code")
                if not code:
                    continue
                if item.get("origin_hypothesis"):
                    hypotheses_by_construct.setdefault(code, []).append(item["origin_hypothesis"])
                if item.get("action_description"):
                    actions_by_construct.setdefault(code, []).append(item["action_description"])

        entries = []
        for result in dimension_results:
            code = result.get("construct_code")
            name = result.get("construct_name") or code or "—"
            if result.get("suppressed"):
                entries.append(
                    {
                        "construct_code": code,
                        "construct_name": name,
                        "finding": "Resultado suprimido por privacidad (n por debajo del mínimo publicable).",
                        "classification": None,
                        "priority_rank": None,
                        "origin_hypothesis": [],
                        "preventive_orientation": [],
                        "limitation": "No es posible interpretar un resultado suprimido sin exponer el grupo.",
                    }
                )
                continue
            classification = result.get("collective_classification")
            entries.append(
                {
                    "construct_code": code,
                    "construct_name": name,
                    "finding": (
                        f"Se observó una distribución colectiva en {name} "
                        f"(n={result.get('n_valid', '—')})."
                    ),
                    "classification": classification,
                    "priority_rank": result.get("priority_rank"),
                    "origin_hypothesis": hypotheses_by_construct.get(code, []),
                    "preventive_orientation": actions_by_construct.get(code, [])
                    or [
                        "El Grupo de Trabajo deberá contrastar hipótesis de origen y definir "
                        "medidas preventivas para esta dimensión."
                    ],
                    "limitation": (
                        "El resultado describe una exposición colectiva; no permite diagnóstico "
                        "individual. La hipótesis de origen es algo a contrastar, no una causa "
                        "demostrada."
                    ),
                }
            )
        return entries

    def _build_conclusions(self, bundle: dict) -> list[str]:
        """Fase 9: solo texto derivado de datos ya calculados en el bundle —
        ningún resultado concreto queda hardcodeado, se lee de
        `executive_summary`/`dimension_results`/`methodological_label`."""
        conclusions: list[str] = []
        summary = bundle.get("executive_summary") or {}
        priority_dimensions = summary.get("priority_dimensions") or []
        if priority_dimensions:
            names = ", ".join(
                d.get("construct_name") or d.get("construct_code") or "—"
                for d in priority_dimensions
            )
            conclusions.append(f"Las dimensiones prioritarias para intervención preventiva fueron: {names}.")
        else:
            conclusions.append(
                "No se identificaron dimensiones con prioridad de intervención alta en esta medición."
            )

        protective = [
            r
            for r in bundle.get("dimension_results") or []
            if not r.get("suppressed")
            and r.get("collective_classification") == "FACTOR_PROTECTOR"
        ]
        if protective:
            names = ", ".join(r.get("construct_name") or r.get("construct_code") or "—" for r in protective)
            conclusions.append(f"Se identificaron factores protectores en: {names}.")
        else:
            conclusions.append("No se identificaron factores protectores destacados en esta medición.")

        conclusions.append(
            "Los resultados son de carácter colectivo — describen a un grupo de trabajadores, "
            "no a personas individuales, y no constituyen diagnóstico clínico."
        )

        label = bundle.get("methodological_label") or {}
        barem = (bundle.get("traceability") or {}).get("barem") or {}
        if not label.get("official_equivalence"):
            conclusions.append(
                "Resultado basado en baremo de referencia. No equivalente al resultado oficial "
                "CENSOPAS-COPSOQ."
            )
        conclusions.append(
            "Se recomienda conservar la versión del instrumento"
            + (f" ({bundle['study'].get('instrument_version_code')})" if bundle.get("study", {}).get("instrument_version_code") else "")
            + " y el baremo aplicado"
            + (f" ({barem.get('name')} · versión {barem.get('version')})" if barem.get("name") else "")
            + " para permitir comparaciones futuras."
        )
        return conclusions

    async def _build_action_plans(self, study_id: int) -> list[dict]:
        stmt = (
            select(ActionPlan)
            .where(ActionPlan.study_id == study_id)
            .options(
                selectinload(ActionPlan.items)
                .selectinload(ActionPlanItem.kpis)
                .selectinload(Kpi.measurements)
            )
            .order_by(ActionPlan.created_at, ActionPlan.id)
        )
        plans = list((await self.session.execute(stmt)).scalars().all())
        construct_ids = {
            item.construct_id
            for plan in plans
            for item in plan.items
            if item.construct_id is not None
        }
        constructs = {}
        if construct_ids:
            construct_stmt = select(Construct).where(Construct.id.in_(construct_ids))
            constructs = {
                construct.id: construct
                for construct in (await self.session.execute(construct_stmt)).scalars().all()
            }
        payload = []
        for plan in plans:
            items = []
            for item in sorted(
                plan.items,
                key=lambda value: (
                    value.priority is None,
                    value.priority or 0,
                    value.id,
                ),
            ):
                construct = constructs.get(item.construct_id)
                kpis = []
                for kpi in sorted(item.kpis, key=lambda value: (value.code or "", value.id)):
                    measurements = sorted(
                        kpi.measurements, key=lambda value: value.measured_at
                    )
                    latest = measurements[-1] if measurements else None
                    kpis.append(
                        {
                            "code": kpi.code,
                            "name": kpi.name,
                            "description": kpi.description,
                            "formula": kpi.formula,
                            "unit": kpi.unit,
                            "baseline_value": float(kpi.baseline_value)
                            if kpi.baseline_value is not None
                            else None,
                            "target_value": float(kpi.target_value)
                            if kpi.target_value is not None
                            else None,
                            "frequency": kpi.frequency,
                            "status": kpi.status,
                            "latest_measurement": (
                                {
                                    "measured_at": latest.measured_at.isoformat(),
                                    "numeric_value": float(latest.numeric_value)
                                    if latest.numeric_value is not None
                                    else None,
                                    "text_value": latest.text_value,
                                    "status": latest.status,
                                    "source_reference": latest.source_reference,
                                }
                                if latest
                                else None
                            ),
                            "current_value": (
                                float(latest.numeric_value)
                                if latest and latest.numeric_value is not None
                                else None
                            ),
                        }
                    )
                items.append(
                    {
                        "construct_code": construct.code if construct else None,
                        "construct_name": construct.name if construct else None,
                        "analysis_run_id": item.analysis_run_id,
                        "title": item.title,
                        "finding": item.finding,
                        "origin_hypothesis": item.origin_hypothesis,
                        "action_description": item.action_description,
                        "responsible_label": item.responsible_label,
                        "priority": item.priority,
                        "due_date": item.due_date.isoformat() if item.due_date else None,
                        "status": item.status,
                        "effective_status": compute_effective_status(item.status, item.due_date),
                        "kpis": kpis,
                    }
                )
            payload.append(
                {
                    "name": plan.name,
                    "status": plan.status,
                    "approved": plan.approved_at is not None,
                    "approved_at": plan.approved_at.isoformat()
                    if plan.approved_at
                    else None,
                    "items": items,
                }
            )
        return payload


    
    @staticmethod
    def _build_executive_summary(
        censopas_results: list[dict],
        data_quality: dict | None,
        methodological_label: dict | None = None,
    ) -> dict:
        """Guía y modelos de reporte §31: primer contenido sustantivo del
        informe — participación, niveles principales, prioridades. Se deriva
        de `censopas_results` (ya con privacidad aplicada) y `data_quality`;
        no ejecuta cálculo nuevo."""
        publishable = [
            result
            for result in censopas_results
            if not result.get("suppressed") and result.get("unfavorable_pct") is not None
        ]
        ranked = sorted(publishable, key=lambda result: result["unfavorable_pct"], reverse=True)
        high_risk_count = sum(
            1 for result in ranked if result.get("collective_classification") == "RIESGO_ALTO"
        )
        if ranked:
            headline = (
                f"{high_risk_count} de {len(ranked)} dimensiones en riesgo alto (≥50% desfavorable)."
                if high_risk_count
                else "Ninguna dimensión alcanza el umbral de riesgo alto (≥50% desfavorable)."
            )
        else:
            headline = "Todavía no hay dimensiones con resultados publicables para este estudio."

        return {
            "n_valid": (data_quality or {}).get("valid_count"),
            "completion_rate": (data_quality or {}).get("completion_rate"),
            "headline": headline,
            "barem_status": (methodological_label or {}).get("barem_status"),
            "official_equivalence": (methodological_label or {}).get("official_equivalence"),
            "priority_dimensions": [
                {
                    "construct_code": result.get("construct_code"),
                    "construct_name": result.get("construct_name"),
                    "unfavorable_pct": result.get("unfavorable_pct"),
                    "classification": result.get("collective_classification"),
                }
                for result in ranked[:3]
            ],
        }

    @staticmethod
    def _build_premium_analytics(
        analysis_results: list[dict], min_publishable_n: int
    ) -> dict:
        premium_types = {
            "SPEARMAN",
            "CHI_SQUARE",
            "MANN_WHITNEY",
            "KRUSKAL_WALLIS",
            "NORMALITY",
            "LOGISTIC_REGRESSION",
            "KMEANS",
            "CRONBACH_ALPHA",
            "MCDONALD_OMEGA",
        }
        results = [
            result
            for result in analysis_results
            if result.get("result_type") in premium_types
            and (
                result.get("n_valid") is None
                or result["n_valid"] >= min_publishable_n
            )
        ]
        significant = [
            result
            for result in results
            if (
                result.get("adjusted_p_value")
                if result.get("adjusted_p_value") is not None
                else result.get("p_value")
            )
            is not None
            and (
                result.get("adjusted_p_value")
                if result.get("adjusted_p_value") is not None
                else result.get("p_value")
            )
            < 0.05
        ]
        return {
            "status": "AVAILABLE" if results else "NO_RESULTS",
            "methods": sorted({result["result_type"] for result in results}),
            "result_count": len(results),
            "significant_result_count": len(significant),
            "privacy": {
                "minimum_n": min_publishable_n,
                "individual_assignments_removed": True,
                "small_group_results_removed": True,
            },
            "limitations": [
                "Los resultados premium complementan y no modifican el semáforo CENSOPAS.",
                "Las asociaciones no demuestran causalidad.",
                "K-means es exploratorio y no publica asignaciones individuales.",
                "La regresión no debe utilizarse para decisiones laborales individuales.",
            ],
            "results": results[:100],
        }

    async def _build_traceability(
        self, study, bundle: dict, report_run=None, requested_analysis_run_id: int | None = None
    ) -> dict:
        runs_stmt = (
            select(AnalysisRun)
            .where(AnalysisRun.study_id == study.id)
            .order_by(AnalysisRun.created_at, AnalysisRun.id)
        )
        runs = list((await self.session.execute(runs_stmt)).scalars().all())
        barem_payload = None
        if study.barem_id is not None:
            barem = await self.session.get(Barem, study.barem_id)
            if barem is not None:
                barem_payload = {
                    "id": barem.id,
                    "name": barem.name,
                    "version": barem.barem_version,
                    "type": barem.metadata_.get("barem_type"),
                    "source_reference": barem.source_reference,
                    "content_hash": barem.metadata_.get("content_hash"),
                    "status": barem.status,
                }
        readiness = bundle.get("methodological_status") or {}
        methodological_label = bundle.get("methodological_label") or {}
        data_quality = bundle.get("data_quality") or {}
        return {
            "report_run_id": getattr(report_run, "id", None),
            "report_run_public_id": (
                str(report_run.public_id) if getattr(report_run, "public_id", None) else None
            ),
            "study_id": study.id,
            "study_code": bundle.get("study", {}).get("code"),
            "analysis_run_id": requested_analysis_run_id,
            "lineage": [
                "responses.raw_code",
                "response_scores.risk_value",
                "response_scores.score_0_100",
                "construct_scores.score_0_100",
                "construct_results",
                "report_run",
            ],
            "instrument_version_id": study.instrument_version_id,
            "version_kind": readiness.get("version_kind"),
            "manifest_hash": (
                readiness.get("manifest_hash")
                or (getattr(study.instrument_version, "config", {}) or {}).get(
                    "manifest_hash"
                )
            ),
            "barem": barem_payload,
            "official_equivalence": methodological_label.get("official_equivalence"),
            "exclusions": {
                "excluded_count": data_quality.get("excluded_count"),
                "abandoned_count": data_quality.get("abandoned_count"),
                "review_count": data_quality.get("review_count"),
                "criteria": (
                    "Sesiones sin estado COMPLETED/validation_status=VALID quedan fuera de "
                    "`n_valid`; el detalle agregado está en Calidad de datos."
                ),
            },
            "analysis_runs": [
                {
                    "analysis_type": run.analysis_type,
                    "status": run.status,
                    "engine": run.engine,
                    "engine_version": run.engine_version,
                    "algorithm_version": run.algorithm_version,
                    "input_hash": run.input_hash,
                    "completed_at": run.completed_at.isoformat()
                    if run.completed_at
                    else None,
                }
                for run in runs
            ],
            "privacy": {
                "min_publishable_n": study.min_publishable_n,
                "individual_records_included": False,
                "secondary_suppression": True,
            },
            "report": {
                "mode": bundle.get("report_mode"),
                "sections": bundle.get("sections"),
                "generated_at": bundle.get("generated_at"),
            },
        }

    # E-09: ningún reporte descargable debe exponer datos punto-a-punto,
    # aunque en el futuro algún otro tipo de análisis los incluya en
    # result_data — defensa en profundidad, independiente del control de rol
    # aplicado al generar el resultado.
    _INDIVIDUAL_LEVEL_KEYS = frozenset(
        {
            "points",
            "points_binned",
            "labels",
            "assignments",
            "predictions",
            "probabilities",
            "session_ids",
            "response_session_ids",
            "anonymous_tokens",
            "tokens",
            "row_ids",
        }
    )


    
    @classmethod
    def _sanitize_result_data(cls, value):
        """Retira identificadores y vectores fila-a-fila en cualquier profundidad."""
        if isinstance(value, dict):
            sanitized = {}
            for key, nested_value in value.items():
                normalized = str(key).lower()
                if (
                    normalized in cls._INDIVIDUAL_LEVEL_KEYS
                    or "session_id" in normalized
                    or "anonymous_token" in normalized
                ):
                    continue
                sanitized[key] = cls._sanitize_result_data(nested_value)
            return sanitized
        if isinstance(value, list):
            return [cls._sanitize_result_data(item) for item in value]
        return value

    @classmethod
    def _serialize_result(cls, result: AnalysisResult) -> dict:
        result_data = cls._sanitize_result_data(result.result_data or {})
        return {
            "result_type": result.result_type,
            "result_code": result.result_code,
            "n_valid": result.n_valid,
            "numeric_value": float(result.numeric_value) if result.numeric_value is not None else None,
            "statistic_value": float(result.statistic_value) if result.statistic_value is not None else None,
            "p_value": float(result.p_value) if result.p_value is not None else None,
            "adjusted_p_value": float(result.adjusted_p_value)
            if result.adjusted_p_value is not None
            else None,
            "effect_size": float(result.effect_size) if result.effect_size is not None else None,
            "effect_label": result.effect_label,
            "ci_lower": float(result.ci_lower) if result.ci_lower is not None else None,
            "ci_upper": float(result.ci_upper) if result.ci_upper is not None else None,
            "text_value": result.text_value,
            "result_data": result_data,
        }
