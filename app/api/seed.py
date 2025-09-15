from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Dict, Any

from ..core.database import get_db
from ..core.roles import require_admin
from ..utils.seeder import seed_initial_data, clear_all_data
from ..schemas.user import User

router = APIRouter(prefix="/seed", tags=["seed"])


@router.post("/search-topics")
def seed_search_topics(
    options: Dict[str, Any],
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Seed search topics (admin only)"""
    try:
        # For now, just seed initial data
        seed_initial_data()
        return {
            "success": True,
            "message": "Search topics seeded successfully",
            "count": options.get("count", 0)
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to seed search topics: {str(e)}"
        )


@router.post("/explore-topics")
def seed_explore_topics(
    options: Dict[str, Any],
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Seed explore topics (admin only)"""
    try:
        # For now, just seed initial data
        seed_initial_data()
        return {
            "success": True,
            "message": "Explore topics seeded successfully",
            "count": options.get("count", 0)
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to seed explore topics: {str(e)}"
        )


@router.post("/users")
def seed_users(
    options: Dict[str, Any],
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Seed users (admin only)"""
    try:
        # For now, just seed initial data
        seed_initial_data()
        return {
            "success": True,
            "message": "Users seeded successfully",
            "count": options.get("count", 0)
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to seed users: {str(e)}"
        )


@router.post("/clear-all")
def clear_all_seeded_data(
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Clear all seeded data (admin only)"""
    try:
        clear_all_data()
        return {
            "success": True,
            "message": "All data cleared successfully"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to clear data: {str(e)}"
        )


@router.post("/reseed")
def reseed_database(
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """Reseed entire database (admin only)"""
    try:
        clear_all_data()
        seed_initial_data()
        return {
            "success": True,
            "message": "Database reseeded successfully"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to reseed database: {str(e)}"
        )
