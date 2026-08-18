import requests
import pytest

from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.login_user_request import LoginUserRequest
from src.main.api.models.login_user_response import LoginUserResponse


@pytest.mark.api
class TestUserLogin:

    def test_login_admin(self):
        login_user_request = LoginUserRequest(username="admin", password="123456")
        # Авторизация администратора
        response = requests.post(url="http://localhost:4111/api/auth/token/login",
                                             json=login_user_request.model_dump(),
                                             headers={"accept": "application/json",
                                                      "Content-Type": "application/json"}
                                             )

        assert response.status_code == 200
        login_user_response = LoginUserResponse(**response.json())
        # Работа с вложенным словарем
        assert login_user_request.username == login_user_response.user.username
        assert login_user_response.user.role == "ROLE_ADMIN"
        print(f"ПЕЧАТАЮ ИМЯ АДМИНА: {response.json().get("user").get("username")}")


    def test_login_user(self):
        login_admin_request = LoginUserRequest(username="admin", password="123456")
        # Авторизация админа
        response = requests.post(url="http://localhost:4111/api/auth/token/login",
                                             json=login_admin_request.model_dump(),
                                             headers={"accept": "application/json",
                                                      "Content-Type": "application/json"}
                                             )
        assert response.status_code == 200

        # Получение токена
        token = response.json().get("token")


        create_user_request = CreateUserRequest(username="Max23", password="Pas!sw0rd", role="ROLE_USER")
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

        login_user_request = LoginUserRequest(username="Max23", password="Pas!sw0rd")
        response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json=login_user_request.model_dump(),
            headers={
                "accept": "application/json",
                "Content-Type": "application/json"
            }
        )

        assert response.status_code == 200
        login_user_response = LoginUserResponse(**response.json())
        assert login_user_request.username == login_user_response.user.username
        assert login_user_response.user.role == "ROLE_USER"
