from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..core.database import get_db
from ..core.roles import require_admin, get_current_user
from ..crud.user import get_users_count
from ..crud.search import get_search_topics_count, get_related_videos_count
from ..crud.explore import get_explore_topics_count
from ..schemas.user import User

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/stats")
def get_dashboard_stats(
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
) -> dict:
    """Get dashboard statistics (admin only)"""
    try:
        # Get counts for all entities
        total_users = get_users_count(db)
        total_search_topics = get_search_topics_count(db)
        total_explore_topics = get_explore_topics_count(db)
        total_videos = get_related_videos_count(db)
        
        # For now, we'll return empty recent activity
        # In a real implementation, you'd have an activity log table
        recent_activity = []
        
        return {
            "total_users": total_users,
            "total_search_topics": total_search_topics,
            "total_explore_topics": total_explore_topics,
            "total_videos": total_videos,
            "recent_activity": recent_activity
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch dashboard stats: {str(e)}"
        )
