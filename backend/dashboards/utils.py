# backend/dashboards/utils.py
from backend.users import utils as user_utils
from backend.movies import utils as movie_utils
from backend.reviews import utils as review_utils
from backend.penalties import utils as penalty_utils
from backend.reports import utils as report_utils

def build_member_dashboard(user_id: str):
    user = user_utils.get_user_by_id(user_id)
    reviews = review_utils.get_reviews_by_user(user_id)
    penalties = penalty_utils.get_penalties_by_user(user_id)
    watch_later = [movie_utils.get_movie(mid) for mid in user.get("watch_later", [])]

    return {
        "username": user["username"],
        "status": user["status"],
        "movies_reviewed": len(user["movies_reviewed"]),
        "watch_later": watch_later,
        "penalties": penalties,
        "recent_reviews": reviews[-3:],
    }

def build_critic_dashboard(user_id: str):
    data = build_member_dashboard(user_id)
    data.update({
        "avg_review_rating": _calculate_avg_rating(user_id)
    })
    return data

def build_moderator_dashboard(user_id: str):
    open_reports = report_utils.list_reports(status="pending")
    resolved_reports = report_utils.list_reports(status="resolved")
    return {
        "total_reports": len(open_reports) + len(resolved_reports),
        "open_reports": open_reports,
        "resolved_reports": resolved_reports,
    }

def build_admin_dashboard():
    active_users = user_utils.load_active_users()
    inactive_users = user_utils.load_inactive_users()
    penalties = penalty_utils.load_all_penalties()
    return {
        "total_users": len(active_users) + len(inactive_users),
        "active_users": len(active_users),
        "inactive_users": len(inactive_users),
        "active_penalties": len([p for p in penalties if p["status"] == "active"]),
    }

def _calculate_avg_rating(user_id: str):
    reviews = review_utils.get_reviews_by_user(user_id)
    ratings = [r["rating"] for r in reviews if "rating" in r]
    return round(sum(ratings)/len(ratings), 2) if ratings else 0.0
