from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class ScriptSceneBase(BaseModel):
    scene_number: int
    visual_description: str
    voice_over: Optional[str] = None


class ScriptSceneCreate(ScriptSceneBase):
    pass


class ScriptScene(ScriptSceneBase):
    id: int
    detail_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class RelatedVideoBase(BaseModel):
    title: str
    creator: str
    views: int = 0
    hashtags: Optional[str] = None
    video_url: Optional[str] = None


class RelatedVideoCreate(RelatedVideoBase):
    pass


class RelatedVideo(RelatedVideoBase):
    id: int
    detail_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class SearchDetailsBase(BaseModel):
    popularity_value: float = 0.0
    time_range: str = "last 7 days"
    region: str = "Global"
    suggested_title: Optional[str] = None
    suggested_hashtags: Optional[str] = None
    suggested_script: Optional[str] = None


class SearchDetailsCreate(SearchDetailsBase):
    pass


class SearchDetailsUpdate(BaseModel):
    popularity_value: Optional[float] = None
    time_range: Optional[str] = None
    region: Optional[str] = None
    suggested_title: Optional[str] = None
    suggested_hashtags: Optional[str] = None
    suggested_script: Optional[str] = None


class SearchDetails(SearchDetailsBase):
    id: int
    search_topic_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    script_scenes: List[ScriptScene] = []
    related_videos: List[RelatedVideo] = []
    
    class Config:
        from_attributes = True


class SearchDetailsWithTopic(SearchDetails):
    search_topic: "SearchTopic"


class SearchTopicBase(BaseModel):
    title: str
    popularity: float = 0.0
    ai_tips: Optional[str] = None
    quick_actions: Optional[str] = None


class SearchTopicCreate(SearchTopicBase):
    pass


class SearchTopicUpdate(BaseModel):
    title: Optional[str] = None
    popularity: Optional[float] = None
    ai_tips: Optional[str] = None
    quick_actions: Optional[str] = None


class SearchTopic(SearchTopicBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class SearchTopicWithDetails(SearchTopic):
    search_details: Optional[SearchDetails] = None


# Update forward references
SearchDetailsWithTopic.model_rebuild()
