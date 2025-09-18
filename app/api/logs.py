from fastapi import APIRouter, HTTPException, status
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging

# Configure logger for this module
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/logs", tags=["logs"])

# In-memory storage for logs (since no database is needed)
logs_storage: List[Dict[str, Any]] = []


@router.post("/")
def create_log(log_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Receive and store log data in memory

    Args:
        log_data: Dictionary containing log information

    Returns:
        Dictionary with confirmation and stored log data
    """
    try:
        # Add timestamp and unique ID to the log entry
        log_entry = {
            "id": len(logs_storage) + 1,
            "timestamp": datetime.utcnow().isoformat(),
            "data": log_data,
        }

        # Store in memory
        logs_storage.append(log_entry)

        # Log to application logger as well
        logger.info(f"Received log entry: {log_data}")

        return {
            "message": "Log entry created successfully",
            "log_id": log_entry["id"],
            "timestamp": log_entry["timestamp"],
            "data": log_entry["data"],
        }

    except Exception as e:
        logger.error(f"Failed to create log entry: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create log entry: {str(e)}",
        )


@router.get("/")
def get_logs(limit: Optional[int] = 100, offset: Optional[int] = 0) -> Dict[str, Any]:
    """
    Retrieve stored log entries

    Args:
        limit: Maximum number of logs to return (default: 100)
        offset: Number of logs to skip (default: 0)

    Returns:
        Dictionary containing logs and metadata
    """
    try:
        # Apply pagination
        start_idx = offset
        end_idx = offset + limit

        paginated_logs = logs_storage[start_idx:end_idx]

        return {
            "logs": paginated_logs,
            "total_count": len(logs_storage),
            "returned_count": len(paginated_logs),
            "offset": offset,
            "limit": limit,
        }

    except Exception as e:
        logger.error(f"Failed to retrieve logs: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve logs: {str(e)}",
        )


@router.get("/{log_id}")
def get_log_by_id(log_id: int) -> Dict[str, Any]:
    """
    Retrieve a specific log entry by ID

    Args:
        log_id: The ID of the log entry to retrieve

    Returns:
        Dictionary containing the log entry
    """
    try:
        # Find log by ID
        for log_entry in logs_storage:
            if log_entry["id"] == log_id:
                return log_entry

        # If not found
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Log entry with ID {log_id} not found",
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to retrieve log {log_id}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve log: {str(e)}",
        )


@router.delete("/")
def clear_logs() -> Dict[str, Any]:
    """
    Clear all stored log entries

    Returns:
        Dictionary with confirmation message
    """
    try:
        cleared_count = len(logs_storage)
        logs_storage.clear()

        logger.info(f"Cleared {cleared_count} log entries")

        return {
            "message": f"Successfully cleared {cleared_count} log entries",
            "cleared_count": cleared_count,
        }

    except Exception as e:
        logger.error(f"Failed to clear logs: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to clear logs: {str(e)}",
        )


@router.get("/stats/summary")
def get_logs_summary() -> Dict[str, Any]:
    """
    Get summary statistics about stored logs

    Returns:
        Dictionary containing log statistics
    """
    try:
        if not logs_storage:
            return {
                "total_logs": 0,
                "oldest_log": None,
                "newest_log": None,
                "message": "No logs available",
            }

        # Get oldest and newest timestamps
        timestamps = [log["timestamp"] for log in logs_storage]
        oldest_timestamp = min(timestamps)
        newest_timestamp = max(timestamps)

        return {
            "total_logs": len(logs_storage),
            "oldest_log": oldest_timestamp,
            "newest_log": newest_timestamp,
            "storage_type": "in_memory",
        }

    except Exception as e:
        logger.error(f"Failed to get logs summary: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get logs summary: {str(e)}",
        )
