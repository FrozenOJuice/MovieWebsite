"""Shared authorization and penalty-check helpers for routers."""
from fastapi import HTTPException, status
from functools import wraps
from backend.penalties import utils as penalty_utils


def require_role(user, allowed_roles: list[str]) -> None:
    """Raise 403 if the current user's role is not in allowed_roles."""
    if user.role not in allowed_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied."
        )


def block_if_penalized(blocked_types: list[str]):
    """
    Decorator for FastAPI route handlers that blocks access when a user has
    an active penalty of any type in `blocked_types`. Expects the route to
    receive `current_user` via Depends(get_current_user).
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            current_user = kwargs.get("current_user")
            if not current_user:
                raise HTTPException(status_code=401, detail="User context missing.")
            restriction = penalty_utils.check_active_penalty(current_user.user_id, blocked_types)
            if restriction:
                raise HTTPException(status_code=403, detail=restriction)
            return await func(*args, **kwargs)
        return wrapper
    return decorator
