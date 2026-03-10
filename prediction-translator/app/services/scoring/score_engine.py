def build_signal_score(
    event_magnitude_score: float,
    liquidity_quality_score: float,
    mapping_confidence_score: float,
    basket_lag_score: float,
    cleanliness_score: float,
) -> tuple[float, str]:
    score = (
        0.25 * event_magnitude_score
        + 0.15 * liquidity_quality_score
        + 0.15 * mapping_confidence_score
        + 0.35 * basket_lag_score
        + 0.10 * cleanliness_score
    )
    if score >= 70:
        label = "strong"
    elif score >= 40:
        label = "moderate"
    else:
        label = "weak"
    return score, label
