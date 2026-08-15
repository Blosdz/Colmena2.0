from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.analytics import AnalysisRunRead
from app.schemas.censopas import (
    BaremActivationRead,
    BaremBandGenerate,
    BaremBandsReplace,
    BaremDetailRead,
    BaremCreate,
    BaremEditableCopyCreate,
    BaremCutoffCreate,
    BaremCutoffRead,
    BaremRead,
    CensopasBaremImportRead,
    CensopasBaremManifest,
    CensopasBaremManifestValidation,
    CensopasManifest,
    CensopasManifestImportRead,
    CensopasManifestValidation,
    CensopasReadiness,
    CensopasResultsResponse,
    CensopasUnitResultsResponse,
    ConstructResultRead,
    ScoringRuleCreate,
    ScoringRuleRead,
)
from app.repositories.analytics import AnalyticsRepository
from app.services.censopas_service import CensopasScoringService
from app.services.study_service import StudyService

router = APIRouter(tags=["censopas"])


@router.post(
    "/instrument-versions/{version_id}/validate-manifest",
    response_model=CensopasManifestValidation,
)
async def validate_censopas_manifest(
    version_id: int,
    payload: CensopasManifest,
    session: AsyncSession = Depends(get_db),
):
    service = CensopasScoringService(session)
    await service.get_readiness(version_id)
    return service.validate_manifest_payload(payload)


@router.post(
    "/instrument-versions/{version_id}/import-manifest",
    response_model=CensopasManifestImportRead,
    status_code=201,
)
async def import_censopas_manifest(
    version_id: int,
    payload: CensopasManifest,
    session: AsyncSession = Depends(get_db),
):
    return await CensopasScoringService(session).import_manifest(version_id, payload)


@router.post(
    "/instrument-versions/{version_id}/validate-barem-manifest",
    response_model=CensopasBaremManifestValidation,
)
async def validate_censopas_barem_manifest(
    version_id: int,
    payload: CensopasBaremManifest,
    session: AsyncSession = Depends(get_db),
):
    return await CensopasScoringService(session).validate_barem_manifest(
        version_id, payload
    )


@router.post(
    "/instrument-versions/{version_id}/import-barem-manifest",
    response_model=CensopasBaremImportRead,
    status_code=201,
)
async def import_censopas_barem_manifest(
    version_id: int,
    payload: CensopasBaremManifest,
    session: AsyncSession = Depends(get_db),
):
    return await CensopasScoringService(session).import_barem_manifest(
        version_id, payload
    )


@router.get(
    "/instrument-versions/{version_id}/censopas/readiness",
    response_model=CensopasReadiness,
)
async def get_censopas_readiness(
    version_id: int, session: AsyncSession = Depends(get_db)
):
    service = CensopasScoringService(session)
    return CensopasReadiness(**(await service.get_readiness(version_id)))


@router.post(
    "/instrument-versions/{version_id}/scoring-rules",
    response_model=ScoringRuleRead,
    status_code=201,
)
async def create_scoring_rule(
    version_id: int, payload: ScoringRuleCreate, session: AsyncSession = Depends(get_db)
):
    service = CensopasScoringService(session)
    rule = await service.create_scoring_rule(version_id, payload)
    return ScoringRuleRead.model_validate(rule)


@router.get(
    "/instrument-versions/{version_id}/scoring-rules", response_model=list[ScoringRuleRead]
)
async def list_scoring_rules(version_id: int, session: AsyncSession = Depends(get_db)):
    service = CensopasScoringService(session)
    rules = await service.list_scoring_rules(version_id)
    return [ScoringRuleRead.model_validate(r) for r in rules]


@router.post(
    "/instrument-versions/{version_id}/barems", response_model=BaremRead, status_code=201
)
async def create_barem(
    version_id: int, payload: BaremCreate, session: AsyncSession = Depends(get_db)
):
    service = CensopasScoringService(session)
    barem = await service.create_barem(version_id, payload)
    return BaremRead.model_validate(barem)


