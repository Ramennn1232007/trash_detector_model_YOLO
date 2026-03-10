from sqlalchemy import Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class EventBasketLink(Base):
    __tablename__ = "event_basket_links"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    normalized_event_key: Mapped[str] = mapped_column(String(128), index=True, nullable=False)
    basket_id: Mapped[int] = mapped_column(ForeignKey("basket_definitions.id"), nullable=False)
    relationship_direction: Mapped[str] = mapped_column(String(16), nullable=False)
    confidence_weight: Mapped[float] = mapped_column(Float, nullable=False)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
