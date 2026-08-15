from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import get_optional_current_user
from app.models.user import User
from app.schemas.analytics import (
    AnalysisMethodRead,
    AnalysisRunCreate,
    AnalysisRunRead,
    AvailableMethodsRequest,
    AvailableMethodsResponse,
    CompareGroupsRequest,
    ConstructCompareGroupsRequest,
    ConstructCompareGroupsResponse,
    CorrelationRequest,
    CrosstabRequest,
    DescribeRequest,
    FrequenciesRequest,
    KMeansRequest,
    LogisticRegressionRequest,
    NormalityRequest,
    NormalityResponse,
    ReliabilityRequest,
    SpearmanMatrixRequest,
    SpearmanMatrixResponse,
)
from app.services.analysis_service import AnalysisService
from app.services.advanced_analysis_service import AdvancedAnalysisService

router = APIRouter(tags=["analytics"])


@router.get("/analytics/methods", response_model=list[AnalysisMethodRead])
async def list_analysis_methods(session: AsyncSession = Depends(get_db)):
    service = AnalysisService(session)
    methods = await service.list_methods()
    return [AnalysisMethodRead.model_validate(m) for m in methods]


@router.post(
    "/studies/{study_id}/analytics/available-methods", response_model=AvailableMethodsResponse
)
async def available_methods(
    study_id: int, payload: AvailableMethodsRequest, session: AsyncSession = Depends(get_db)
):
    del study_id
    service = AnalysisService(session)
    methods = await service.available_methods(payload.variable_ids)
    return AvailableMethodsResponse(methods=methods)


@router.post("/studies/{study_id}/analytics/describe", response_model=AnalysisRunRead)
async def describe(
    study_id: int, payload: DescribeRequest, session: AsyncSession = Depends(get_db)
):
    service = AnalysisService(session)
    run = await service.run_descriptive(study_id, payload)
    return AnalysisRunRead.model_validate(run)


@router.post("/studies/{study_id}/analytics/frequencies", response_model=AnalysisRunRead)
async def frequencies(
    study_id: int, payload: FrequenciesRequest, session: AsyncSession = Depends(get_db)
):
    service = AnalysisService(session)
    run = await service.run_frequencies(study_id, payload)
    return AnalysisRunRead.model_validate(run)


@router.post("/studies/{study_id}/analytics/crosstab", response_model=AnalysisRunRead)
async def crosstab(
    study_id: int, payload: CrosstabRequest, session: AsyncSession = Depends(get_db)
):
    service = AnalysisService(session)
    run = await service.run_crosstab(study_id, payload)
    return AnalysisRunRead.model_validate(run)


@router.post("/studies/{study_id}/analytics/compare-groups", response_model=AnalysisRunRead)
async def compare_groups(
    study_id: int, payload: CompareGroupsRequest, session: AsyncSession = Depends(get_db)
):
    service = AnalysisService(session)
    run = await service.run_compare_groups(study_id, payload)
    return AnalysisRunRead.model_validate(run)


@router.post("/studies/{study_id}/analytics/correlation", response_model=AnalysisRunRead)
async def correlation(
    study_id: int, payload: CorrelationRequest, session: AsyncSession = Depends(get_db)
):
    service = AnalysisService(session)
    run = await service.run_correlation(study_id, payload)
    return AnalysisRunRead.model_validate(run)


@router.post("/studies/{study_id}/analytics/reliability", response_model=AnalysisRunRead)
async def reliability(
    study_id: int, payload: ReliabilityRequest, session: AsyncSession = Depends(get_db)
):
    service = AnalysisService(session)
    run = await service.run_reliability(study_id, payload)
    return AnalysisRunRead.model_validate(run)


@router.post("/studies/{study_id}/analytics/logistic-regression", response_model=AnalysisRunRead)
async def logistic_regression(
    study_id: int, payload: LogisticRegressionRequest, session: AsyncSession = Depends(get_db)
):
    service = AnalysisService(session)
    run = await service.run_logistic_regression(study_id, payload)
    return AnalysisRunRead.model_validate(run)


@router.post("/studies/{study_id}/analytics/kmeans", response_model=AnalysisRunRead)
async def kmeans(study_id: int, payload: KMeansRequest, session: AsyncSession = Depends(get_db)):
    service = AnalysisService(session)
    run = await service.run_kmeans(study_id, payload)
    return AnalysisRunRead.model_validate(run)


@router.post(
    "/studies/{study_id}/analytics/normality", response_model=NormalityResponse
)
async def normality(
    study_id: int, payload: NormalityRequest, session: AsyncSession = Depends(get_db)
):
    return await AdvancedAnalysisService(session).run_normality(study_id, payload)


@router.post(
    "/studies/{study_id}/analytics/spearman-matrix",
    response_model=SpearmanMatrixResponse,
)
async def spearman_matrix(
    study_id: int,
    payload: SpearmanMatrixRequest,
    current_user: User | None = Depends(get_optional_current_user),
    session: AsyncSession = Depends(get_db),
):
    return await AdvancedAnalysisService(session).run_spearman_matrix(
        study_id, payload, current_user
    )


@router.post(
    "/studies/{study_id}/analytics/construct-compare-groups",
    response_model=ConstructCompareGroupsResponse,
)
async def construct_compare_groups(
    study_id: int,
    payload: ConstructCompareGroupsRequest,
    session: AsyncSession = Depends(get_db),
):
    return await AdvancedAnalysisService(session).compare_construct_groups(study_id, payload)


@router.post("/studies/{study_id}/analysis-runs", response_model=AnalysisRunRead, status_code=201)
async def create_analysis_run(
    study_id: int, payload: AnalysisRunCreate, session: AsyncSession = Depends(get_db)
):
    service = AnalysisService(session)
    run = await service.run_generic(study_id, payload)
    return AnalysisRunRead.model_validate(run)


@router.get("/analysis-runs/{run_id}", response_model=AnalysisRunRead)
async def get_analysis_run(run_id: int, session: AsyncSession = Depends(get_db)):
    service = AnalysisService(session)
    run = await service.get_run(run_id)
    return AnalysisRunRead.model_validate(run)
