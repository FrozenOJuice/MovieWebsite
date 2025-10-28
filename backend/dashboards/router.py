# backend/dashboards/router.py
from fastapi import APIRouter, Depends, HTTPException
from backend.authentication.security import get_current_user
from backend.authentication import schemas as auth_schemas
from backend.dashboards import utils, schemas

router = APIRouter(prefix="/dashboards", tags=["Dashboards"])


@router.get("/member", response_model=schemas.MemberDashboard)
def member_dashboard(current_user: auth_schemas.UserToken = Depends(get_current_user)):
    if current_user.role not in ["member", "critic"]:
        raise HTTPException(status_code=403, detail="Access denied")
    return utils.build_member_dashboard(current_user.user_id)


@router.get("/critic", response_model=schemas.CriticDashboard)
def critic_dashboard(current_user: auth_schemas.UserToken = Depends(get_current_user)):
    if current_user.role != "critic":
        raise HTTPException(status_code=403, detail="Access denied")
    return utils.build_critic_dashboard(current_user.user_id)


@router.get("/moderator", response_model=schemas.ModeratorDashboard)
def moderator_dashboard(current_user: auth_schemas.UserToken = Depends(get_current_user)):
    if current_user.role != "moderator":
        raise HTTPException(status_code=403, detail="Access denied")
    return utils.build_moderator_dashboard(current_user.user_id)


@router.get("/admin", response_model=schemas.AdminDashboard)
def admin_dashboard(current_user: auth_schemas.UserToken = Depends(get_current_user)):
    if current_user.role != "administrator":
        raise HTTPException(status_code=403, detail="Access denied")
    return utils.build_admin_dashboard()
