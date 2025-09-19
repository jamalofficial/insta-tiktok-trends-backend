#!/usr/bin/env python3
"""
Test script to verify database setup and models work correctly.
Run this to test the database connection and table creation.
"""

import sys
import os

# Add the app directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database.db_setup import create_tables, get_db, engine
from app.models.explore_topic import ExploreTopic
from app.models.topic_result import TopicResult
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import datetime, date


def test_database_setup():
    """Test database connection and table creation"""
    try:
        print("Creating database tables...")
        create_tables()
        print("✅ Database tables created successfully!")
        
        # Test database connection
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("✅ Database connection successful!")
        
        return True
    except Exception as e:
        print(f"❌ Database setup failed: {e}")
        return False


def test_model_creation():
    """Test creating sample records"""
    try:
        db = next(get_db())
        
        # Create a sample ExploreTopic
        topic = ExploreTopic(
            topic="Dance Trends 2024",
            origin_user_id=1,
            last_scrape=datetime.utcnow()
        )
        db.add(topic)
        db.commit()
        db.refresh(topic)
        print(f"✅ Created ExploreTopic: {topic}")
        
        # Create sample TopicResults
        result1 = TopicResult(
            explore_id=topic.id,
            relevant_keyword="viral dance",
            search_popularity=85.5,
            search_increase=12.3,
            location_data={"country": "US", "region": "California"},
            demographic_data={"age_group": "18-24", "gender": "mixed"},
            time_period_7_days=date.today(),
            time_period_today=date.today()
        )
        
        result2 = TopicResult(
            explore_id=topic.id,
            relevant_keyword="tiktok dance",
            search_popularity=92.1,
            search_increase=8.7,
            location_data={"country": "US", "region": "Texas"},
            demographic_data={"age_group": "13-17", "gender": "female"},
            time_period_7_days=date.today(),
            time_period_today=date.today()
        )
        
        db.add(result1)
        db.add(result2)
        db.commit()
        print(f"✅ Created TopicResults: {result1}, {result2}")
        
        # Test relationship query
        topic_with_results = db.query(ExploreTopic).filter(ExploreTopic.id == topic.id).first()
        print(f"✅ Topic has {len(topic_with_results.topic_results)} results")
        
        # Test keyword query
        keywords = db.query(TopicResult.relevant_keyword).filter(
            TopicResult.explore_id == topic.id
        ).all()
        print(f"✅ Keywords found: {[k[0] for k in keywords]}")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ Model creation failed: {e}")
        return False


if __name__ == "__main__":
    print("🧪 Testing TikTok Trends Backend Database Setup")
    print("=" * 50)
    
    # Test database setup
    if not test_database_setup():
        sys.exit(1)
    
    # Test model creation
    if not test_model_creation():
        sys.exit(1)
    
    print("\n🎉 All tests passed! Database setup is working correctly.")
    print("\nYou can now run the main application with: python -m app.main")
