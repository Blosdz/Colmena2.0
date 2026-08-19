from __future__ import annotations

from datetime import UTC, datetime, timedelta
from random import Random

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.exceptions import NotFoundError
from app.data.censopas_demo_catalog import CENSOPAS_DEMO_ITEMS
from app.models.censopas import Barem, BaremCutoff
from app.models.construct import Construct, ConstructItem
from app.models.instrument import Instrument, InstrumentVersion
from app.models.option_set import OptionSet, OptionSetOption
from app.models.project import Project
from app.models.question import Question
from app.models.response import Response, ResponseSession, ResponseSessionUnit
from app.models.scoring import ScoringRule
from app.models.study import Study, StudyUnit, StudyUnitType
from app.models.survey import Survey, SurveyQuestion, SurveySection
from app.services.censopas_service import CensopasScoringService

router = APIRouter(tags=["demo"])


class DemoCampaignCreate(BaseModel):
    version_kind: str = Field(default="SHORT", pattern="^(SHORT|MEDIUM)$")
    synthetic_responses: int = Field(default=48, ge=8, le=250)
    industry: str = Field(default="MINERIA", max_length=80)


class DemoCampaignRead(BaseModel):
    project_id: int
    study_id: int
    study_public_id: str
    instrument_version_id: int
    barem_id: int
    version_kind: str
    item_count: int
    synthetic_responses: int
    public_path: str
    methodology_mode: str
    report_disclaimer: str


_DIMENSIONS = [
    ("D1", "Exigencias psicológicas"),
    ("D2", "Conflicto trabajo-familia"),
    ("D3", "Control sobre el trabajo"),
    ("D4", "Apoyo social y calidad de liderazgo"),
    ("D5", "Compensaciones"),
    ("D6", "Capital social"),
]

# Estructura de demostración para navegación analítica. La concordancia oficial
# ítem-subdimensión y los baremos sólo se habilitan con el artefacto autorizado.
_SUBDIMENSIONS = [
    ("D1_S1", "Exigencias cuantitativas", "D1"),
    ("D1_S2", "Ritmo de trabajo", "D1"),
    ("D1_S3", "Exigencias emocionales", "D1"),
    ("D1_S4", "Exigencias de esconder emociones", "D1"),
    ("D2_S1", "Doble presencia", "D2"),
    ("D3_S1", "Influencia", "D3"),
    ("D3_S2", "Posibilidades de desarrollo", "D3"),
    ("D3_S3", "Sentido del trabajo", "D3"),
    ("D3_S4", "Claridad de rol", "D3"),
    ("D3_S5", "Conflicto de rol", "D3"),
    ("D4_S1", "Apoyo de compañeros", "D4"),
    ("D4_S2", "Apoyo de superiores", "D4"),
    ("D4_S3", "Calidad de liderazgo", "D4"),
    ("D4_S4", "Sentimiento de grupo", "D4"),
    ("D4_S5", "Previsibilidad", "D4"),
    ("D4_S6", "Justicia organizacional", "D4"),
    ("D5_S1", "Inseguridad sobre el empleo", "D5"),
    ("D5_S2", "Inseguridad sobre las condiciones", "D5"),
    ("D5_S3", "Estima", "D5"),
    ("D6_S1", "Confianza y gobernanza", "D6"),
]


def _result(project_id: int, metadata: dict) -> DemoCampaignRead:
    demo = metadata["demo_campaign"]
    return DemoCampaignRead(
        project_id=project_id,
        study_id=demo["study_id"],
        study_public_id=demo["study_public_id"],
        instrument_version_id=demo["instrument_version_id"],
        barem_id=demo["barem_id"],
        version_kind=demo["version_kind"],
        item_count=demo["item_count"],
        synthetic_responses=demo["synthetic_responses"],
        public_path=f"/encuesta/{demo['study_public_id']}",
        methodology_mode="COLMENA_EXPLORATORY_SYNTHETIC",
        report_disclaimer="Datos sintéticos y umbrales exploratorios. No equivalen a un baremo oficial ni constituyen un informe para SUNAFIL.",
    )