@router.get(
    "/instrument-versions/{version_id}/barems", response_model=list[BaremDetailRead]
)
async def list_barems(version_id: int, session: AsyncSession = Depends(get_db)):
    service = CensopasScoringService(session)
    barems = await service.list_barems(version_id)
    return [BaremDetailRead.model_validate(barem) for barem in barems]


@router.put("/barems/{barem_id}/bands", response_model=BaremDetailRead)
async def replace_barem_bands(
    barem_id: int,
    payload: BaremBandsReplace,
    session: AsyncSession = Depends(get_db),
):
    service = CensopasScoringService(session)
    barem = await service.replace_bands(barem_id, payload)
    return BaremDetailRead.model_validate(barem)


@router.post("/barems/{barem_id}/generate-bands", response_model=BaremDetailRead)
async def generate_barem_bands(
    barem_id: int,
    payload: BaremBandGenerate,
    session: AsyncSession = Depends(get_db),
):
    service = CensopasScoringService(session)
    barem = await service.generate_bands(barem_id, payload)
    return BaremDetailRead.model_validate(barem)


@router.post("/barems/{barem_id}/editable-copy", response_model=BaremDetailRead, status_code=201)
async def create_editable_barem_copy(
    barem_id: int,
    payload: BaremEditableCopyCreate,
    session: AsyncSession = Depends(get_db),
):
    service = CensopasScoringService(session)
    barem = await service.create_editable_barem_copy(barem_id, payload)
    return BaremDetailRead.model_validate(barem)


@router.post("/barems/{barem_id}/activate", response_model=BaremActivationRead)
async def activate_barem(barem_id: int, session: AsyncSession = Depends(get_db)):
    service = CensopasScoringService(session)
    barem = await service.activate_barem(barem_id)
    return BaremActivationRead(id=barem.id, status=barem.status, activated=True, validations=[])


@router.post("/barems/{barem_id}/cutoffs", response_model=BaremCutoffRead, status_code=201)
async def add_barem_cutoff(
    barem_id: int, payload: BaremCutoffCreate, session: AsyncSession = Depends(get_db)
):
    service = CensopasScoringService(session)
    cutoff = await service.add_cutoff(barem_id, payload)
    return BaremCutoffRead.model_validate(cutoff)


@router.post("/studies/{study_id}/censopas/scoring", response_model=AnalysisRunRead)
async def run_censopas_scoring(study_id: int, session: AsyncSession = Depends(get_db)):
    service = CensopasScoringService(session)
    run = await service.run_scoring(study_id)
    # CENSOPAS scoring no persiste analysis_results genéricos (usa
    # construct_results); recargar con `results` eager-loaded evita un
    # lazy-load fuera de contexto async al serializar la respuesta.
    run = await AnalyticsRepository(session).get_run(run.id)
    return AnalysisRunRead.model_validate(run)


@router.get(
    "/studies/{study_id}/censopas/unit-results",
    response_model=CensopasUnitResultsResponse,
)
async def get_censopas_unit_results(
    study_id: int,
    unit_type_id: int,
    session: AsyncSession = Depends(get_db),
):
    return CensopasUnitResultsResponse(
        **(
            await CensopasScoringService(session).get_unit_results(
                study_id, unit_type_id
            )
        )
    )


@router.get("/studies/{study_id}/censopas/results", response_model=CensopasResultsResponse)
async def get_censopas_results(study_id: int, session: AsyncSession = Depends(get_db)):
    study_service = StudyService(session)
    study = await study_service.get(study_id)

    scoring_status = "NOT_CONFIGURED"
    official_equivalence_enabled = False
    if study.instrument_version_id is not None:
        version = await study_service.instrument_repo.get_version_with_instrument(
            study.instrument_version_id
        )
        if version is not None:
            scoring_status = version.scoring_status
            official_equivalence_enabled = bool(
                version.instrument.metadata_.get("official_equivalence_enabled", False)
            )

    service = CensopasScoringService(session)
    results = await service.get_results_or_conflict(study_id)
    payload = [
        ConstructResultRead(**service.apply_privacy(r, study.min_publishable_n)) for r in results
    ]

    return CensopasResultsResponse(
        study_id=study_id,
        scoring_status=scoring_status,
        official_equivalence_enabled=official_equivalence_enabled,
        results=payload,
    )
