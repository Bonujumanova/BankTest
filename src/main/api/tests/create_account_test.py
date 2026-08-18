import requests
import pytest

@pytest.mark.api
class TestCreateAccount:
    def test_create_account(self):
        # Авторизация администратора
        login_admin_response = requests.post(url="http://localhost:4111/api/auth/token/login",
                                             json={"username": "admin",
                                                   "password": "123456"
                                                   },
                                             headers={"accept": "application/json",
                                                      "Content-Type": "application/json"}
                                             )

        assert login_admin_response.status_code == 200
        # Работа с вложенным словарем
        assert login_admin_response.json().get("user").get("username") == "admin"
        assert login_admin_response.json().get("user").get("role") == "ROLE_ADMIN"

    def test_login_user(self):
        # Авторизация админа
        login_admin_response = requests.post(url="http://localhost:4111/api/auth/token/login",
                                             json={"username": "admin",
                                                   "password": "123456"
                                                   },
                                             headers={"accept": "application/json",
                                                      "Content-Type": "application/json"}
                                             )
        assert login_admin_response.status_code == 200

        # Получение токена
        token = login_admin_response.json().get("token")

        # Админ создает пользователя
        create_user_response = requests.post(
            url="http://localhost:4111/api/admin/create",
            json={
                "username": "Max8",
                "password": "Pas!sw0rd",
                "role": "ROLE_USER"
            },
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )

        assert create_user_response.status_code == 200

        # Авторизация пользователя
        login_user_response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json={
                "username": "Max8",
                "password": "Pas!sw0rd"
            },
            headers={
                "accept": "application/json",
                "Content-Type": "application/json"
            }
        )

        assert login_user_response.status_code == 200

        user_token = login_user_response.json().get("token")

        create_account_response = requests.post(
            url="http://localhost:4111/api/account/create",
            headers={
                "accept": "application/json",
                "Authorization": f"Bearer {user_token}"
            }
        )

        assert create_account_response.status_code == 201
        assert create_account_response.json().get("balance") == 0

