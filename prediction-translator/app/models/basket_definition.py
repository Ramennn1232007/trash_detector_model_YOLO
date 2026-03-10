from sqlalchemy import Boolean, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class BasketDefinition(Base):
    __tablename__ = "basket_definitions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    ticker_symbol: Mapped[str | None] = mapped_column(String(16), nullable=True)
    basket_type: Mapped[str] = mapped_column(String(16), default="etf")
    theme: Mapped[str] = mapped_column(String(64), nullable=False)
    directionality: Mapped[str] = mapped_column(String(16), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
