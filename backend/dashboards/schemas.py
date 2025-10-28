# backend/dashboards/schemas.py
from pydantic import BaseModel
from typing import List, Optional, Any

class MemberDashboard(BaseModel):
    username: str
    status: str
    movies_reviewed: int
    watch_later: List[Any]
    penalties: List[Any]
    recent_reviews: List[Any]

class CriticDashboard(MemberDashboard):
    avg_review_rating: float

class ModeratorDashboard(BaseModel):
    total_reports: int
    open_reports: List[Any]
    resolved_reports: List[Any]

class AdminDashboard(BaseModel):
    total_users: int
    active_users: int
    inactive_users: int
    active_penalties: int
