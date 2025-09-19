from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.db_setup import Base


class ExploreTopic(Base):
    """
    Represents a high-level topic created by a user.
    Each topic can have multiple TopicResults associated with it.
    """
    __tablename__ = "explore_topics"

    id = Column(Integer, primary_key=True, index=True)
    topic = Column(String(255), nullable=False, index=True)
    origin_user_id = Column(Integer, nullable=False, index=True)
    last_scrape = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationship to TopicResult
    topic_results = relationship("TopicResult", back_populates="explore_topic", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<ExploreTopic(id={self.id}, topic='{self.topic}', origin_user_id={self.origin_user_id})>"
