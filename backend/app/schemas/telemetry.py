from __future__ import annotations

import datetime as dt

from pydantic import BaseModel, Field


class TelemetrySeriesPoint(BaseModel):
    date: dt.date
    started: int
    completed: int


class VariableTelemetry(BaseModel):
    construct_id: int
    variable_code: str
    variable_name: str
    role: str | None = None
    question_count: int
    sessions_started: int
    sessions_answered: int
    sessions_completed: int
    completion_rate: float | None
    avg_completion_pct: float | None


class StudyTelemetry(BaseModel):
    study_id: int
    study_name: str
    instrument_id: int | None = None
    instrument_name: str | None = None
    instrument_version_id: int | None = None
    instrument_version_code: str | None = None
    started_count: int
    completed_count: int
    abandoned_count: int
    valid_count: int
    review_count: int
    excluded_count: int
    completion_rate: float | None
    avg_completion_pct: float | None
    avg_duration_seconds: float | None
    series: list[TelemetrySeriesPoint] = Field(default_factory=list)
    variables: list[VariableTelemetry] = Field(default_factory=list)


class ProjectTelemetry(BaseModel):
    project_id: int
    studies: list[StudyTelemetry] = Field(default_factory=list)
