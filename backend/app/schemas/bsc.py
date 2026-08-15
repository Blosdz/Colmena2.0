from __future__ import annotations

import datetime as dt
import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ActionPlanCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)


class ActionPlanRead(BaseModel):
    id: int
    public_id: uuid.UUID
    study_id: int
    name: str
    status: str
    approved_by_user_id: int | None
    approved_at: datetime | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ActionPlanItemCreate(BaseModel):
    construct_id: int | None = None
    title: str = Field(min_length=1, max_length=255)
    finding: str | None = None
    action_description: str = Field(min_length=1)
    responsible_user_id: int | None = None
    responsible_label: str | None = None
    priority: int | None = None
    due_date: dt.date | None = None


class ActionPlanItemUpdate(BaseModel):
    title: str | None = None
    finding: str | None = None
    action_description: str | None = None
    responsible_label: str | None = None
    priority: int | None = None
    due_date: dt.date | None = None
    status: str | None = None


class ActionPlanItemRead(BaseModel):
    id: int
    action_plan_id: int
    construct_id: int | None
    title: str
    finding: str | None
    action_description: str
    responsible_label: str | None
    priority: int | None
    due_date: dt.date | None
    status: str

    model_config = ConfigDict(from_attributes=True)


class KpiCreate(BaseModel):
    action_plan_item_id: int | None = None
    code: str | None = None
    name: str = Field(min_length=1, max_length=255)
    description: str | None = None
    formula: str | None = None
    unit: str | None = None
    baseline_value: float | None = None
    target_value: float | None = None
    frequency: str | None = None


class KpiRead(BaseModel):
    id: int
    study_id: int
    action_plan_item_id: int | None
    code: str | None
    name: str
    baseline_value: float | None
    target_value: float | None
    frequency: str | None
    status: str

    model_config = ConfigDict(from_attributes=True)


class KpiMeasurementCreate(BaseModel):
    measured_at: datetime
    numeric_value: float | None = None
    text_value: str | None = None
    status: str | None = None
    source_reference: str | None = None


class KpiMeasurementRead(BaseModel):
    id: int
    kpi_id: int
    measured_at: datetime
    numeric_value: float | None
    text_value: str | None
    status: str | None

    model_config = ConfigDict(from_attributes=True)
