from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class KeywordBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, description="Keyword name")
    description: Optional[str] = Field(None, description="Keyword description")
    popularity: Optional[float] = Field(0.0, ge=0, description="Keyword popularity score")
    is_trending: Optional[bool] = Field(False, description="Whether keyword is trending")
    topics_count: Optional[int] = Field(0, ge=0, description="Number of related search topics")


class KeywordCreate(KeywordBase):
    pass


class KeywordUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    popularity: Optional[float] = Field(None, ge=0)
    is_trending: Optional[bool] = None
    topics_count: Optional[int] = Field(None, ge=0)


class Keyword(KeywordBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class SearchTopicKeywordBase(BaseModel):
    search_topic_id: int
    keyword_id: int


class SearchTopicKeywordCreate(SearchTopicKeywordBase):
    pass


class SearchTopicKeyword(SearchTopicKeywordBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class KeywordWithTopics(Keyword):
    search_topics: List[dict] = Field(default_factory=list)


class SearchTopicWithKeywords(BaseModel):
    id: int
    title: str
    popularity: Optional[float] = None
    ai_tips: Optional[str] = None
    quick_actions: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    keywords: List[Keyword] = Field(default_factory=list)

    class Config:
        from_attributes = True
