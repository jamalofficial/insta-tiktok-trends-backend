"""
Example queries for frontend integration.
This file demonstrates how to query the database for frontend requirements.
"""

from sqlalchemy.orm import Session
from app.database.db_setup import get_db
from app.models.explore_topic import ExploreTopic
from app.models.topic_result import TopicResult


def get_topic_with_keywords(topic_id: int, db: Session):
    """
    Get a topic with all its keywords for frontend display.
    This satisfies the frontend requirement to fetch all relevant_keywords.
    """
    topic = db.query(ExploreTopic).filter(ExploreTopic.id == topic_id).first()
    if not topic:
        return None
    
    # Get all keywords for this topic
    keywords = db.query(TopicResult.relevant_keyword).filter(
        TopicResult.explore_id == topic_id
    ).distinct().all()
    
    return {
        "topic": topic,
        "keywords": [keyword[0] for keyword in keywords]
    }


def get_topic_result_by_keyword(keyword: str, topic_id: int, db: Session):
    """
    Get full record details for a specific keyword.
    This satisfies the frontend requirement for clicking on keywords.
    """
    result = db.query(TopicResult).filter(
        TopicResult.explore_id == topic_id,
        TopicResult.relevant_keyword == keyword
    ).first()
    
    return result


def get_all_topics_with_keyword_counts(db: Session):
    """
    Get all topics with their keyword counts for dashboard display.
    """
    topics = db.query(ExploreTopic).all()
    result = []
    
    for topic in topics:
        keyword_count = db.query(TopicResult).filter(
            TopicResult.explore_id == topic.id
        ).count()
        
        result.append({
            "topic": topic,
            "keyword_count": keyword_count
        })
    
    return result


def search_topics_by_keyword(keyword: str, db: Session):
    """
    Search for topics that contain a specific keyword.
    """
    topics = db.query(ExploreTopic).join(TopicResult).filter(
        TopicResult.relevant_keyword.ilike(f"%{keyword}%")
    ).distinct().all()
    
    return topics
