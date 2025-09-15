from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from ..core.database import get_db
from ..core.roles import require_viewer, require_editor, require_admin, get_current_user
from ..crud.search import (
    get_search_topics, get_search_topic_by_id, create_search_topic,
    update_search_topic, delete_search_topic, search_topics_by_title,
    search_topics_comprehensive, get_search_details_by_topic_id, create_search_details, update_search_details,
    get_script_scenes_by_detail_id, create_script_scene, update_script_scene,
    delete_script_scene, get_related_videos_by_detail_id, create_related_video,
    update_related_video, delete_related_video
)
from ..schemas.search import (
    SearchTopic, SearchTopicCreate, SearchTopicUpdate,
    SearchDetails, SearchDetailsCreate, SearchDetailsUpdate,
    ScriptScene, ScriptSceneCreate, RelatedVideo, RelatedVideoCreate
)

router = APIRouter(prefix="/search", tags=["search"])


@router.get("/topics", response_model=List[SearchTopic])
def get_all_search_topics(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    sort_by: str = Query("popularity", regex="^(popularity|title|created_at)$"),
    current_user = Depends(require_viewer),
    db: Session = Depends(get_db)
) -> List[SearchTopic]:
    """Get all search topics with pagination and sorting"""
    topics = get_search_topics(db, skip=skip, limit=limit, sort_by=sort_by)
    return topics


@router.get("/topics/search", response_model=List[SearchTopic])
def search_topics(
    q: str = Query(..., min_length=1),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user = Depends(require_viewer),
    db: Session = Depends(get_db)
) -> List[SearchTopic]:
    """Search topics across title, AI tips, and quick actions"""
    topics = search_topics_comprehensive(db, q, skip=skip, limit=limit)
    return topics


@router.get("/topics/{topic_id}", response_model=SearchTopic)
def get_search_topic(
    topic_id: int,
    current_user = Depends(require_viewer),
    db: Session = Depends(get_db)
) -> SearchTopic:
    """Get search topic by ID"""
    topic = get_search_topic_by_id(db, topic_id)
    if not topic:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Search topic not found"
        )
    return topic


@router.post("/topics", response_model=SearchTopic)
def create_new_search_topic(
    topic_data: SearchTopicCreate,
    current_user = Depends(require_editor),
    db: Session = Depends(get_db)
) -> SearchTopic:
    """Create a new search topic (editor or admin)"""
    topic = create_search_topic(db, topic_data)
    return topic


@router.put("/topics/{topic_id}", response_model=SearchTopic)
def update_search_topic_info(
    topic_id: int,
    topic_update: SearchTopicUpdate,
    current_user = Depends(require_editor),
    db: Session = Depends(get_db)
) -> SearchTopic:
    """Update search topic (editor or admin)"""
    topic = update_search_topic(db, topic_id, topic_update)
    if not topic:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Search topic not found"
        )
    return topic


@router.delete("/topics/{topic_id}")
def delete_search_topic_entry(
    topic_id: int,
    current_user = Depends(require_admin),
    db: Session = Depends(get_db)
) -> dict:
    """Delete search topic (admin only)"""
    success = delete_search_topic(db, topic_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Search topic not found"
        )
    return {"message": "Search topic deleted successfully"}


@router.get("/details/{topic_id}", response_model=SearchDetails)
def get_search_details(
    topic_id: int,
    current_user = Depends(require_viewer),
    db: Session = Depends(get_db)
) -> SearchDetails:
    """Get search details for a topic"""
    details = get_search_details_by_topic_id(db, topic_id)
    if not details:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Search details not found for this topic"
        )
    return details


@router.post("/details/{topic_id}", response_model=SearchDetails)
def create_search_details_for_topic(
    topic_id: int,
    details_data: SearchDetailsCreate,
    current_user = Depends(require_editor),
    db: Session = Depends(get_db)
) -> SearchDetails:
    """Create search details for a topic (editor or admin)"""
    # Check if topic exists
    topic = get_search_topic_by_id(db, topic_id)
    if not topic:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Search topic not found"
        )
    
    # Check if details already exist
    existing_details = get_search_details_by_topic_id(db, topic_id)
    if existing_details:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Search details already exist for this topic"
        )
    
    details = create_search_details(db, details_data, topic_id)
    return details


