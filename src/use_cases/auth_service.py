from datetime import timedelta

from sqlalchemy.orm import Session

from src.core.security import create_access_token, verify_password
from src.core.settings import get_settings
from src.models.user import User
from src.schemas.token import Token

settings = get_settings()


def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


def login(db: Session, email: str, password: str):
    user = authenticate_user(db, email, password)
    if not user:
        return None
    token_data = {
        "sub": user.email,
        "is_admin": user.is_admin,
        "is_reader": user.is_reader,
        "is_editor": user.is_editor,
    }
    token = create_access_token(
        token_data, timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return Token(access_token=token, token_type="bearer")
