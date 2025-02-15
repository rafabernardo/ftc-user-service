from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import EmailStr

from core.dependency_injection import Container
from services.user_service import UserService
from src.schemas.user import User, UserInput, UserUpdate

router = APIRouter(prefix="/users")


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
@inject
def create_user(
    user: UserInput,
    user_service: UserService = (Depends(Provide[Container.user_service])),
):
    try:
        user = user_service.create_user(user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    return user


@router.get("/{user_email}", response_model=User)
@inject
def get_user(
    user_email: EmailStr,
    user_service: UserService = (Depends(Provide[Container.user_service])),
):
    user = user_service.get_user_by_email(user_email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/", response_model=list[User])
@inject
def list_users(
    limit: int = Query(10, ge=1, le=100),
    page: int = Query(1, ge=1, le=100),
    user_service: UserService = (Depends(Provide[Container.user_service])),
):
    users = user_service.list_users(limit=limit, page=page)
    return users


@router.patch("/{user_id}", response_model=User)
@inject
def update_user(
    user_id: str,
    user_data: UserUpdate,
    user_service: UserService = (Depends(Provide[Container.user_service])),
):
    users = user_service.update_user(user_id, user_data)
    if users is None:
        raise HTTPException(status_code=404, detail="User not found")
    return users
