from fastapi import APIRouter

router = APIRouter(prefix="/baskets", tags=["baskets"])


@router.get("")
def list_baskets() -> list[dict]:
    return [
        {"name": "energy_winners", "ticker": "XLE", "return_3d": 1.8},
        {"name": "airlines", "ticker": "JETS", "return_3d": -0.9},
        {"name": "growth_proxy", "ticker": "QQQ", "return_3d": 0.7},
        {"name": "staples", "ticker": "XLP", "return_3d": 0.5},
        {"name": "small_caps", "ticker": "IWM", "return_3d": -0.4},
    ]
