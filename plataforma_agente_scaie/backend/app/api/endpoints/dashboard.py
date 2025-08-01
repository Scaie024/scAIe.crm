from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Dict, Any

from ...core.database import get_db

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.get("/stats")
def get_dashboard_stats(
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get dashboard statistics (placeholder).
    """
    # In a full implementation, this would query the database for real statistics
    return {
        "total_contacts": 120,
        "total_conversations": 85,
        "active_conversations": 12,
        "total_messages": 1250,
        "conversion_rate": "24.5%",
        "avg_response_time": "2.3s"
    }

@router.get("/recent-activity")
def get_recent_activity(
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    """
    Get recent activity (placeholder).
    """
    # In a full implementation, this would query the database for recent activity
    return {
        "recent_contacts": [
            {"name": "Juan Pérez", "phone": "+52 55 1234 5678", "time": "2 min ago"},
            {"name": "María García", "phone": "+52 55 8765 4321", "time": "15 min ago"},
            {"name": "Carlos López", "phone": "+52 55 1111 2222", "time": "1 hour ago"}
        ],
        "recent_messages": [
            {"contact": "Juan Pérez", "message": "¿Tienen disponibilidad para mañana?", "time": "5 min ago"},
            {"contact": "María García", "message": "Gracias por la información", "time": "20 min ago"}
        ]
    }