"""Review storage and user linkage utilities."""
import os, glob
from datetime import datetime
from typing import List, Dict, Optional
from backend.core.paths import REVIEWS_DIR
from backend.core.jsonio import load_json, save_json, ensure_parent
from backend.authentication.utils import load_active_users, save_active_users
from backend.reviews import schemas


def _path(movie_id: str) -> str:
    ensure_parent(os.path.join(REVIEWS_DIR, "placeholder"))
    return os.path.join(REVIEWS_DIR, f"{movie_id}_reviews.json")


def load_reviews(movie_id: str) -> List[Dict]:
    return load_json(_path(movie_id), default=[])


def save_reviews(movie_id: str, reviews: List[Dict]) -> None:
    save_json(_path(movie_id), reviews, atomic=True)


def user_already_reviewed(movie_id: str, user_id: str) -> bool:
    """Check if the user already has a review for the movie."""
    users = load_active_users()
    for u in users:
        if u.get("user_id") == user_id:
            return movie_id in u.get("movies_reviewed", [])
    return False


def add_review(movie_id: str, review_data: schemas.ReviewCreate, user_id: str) -> Dict:
    reviews = load_reviews(movie_id)
    if any(r.get("user_id") == user_id for r in reviews):
        raise ValueError("User already has a review for this movie.")

    new_review = schemas.Review(
        movie_id=movie_id,
        user_id=user_id,
        title=review_data.title,
        rating=review_data.rating,
        text=review_data.text,
    ).dict()

    reviews.append(new_review)
    save_reviews(movie_id, reviews)

    users = load_active_users()
    for u in users:
        if u.get("user_id") == user_id:
            u.setdefault("movies_reviewed", [])
            if movie_id not in u["movies_reviewed"]:
                u["movies_reviewed"].append(movie_id)
            break
    save_active_users(users)
    return new_review


def get_review(movie_id: str, review_id: str) -> Optional[Dict]:
    return next((r for r in load_reviews(movie_id) if r.get("review_id") == review_id), None)


def update_review(movie_id: str, review_id: str, updates: schemas.ReviewUpdate) -> Optional[Dict]:
    reviews = load_reviews(movie_id)
    for r in reviews:
        if r.get("review_id") == review_id:
            for k, v in updates.dict(exclude_unset=True).items():
                r[k] = v
            r["date"] = datetime.utcnow().date().isoformat()
            save_reviews(movie_id, reviews)
            return r
    return None


def delete_review(movie_id: str, review_id: str) -> bool:
    reviews = load_reviews(movie_id)
    updated = [r for r in reviews if r.get("review_id") != review_id]
    if len(updated) == len(reviews):
        return False
    save_reviews(movie_id, updated)
    return True


def add_vote(movie_id: str, review_id: str, vote: schemas.Vote) -> Optional[Dict]:
    reviews = load_reviews(movie_id)
    for r in reviews:
        if r.get("review_id") == review_id:
            r.setdefault("usefulness", {"helpful": 0, "total_votes": 0})
            r["usefulness"]["total_votes"] += 1
            if vote.vote:
                r["usefulness"]["helpful"] += 1
            save_reviews(movie_id, reviews)
            return r
    return None


def filter_sort_reviews(
    movie_id: str,
    rating: Optional[int] = None,
    sort_by: str = "date",
    order: str = "desc",
    skip: int = 0,
    limit: int = 20,
) -> List[Dict]:
    """Filter and sort reviews for a movie."""
    reviews = load_reviews(movie_id)
    if rating is not None:
        reviews = [r for r in reviews if r.get("rating") == rating]

    reverse = order.lower() == "desc"
    if sort_by in {"date", "rating"}:
        reviews.sort(key=lambda r: r.get(sort_by), reverse=reverse)
    elif sort_by == "helpful":
        reviews.sort(key=lambda r: r.get("usefulness", {}).get("helpful", 0), reverse=reverse)
    elif sort_by == "total_votes":
        reviews.sort(key=lambda r: r.get("usefulness", {}).get("total_votes", 0), reverse=reverse)

    return reviews[skip: skip + limit]


def get_reviews_by_user(user_id: str) -> List[Dict]:
    """Return all reviews by a specific user across all movies."""
    out: List[Dict] = []
    for path in glob.glob(os.path.join(REVIEWS_DIR, "*_reviews.json")):
        out.extend([r for r in load_json(path, default=[]) if r.get("user_id") == user_id])
    return out
