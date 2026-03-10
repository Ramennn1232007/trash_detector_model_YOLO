from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.event import Event
from app.models.market import Market
from app.models.market_snapshot import MarketSnapshot
from app.models.venue import Venue
from app.services.ingest import kalshi_client, polymarket_client
from app.services.normalize.event_normalizer import normalize_event_text


def run_ingestion(db: Session) -> int:
    rows = kalshi_client.fetch_market_snapshots() + polymarket_client.fetch_market_snapshots()
    inserted = 0

    for row in rows:
        venue = db.execute(select(Venue).where(Venue.name == row["venue"])).scalar_one_or_none()
        if not venue:
            venue = Venue(name=row["venue"], active=True)
            db.add(venue)
            db.flush()

        norm = normalize_event_text(row["title"])
        event = db.execute(
            select(Event).where(
                Event.venue_id == venue.id,
                Event.external_event_id == row["external_event_id"],
            )
        ).scalar_one_or_none()
        if not event:
            event = Event(
                venue_id=venue.id,
                external_event_id=row["external_event_id"],
                title=row["title"],
                normalized_key=norm["normalized_key"],
                category=norm["category"],
                subcategory=norm["subcategory"],
                region=norm["region"],
            )
            db.add(event)
            db.flush()

        market = db.execute(
            select(Market).where(
                Market.venue_id == venue.id,
                Market.external_market_id == row["external_market_id"],
            )
        ).scalar_one_or_none()
        if not market:
            market = Market(
                event_id=event.id,
                venue_id=venue.id,
                external_market_id=row["external_market_id"],
                ticker_or_slug=row["external_market_id"],
                question=row["question"],
                outcome_type="yes_no",
                status="open",
                active=True,
            )
            db.add(market)
            db.flush()

        db.add(
            MarketSnapshot(
                market_id=market.id,
                snapshot_ts=row["snapshot_ts"],
                probability_mid=row["probability_mid"],
                best_bid=row.get("best_bid"),
                best_ask=row.get("best_ask"),
                volume_24h=row.get("volume_24h"),
            )
        )
        inserted += 1

    db.commit()
    return inserted
