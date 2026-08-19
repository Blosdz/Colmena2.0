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

from app.core.config import get_settings
from app.core.exceptions import ConflictError, NotFoundError, ValidationDomainError
from app.models.analysis import AnalysisResult, AnalysisRun
from app.models.bsc import ActionPlan, ActionPlanItem, Kpi
from app.models.censopas import Barem
from app.models.construct import Construct
from app.models.project import Project
from app.models.user import Organization
from app.repositories.analytics import AnalyticsRepository
from app.repositories.reports import ReportRepository
from app.repositories.studies import StudyRepository
from app.schemas.reports import ReportRunCreate, ReportTemplateCreate
from app.services.censopas_service import CensopasScoringService
from app.services.intelligence_service import IntelligenceService
from app.services.scoring_service import ScoringService


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
            )

            storage_dir = Path(get_settings().export_storage_dir).parent / "reports_storage"
            storage_dir.mkdir(parents=True, exist_ok=True)

            if payload.output_format == "DOCX":
                from app.services.report_docx import render_report_docx

                file_bytes = render_report_docx(bundle)
                path = storage_dir / f"{report_run.public_id}.docx"
                path.write_bytes(file_bytes)
            elif payload.output_format == "PDF":
                from app.services.report_pdf import render_report_pdf
                file_bytes = render_report_pdf(bundle)
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
    ) -> dict:
        bundle: dict = {
            "study": {
                "id": study.id,
                "public_id": str(study.public_id),
                "name": study.name,
                "study_type": study.study_type,
                "status": study.status,
            },
            "generated_at": datetime.now(UTC).isoformat(),
            "report_mode": report_mode,
            "sections": sections or [],
            "methodological_status": None,
            "project": None,
            "company": None,
            "thresholds": {},
            "intelligence": None,
            "analysis_results": [],
            "censopas_results": [],
            "barem_results": None,
            "action_plans": [],
            "premium_analytics": None,
            "traceability": None,
        }

        project = await self.session.get(Project, study.project_id)
        if project is not None:
            project_metadata = project.metadata_ or {}
            bundle["project"] = {
                "id": project.id,
                "public_id": str(project.public_id),
                "name": project.name,
                "description": project.description,
                "status": project.status,
            }
            bundle["thresholds"] = project_metadata.get("thresholds") or {}
            organization = (
                await self.session.get(Organization, project.organization_id)
                if project.organization_id is not None
                else None
            )
            if organization is not None:
                metadata = organization.metadata_ or {}
                bundle["company"] = {
                    "name": organization.name,
                    "legal_name": organization.legal_name,
                    "tax_id": organization.tax_id,
                    "organization_type": organization.organization_type,
                    "industry": metadata.get("industry"),
                    "ciiu_code": metadata.get("ciiu_code"),
                    "fiscal_address": metadata.get("fiscal_address"),
                    "worker_count": metadata.get("worker_count"),
                    "representative_name": metadata.get("representative_name"),
                    "study_lead_name": metadata.get("study_lead_name"),
                    "locations": metadata.get("locations") or [],
                    "signatories": metadata.get("signatories") or [],
                }
            elif project_metadata.get("company_snapshot"):
                bundle["company"] = project_metadata["company_snapshot"]


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
        bundle["censopas_results"] = [
            censopas_service.apply_privacy(r, study.min_publishable_n) for r in construct_results
        ]
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

        bundle["action_plans"] = await self._build_action_plans(study.id)
        bundle["premium_analytics"] = self._build_premium_analytics(
            bundle["analysis_results"], study.min_publishable_n
        )
        try:
            bundle["intelligence"] = await IntelligenceService(self.session).build(study.id)
        except (NotFoundError, ValidationDomainError):
            # Estudios genéricos o sin scoring conservan un reporte válido sin esta capa.
            bundle["intelligence"] = None

        bundle["traceability"] = await self._build_traceability(study, bundle)
        return bundle

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
                        }
                    )
                items.append(
                    {
                        "construct_code": construct.code if construct else None,
                        "construct_name": construct.name if construct else None,
                        "title": item.title,
                        "finding": item.finding,
                        "action_description": item.action_description,
                        "responsible_label": item.responsible_label,
                        "priority": item.priority,
                        "due_date": item.due_date.isoformat() if item.due_date else None,
                        "status": item.status,
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

    async def _build_traceability(self, study, bundle: dict) -> dict:
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
                    "name": barem.name,
                    "version": barem.barem_version,
                    "type": barem.metadata_.get("barem_type"),
                    "source_reference": barem.source_reference,
                    "content_hash": barem.metadata_.get("content_hash"),
                    "status": barem.status,
                }
        readiness = bundle.get("methodological_status") or {}
        return {
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
