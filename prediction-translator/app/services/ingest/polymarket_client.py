from datetime import datetime, timezone


def fetch_market_snapshots() -> list[dict]:
    """Stubbed shape for Polymarket ingestion output."""
    return [
        {
            "venue": "polymarket",
            "external_event_id": "oil-disruption-30d",
            "external_market_id": "PM-OIL-30D",
            "title": "Will oil disruption odds rise in the next 30 days?",
            "question": "Will oil disruption odds rise in the next 30 days?",
            "snapshot_ts": datetime.now(timezone.utc),
            "probability_mid": 0.36,
            "best_bid": 0.35,
            "best_ask": 0.37,
            "volume_24h": 240000,
        }
    ]
