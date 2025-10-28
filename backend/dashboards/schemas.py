"""Dashboard response models for each role."""
from typing import List, Any
from pydantic import BaseModel
from backend.movies.schemas import Movie
from backend.reports.schemas import Report


class MemberDashboard(BaseModel):
    username: str
    status: str
    movies_reviewed: int
    watch_later: List[Movie]
    penalties: List[Any]  # simplified to avoid circular imports with penalty model
    recent_reviews: List[Any] = []


class CriticDashboard(MemberDashboard):
    avg_review_rating: float = 0.0


class ModeratorDashboard(BaseModel):
    total_reports: int
    open_reports: List[Report]
    resolved_reports: List[Report]


class AdminDashboard(BaseModel):
    total_users: int
    active_users: int
    inactive_users: int
    active_penalties: int
