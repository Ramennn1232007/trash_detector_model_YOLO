from sqlalchemy import Boolean, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class BasketMember(Base):
    __tablename__ = "basket_members"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    basket_id: Mapped[int] = mapped_column(ForeignKey("basket_definitions.id"), nullable=False)
    ticker: Mapped[str] = mapped_column(String(16), nullable=False)
    weight: Mapped[float] = mapped_column(Float, default=1.0)
    active: Mapped[bool] = mapped_column(Boolean, default=True)
