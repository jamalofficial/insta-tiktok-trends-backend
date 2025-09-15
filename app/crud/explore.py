from sqlalchemy.orm import Session
from sqlalchemy import desc, asc
from typing import Optional, List
from ..models.explore import ExploreTopics
from ..schemas.explore import ExploreTopicCreate, ExploreTopicUpdate


def get_explore_topic_by_id(db: Session, topic_id: int) -> Optional[ExploreTopics]:
    """Get explore topic by ID"""
    return db.query(ExploreTopics).filter(ExploreTopics.id == topic_id).first()


def get_explore_topics(db: Session, skip: int = 0, limit: int = 100, sort_by: str = "popularity") -> List[ExploreTopics]:
    """Get all explore topics with pagination and sorting"""
    query = db.query(ExploreTopics)
    
    if sort_by == "popularity":
        query = query.order_by(desc(ExploreTopics.popularity))
    elif sort_by == "title":
        query = query.order_by(asc(ExploreTopics.title))
    elif sort_by == "created_at":
        query = query.order_by(desc(ExploreTopics.created_at))
    
    return query.offset(skip).limit(limit).all()


def create_explore_topic(db: Session, topic: ExploreTopicCreate) -> ExploreTopics:
    """Create a new explore topic"""
    db_topic = ExploreTopics(**topic.dict())
    db.add(db_topic)
    db.commit()
    db.refresh(db_topic)
    return db_topic


def update_explore_topic(db: Session, topic_id: int, topic_update: ExploreTopicUpdate) -> Optional[ExploreTopics]:
    """Update explore topic"""
    db_topic = get_explore_topic_by_id(db, topic_id)
    if not db_topic:
        return None
    
    update_data = topic_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_topic, field, value)
    
    db.commit()
    db.refresh(db_topic)
    return db_topic


def delete_explore_topic(db: Session, topic_id: int) -> bool:
    """Delete explore topic"""
    db_topic = get_explore_topic_by_id(db, topic_id)
    if not db_topic:
        return False
    
    db.delete(db_topic)
    db.commit()
    return True


def search_explore_topics_by_title(db: Session, title: str, skip: int = 0, limit: int = 100) -> List[ExploreTopics]:
    """Search explore topics by title (case-insensitive)"""
    return db.query(ExploreTopics).filter(
        ExploreTopics.title.ilike(f"%{title}%")
    ).offset(skip).limit(limit).all()


def get_trending_explore_topics(db: Session, limit: int = 10) -> List[ExploreTopics]:
    """Get trending explore topics (highest popularity)"""
    return db.query(ExploreTopics).order_by(
        desc(ExploreTopics.popularity)
    ).limit(limit).all()


def get_explore_topics_count(db: Session) -> int:
    """Get total count of explore topics"""
    return db.query(ExploreTopics).count()