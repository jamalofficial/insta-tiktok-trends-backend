from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from ..core.database import get_db
from ..core.roles import require_admin, require_editor, get_current_user
from ..crud.user import (
    get_users, get_user_by_id, create_user, update_user, delete_user,
    get_roles, create_role
)
from ..schemas.user import User, UserCreate, UserUpdate, Role, RoleCreate

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=List[User])
def get_all_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
) -> List[User]:
    """Get all users (admin only)"""
    users = get_users(db, skip=skip, limit=limit)
    return users


@router.get("/me", response_model=User)
def get_my_profile(
    current_user: User = Depends(get_current_user)
) -> User:
    """Get current user's profile"""
    return current_user


@router.get("/{user_id}", response_model=User)
def get_user(
    user_id: int,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
) -> User:
    """Get user by ID (admin only)"""
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@router.post("/", response_model=User)
def create_new_user(
    user_data: UserCreate,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
) -> User:
    """Create a new user (admin only)"""
    # Check if username already exists
    from ..crud.user import get_user_by_username, get_user_by_email
    if get_user_by_username(db, user_data.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )
    
    if get_user_by_email(db, user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
        )
    
    user = create_user(db, user_data)
    return user


@router.put("/{user_id}", response_model=User)
def update_user_profile(
    user_id: int,
    user_update: UserUpdate,
    current_user: User = Depends(require_editor),
    db: Session = Depends(get_db)
) -> User:
    """Update user profile (editor or admin)"""
    # Users can only update their own profile unless they're admin
    if current_user.role.name != "admin" and current_user.id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Can only update your own profile"
        )
    
    user = update_user(db, user_id, user_update)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@router.delete("/{user_id}")
def delete_user_account(
    user_id: int,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
) -> dict:
    """Delete user account (admin only)"""
    # Prevent admin from deleting themselves
    if current_user.id == user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete your own account"
        )
    
    success = delete_user(db, user_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return {"message": "User deleted successfully"}


# Role management endpoints
@router.get("/roles/", response_model=List[Role])
def get_all_roles(
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
) -> List[Role]:
    """Get all roles (admin only)"""
    roles = get_roles(db)
    return roles


@router.post("/roles/", response_model=Role)
def create_new_role(
    role_data: RoleCreate,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
) -> Role:
    """Create a new role (admin only)"""
    # Check if role already exists
    from ..crud.user import get_role_by_name
    if get_role_by_name(db, role_data.name):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Role already exists"
        )
    
    role = create_role(db, role_data.name)
    return role