async def _require_project(session: AsyncSession, project_id: int) -> Project:
    project = await session.get(Project, project_id)
    if project is None:
        raise NotFoundError(f"Proyecto {project_id} no encontrado")
    return project


async def _create_demo_campaign(
    session: AsyncSession, project: Project, payload: DemoCampaignCreate
) -> DemoCampaignRead:
    existing = (project.metadata_ or {}).get("demo_campaign")
    if existing:
        study = await session.get(Study, existing.get("study_id"))
        if study is not None:
            return _result(project.id, project.metadata_)

    items = CENSOPAS_DEMO_ITEMS[payload.version_kind]
    descriptive_count = 11 if payload.version_kind == "SHORT" else 43
    scored_items = items[descriptive_count:]
    owner_id = project.owner_user_id
    now = datetime.now(UTC)
    code_suffix = f"DEMO-{project.id}-{payload.version_kind}"

    instrument = Instrument(
        project_id=project.id,
        owner_user_id=owner_id,
        organization_id=project.organization_id,
        code=f"CENSOPAS-{code_suffix}",
        name=f"CENSOPAS-COPSOQ {payload.version_kind} · Demo sintético",
        instrument_type="CENSOPAS_COPSOQ",
        description="Instrumento demo alimentado con el diccionario proporcionado; sin equivalencia oficial.",
        source_name="Manual CENSOPAS-COPSOQ V2 y diccionario de datos proporcionado",
        is_system=False,
        metadata_={
            "methodology": "CENSOPAS_COPSOQ",
            "methodology_mode": "COLMENA_EXPLORATORY_SYNTHETIC",
            "official_equivalence_enabled": False,
            "synthetic": True,
        },
    )
    session.add(instrument)
    await session.flush()

    version = InstrumentVersion(
        instrument_id=instrument.id,
        version_code=f"{payload.version_kind}-DEMO",
        version_name=f"Versión {payload.version_kind.lower()} · demo sintético",
        edition="Demo 1.0",
        status="TEST",
        scoring_status="CONFIGURED",
        source_reference="Diccionario de datos CENSOPAS-COPSOQ proporcionado por el cliente.",
        config={
            "version_kind": payload.version_kind,
            "censopas_version_kind": payload.version_kind,
            "censopas_expected": {
                "questions": len(items),
                "scored": len(scored_items),
                "descriptive": descriptive_count,
                "dimensions": 6,
                "subdimensions": 20 if payload.version_kind == "MEDIUM" else 0,
            },
            "methodology_mode": "COLMENA_EXPLORATORY_SYNTHETIC",
            "official_equivalence_enabled": False,
        },
    )
    session.add(version)
    await session.flush()

    scale = OptionSet(
        instrument_version_id=version.id,
        owner_user_id=owner_id,
        code="DEMO_LIKERT_RIESGO_5",
        name="Escala demo de frecuencia (5 puntos)",
        description="Escala exploratoria para el recorrido sintético; no reemplaza la codificación oficial.",
        metadata_={"synthetic": True},
    )
    session.add(scale)
    await session.flush()
    options = []
    for score, label in enumerate(("Nunca", "Casi nunca", "Algunas veces", "Muchas veces", "Siempre"), start=1):
        option = OptionSetOption(
            option_set_id=scale.id,
            raw_code=str(score),
            label=label,
            numeric_value=score,
            sort_order=score,
        )
        session.add(option)
        options.append(option)
    await session.flush()

    questions: list[Question] = []
    for index, item in enumerate(items, start=1):
        scored = index > descriptive_count
        question = Question(
            instrument_version_id=version.id,
            option_set_id=scale.id if scored else None,
            code=f"Q{index:03d}",
            source_code=item["source_code"],
            question_text=item["question_text"],
            short_label=item["source_code"],
            question_type="LIKERT" if scored else "TEXT",
            question_role="SCORED" if scored else "DESCRIPTIVE",
            category="RIESGO_PSICOSOCIAL" if scored else "PERFIL_NO_IDENTIFICABLE",
            is_scored=scored,
            is_required_default=scored,
            sort_order=index,
            metadata_={"source_number": item["number"], "synthetic_demo": True},
        )
        session.add(question)
        questions.append(question)
    await session.flush()

    root = Construct(
        instrument_version_id=version.id,
        code="PSICOSOCIAL",
        name="Riesgo psicosocial",
        construct_type="VARIABLE",
        sort_order=1,
        metadata_={"synthetic_demo": True},
    )
    session.add(root)
    await session.flush()
    dimensions: dict[str, Construct] = {}
    for order, (code, name) in enumerate(_DIMENSIONS, start=1):
        dimension = Construct(
            instrument_version_id=version.id,
            parent_id=root.id,
            code=code,
            name=name,
            construct_type="DIMENSION",
            sort_order=order,
            metadata_={"synthetic_demo": True, "mapping_status": "EXPLORATORY"},
        )
        session.add(dimension)
        dimensions[code] = dimension
    await session.flush()

    leaves: list[tuple[Construct, Construct]] = []
    if payload.version_kind == "MEDIUM":
        for order, (code, name, parent_code) in enumerate(_SUBDIMENSIONS, start=1):
            leaf = Construct(
                instrument_version_id=version.id,
                parent_id=dimensions[parent_code].id,
                code=code,
                name=name,
                construct_type="SUBDIMENSION",
                sort_order=order,
                metadata_={"synthetic_demo": True, "mapping_status": "EXPLORATORY"},
            )
            session.add(leaf)
            leaves.append((dimensions[parent_code], leaf))
        await session.flush()

    dimension_counts = (4, 3, 7, 6, 5, 6) if payload.version_kind == "SHORT" else None
    buckets: list[tuple[Construct, Construct | None, list[Question]]] = []
    if dimension_counts:
        cursor = 0
        for (code, _name), count in zip(_DIMENSIONS, dimension_counts):
            buckets.append((dimensions[code], None, questions[descriptive_count + cursor:descriptive_count + cursor + count]))
            cursor += count
    else:
        for position, question in enumerate(scored_items):
            dimension, leaf = leaves[position % len(leaves)]
            found = next((bucket for bucket in buckets if bucket[0].id == dimension.id and bucket[1].id == leaf.id), None)
            if found is None:
                found = (dimension, leaf, [])
                buckets.append(found)
            found[2].append(questions[descriptive_count + position])

    for dimension, leaf, bucket_questions in buckets:
        for order, question in enumerate(bucket_questions, start=1):
            session.add(ConstructItem(
                construct_id=dimension.id,
                question_id=question.id,
                weight=1,
                item_role="SCORED",
                scoring_direction="DIRECT",
                sort_order=order,
                metadata_={"mapping_status": "EXPLORATORY"},
            ))
            if leaf is not None:
                session.add(ConstructItem(
                    construct_id=leaf.id,
                    question_id=question.id,
                    weight=1,
                    item_role="SCORED",
                    scoring_direction="DIRECT",
                    sort_order=order,
                    metadata_={"mapping_status": "EXPLORATORY"},
                ))

    for question in questions[descriptive_count:]:
        session.add(ScoringRule(
            instrument_version_id=version.id,
            question_id=question.id,
            rule_code=f"DEMO_RISK_{question.code}",
            rule_type="RISK_MAP",
            parameters={"risk_map": {str(value): float(value) for value in range(1, 6)}},
            source_reference="Regla exploratoria de demostración; no baremo oficial.",
            rule_version="demo-1",
            status="VALIDATED",
        ))
    await session.flush()

    survey = Survey(
        project_id=project.id,
        instrument_version_id=version.id,
        created_by_user_id=owner_id,
        name=f"Encuesta psicosocial {payload.version_kind.lower()} · demo",
        description="Encuesta anónima de demostración con datos sintéticos.",
        survey_type="CENSO",
        status="ACTIVE",
        settings={"anonymous": True, "synthetic_demo": True},
    )
    session.add(survey)
    await session.flush()
    profile_section = SurveySection(survey_id=survey.id, title="Perfil no identificable", description="Datos opcionales y no puntuables.", section_kind="EXOGENOUS", sort_order=1)
    risk_section = SurveySection(survey_id=survey.id, title="Factores psicosociales", description="Preguntas puntuables del escenario de demostración.", section_kind="INSTRUMENT", sort_order=2)
    session.add_all([profile_section, risk_section])
    await session.flush()
    for order, question in enumerate(questions, start=1):
        session.add(SurveyQuestion(
            survey_id=survey.id,
            question_id=question.id,
            section_id=profile_section.id if order <= descriptive_count else risk_section.id,
            sort_order=order,
            is_required=question.is_required_default,
            settings={},
        ))

    study = Study(
        project_id=project.id,
        survey_id=survey.id,
        instrument_version_id=version.id,
        name=f"{project.name} · CENSOPAS versión {payload.version_kind.lower()}",
        study_type="CENSO",
        status="OPEN",
        start_at=now,
        min_publishable_n=5,
        algorithm_version="colmena-demo-synthetic-1",
        settings={
            "industry": payload.industry,
            "anonymous_link": True,
            "synthetic_demo": True,
            "methodology_mode": "COLMENA_EXPLORATORY_SYNTHETIC",
            "report_disclaimer": "Datos sintéticos; no usar como expediente oficial.",
        },
        requires_invitation=False,
    )
    session.add(study)
    await session.flush()

    area_type = StudyUnitType(study_id=study.id, code="AREA", name="Área de trabajo", is_sensitive=False, sort_order=1, metadata_={"synthetic_demo": True})
    session.add(area_type)
    location_type = StudyUnitType(study_id=study.id, code="LOCATION", name="Sede", is_sensitive=False, sort_order=2, metadata_={"synthetic_demo": True})
    shift_type = StudyUnitType(study_id=study.id, code="SHIFT", name="Turno", is_sensitive=False, sort_order=3, metadata_={"synthetic_demo": True})
    job_type = StudyUnitType(study_id=study.id, code="JOB_FAMILY", name="Familia ocupacional", is_sensitive=False, sort_order=4, metadata_={"synthetic_demo": True})
    contract_type = StudyUnitType(study_id=study.id, code="CONTRACT", name="Tipo de contrato", is_sensitive=True, sort_order=5, metadata_={"synthetic_demo": True})
    session.add_all([location_type, shift_type, job_type, contract_type])
    await session.flush()
    areas = []
    for code, name in (("OPER", "Operaciones"), ("MANT", "Mantenimiento"), ("PLANTA", "Planta"), ("ADM", "Administración")):
        area = StudyUnit(study_unit_type_id=area_type.id, code=code, name=name, metadata_={"synthetic_demo": True})
        session.add(area)
        areas.append(area)
    locations = []
    for code, name in (("UM-CENTRAL", "Unidad Minera Central"), ("PLANTA-SUR", "Planta Sur"), ("LIMA", "Sede Lima")):
        unit = StudyUnit(study_unit_type_id=location_type.id, code=code, name=name, metadata_={"synthetic_demo": True})
        session.add(unit)
        locations.append(unit)
    shifts = []
    for code, name in (("DIA", "Turno día"), ("NOCHE", "Turno noche"), ("ADMIN", "Horario administrativo")):
        unit = StudyUnit(study_unit_type_id=shift_type.id, code=code, name=name, metadata_={"synthetic_demo": True})
        session.add(unit)
        shifts.append(unit)
    job_families = []
    for code, name in (("OPERATIVO", "Personal operativo"), ("TECNICO", "Técnicos y mantenimiento"), ("SUPERV", "Supervisión"), ("ADMIN", "Administración")):
        unit = StudyUnit(study_unit_type_id=job_type.id, code=code, name=name, metadata_={"synthetic_demo": True})
        session.add(unit)
        job_families.append(unit)
    contracts = []
    for code, name in (("INDEFINIDO", "Plazo indeterminado"), ("TEMPORAL", "Temporal · grupo protegido")):
        unit = StudyUnit(study_unit_type_id=contract_type.id, code=code, name=name, metadata_={"synthetic_demo": True})
        session.add(unit)
        contracts.append(unit)
    await session.flush()

    # Umbrales de navegación únicamente. Se guardan como EXPLORATORY y DRAFT,
    # por lo que el motor nunca los considera equivalentes a baremos oficiales.
    barem = Barem(
        instrument_version_id=version.id,
        name="Umbrales exploratorios del demo",
        population_label="Escenario sintético de minería",
        source_reference="Configuración de demo Colmena; no es un baremo oficial.",
        barem_version="demo-1",
        status="DRAFT",
        metadata_={"barem_type": "EXPLORATORY", "synthetic": True, "official_equivalence_enabled": False},
    )
    session.add(barem)
    await session.flush()
    constructs = list(dimensions.values()) + [leaf for _dimension, leaf in leaves]
    for construct in constructs:
        session.add(BaremCutoff(
            barem_id=barem.id,
            construct_id=construct.id,
            cut_1=33.33,
            cut_2=66.67,
            direction="LOWER_BETTER",
            favorable_label="FAVORABLE (demo)",
            intermediate_label="INTERMEDIO (demo)",
            unfavorable_label="DESFAVORABLE (demo)",
        ))
    study.barem_id = barem.id

    rng = Random(f"colmena-demo-{project.id}-{payload.version_kind}")
    risk_bias = (2.9, 3.7, 3.1, 3.8, 3.2, 3.5)
    excluded_limit = max(1, round(payload.synthetic_responses * 0.032))
    incomplete_limit = excluded_limit + max(1, round(payload.synthetic_responses * 0.04))
    question_dimension_index: dict[int, int] = {}
    for dimension_index, (_dimension, _leaf, bucket_questions) in enumerate(buckets):
        for question in bucket_questions:
            question_dimension_index[question.id] = dimension_index % len(_DIMENSIONS)
    for response_index in range(payload.synthetic_responses):
        started_at = now - timedelta(days=rng.randint(0, 20), minutes=rng.randint(5, 720))
        is_excluded = response_index < excluded_limit
        is_incomplete = excluded_limit <= response_index < incomplete_limit
        if is_excluded:
            status = "COMPLETED"
            validation_status = "EXCLUDED"
            duration_seconds = rng.randint(65, 130)
            completion_pct = 100
            completed_at = started_at + timedelta(seconds=duration_seconds)
            exclusion_reason = "Patrón sintético de velocidad o respuesta uniforme"
            quality_flags = ["SPEEDING", "STRAIGHT_LINING"]
        elif is_incomplete:
            status = "ABANDONED"
            validation_status = "PENDING"
            duration_seconds = rng.randint(170, 540)
            completion_pct = rng.randint(45, 82)
            completed_at = None
            exclusion_reason = None
            quality_flags = ["INCOMPLETE"]
        else:
            status = "COMPLETED"
            validation_status = "VALID"
            duration_seconds = rng.randint(420, 1500)
            completion_pct = 100
            completed_at = started_at + timedelta(seconds=duration_seconds)
            exclusion_reason = None
            quality_flags = []
        response_session = ResponseSession(
            study_id=study.id,
            status=status,
            validation_status=validation_status,
            started_at=started_at,
            completed_at=completed_at,
            duration_seconds=duration_seconds,
            completion_pct=completion_pct,
            exclusion_reason=exclusion_reason,
            metadata_={"synthetic_demo": True, "telemetry_profile": "mining", "quality_flags": quality_flags},
        )
        session.add(response_session)
        await session.flush()
        position = response_index / max(payload.synthetic_responses, 1)
        area = areas[0] if position < 0.38 else areas[2] if position < 0.64 else areas[1] if position < 0.86 else areas[3]
        location = locations[0] if position < 0.60 else locations[1] if position < 0.88 else locations[2]
        shift = shifts[0] if position < 0.48 else shifts[1] if position < 0.82 else shifts[2]
        job_family = job_families[0] if position < 0.44 else job_families[1] if position < 0.70 else job_families[2] if position < 0.86 else job_families[3]
        contract = contracts[1] if response_index >= payload.synthetic_responses - min(4, payload.synthetic_responses) else contracts[0]
        session.add_all([
            ResponseSessionUnit(response_session_id=response_session.id, study_unit_id=area.id),
            ResponseSessionUnit(response_session_id=response_session.id, study_unit_id=location.id),
            ResponseSessionUnit(response_session_id=response_session.id, study_unit_id=shift.id),
            ResponseSessionUnit(response_session_id=response_session.id, study_unit_id=job_family.id),
            ResponseSessionUnit(response_session_id=response_session.id, study_unit_id=contract.id),
        ])
        scored_questions = questions[descriptive_count:]
        answer_limit = round(len(scored_questions) * completion_pct / 100)
        for question in scored_questions[:answer_limit]:
            center = risk_bias[question_dimension_index.get(question.id, 0)]
            value = 3 if is_excluded else min(5, max(1, round(rng.gauss(center, 0.85))))
            option = options[value - 1]
            session.add(Response(
                study_id=study.id,
                response_session_id=response_session.id,
                question_id=question.id,
                option_id=option.id,
                raw_code=option.raw_code,
                numeric_value=value,
                is_missing=False,
                metadata_={"synthetic_demo": True},
            ))

    metadata = dict(project.metadata_ or {})
    metadata.update({
        "methodology": "CENSOPAS_COPSOQ",
        "methodology_mode": "COLMENA_EXPLORATORY_SYNTHETIC",
        "official_equivalence_enabled": False,
        "campaign_status": "OPEN",
        "demo_campaign": {
            "study_id": study.id,
            "study_public_id": str(study.public_id),
            "instrument_version_id": version.id,
            "barem_id": barem.id,
            "version_kind": payload.version_kind,
            "item_count": len(items),
            "synthetic_responses": payload.synthetic_responses,
        },
    })
    project.metadata_ = metadata
    await session.commit()

    # Ejecuta el mismo motor usado por los resultados internos. El baremo demo
    # queda DRAFT/EXPLORATORY y todas las salidas se presentan como provisionales.
    await CensopasScoringService(session).run_scoring(study.id)
    await session.refresh(project)
    return _result(project.id, project.metadata_)


@router.post("/projects/{project_id}/demo-campaign", response_model=DemoCampaignRead, status_code=201)
async def create_demo_campaign(project_id: int, payload: DemoCampaignCreate, session: AsyncSession = Depends(get_db)):
    project = await _require_project(session, project_id)
    return await _create_demo_campaign(session, project, payload)


@router.get("/projects/{project_id}/demo-campaign", response_model=DemoCampaignRead)
async def get_demo_campaign(project_id: int, session: AsyncSession = Depends(get_db)):
    project = await _require_project(session, project_id)
    if not (project.metadata_ or {}).get("demo_campaign"):
        raise NotFoundError("Este proyecto aún no tiene una campaña demo creada")
    return _result(project.id, project.metadata_)