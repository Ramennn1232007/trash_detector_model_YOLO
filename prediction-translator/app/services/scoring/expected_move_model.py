def expected_basket_move(event_delta_3d: float, beta: float = 0.2, intercept: float = 0.0) -> float:
    """Simple baseline regression placeholder: basket_move = a + b * event_delta_3d."""
    return intercept + (beta * event_delta_3d)
