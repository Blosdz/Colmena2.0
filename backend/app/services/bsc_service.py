"""Plan preventivo / Balanced Scorecard (harness §20 tablas, mencionado en §78 dashboard empresarial).

CRUD directo — no hay lógica de negocio compleja explícita en el harness
para esta parte más allá de "seguimiento preventivo".
"""

from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import NotFoundError
from app.models.bsc import ActionPlan, ActionPlanItem, Kpi, KpiMeasurement
from app.repositories.bsc import BscRepository
from app.repositories.studies import StudyRepository
from app.schemas.bsc import (
    ActionPlanCreate,
    ActionPlanItemCreate,
    ActionPlanItemUpdate,
    KpiCreate,
    KpiMeasurementCreate,
)


class BscService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.repo = BscRepository(session)
        self.study_repo = StudyRepository(session)

    async def create_action_plan(self, study_id: int, payload: ActionPlanCreate) -> ActionPlan:
        study = await self.study_repo.get(study_id)
        if study is None:
            raise NotFoundError(f"Estudio {study_id} no encontrado")
        plan = ActionPlan(study_id=study_id, name=payload.name)
        plan = await self.repo.add_action_plan(plan)
        await self.session.commit()
        return plan

    async def list_action_plans(self, study_id: int) -> list[ActionPlan]:
        return await self.repo.list_action_plans(study_id)

    async def get_action_plan(self, action_plan_id: int) -> ActionPlan:
        plan = await self.repo.get_action_plan(action_plan_id)
        if plan is None:
            raise NotFoundError(f"Plan de acción {action_plan_id} no encontrado")
        return plan

    async def add_item(self, action_plan_id: int, payload: ActionPlanItemCreate) -> ActionPlanItem:
        await self.get_action_plan(action_plan_id)
        item = ActionPlanItem(
            action_plan_id=action_plan_id,
            construct_id=payload.construct_id,
            title=payload.title,
            finding=payload.finding,
            action_description=payload.action_description,
            responsible_user_id=payload.responsible_user_id,
            responsible_label=payload.responsible_label,
            priority=payload.priority,
            due_date=payload.due_date,
        )
        item = await self.repo.add_item(item)
        await self.session.commit()
        return item

    async def list_items(self, action_plan_id: int) -> list[ActionPlanItem]:
        await self.get_action_plan(action_plan_id)
        return await self.repo.list_items(action_plan_id)

    async def update_item(self, item_id: int, payload: ActionPlanItemUpdate) -> ActionPlanItem:
        item = await self.repo.get_item(item_id)
        if item is None:
            raise NotFoundError(f"Ítem de plan de acción {item_id} no encontrado")
        data = payload.model_dump(exclude_unset=True)
        for field, value in data.items():
            setattr(item, field, value)
        await self.session.commit()
        await self.session.refresh(item)
        return item

    async def create_kpi(self, study_id: int, payload: KpiCreate) -> Kpi:
        study = await self.study_repo.get(study_id)
        if study is None:
            raise NotFoundError(f"Estudio {study_id} no encontrado")
        kpi = Kpi(
            study_id=study_id,
            action_plan_item_id=payload.action_plan_item_id,
            code=payload.code,
            name=payload.name,
            description=payload.description,
            formula=payload.formula,
            unit=payload.unit,
            baseline_value=payload.baseline_value,
            target_value=payload.target_value,
            frequency=payload.frequency,
        )
        kpi = await self.repo.add_kpi(kpi)
        await self.session.commit()
        return kpi

    async def list_kpis(self, study_id: int) -> list[Kpi]:
        return await self.repo.list_kpis(study_id)

    async def add_measurement(self, kpi_id: int, payload: KpiMeasurementCreate) -> KpiMeasurement:
        kpi = await self.repo.get_kpi(kpi_id)
        if kpi is None:
            raise NotFoundError(f"KPI {kpi_id} no encontrado")
        measurement = KpiMeasurement(
            kpi_id=kpi_id,
            measured_at=payload.measured_at,
            numeric_value=payload.numeric_value,
            text_value=payload.text_value,
            status=payload.status,
            source_reference=payload.source_reference,
        )
        measurement = await self.repo.add_measurement(measurement)
        await self.session.commit()
        return measurement

    async def list_measurements(self, kpi_id: int) -> list[KpiMeasurement]:
        return await self.repo.list_measurements(kpi_id)
