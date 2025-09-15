from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ExploreTopicBase(BaseModel):
    title: str
    popularity: float = 0.0
    ai_tip: Optional[str] = None


class ExploreTopicCreate(ExploreTopicBase):
    pass


class ExploreTopicUpdate(BaseModel):
    title: Optional[str] = None
    popularity: Optional[float] = None
    ai_tip: Optional[str] = None


class ExploreTopic(ExploreTopicBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True
