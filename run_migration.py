#!/usr/bin/env python3
"""
Script to run initial database migration
"""
import sys
import os

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import create_tables, engine
from app.models.user import User, Role
from app.models.search import SearchTopic, SearchDetails, ScriptScenes, RelatedVideos
from app.models.explore import ExploreTopics

def main():
    """Create all database tables"""
    print("Creating database tables...")
    try:
        create_tables()
        print("✅ Database tables created successfully!")
        print(f"Database URL: {engine.url}")
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
