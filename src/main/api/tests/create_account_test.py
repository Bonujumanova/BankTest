import requests
import pytest

from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.models.login_user_response import LoginUserResponse


@pytest.mark.api
class TestCreateAccount:
    def test_create_account(self):
        login_admin_request = LoginUserRequest(username="admin", password="123456")
        # Авторизация администратора
        response = requests.post(url="http://localhost:4111/api/auth/token/login",
                                             json=login_admin_request.model_dump(),
                                             headers={"accept": "application/json",
                                                      "Content-Type": "application/json"}
                                             )

        assert response.status_code == 200
        login_admin_response = LoginUserResponse(**response.json())
        assert login_admin_request.username == login_admin_response.user.username
        assert login_admin_response.user.role == "ROLE_ADMIN"

        # Получение токена
        token = response.json().get("token")

        create_user_request = CreateUserRequest(username="Max28", password="Pas!sw0rd", role="ROLE_USER")
        # Админ создает пользователя
        response = requests.post(
            url="http://localhost:4111/api/admin/create",
            json=create_user_request.model_dump(),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )

        assert response.status_code == 200


        # Данные для авторизации
        login_user_request = LoginUserRequest(username="Max28", password="Pas!sw0rd")
        # Авторизация пользователя
        response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json=login_user_request.model_dump(),
            headers={
                "accept": "application/json",
                "Content-Type": "application/json"
            }
        )
        assert response.status_code == 200

        user_token = response.json().get("token")

        response = requests.post(
            url="http://localhost:4111/api/account/create",
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {user_token}"
            }
        )

        assert response.status_code == 201
        create_account_response = CreateAccountResponse(**response.json())
        assert create_account_response.balance == 0

