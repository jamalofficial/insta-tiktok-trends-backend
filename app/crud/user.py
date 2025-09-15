from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional, List
from ..models.user import User, Role
from ..schemas.user import UserCreate, UserUpdate
from ..core.security import get_password_hash


def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    """Get user by ID"""
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_username(db: Session, username: str) -> Optional[User]:
    """Get user by username"""
    return db.query(User).filter(User.username == username).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Get user by email"""
    return db.query(User).filter(User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[User]:
    """Get all users with pagination"""
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate) -> User:
    """Create a new user"""
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        password_hash=hashed_password,
        role_id=user.role_id
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, user_update: UserUpdate) -> Optional[User]:
    """Update user"""
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return None
    
    update_data = user_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_user, field, value)
    
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int) -> bool:
    """Delete user"""
    db_user = get_user_by_id(db, user_id)
    if not db_user:
        return False
    
    db.delete(db_user)
    db.commit()
    return True


def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
    """Authenticate user with username/email and password"""
    user = db.query(User).filter(
        or_(User.username == username, User.email == username)
    ).first()
    
    if not user:
        return None
    
    from ..core.security import verify_password
    if not verify_password(password, user.password_hash):
        return None
    
    return user


# Role CRUD operations
def get_role_by_id(db: Session, role_id: int) -> Optional[Role]:
    """Get role by ID"""
    return db.query(Role).filter(Role.id == role_id).first()


def get_role_by_name(db: Session, name: str) -> Optional[Role]:
    """Get role by name"""
    return db.query(Role).filter(Role.name == name).first()


def get_roles(db: Session, skip: int = 0, limit: int = 100) -> List[Role]:
    """Get all roles"""
    return db.query(Role).offset(skip).limit(limit).all()


def create_role(db: Session, name: str) -> Role:
    """Create a new role"""
    db_role = Role(name=name)
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role


def get_users_count(db: Session) -> int:
    """Get total count of users"""
    return db.query(User).count()