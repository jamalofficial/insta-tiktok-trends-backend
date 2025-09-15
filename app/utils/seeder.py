from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.crud.user import get_role_by_name, create_role, create_user
from app.models.user import Role
from app.core.security import get_password_hash
import logging

logger = logging.getLogger(__name__)


def seed_initial_data():
    """Seed initial data for the application"""
    db = SessionLocal()
    try:
        # Create default roles if they don't exist
        roles_data = [
            {"name": "super_admin"},  # Super admin with all permissions
            {"name": "admin"},
            {"name": "editor"},
            {"name": "viewer"}
        ]
        
        for role_data in roles_data:
            existing_role = get_role_by_name(db, role_data["name"])
            if not existing_role:
                create_role(db, role_data["name"])
                logger.info(f"Created role: {role_data['name']}")
            else:
                logger.info(f"Role already exists: {role_data['name']}")
        
        # Create super admin user for testing
        super_admin_role = get_role_by_name(db, "super_admin")
        if super_admin_role:
            from app.schemas.user import UserCreate
            super_admin_data = UserCreate(
                username="superadmin",
                email="superadmin@tiktokdb.com",
                password="admin123",  # Simple password for testing
                role_id=super_admin_role.id
            )
            
            # Check if super admin user already exists
            from app.crud.user import get_user_by_username
            existing_user = get_user_by_username(db, super_admin_data.username)
            if not existing_user:
                create_user(db, super_admin_data)
                logger.info("Created super admin user: superadmin/admin123")
            else:
                logger.info("Super admin user already exists")
        
        db.commit()
        logger.info("Initial data seeding completed successfully")
        
    except Exception as e:
        logger.error(f"Error seeding initial data: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def clear_all_data():
    """Clear all seeded data from the database"""
    db = SessionLocal()
    try:
        # Import all models
        from app.models.user import User, Role
        from app.models.search import SearchTopic, SearchDetails, ScriptScenes, RelatedVideos
        from app.models.explore import ExploreTopics
        
        # Delete all data in reverse dependency order
        db.query(RelatedVideos).delete()
        db.query(ScriptScenes).delete()
        db.query(SearchDetails).delete()
        db.query(SearchTopic).delete()
        db.query(ExploreTopics).delete()
        db.query(User).delete()
        db.query(Role).delete()
        
        db.commit()
        logger.info("All data cleared successfully")
        
    except Exception as e:
        logger.error(f"Error clearing data: {e}")
        db.rollback()
        raise
    finally:
        db.close()