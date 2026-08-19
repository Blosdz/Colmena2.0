from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class CompanyLocation(BaseModel):
    code: str = Field(min_length=1, max_length=40)
    name: str = Field(min_length=1, max_length=160)
    address: str | None = Field(default=None, max_length=300)
    worker_count: int = Field(default=0, ge=0, le=1_000_000)


class CompanySignatory(BaseModel):
    role: str = Field(min_length=1, max_length=80)
    full_name: str = Field(default="", max_length=180)
    professional_id: str | None = Field(default=None, max_length=80)
    position: str | None = Field(default=None, max_length=160)


class CompanyProfileUpdate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    legal_name: str = Field(min_length=1, max_length=255)
    tax_id: str = Field(min_length=11, max_length=11)
    organization_type: str = Field(default="EMPRESA", max_length=80)
    industry: str = Field(default="MINERIA", max_length=120)
    ciiu_code: str | None = Field(default=None, max_length=20)
    fiscal_address: str | None = Field(default=None, max_length=300)
    worker_count: int = Field(ge=1, le=1_000_000)
    representative_name: str | None = Field(default=None, max_length=180)
    study_lead_name: str | None = Field(default=None, max_length=180)
    contact_email: str | None = Field(default=None, max_length=320)
    contact_phone: str | None = Field(default=None, max_length=40)
    brand_color: str = Field(default="#D59B27", pattern=r"^#[0-9A-Fa-f]{6}$")
    locations: list[CompanyLocation] = Field(default_factory=list)
    signatories: list[CompanySignatory] = Field(default_factory=list)

    @field_validator("tax_id")
    @classmethod
    def validate_tax_id(cls, value: str) -> str:
        if not value.isdigit():
            raise ValueError("El RUC debe contener exactamente 11 dígitos.")
        return value


class CompanyProfileRead(BaseModel):
    id: int
    public_id: uuid.UUID
    name: str
    legal_name: str | None
    tax_id: str | None
    organization_type: str | None
    status: str
    industry: str | None = None
    ciiu_code: str | None = None
    fiscal_address: str | None = None
    worker_count: int | None = None
    representative_name: str | None = None
    study_lead_name: str | None = None
    contact_email: str | None = None
    contact_phone: str | None = None
    brand_color: str = "#D59B27"
    locations: list[CompanyLocation] = Field(default_factory=list)
    signatories: list[CompanySignatory] = Field(default_factory=list)
    completeness_pct: int = 0
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
