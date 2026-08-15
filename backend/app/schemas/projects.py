from __future__ import annotations

import uuid
from datetime import datetime
from typing import Literal

from pydantic import AliasChoices, BaseModel, ConfigDict, Field

ProjectType = Literal["ACADEMIC", "CENSO", "CUSTOM", "RESEARCH"]


class ProjectCreate(BaseModel):
    owner_user_id: int
    organization_id: int | None = None
    name: str = Field(min_length=1, max_length=255)
    project_type: ProjectType
    description: str | None = None
    metadata: dict = Field(default_factory=dict)


class ProjectUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None
    status: str | None = None
    metadata: dict | None = None


class ProjectRead(BaseModel):
    id: int
    public_id: uuid.UUID
    owner_user_id: int
    organization_id: int | None
    name: str
    project_type: str
    description: str | None
    status: str
    # El atributo Python en el modelo ORM es `metadata_` (para no chocar con
    # `DeclarativeBase.metadata`); aquí se lee desde ahí pero se expone como
    # `metadata` en la API (harness §7).
    metadata: dict = Field(validation_alias=AliasChoices("metadata_", "metadata"))
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
