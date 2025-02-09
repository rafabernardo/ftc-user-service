from datetime import datetime

from db.postgresql.database import get_postgresql_session

from src.db.postgresql.interfaces.user import UserRepositoryInterface
from src.db.postgresql.models.user import User as UserDB
from src.schemas.user import User, UserCredentials, UserInput


class UserRepository(UserRepositoryInterface):
    def __init__(self):
        self.db_session = get_postgresql_session()

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
        with self.db_session as session:
            session.add(db_user)
            session.commit()
            session.refresh(db_user)
            return User.model_validate(db_user)

    def get_by_email(self, email: str) -> User | None:
        with self.db_session as session:
            db_user = (
                session.query(UserDB).filter(UserDB.email == email).first()
            )
            user = User.model_validate(db_user) if db_user else None
        return user

    def validate_credentials(
        self, user_credentials: UserCredentials
    ) -> User | None:
        with self.db_session as session:
            db_user = (
                session.query(UserDB)
                .filter(
                    UserDB.email == user_credentials.email,
                    UserDB.hashed_password == user_credentials.password,
                )
                .first()
            )
            user = User.model_validate(db_user)
        return user

    def exists_by_id(self, id: int) -> bool:
        return self.db_session.query(User).filter(User.id == id).count() > 0

    def list_users(self) -> list[User]:
        return self.db_session.query(User).all()

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
