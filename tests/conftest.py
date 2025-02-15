from unittest.mock import MagicMock

import pytest

from repositories.user import UserRepository
from services.auth_service import AuthService
from services.user_service import UserService


@pytest.fixture
def mock_user_repo():
    return MagicMock(spec=UserRepository)


@pytest.fixture
def user_service(mock_user_repo):
    return UserService(user_repository=mock_user_repo)


@pytest.fixture
def auth_service(mock_user_repo):
    return AuthService(user_repository=mock_user_repo)
