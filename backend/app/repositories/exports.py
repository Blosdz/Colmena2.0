from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.export import Export


class ExportRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get(self, export_id: int) -> Export | None:
        return await self.session.get(Export, export_id)

    async def create(self, export: Export) -> Export:
        self.session.add(export)
        await self.session.flush()
        return export
