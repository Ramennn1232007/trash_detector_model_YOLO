from sqlalchemy import DateTime, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class SignalRun(Base):
    __tablename__ = "signal_runs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    run_ts: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    run_type: Mapped[str] = mapped_column(String(32), default="scheduled")
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
