from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.core.database import get_db
from src.schemas.token import Token
from src.use_cases.auth_service import login

router = APIRouter()


@router.post("/login", response_model=Token)
def login_user(email: str, password: str, db: Session = Depends(get_db)):
    token = login(db, email, password)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return token
