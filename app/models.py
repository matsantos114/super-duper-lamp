from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, String, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Run(Base):
    __tablename__ = "runs"

    __table_args__ = (
        CheckConstraint(
            "distance_meters > 0",
            name="ck_runs_distance_meters_positive",
        ),
        CheckConstraint(
            "duration_seconds > 0",
            name="ck_runs_duration_seconds_positive",
        ),
        CheckConstraint(
            "elevation_gain_meters >= 0",
            name="ck_runs_elevation_gain_meters_nonnegative",
        ),
        CheckConstraint(
            "average_heart_rate BETWEEN 30 AND 250",
            name="ck_runs_average_heart_rate_range",
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    external_activity_id: Mapped[str] = mapped_column(String(255), unique=True)
    distance_meters: Mapped[int] = mapped_column()
    duration_seconds: Mapped[int] = mapped_column()
    started_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    elevation_gain_meters: Mapped[int | None] = mapped_column()
    average_heart_rate: Mapped[int | None] = mapped_column()
    notes: Mapped[str | None] = mapped_column(String(1000))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )