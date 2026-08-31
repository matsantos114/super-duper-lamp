from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String


class Base(DeclarativeBase):
    pass


class Run(Base):
    __tablename__ = "runs"
    id: Mapped[int] = mapped_column(primary_key=True)
    external_activity_id: Mapped[str] = mapped_column(String(255), unique=True)
    distance_meters: Mapped[int] = mapped_column()
    duration_seconds: Mapped[int] = mapped_column()