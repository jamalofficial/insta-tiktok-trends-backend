from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any
from datetime import datetime
import re

from app.database.db_setup import get_db
from app.models.explore_topic import ExploreTopic
from app.models.topic_result import TopicResult

router = APIRouter(prefix="/logs", tags=["logs"])


def parse_popularity(value: str):
    """Parse strings like '134K' -> 134000, '1.2M' -> 1_200_000, or plain numbers."""
    if not value:
        return None
    try:
        v = str(value).strip()
        # remove commas
        v = v.replace(',', '')
        m = re.match(r'^([0-9,.]+)\s*([kKmM]?)$', v)
        if not m:
            # try to extract digits
            num = float(re.sub(r'[^0-9.]', '', v))
            return num
        num_str, suffix = m.groups()
        num = float(num_str)
        if suffix.lower() == 'k':
            return num * 1000
        if suffix.lower() == 'm':
            return num * 1_000_000
        return num
    except Exception:
        return None


def parse_percent(value: str):
    if not value:
        return None
    try:
        return float(str(value).strip().replace('%', ''))
    except Exception:
        return None


@router.post("/")
def import_logs(log_data: Dict[str, Any], db: Session = Depends(get_db)):
    """
    Import log data and save to ExploreTopic and TopicResult tables.

    Expected payload: { log: [ { title, demographics, locations, relatedTopics, searchPopularity, trendPercent, url }, ... ], info: { keyword: 'Logo' } }
    """
    try:
        logs = log_data.get("log", []) or []
        info = log_data.get("info", {}) or {}

        # Use info.keyword as the ExploreTopic.topic, fallback to 'logs'
        keyword = info.get("keyword") or info.get("key") or "logs"

        # Get or create ExploreTopic
        explore = db.query(ExploreTopic).filter(ExploreTopic.topic == keyword).first()
        if not explore:
            explore = ExploreTopic(topic=keyword, origin_user_id=0)
            db.add(explore)
            db.commit()
            db.refresh(explore)

        imported = 0
        for entry in logs:
            title = entry.get("title")
            if not title:
                continue

            # Build TopicResult row
            search_pop = parse_popularity(entry.get("searchPopularity"))
            trend = parse_percent(entry.get("trendPercent"))
            location_data = entry.get("locations") or []
            demographic_data = entry.get("demographics") or []

            tr = TopicResult(
                explore_id=explore.id,
                relevant_keyword=title,
                search_popularity=search_pop,
                search_increase=trend,
                location_data=location_data,
                demographic_data=demographic_data,
            )
            db.add(tr)
            imported += 1

        db.commit()
        return {"imported": imported, "explore_id": explore.id, "keyword": keyword}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to import logs: {e}")
