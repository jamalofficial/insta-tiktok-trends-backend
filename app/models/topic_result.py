from sqlalchemy import Column, Integer, String, Float, DateTime, Date, ForeignKey, Text
from sqlalchemy.dialects.mysql import JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.db_setup import Base


class TopicResult(Base):
    """
    Stores search result entries for a topic.
    Each result is associated with an ExploreTopic via foreign key.
    """
    __tablename__ = "topic_results"

    id = Column(Integer, primary_key=True, index=True)
    explore_id = Column(Integer, ForeignKey("explore_topics.id"), nullable=False, index=True)
    relevant_keyword = Column(String(255), nullable=False, index=True)
    search_popularity = Column(Float, nullable=True)
    search_increase = Column(Float, nullable=True)
    location_data = Column(JSON, nullable=True)  # JSON field for location information
    demographic_data = Column(JSON, nullable=True)  # JSON field for demographic information
    time_period_7_days = Column(Date, nullable=True)
    time_period_today = Column(Date, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationship back to ExploreTopic
    explore_topic = relationship("ExploreTopic", back_populates="topic_results")

    def __repr__(self):
        return f"<TopicResult(id={self.id}, explore_id={self.explore_id}, keyword='{self.relevant_keyword}')>"
