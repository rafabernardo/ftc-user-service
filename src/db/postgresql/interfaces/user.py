import abc

from schemas.user import User, UserCredentials, UserInput


class UserRepositoryInterface(abc.ABC):
    @abc.abstractmethod
    def __init__(self): ...

    @abc.abstractmethod
    def add(self, user: UserInput) -> User:
        raise NotImplementedError

    @abc.abstractmethod
    def get_by_email(self, email: str) -> User | None:
        raise NotImplementedError

    @abc.abstractmethod
    def validate_credentials(
        self, user_credentials: UserCredentials
    ) -> User | None:
        raise NotImplementedError

    @abc.abstractmethod
    def exists_by_id(self, id: int) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def list_users(self) -> list[User]:
        raise NotImplementedError

    @abc.abstractmethod
    def delete_user(self, id: int) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def update_user(self, id: int, **kwargs) -> User:
        raise NotImplementedError
