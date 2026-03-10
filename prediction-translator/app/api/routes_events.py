from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db import get_db

router = APIRouter(prefix="/events", tags=["events"])


@router.get("/movers")
def get_event_movers(db: Session = Depends(get_db)) -> list[dict]:
    query = text(
        """
        WITH latest AS (
            SELECT m.id market_id, e.id event_id, e.title, e.category, v.name venue,
                   ms.probability_mid, ms.snapshot_ts,
                   ROW_NUMBER() OVER (PARTITION BY m.id ORDER BY ms.snapshot_ts DESC) as rn
            FROM market_snapshots ms
            JOIN markets m ON m.id = ms.market_id
            JOIN events e ON e.id = m.event_id
            JOIN venues v ON v.id = e.venue_id
        )
        SELECT event_id, title, category, venue, probability_mid as current_probability,
               0.0 as change_1d,
               0.0 as change_3d
        FROM latest WHERE rn = 1
        ORDER BY current_probability DESC
        LIMIT 25
        """
    )
    rows = db.execute(query).mappings().all()
    return [dict(r) for r in rows]
