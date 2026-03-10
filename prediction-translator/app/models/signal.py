from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class Signal(Base):
    __tablename__ = "signals"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    signal_run_id: Mapped[int] = mapped_column(ForeignKey("signal_runs.id"), nullable=False)
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"), nullable=False)
    market_id: Mapped[int] = mapped_column(ForeignKey("markets.id"), nullable=False)
    basket_id: Mapped[int] = mapped_column(ForeignKey("basket_definitions.id"), nullable=False)
    signal_ts: Mapped[DateTime] = mapped_column(DateTime(timezone=True), nullable=False)
    event_move_1d: Mapped[float] = mapped_column(Float, nullable=False)
    event_move_3d: Mapped[float] = mapped_column(Float, nullable=False)
    event_zscore: Mapped[float] = mapped_column(Float, nullable=False)
    basket_move_1d: Mapped[float] = mapped_column(Float, nullable=False)
    basket_move_3d: Mapped[float] = mapped_column(Float, nullable=False)
    expected_basket_move: Mapped[float] = mapped_column(Float, nullable=False)
    lag_gap: Mapped[float] = mapped_column(Float, nullable=False)
    signal_score: Mapped[float] = mapped_column(Float, nullable=False)
    signal_label: Mapped[str] = mapped_column(String(16), nullable=False)
    status: Mapped[str] = mapped_column(String(16), default="open")
    explanation_text: Mapped[str] = mapped_column(Text, nullable=False)
