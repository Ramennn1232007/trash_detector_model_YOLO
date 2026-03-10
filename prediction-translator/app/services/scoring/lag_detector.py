def compute_lag_gap(expected_move: float, actual_move: float, relationship_direction: str) -> float:
    if relationship_direction == "negative":
        expected_move = -abs(expected_move)
    return expected_move - actual_move
