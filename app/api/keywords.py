from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from ..core.database import get_db
from ..core.roles import require_viewer, require_editor, require_admin, get_current_user
from ..crud.keyword import (
    get_keywords, get_keyword_by_id, get_keyword_by_name, create_keyword,
    update_keyword, delete_keyword, search_keywords, get_trending_keywords,
    get_search_topics_by_keyword, get_keywords_by_search_topic,
    create_search_topic_keyword_relation, delete_search_topic_keyword_relation,
    update_keyword_topics_count, get_keyword_stats
)
from ..schemas.keyword import (
    Keyword, KeywordCreate, KeywordUpdate, SearchTopicKeywordCreate,
    KeywordWithTopics
)

router = APIRouter(prefix="/keywords", tags=["keywords"])


@router.get("/", response_model=List[Keyword])
def get_all_keywords(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    sort_by: str = Query("popularity", regex="^(popularity|name|created_at|topics_count)$"),
    current_user = Depends(require_viewer),
    db: Session = Depends(get_db)
) -> List[Keyword]:
    """Get all keywords with pagination and sorting"""
    keywords = get_keywords(db, skip=skip, limit=limit, sort_by=sort_by)
    return keywords


@router.get("/search", response_model=List[Keyword])
def search_keywords_endpoint(
    q: str = Query(..., min_length=1),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user = Depends(require_viewer),
    db: Session = Depends(get_db)
) -> List[Keyword]:
    """Search keywords by name or description"""
    keywords = search_keywords(db, q, skip=skip, limit=limit)
    return keywords


@router.get("/trending", response_model=List[Keyword])
def get_trending_keywords_endpoint(
    limit: int = Query(10, ge=1, le=50),
    current_user = Depends(require_viewer),
    db: Session = Depends(get_db)
) -> List[Keyword]:
    """Get trending keywords"""
    keywords = get_trending_keywords(db, limit=limit)
    return keywords


@router.get("/stats")
def get_keyword_statistics(
    current_user = Depends(require_viewer),
    db: Session = Depends(get_db)
) -> dict:
    """Get keyword statistics"""
    stats = get_keyword_stats(db)
    return stats


@router.get("/{keyword_id}", response_model=KeywordWithTopics)
def get_keyword(
    keyword_id: int,
    current_user = Depends(require_viewer),
    db: Session = Depends(get_db)
) -> KeywordWithTopics:
    """Get keyword by ID with related search topics"""
    keyword = get_keyword_by_id(db, keyword_id)
    if not keyword:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Keyword not found"
        )
    
    # Get related search topics
    search_topics = get_search_topics_by_keyword(db, keyword_id)
    
    keyword_with_topics = KeywordWithTopics(
        **keyword.__dict__,
        search_topics=[{"id": topic.id, "title": topic.title, "popularity": topic.popularity} for topic in search_topics]
    )
    
    return keyword_with_topics


@router.post("/", response_model=Keyword)
def create_new_keyword(
    keyword_data: KeywordCreate,
    current_user = Depends(require_editor),
    db: Session = Depends(get_db)
) -> Keyword:
    """Create a new keyword (editor or admin)"""
    # Check if keyword already exists
    existing_keyword = get_keyword_by_name(db, keyword_data.name)
    if existing_keyword:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Keyword with this name already exists"
        )
    
    keyword = create_keyword(db, keyword_data)
    return keyword


@router.put("/{keyword_id}", response_model=Keyword)
def update_keyword_info(
    keyword_id: int,
    keyword_update: KeywordUpdate,
    current_user = Depends(require_editor),
    db: Session = Depends(get_db)
) -> Keyword:
    """Update keyword (editor or admin)"""
    # Check if name is being updated and if it already exists
    if keyword_update.name:
        existing_keyword = get_keyword_by_name(db, keyword_update.name)
        if existing_keyword and existing_keyword.id != keyword_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Keyword with this name already exists"
            )
    
    keyword = update_keyword(db, keyword_id, keyword_update)
    if not keyword:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Keyword not found"
        )
    return keyword


@router.delete("/{keyword_id}")
def delete_keyword_entry(
    keyword_id: int,
    current_user = Depends(require_admin),
    db: Session = Depends(get_db)
) -> dict:
    """Delete keyword (admin only)"""
    success = delete_keyword(db, keyword_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Keyword not found"
        )
    return {"message": "Keyword deleted successfully"}


@router.get("/{keyword_id}/search-topics")
def get_keyword_search_topics(
    keyword_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user = Depends(require_viewer),
    db: Session = Depends(get_db)
) -> List[dict]:
    """Get search topics associated with a keyword"""
    # Check if keyword exists
    keyword = get_keyword_by_id(db, keyword_id)
    if not keyword:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Keyword not found"
        )
    
    search_topics = get_search_topics_by_keyword(db, keyword_id, skip=skip, limit=limit)
    return [{"id": topic.id, "title": topic.title, "popularity": topic.popularity, "created_at": topic.created_at} for topic in search_topics]


@router.post("/{keyword_id}/search-topics/{search_topic_id}")
def associate_keyword_with_search_topic(
    keyword_id: int,
    search_topic_id: int,
    current_user = Depends(require_editor),
    db: Session = Depends(get_db)
) -> dict:
    """Associate a keyword with a search topic (editor or admin)"""
    # Check if keyword exists
    keyword = get_keyword_by_id(db, keyword_id)
    if not keyword:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Keyword not found"
        )
    
    # Check if search topic exists
    from ..crud.search import get_search_topic_by_id
    search_topic = get_search_topic_by_id(db, search_topic_id)
    if not search_topic:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Search topic not found"
        )
    
    # Check if relationship already exists
    existing_relations = db.query(SearchTopicKeyword).filter(
        SearchTopicKeyword.keyword_id == keyword_id,
        SearchTopicKeyword.search_topic_id == search_topic_id
    ).first()
    
    if existing_relations:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Relationship already exists"
        )
    
    relation_data = SearchTopicKeywordCreate(
        keyword_id=keyword_id,
        search_topic_id=search_topic_id
    )
    
    create_search_topic_keyword_relation(db, relation_data)
    return {"message": "Keyword associated with search topic successfully"}


@router.delete("/{keyword_id}/search-topics/{search_topic_id}")
def remove_keyword_search_topic_association(
    keyword_id: int,
    search_topic_id: int,
    current_user = Depends(require_editor),
    db: Session = Depends(get_db)
) -> dict:
    """Remove association between keyword and search topic (editor or admin)"""
    success = delete_search_topic_keyword_relation(db, search_topic_id, keyword_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Relationship not found"
        )
    return {"message": "Association removed successfully"}
