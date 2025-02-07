from sqlalchemy.orm import Session

from src.core.security import hash_password
from src.models.user import User
from src.schemas.user import UserCreate, UserUpdate


def create_user(db: Session, user_data: UserCreate):
    """Creates a new user with a hashed password."""
    hashed_password = hash_password(user_data.password)
    user = User(
        email=user_data.email,
        hashed_password=hashed_password,
        is_admin=user_data.is_admin,
        is_editor=user_data.is_editor,
        is_reader=user_data.is_reader,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user(db: Session, user_id: int):
    """Retrieve a user by ID."""
    return db.query(User).filter(User.id == user_id).first()


def update_user(db: Session, user_id: int, user_data: UserUpdate):
    """Update user details."""
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        for key, value in user_data.dict(exclude_unset=True).items():
            setattr(user, key, value)
        db.commit()
        db.refresh(user)
    return user


def delete_user(db: Session, user_id: int):
    """Delete a user."""
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
    return user
