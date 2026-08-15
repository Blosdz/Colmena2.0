from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.core.pagination import Page, PageParams, paginate
from app.models.project import Project
from app.repositories.projects import ProjectRepository
from app.schemas.projects import ProjectCreate, ProjectRead, ProjectUpdate


class ProjectService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.repo = ProjectRepository(session)

    async def create(self, payload: ProjectCreate) -> Project:
        project = Project(
            owner_user_id=payload.owner_user_id,
            organization_id=payload.organization_id,
            name=payload.name,
            project_type=payload.project_type,
            description=payload.description,
            metadata_=payload.metadata,
        )
        project = await self.repo.create(project)
        await self.session.commit()
        return project

    async def get(self, project_id: int) -> Project:
        project = await self.repo.get(project_id)
        if project is None:
            raise NotFoundError(f"Proyecto {project_id} no encontrado")
        return project

    async def list(self, params: PageParams) -> Page[ProjectRead]:
        items, total = await paginate(self.session, self.repo.list_stmt(), params)
        return Page[ProjectRead](
            items=[ProjectRead.model_validate(item) for item in items],
            page=params.page,
            page_size=params.page_size,
            total=total,
        )

    async def update(self, project_id: int, payload: ProjectUpdate) -> Project:
        project = await self.get(project_id)
        data = payload.model_dump(exclude_unset=True)
        if "metadata" in data:
            project.metadata_ = data.pop("metadata")
        for field, value in data.items():
            setattr(project, field, value)
        await self.session.commit()
        await self.session.refresh(project)
        return project
