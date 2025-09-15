from sqlalchemy.orm import Session
from sqlalchemy import desc, asc
from typing import Optional, List
from ..models.search import SearchTopic, SearchDetails, ScriptScenes, RelatedVideos
from ..schemas.search import SearchTopicCreate, SearchTopicUpdate, SearchDetailsCreate, SearchDetailsUpdate, ScriptSceneCreate, RelatedVideoCreate


# SearchTopic CRUD operations
def get_search_topic_by_id(db: Session, topic_id: int) -> Optional[SearchTopic]:
    """Get search topic by ID"""
    return db.query(SearchTopic).filter(SearchTopic.id == topic_id).first()


def get_search_topics(db: Session, skip: int = 0, limit: int = 100, sort_by: str = "popularity") -> List[SearchTopic]:
    """Get all search topics with pagination and sorting"""
    query = db.query(SearchTopic)
    
    if sort_by == "popularity":
        query = query.order_by(desc(SearchTopic.popularity))
    elif sort_by == "title":
        query = query.order_by(asc(SearchTopic.title))
    elif sort_by == "created_at":
        query = query.order_by(desc(SearchTopic.created_at))
    
    return query.offset(skip).limit(limit).all()


def create_search_topic(db: Session, topic: SearchTopicCreate) -> SearchTopic:
    """Create a new search topic"""
    db_topic = SearchTopic(**topic.dict())
    db.add(db_topic)
    db.commit()
    db.refresh(db_topic)
    return db_topic


def update_search_topic(db: Session, topic_id: int, topic_update: SearchTopicUpdate) -> Optional[SearchTopic]:
    """Update search topic"""
    db_topic = get_search_topic_by_id(db, topic_id)
    if not db_topic:
        return None
    
    update_data = topic_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_topic, field, value)
    
    db.commit()
    db.refresh(db_topic)
    return db_topic


def delete_search_topic(db: Session, topic_id: int) -> bool:
    """Delete search topic"""
    db_topic = get_search_topic_by_id(db, topic_id)
    if not db_topic:
        return False
    
    db.delete(db_topic)
    db.commit()
    return True


def search_topics_by_title(db: Session, title: str, skip: int = 0, limit: int = 100) -> List[SearchTopic]:
    """Search topics by title (case-insensitive)"""
    return db.query(SearchTopic).filter(
        SearchTopic.title.ilike(f"%{title}%")
    ).offset(skip).limit(limit).all()


def search_topics_comprehensive(db: Session, query: str, skip: int = 0, limit: int = 100) -> List[SearchTopic]:
    """Search topics across title, AI tips, and quick actions (case-insensitive)"""
    search_term = f"%{query}%"
    return db.query(SearchTopic).filter(
        (SearchTopic.title.ilike(search_term)) |
        (SearchTopic.ai_tips.ilike(search_term)) |
        (SearchTopic.quick_actions.ilike(search_term))
    ).offset(skip).limit(limit).all()


# SearchDetails CRUD operations
def get_search_details_by_id(db: Session, details_id: int) -> Optional[SearchDetails]:
    """Get search details by ID"""
    return db.query(SearchDetails).filter(SearchDetails.id == details_id).first()


def get_search_details_by_topic_id(db: Session, topic_id: int) -> Optional[SearchDetails]:
    """Get search details by topic ID"""
    return db.query(SearchDetails).filter(SearchDetails.search_topic_id == topic_id).first()


def create_search_details(db: Session, details: SearchDetailsCreate, topic_id: int) -> SearchDetails:
    """Create search details for a topic"""
    db_details = SearchDetails(**details.dict(), search_topic_id=topic_id)
    db.add(db_details)
    db.commit()
    db.refresh(db_details)
    return db_details


def update_search_details(db: Session, details_id: int, details_update: SearchDetailsUpdate) -> Optional[SearchDetails]:
    """Update search details"""
    db_details = get_search_details_by_id(db, details_id)
    if not db_details:
        return None
    
    update_data = details_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_details, field, value)
    
    db.commit()
    db.refresh(db_details)
    return db_details


def delete_search_details(db: Session, details_id: int) -> bool:
    """Delete search details"""
    db_details = get_search_details_by_id(db, details_id)
    if not db_details:
        return False
    
    db.delete(db_details)
    db.commit()
    return True


# ScriptScenes CRUD operations
def get_script_scenes_by_detail_id(db: Session, detail_id: int) -> List[ScriptScenes]:
    """Get all script scenes for a detail"""
    return db.query(ScriptScenes).filter(
        ScriptScenes.detail_id == detail_id
    ).order_by(ScriptScenes.scene_number).all()


def create_script_scene(db: Session, scene: ScriptSceneCreate, detail_id: int) -> ScriptScenes:
    """Create a new script scene"""
    db_scene = ScriptScenes(**scene.dict(), detail_id=detail_id)
    db.add(db_scene)
    db.commit()
    db.refresh(db_scene)
    return db_scene


def update_script_scene(db: Session, scene_id: int, scene_update: dict) -> Optional[ScriptScenes]:
    """Update script scene"""
    db_scene = db.query(ScriptScenes).filter(ScriptScenes.id == scene_id).first()
    if not db_scene:
        return None
    
    for field, value in scene_update.items():
        setattr(db_scene, field, value)
    
    db.commit()
    db.refresh(db_scene)
    return db_scene


def delete_script_scene(db: Session, scene_id: int) -> bool:
    """Delete script scene"""
    db_scene = db.query(ScriptScenes).filter(ScriptScenes.id == scene_id).first()
    if not db_scene:
        return False
    
    db.delete(db_scene)
    db.commit()
    return True


# RelatedVideos CRUD operations
def get_related_videos_by_detail_id(db: Session, detail_id: int) -> List[RelatedVideos]:
    """Get all related videos for a detail"""
    return db.query(RelatedVideos).filter(
        RelatedVideos.detail_id == detail_id
    ).order_by(desc(RelatedVideos.views)).all()


def create_related_video(db: Session, video: RelatedVideoCreate, detail_id: int) -> RelatedVideos:
    """Create a new related video"""
    db_video = RelatedVideos(**video.dict(), detail_id=detail_id)
    db.add(db_video)
    db.commit()
    db.refresh(db_video)
    return db_video


def update_related_video(db: Session, video_id: int, video_update: dict) -> Optional[RelatedVideos]:
    """Update related video"""
    db_video = db.query(RelatedVideos).filter(RelatedVideos.id == video_id).first()
    if not db_video:
        return None
    
    for field, value in video_update.items():
        setattr(db_video, field, value)
    
    db.commit()
    db.refresh(db_video)
    return db_video


def delete_related_video(db: Session, video_id: int) -> bool:
    """Delete related video"""
    db_video = db.query(RelatedVideos).filter(RelatedVideos.id == video_id).first()
    if not db_video:
        return False
    
    db.delete(db_video)
    db.commit()
    return True


def get_search_topics_count(db: Session) -> int:
    """Get total count of search topics"""
    return db.query(SearchTopic).count()


def get_related_videos_count(db: Session) -> int:
    """Get total count of related videos"""
    return db.query(RelatedVideos).count()