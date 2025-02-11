from datetime import datetime

from db.postgresql.database import get_postgresql_session
from src.db.postgresql.interfaces.user import UserRepositoryInterface
from src.db.postgresql.models.user import User as UserDB
from src.schemas.user import User, UserCredentials, UserInput


class UserRepository(UserRepositoryInterface):
    def __init__(self): ...

    def add(self, user: UserInput) -> User:
        now = datetime.now()
        db_user = UserDB(
            name=user.name,
            email=user.email,
            hashed_password=user.password,
            is_admin=user.is_admin,
            is_reader=user.is_reader,
            is_editor=user.is_editor,
            created_at=now,
            updated_at=now,
        )
        with get_postgresql_session() as session:
            session.add(db_user)
            session.commit()
            session.refresh(db_user)
            user = User.model_validate(db_user)
        return user

    def get_by_email(self, email: str) -> User | None:
        with get_postgresql_session() as session:
            db_user = (
                session.query(UserDB).filter(UserDB.email == email).first()
            )
            user = User.model_validate(db_user) if db_user else None
        return user

    def validate_credentials(
        self, user_credentials: UserCredentials
    ) -> User | None:
        with get_postgresql_session() as session:
            db_user = (
                session.query(UserDB)
                .filter(
                    UserDB.email == user_credentials.email,
                    UserDB.hashed_password == user_credentials.password,
                )
                .first()
            )
            user = User.model_validate(db_user) if db_user else None
        return user

    def list_users(self, limit: int, offset: int) -> list[User]:
        with get_postgresql_session() as session:
            db_users = session.query(UserDB).offset(offset).limit(limit).all()
            users = [User.model_validate(db_user) for db_user in db_users]
        return users

    def delete_user(self, id: int) -> bool:
        user = self.get_by_id(id)
        if user:
            self.db_session.delete(user)
            self.db_session.commit()
            return True
        return False

    def update_user(self, id: int, **kwargs) -> User:
        user = self.get_by_id(id)
        if user:
            for key, value in kwargs.items():
                setattr(user, key, value)
            self.db_session.commit()
            self.db_session.refresh(user)
        return user
