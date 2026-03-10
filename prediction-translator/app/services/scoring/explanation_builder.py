def build_explanation(
    event_name: str,
    move_3d_pts: float,
    basket_name: str,
    expected_move: float,
    actual_move: float,
    lag_gap: float,
) -> str:
    return (
        f"{event_name} moved {move_3d_pts:+.1f} pts over 3d. "
        f"Linked basket {basket_name} was expected to move {expected_move:+.2f}% "
        f"but moved {actual_move:+.2f}% (lag gap {lag_gap:+.2f}%)."
    )
