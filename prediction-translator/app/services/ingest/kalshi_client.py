from datetime import datetime, timezone


def fetch_market_snapshots() -> list[dict]:
    """Stubbed shape for Kalshi ingestion output."""
    return [
        {
            "venue": "kalshi",
            "external_event_id": "fed-cut-sep",
            "external_market_id": "KX-FEDCUT-SEP",
            "title": "Will the Fed cut rates by September?",
            "question": "Will the Fed cut rates by September?",
            "snapshot_ts": datetime.now(timezone.utc),
            "probability_mid": 0.44,
            "best_bid": 0.43,
            "best_ask": 0.45,
            "volume_24h": 180000,
        }
    ]
