from pydantic import BaseModel


class EventMover(BaseModel):
    event_id: int
    title: str
    category: str
    venue: str
    current_probability: float
    change_1d: float
    change_3d: float
