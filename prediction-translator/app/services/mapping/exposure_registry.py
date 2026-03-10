EVENT_TO_BASKETS = {
    "oil_shock_near_term": [
        {"basket": "energy_winners", "direction": "positive", "confidence": 0.90},
        {"basket": "airlines", "direction": "negative", "confidence": 0.95},
        {"basket": "transports", "direction": "negative", "confidence": 0.80},
    ],
    "us_fed_cut_near_term": [
        {"basket": "duration_software", "direction": "positive", "confidence": 0.80},
        {"basket": "growth_proxy", "direction": "positive", "confidence": 0.70},
        {"basket": "banks", "direction": "conditional", "confidence": 0.50},
    ],
    "us_recession_odds": [
        {"basket": "staples", "direction": "positive", "confidence": 0.85},
        {"basket": "small_caps", "direction": "negative", "confidence": 0.85},
    ],
}
