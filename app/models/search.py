from sqlalchemy import Column, Integer, String, Text, Float, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base


class SearchTopic(Base):
    __tablename__ = "search_topics"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    popularity = Column(Float, default=0.0)
    ai_tips = Column(Text)
    quick_actions = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    search_details = relationship("SearchDetails", back_populates="search_topic", uselist=False)
    topic_keywords = relationship("SearchTopicKeyword", back_populates="search_topic", cascade="all, delete-orphan")


class SearchDetails(Base):
    __tablename__ = "search_details"
    
    id = Column(Integer, primary_key=True, index=True)
    search_topic_id = Column(Integer, ForeignKey("search_topics.id"), nullable=False, unique=True)
    popularity_value = Column(Float, default=0.0)
    time_range = Column(String(100), default="last 7 days")
    region = Column(String(100), default="Global")
    suggested_title = Column(String(500))
    suggested_hashtags = Column(Text)
    suggested_script = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    search_topic = relationship("SearchTopic", back_populates="search_details")
    script_scenes = relationship("ScriptScenes", back_populates="detail", cascade="all, delete-orphan")
    related_videos = relationship("RelatedVideos", back_populates="detail", cascade="all, delete-orphan")


class ScriptScenes(Base):
    __tablename__ = "script_scenes"
    
    id = Column(Integer, primary_key=True, index=True)
    detail_id = Column(Integer, ForeignKey("search_details.id"), nullable=False)
    scene_number = Column(Integer, nullable=False)
    visual_description = Column(Text, nullable=False)
    voice_over = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    detail = relationship("SearchDetails", back_populates="script_scenes")


class RelatedVideos(Base):
    __tablename__ = "related_videos"
    
    id = Column(Integer, primary_key=True, index=True)
    detail_id = Column(Integer, ForeignKey("search_details.id"), nullable=False)
    title = Column(String(500), nullable=False)
    creator = Column(String(255), nullable=False)
    views = Column(Integer, default=0)
    hashtags = Column(Text)  # JSON string or comma-separated
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    video_url = Column(String(1000))
    
    # Relationships
    detail = relationship("SearchDetails", back_populates="related_videos")
