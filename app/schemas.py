from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class RunCreate(BaseModel):
    external_activity_id: str = Field(min_length=1, max_length=255)
    distance_meters: int = Field(gt=0)
    duration_seconds: int = Field(gt=0)
    started_at: datetime
    elevation_gain_meters: int | None = Field(default=None, ge=0)
    average_heart_rate: int | None = Field(default=None, ge=30, le=250)
    notes: str | None = Field(default=None, max_length=1000)


class RunRead(RunCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