@router.put("/details/{details_id}", response_model=SearchDetails)
def update_search_details_info(
    details_id: int,
    details_update: SearchDetailsUpdate,
    current_user = Depends(require_editor),
    db: Session = Depends(get_db)
) -> SearchDetails:
    """Update search details (editor or admin)"""
    from ..crud.search import get_search_details_by_id
    details = update_search_details(db, details_id, details_update)
    if not details:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Search details not found"
        )
    return details


# Script Scenes endpoints
@router.get("/details/{topic_id}/scenes", response_model=List[ScriptScene])
def get_script_scenes(
    topic_id: int,
    current_user = Depends(require_viewer),
    db: Session = Depends(get_db)
) -> List[ScriptScene]:
    """Get all script scenes for search details"""
    # Find details by topic_id
    details = get_search_details_by_topic_id(db, topic_id)
    if not details:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Search details not found for this topic"
        )
    scenes = get_script_scenes_by_detail_id(db, details.id)
    return scenes


@router.post("/details/{topic_id}/scenes", response_model=ScriptScene)
def create_script_scene_for_details(
    topic_id: int,
    scene_data: ScriptSceneCreate,
    current_user = Depends(require_editor),
    db: Session = Depends(get_db)
) -> ScriptScene:
    """Create a new script scene (editor or admin)"""
    # Find details by topic_id
    details = get_search_details_by_topic_id(db, topic_id)
    if not details:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Search details not found for this topic"
        )
    scene = create_script_scene(db, scene_data, details.id)
    return scene


@router.put("/scenes/{scene_id}", response_model=ScriptScene)
def update_script_scene_info(
    scene_id: int,
    scene_update: dict,
    current_user = Depends(require_editor),
    db: Session = Depends(get_db)
) -> ScriptScene:
    """Update script scene (editor or admin)"""
    scene = update_script_scene(db, scene_id, scene_update)
    if not scene:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Script scene not found"
        )
    return scene


@router.delete("/scenes/{scene_id}")
def delete_script_scene_entry(
    scene_id: int,
    current_user = Depends(require_admin),
    db: Session = Depends(get_db)
) -> dict:
    """Delete script scene (admin only)"""
    success = delete_script_scene(db, scene_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Script scene not found"
        )
    return {"message": "Script scene deleted successfully"}


# Related Videos endpoints
@router.get("/details/{topic_id}/videos", response_model=List[RelatedVideo])
def get_related_videos(
    topic_id: int,
    current_user = Depends(require_viewer),
    db: Session = Depends(get_db)
) -> List[RelatedVideo]:
    """Get all related videos for search details"""
    # Find details by topic_id
    details = get_search_details_by_topic_id(db, topic_id)
    if not details:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Search details not found for this topic"
        )
    videos = get_related_videos_by_detail_id(db, details.id)
    return videos


@router.post("/details/{topic_id}/videos", response_model=RelatedVideo)
def create_related_video_for_details(
    topic_id: int,
    video_data: RelatedVideoCreate,
    current_user = Depends(require_editor),
    db: Session = Depends(get_db)
) -> RelatedVideo:
    """Create a new related video (editor or admin)"""
    # Find details by topic_id
    details = get_search_details_by_topic_id(db, topic_id)
    if not details:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Search details not found for this topic"
        )
    video = create_related_video(db, video_data, details.id)
    return video


@router.put("/videos/{video_id}", response_model=RelatedVideo)
def update_related_video_info(
    video_id: int,
    video_update: dict,
    current_user = Depends(require_editor),
    db: Session = Depends(get_db)
) -> RelatedVideo:
    """Update related video (editor or admin)"""
    video = update_related_video(db, video_id, video_update)
    if not video:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Related video not found"
        )
    return video


@router.delete("/videos/{video_id}")
def delete_related_video_entry(
    video_id: int,
    current_user = Depends(require_admin),
    db: Session = Depends(get_db)
) -> dict:
    """Delete related video (admin only)"""
    success = delete_related_video(db, video_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Related video not found"
        )
    return {"message": "Related video deleted successfully"}
