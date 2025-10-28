"""Role-specific dashboard aggregation utilities."""
from typing import Dict, Any
from backend.users import utils as user_utils
from backend.movies import utils as movie_utils
from backend.reviews import utils as review_utils
from backend.penalties import utils as penalty_utils
from backend.reports import utils as report_utils


def build_member_dashboard(user_id: str) -> Dict[str, Any]:
    user = user_utils.get_user_by_id(user_id)
    if not user:
        return {"error": "User not found"}

    reviews = review_utils.get_reviews_by_user(user_id)
    penalties = penalty_utils.get_penalties_by_user(user_id)
    watch_later = [movie_utils.get_movie(mid) for mid in user.get("watch_later", [])]

    return {
        "username": user.get("username"),
        "status": user.get("status"),
        "movies_reviewed": len(user.get("movies_reviewed", [])),
        "watch_later": [m for m in watch_later if m],
        "penalties": penalties,
        "recent_reviews": reviews[-3:],
    }


def _avg_rating_by_user(user_id: str) -> float:
    reviews = review_utils.get_reviews_by_user(user_id)
    ratings = [r.get("rating", 0) for r in reviews if isinstance(r.get("rating"), (int, float))]
    return round(sum(ratings) / len(ratings), 2) if ratings else 0.0


def build_critic_dashboard(user_id: str) -> Dict[str, Any]:
    data = build_member_dashboard(user_id)
    data.update({"avg_review_rating": _avg_rating_by_user(user_id)})
    return data


def build_moderator_dashboard(user_id: str) -> Dict[str, Any]:
    pending = report_utils.filter_reports_by_status(report_utils.schemas.ReportStatus.pending)
    resolved = report_utils.filter_reports_by_status(report_utils.schemas.ReportStatus.resolved)
    return {
        "total_reports": len(pending) + len(resolved),
        "open_reports": pending,
        "resolved_reports": resolved,
    }


def build_admin_dashboard() -> Dict[str, Any]:
    active_users = user_utils.load_active_users()
    inactive_users = user_utils.load_inactive_users()
    penalties = penalty_utils._load()
    return {
        "total_users": len(active_users) + len(inactive_users),
        "active_users": len(active_users),
        "inactive_users": len(inactive_users),
        "active_penalties": len([p for p in penalties if p.get("status") == "active"]),
    }
