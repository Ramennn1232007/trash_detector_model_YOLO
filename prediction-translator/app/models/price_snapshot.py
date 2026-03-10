from sqlalchemy import DateTime, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class PriceSnapshot(Base):
    __tablename__ = "price_snapshots"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ticker: Mapped[str] = mapped_column(String(16), index=True, nullable=False)
    snapshot_ts: Mapped[DateTime] = mapped_column(DateTime(timezone=True), index=True, nullable=False)
    close_price: Mapped[float] = mapped_column(Float, nullable=False)
    return_1d: Mapped[float | None] = mapped_column(Float, nullable=True)
    return_3d: Mapped[float | None] = mapped_column(Float, nullable=True)
    return_7d: Mapped[float | None] = mapped_column(Float, nullable=True)
    volume: Mapped[float | None] = mapped_column(Float, nullable=True)
    market_cap: Mapped[float | None] = mapped_column(Float, nullable=True)
    beta_spy: Mapped[float | None] = mapped_column(Float, nullable=True)
