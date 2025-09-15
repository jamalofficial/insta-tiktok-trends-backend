#!/usr/bin/env python3
"""
Create super admin user script
Run this to create the super admin user for testing
"""

from app.core.database import SessionLocal
from app.crud.user import get_role_by_name, create_role, create_user, get_user_by_username
from app.schemas.user import UserCreate
from app.core.security import get_password_hash
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_super_admin():
    """Create super admin user and role"""
    db = SessionLocal()
    try:
        # Create super_admin role if it doesn't exist
        super_admin_role = get_role_by_name(db, "super_admin")
        if not super_admin_role:
            create_role(db, "super_admin")
            super_admin_role = get_role_by_name(db, "super_admin")
            logger.info("✅ Created super_admin role")
        else:
            logger.info("✅ super_admin role already exists")
        
        # Create super admin user if it doesn't exist
        existing_user = get_user_by_username(db, "superadmin")
        if not existing_user:
            super_admin_data = UserCreate(
                username="superadmin",
                email="superadmin@tiktokdb.com",
                password="admin123",
                role_id=super_admin_role.id
            )
            create_user(db, super_admin_data)
            logger.info("✅ Created super admin user")
            logger.info("   Username: superadmin")
            logger.info("   Password: admin123")
            logger.info("   Email: superadmin@tiktokdb.com")
        else:
            logger.info("✅ Super admin user already exists")
        
        db.commit()
        logger.info("🎉 Super admin setup complete!")
        
    except Exception as e:
        logger.error(f"❌ Error creating super admin: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    create_super_admin()
