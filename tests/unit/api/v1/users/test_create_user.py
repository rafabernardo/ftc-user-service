from fastapi.testclient import TestClient

from schemas.user import User, UserInput
from services.user_service import UserService


def test_create_user_success(
    client: TestClient, user_service_mock: UserService, setup_wiring
):
    user_input = UserInput(
        **{
            "name": "John Doe",
            "email": "john@example.com",
            "is_admin": False,
            "is_editor": False,
            "is_reader": True,
            "password": "password",
        }
    )
    user_service_mock.create_user.return_value = User(
        id="123",
        name="John Doe",
        email="john@example.com",
        is_admin=False,
        is_editor=False,
        is_reader=True,
        created_at="2025-02-08T12:57:18.267Z",
        updated_at="2025-02-08T12:57:18.267Z",
    )
    response = client.post("v1/users/", json=user_input.model_dump())

    assert response.status_code == 201
    assert response.json()["name"] == "John Doe"
    assert response.json()["email"] == "john@example.com"
