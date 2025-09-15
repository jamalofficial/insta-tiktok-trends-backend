from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base


class Keyword(Base):
    __tablename__ = "keywords"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True, index=True)
    description = Column(Text)
    popularity = Column(Float, default=0.0)
    is_trending = Column(Boolean, default=False)
    topics_count = Column(Integer, default=0)  # Count of related search topics
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    search_topics = relationship("SearchTopicKeyword", back_populates="keyword", cascade="all, delete-orphan")


class SearchTopicKeyword(Base):
    __tablename__ = "search_topic_keywords"
    
    id = Column(Integer, primary_key=True, index=True)
    search_topic_id = Column(Integer, ForeignKey("search_topics.id"), nullable=False)
    keyword_id = Column(Integer, ForeignKey("keywords.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    search_topic = relationship("SearchTopic", back_populates="topic_keywords")
    keyword = relationship("Keyword", back_populates="search_topics")
