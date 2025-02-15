from fastapi.testclient import TestClient

from schemas.user import User
from services.user_service import UserService


def test_get_user(
    client: TestClient, user_service_mock: UserService, setup_wiring
):
    user_email = "email@test.com"
    user_service_mock.list_users.return_value = User(
        id="123",
        name="User Test",
        email=user_email,
        is_admin=False,
        is_editor=False,
        is_reader=True,
        created_at="2025-02-08T12:57:18.267Z",
        updated_at="2025-02-08T12:57:18.267Z",
    )

    response = client.get(f"/v1/user/{user_email}")

    assert response.status_code == 200
