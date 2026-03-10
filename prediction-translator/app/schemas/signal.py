from pydantic import BaseModel


class SignalOut(BaseModel):
    event: str
    basket: str
    event_move_3d: float
    expected_basket_move: float
    actual_basket_move: float
    lag_gap: float
    score: float
    label: str
    explanation: str
