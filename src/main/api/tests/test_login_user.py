import requests
import pytest

@pytest.mark.api

class TestUserLogin:

    def test_login_admin(self):
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
        print(f"ПЕЧАТАЮ ИМЯ АДМИНА: {login_admin_response.json().get("user").get("username")}")


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
                "username": "Max66",
                "password": "Pas!sw0rd",
                "role": "ROLE_USER"
            },
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            }
        )

        assert create_user_response.status_code == 200

        login_user_response = requests.post(
            url="http://localhost:4111/api/auth/token/login",
            json={
                "username": "Max66",
                "password": "Pas!sw0rd"
            },
            headers={
                "accept": "application/json",
                "Content-Type": "application/json"
            }
        )

        assert login_user_response.status_code == 200
        assert login_user_response.json().get("user").get("username") == "Max66"
        assert login_user_response.json().get("user").get("role") == "ROLE_USER"





