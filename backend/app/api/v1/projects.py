from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.pagination import Page, PageParams, page_params
from app.schemas.projects import ProjectCreate, ProjectRead, ProjectUpdate
from app.services.project_service import ProjectService

router = APIRouter(tags=["projects"])


@router.post("/projects", response_model=ProjectRead, status_code=201)
async def create_project(payload: ProjectCreate, session: AsyncSession = Depends(get_db)):
    service = ProjectService(session)
    project = await service.create(payload)
    return ProjectRead.model_validate(project)


@router.get("/projects", response_model=Page[ProjectRead])
async def list_projects(
    params: PageParams = Depends(page_params), session: AsyncSession = Depends(get_db)
):
    service = ProjectService(session)
    return await service.list(params)


@router.get("/projects/{project_id}", response_model=ProjectRead)
async def get_project(project_id: int, session: AsyncSession = Depends(get_db)):
    service = ProjectService(session)
    project = await service.get(project_id)
    return ProjectRead.model_validate(project)


@router.patch("/projects/{project_id}", response_model=ProjectRead)
async def update_project(
    project_id: int, payload: ProjectUpdate, session: AsyncSession = Depends(get_db)
):
    service = ProjectService(session)
    project = await service.update(project_id, payload)
    return ProjectRead.model_validate(project)
