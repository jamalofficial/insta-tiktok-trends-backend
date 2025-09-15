from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from ..core.database import get_db
from ..core.roles import require_viewer, require_editor, require_admin, get_current_user
from ..crud.explore import (
    get_explore_topics, get_explore_topic_by_id, create_explore_topic,
    update_explore_topic, delete_explore_topic, search_explore_topics_by_title,
    get_trending_explore_topics
)
from ..schemas.explore import ExploreTopic, ExploreTopicCreate, ExploreTopicUpdate

router = APIRouter(prefix="/explore", tags=["explore"])


@router.get("/topics", response_model=List[ExploreTopic])
def get_all_explore_topics(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    sort_by: str = Query("popularity", regex="^(popularity|title|created_at)$"),
    current_user = Depends(require_viewer),
    db: Session = Depends(get_db)
) -> List[ExploreTopic]:
    """Get all explore topics with pagination and sorting"""
    topics = get_explore_topics(db, skip=skip, limit=limit, sort_by=sort_by)
    return topics


@router.get("/topics/trending", response_model=List[ExploreTopic])
def get_trending_topics(
    limit: int = Query(10, ge=1, le=50),
    current_user = Depends(require_viewer),
    db: Session = Depends(get_db)
) -> List[ExploreTopic]:
    """Get trending explore topics (highest popularity)"""
    topics = get_trending_explore_topics(db, limit=limit)
    return topics


@router.get("/topics/search", response_model=List[ExploreTopic])
def search_explore_topics(
    q: str = Query(..., min_length=1),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user = Depends(require_viewer),
    db: Session = Depends(get_db)
) -> List[ExploreTopic]:
    """Search explore topics by title"""
    topics = search_explore_topics_by_title(db, q, skip=skip, limit=limit)
    return topics


@router.get("/topics/{topic_id}", response_model=ExploreTopic)
def get_explore_topic(
    topic_id: int,
    current_user = Depends(require_viewer),
    db: Session = Depends(get_db)
) -> ExploreTopic:
    """Get explore topic by ID"""
    topic = get_explore_topic_by_id(db, topic_id)
    if not topic:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Explore topic not found"
        )
    return topic


@router.post("/topics", response_model=ExploreTopic)
def create_new_explore_topic(
    topic_data: ExploreTopicCreate,
    current_user = Depends(require_editor),
    db: Session = Depends(get_db)
) -> ExploreTopic:
    """Create a new explore topic (editor or admin)"""
    topic = create_explore_topic(db, topic_data)
    return topic


@router.put("/topics/{topic_id}", response_model=ExploreTopic)
def update_explore_topic_info(
    topic_id: int,
    topic_update: ExploreTopicUpdate,
    current_user = Depends(require_editor),
    db: Session = Depends(get_db)
) -> ExploreTopic:
    """Update explore topic (editor or admin)"""
    topic = update_explore_topic(db, topic_id, topic_update)
    if not topic:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Explore topic not found"
        )
    return topic


@router.delete("/topics/{topic_id}")
def delete_explore_topic_entry(
    topic_id: int,
    current_user = Depends(require_admin),
    db: Session = Depends(get_db)
) -> dict:
    """Delete explore topic (admin only)"""
    success = delete_explore_topic(db, topic_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Explore topic not found"
        )
    return {"message": "Explore topic deleted successfully"}
