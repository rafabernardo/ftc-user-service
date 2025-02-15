from fastapi.testclient import TestClient

from schemas.user import User
from services.user_service import UserService


def test_list_users(
    client: TestClient, user_service_mock: UserService, setup_wiring
):
    user_service_mock.list_users.return_value = [
        User(
            id="123",
            name="User Test",
            email="email@test.com",
            is_admin=False,
            is_editor=False,
            is_reader=True,
            created_at="2025-02-08T12:57:18.267Z",
            updated_at="2025-02-08T12:57:18.267Z",
        ),
        User(
            id="456",
            name="User Test",
            email="email2@test.com",
            is_admin=False,
            is_editor=False,
            is_reader=True,
            created_at="2025-02-08T12:57:18.267Z",
            updated_at="2025-02-08T12:57:18.267Z",
        ),
    ]

    response = client.get("/v1/users")

    assert response.status_code == 200
    assert len(response.json()) == 1
