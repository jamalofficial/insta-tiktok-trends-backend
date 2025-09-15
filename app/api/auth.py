from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import Dict, Any

from ..core.database import get_db
from ..core.security import create_access_token, verify_password
from ..core.config import settings
from ..core.roles import get_current_user
from ..crud.user import authenticate_user, get_user_by_username, create_user, get_role_by_name
from ..schemas.user import User, UserCreate, Token, UserLogin

router = APIRouter(prefix="/auth", tags=["authentication"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Authenticate user and return access token"""
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", response_model=User)
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
) -> User:
    """Register a new user"""
    # Check if username already exists
    if get_user_by_username(db, user_data.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Check if email already exists
    from ..crud.user import get_user_by_email
    if get_user_by_email(db, user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Check if role exists
    role = get_role_by_name(db, "viewer")  # Default role
    if not role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Default role not found"
        )
    
    user_data.role_id = role.id
    user = create_user(db, user_data)
    return user


@router.get("/me", response_model=User)
def get_current_user_info(
    current_user: User = Depends(get_current_user)
) -> User:
    """Get current user information"""
    return current_user


@router.post("/refresh", response_model=Token)
def refresh_token(
    current_user: User = Depends(get_current_user)
) -> Dict[str, Any]:
    """Refresh access token"""
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(current_user.id)}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}
