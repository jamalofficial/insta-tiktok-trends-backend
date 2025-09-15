from sqlalchemy.orm import Session
from sqlalchemy import desc, asc, func
from typing import Optional, List
from ..models.keyword import Keyword, SearchTopicKeyword
from ..models.search import SearchTopic
from ..schemas.keyword import KeywordCreate, KeywordUpdate, SearchTopicKeywordCreate


# Keyword CRUD operations
def get_keyword_by_id(db: Session, keyword_id: int) -> Optional[Keyword]:
    """Get keyword by ID"""
    return db.query(Keyword).filter(Keyword.id == keyword_id).first()


def get_keyword_by_name(db: Session, name: str) -> Optional[Keyword]:
    """Get keyword by name (case-insensitive)"""
    return db.query(Keyword).filter(func.lower(Keyword.name) == name.lower()).first()


def get_keywords(db: Session, skip: int = 0, limit: int = 100, sort_by: str = "popularity") -> List[Keyword]:
    """Get all keywords with pagination and sorting"""
    query = db.query(Keyword)
    
    if sort_by == "popularity":
        query = query.order_by(desc(Keyword.popularity))
    elif sort_by == "name":
        query = query.order_by(asc(Keyword.name))
    elif sort_by == "created_at":
        query = query.order_by(desc(Keyword.created_at))
    elif sort_by == "topics_count":
        query = query.order_by(desc(Keyword.topics_count))
    
    return query.offset(skip).limit(limit).all()


def create_keyword(db: Session, keyword: KeywordCreate) -> Keyword:
    """Create a new keyword"""
    db_keyword = Keyword(**keyword.dict())
    db.add(db_keyword)
    db.commit()
    db.refresh(db_keyword)
    return db_keyword


def update_keyword(db: Session, keyword_id: int, keyword_update: KeywordUpdate) -> Optional[Keyword]:
    """Update keyword"""
    db_keyword = get_keyword_by_id(db, keyword_id)
    if not db_keyword:
        return None
    
    update_data = keyword_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_keyword, field, value)
    
    db.commit()
    db.refresh(db_keyword)
    return db_keyword


def delete_keyword(db: Session, keyword_id: int) -> bool:
    """Delete keyword"""
    db_keyword = get_keyword_by_id(db, keyword_id)
    if not db_keyword:
        return False
    
    db.delete(db_keyword)
    db.commit()
    return True


def search_keywords(db: Session, query: str, skip: int = 0, limit: int = 100) -> List[Keyword]:
    """Search keywords by name or description (case-insensitive)"""
    search_term = f"%{query}%"
    return db.query(Keyword).filter(
        (Keyword.name.ilike(search_term)) |
        (Keyword.description.ilike(search_term))
    ).offset(skip).limit(limit).all()


def get_trending_keywords(db: Session, limit: int = 10) -> List[Keyword]:
    """Get trending keywords"""
    return db.query(Keyword).filter(
        Keyword.is_trending == True
    ).order_by(desc(Keyword.popularity)).limit(limit).all()


def update_keyword_topics_count(db: Session, keyword_id: int) -> bool:
    """Update the topics count for a keyword"""
    keyword = get_keyword_by_id(db, keyword_id)
    if not keyword:
        return False
    
    # Count related search topics
    count = db.query(SearchTopicKeyword).filter(
        SearchTopicKeyword.keyword_id == keyword_id
    ).count()
    
    keyword.topics_count = count
    db.commit()
    db.refresh(keyword)
    return True


# SearchTopicKeyword CRUD operations
def get_search_topics_by_keyword(db: Session, keyword_id: int, skip: int = 0, limit: int = 100) -> List[SearchTopic]:
    """Get search topics associated with a keyword"""
    return db.query(SearchTopic).join(SearchTopicKeyword).filter(
        SearchTopicKeyword.keyword_id == keyword_id
    ).offset(skip).limit(limit).all()


def get_keywords_by_search_topic(db: Session, search_topic_id: int) -> List[Keyword]:
    """Get keywords associated with a search topic"""
    return db.query(Keyword).join(SearchTopicKeyword).filter(
        SearchTopicKeyword.search_topic_id == search_topic_id
    ).all()


def create_search_topic_keyword_relation(db: Session, relation: SearchTopicKeywordCreate) -> SearchTopicKeyword:
    """Create a relationship between search topic and keyword"""
    db_relation = SearchTopicKeyword(**relation.dict())
    db.add(db_relation)
    db.commit()
    db.refresh(db_relation)
    
    # Update topics count for the keyword
    update_keyword_topics_count(db, relation.keyword_id)
    
    return db_relation


def delete_search_topic_keyword_relation(db: Session, search_topic_id: int, keyword_id: int) -> bool:
    """Delete relationship between search topic and keyword"""
    relation = db.query(SearchTopicKeyword).filter(
        SearchTopicKeyword.search_topic_id == search_topic_id,
        SearchTopicKeyword.keyword_id == keyword_id
    ).first()
    
    if not relation:
        return False
    
    db.delete(relation)
    db.commit()
    
    # Update topics count for the keyword
    update_keyword_topics_count(db, keyword_id)
    
    return True


def get_keyword_stats(db: Session) -> dict:
    """Get keyword statistics"""
    total_keywords = db.query(Keyword).count()
    trending_keywords = db.query(Keyword).filter(Keyword.is_trending == True).count()
    total_topics = db.query(SearchTopicKeyword).count()
    
    return {
        "total_keywords": total_keywords,
        "trending_keywords": trending_keywords,
        "total_relationships": total_topics,
        "avg_popularity": db.query(func.avg(Keyword.popularity)).scalar() or 0
    }
