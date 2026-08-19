from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class OrganizationCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    legal_name: str | None = None
    tax_id: str | None = None
    organization_type: str | None = None


class RegisterRequest(BaseModel):
    email: EmailStr
    username: str = Field(min_length=3, max_length=120)
    password: str = Field(min_length=8, max_length=128)
    first_name: str | None = None
    last_name: str | None = None
    organization: OrganizationCreate | None = None


class OrganizationRead(BaseModel):
    id: int
    public_id: uuid.UUID
    name: str
    legal_name: str | None
    tax_id: str | None
    organization_type: str | None
    status: str

    model_config = ConfigDict(from_attributes=True)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserRead(BaseModel):
    id: int
    public_id: uuid.UUID
    email: str | None
    username: str | None
    first_name: str | None
    last_name: str | None
    status: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
