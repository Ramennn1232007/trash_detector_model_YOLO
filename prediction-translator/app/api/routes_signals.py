from fastapi import APIRouter

from app.services.scoring.explanation_builder import build_explanation
from app.services.scoring.expected_move_model import expected_basket_move
from app.services.scoring.lag_detector import compute_lag_gap
from app.services.scoring.score_engine import build_signal_score

router = APIRouter(prefix="/signals", tags=["signals"])


@router.get("")
def get_signals() -> list[dict]:
    event_move_3d = 12.4
    expected = expected_basket_move(event_move_3d, beta=-0.21)
    actual = -0.9
    lag_gap = compute_lag_gap(expected, actual, "negative")
    score, label = build_signal_score(80, 70, 95, abs(lag_gap) * 30, 75)

    return [
        {
            "event": "Oil disruption odds (next 30 days)",
            "basket": "Airlines",
            "event_move_3d": event_move_3d,
            "expected_basket_move": round(expected, 2),
            "actual_basket_move": actual,
            "lag_gap": round(lag_gap, 2),
            "score": round(score, 1),
            "label": label,
            "explanation": build_explanation(
                "Oil disruption odds",
                event_move_3d,
                "Airlines",
                expected,
                actual,
                lag_gap,
            ),
        }
    ]
