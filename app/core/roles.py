from enum import Enum
from functools import wraps
from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from typing import List
from ..models.user import User
from .security import verify_token, get_token_from_bearer
from .database import get_db


class UserRole(str, Enum):
    SUPER_ADMIN = "super_admin"
    ADMIN = "admin"
    EDITOR = "editor"
    VIEWER = "viewer"


# Role hierarchy (higher number = more permissions)
ROLE_HIERARCHY = {
    UserRole.VIEWER: 1,
    UserRole.EDITOR: 2,
    UserRole.ADMIN: 3,
    UserRole.SUPER_ADMIN: 4,
}


def get_current_user_id(token_payload: dict = Depends(verify_token)) -> int:
    """Extract user ID from JWT token"""
    return int(token_payload.get("sub"))


def get_current_user(db: Session = Depends(get_db), user_id: int = Depends(get_current_user_id)) -> User:
    """Get current user from database"""
    from ..crud.user import get_user_by_id
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    return user


def is_super_admin(user: User) -> bool:
    """Check if user is super admin"""
    return user.role.name == UserRole.SUPER_ADMIN


def has_permission(user: User, required_role: UserRole) -> bool:
    """Check if user has required permission level"""
    if is_super_admin(user):
        return True  # Super admin has all permissions
    
    user_role = UserRole(user.role.name)
    return ROLE_HIERARCHY[user_role] >= ROLE_HIERARCHY[required_role]


def require_roles(allowed_roles: List[UserRole]):
    """Decorator to require specific roles"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Extract current_user from kwargs
            current_user = kwargs.get('current_user')
            if not current_user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authentication required"
                )
            
            # Super admin bypasses all role checks
            if is_super_admin(current_user):
                return func(*args, **kwargs)
            
            user_role = UserRole(current_user.role.name)
            if user_role not in allowed_roles:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Insufficient permissions"
                )
            
            return func(*args, **kwargs)
        return wrapper
    return decorator


def require_minimum_role(minimum_role: UserRole):
    """Decorator to require minimum role level"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_user = kwargs.get('current_user')
            if not current_user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authentication required"
                )
            
            # Super admin bypasses all role checks
            if is_super_admin(current_user):
                return func(*args, **kwargs)
            
            user_role = UserRole(current_user.role.name)
            if ROLE_HIERARCHY[user_role] < ROLE_HIERARCHY[minimum_role]:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Insufficient permissions"
                )
            
            return func(*args, **kwargs)
        return wrapper
    return decorator


# Common role dependencies
def require_admin(current_user: User = Depends(get_current_user)) -> User:
    """Require admin role or higher"""
    if not has_permission(current_user, UserRole.ADMIN):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user


def require_editor(current_user: User = Depends(get_current_user)) -> User:
    """Require editor or higher role"""
    if not has_permission(current_user, UserRole.EDITOR):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Editor access required"
        )
    return current_user


def require_viewer(current_user: User = Depends(get_current_user)) -> User:
    """Require any authenticated user"""
    return current_user


def require_super_admin(current_user: User = Depends(get_current_user)) -> User:
    """Require super admin role"""
    if not is_super_admin(current_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Super admin access required"
        )
    return current_user
