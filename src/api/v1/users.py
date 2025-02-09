from uuid import uuid4

from core.dependency_injection import Container
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException
from services.user_service import UserService

from src.schemas.user import User, UserInput

router = APIRouter(prefix="/users")


@router.post("/", response_model=User)
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
def get_user(
    email: int,
    user_service: UserService = (Depends(Provide[Container.user_service])),
):
    user = user_service.get_user_by_email(email)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
