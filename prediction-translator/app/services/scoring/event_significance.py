import numpy as np


def compute_event_significance(delta_1d: float, delta_3d: float, recent_deltas: list[float], volume_score: float) -> float:
    std = float(np.std(recent_deltas)) if recent_deltas else 0.0
    z = abs(delta_3d) / std if std > 1e-9 else 0.0
    return (0.4 * abs(delta_1d)) + (0.6 * z) + (0.1 * volume_score)
