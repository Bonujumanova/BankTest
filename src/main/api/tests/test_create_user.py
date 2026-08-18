import requests
import pytest

from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.create_user_response import CreateUserResponse
from src.main.api.models.login_user_request import LoginUserRequest


@pytest.mark.api
class TestCreateUser:

    # Пользователей может создавать Admin, соответственно URL, Данные пользователя берутся из поля Admin
    def test_create_user_valid(self):
        login_user_request = LoginUserRequest(username="admin", password="123456")
        # Необходимо, чтобы Admin авторизовался в системе, для того чтобы у него появилась возможность
        # зарегистрировать нового пользователя
        # Данные URL взяты из пункта Authentication
        login_admin_response = requests.post(url="http://localhost:4111/api/auth/token/login",
                      json=login_user_request.model_dump(),
                      headers={"accept": "application/json",
                               "Content-Type": "application/json"}
        )

        assert login_admin_response.status_code == 200

        # Работа со словарем, достаем значение ключа "token"
        token = login_admin_response.json().get("token")


        # Admin создает нового пользователя(Post)
        #  post запрос содержит -
        #  requests.post(url="", data="", json="", headers="", params="", files="")
        create_user_request = CreateUserRequest(username="Max23", password="Pas!sw0rd", role="ROLE_USER")
        response = requests.post(
            url="http://localhost:4111/api/admin/create",
            json=create_user_request.model_dump(),
            headers={
                "Content-Type": "application/json",
                # Отправляем токен для авторизации
                "Authorization": f"Bearer {token}"
            }
        )

        assert response.status_code == 200
        create_user_response = CreateUserResponse(**response.json())
        assert create_user_request.username == create_user_response.username
        assert create_user_request.role == create_user_response.role


    @pytest.mark.parametrize(
        "username, password",
        [
            ("абв", "Pas!w0rd"),
            ("ab", "Pas!w0rd"),
            ("abc!", "Pas!sw0rd"),
            ("Maxx1", "Pas!w0rд"),
            ("Maxx2", "Pas!w0"),
            ("Maxx3", "pas!w0rd"),
            ("Maxx4", "PAS!W0RD"),
            ("Maxx5", "PASSWRRD"),
            ("Maxx5", "PAS!SWRD")
        ]
    )
    def test_create_user_invalid(self, username: str, password: str):
        login_admin_response = requests.post(url="http://localhost:4111/api/auth/token/login",
                                             json={"username": "admin",
                                                   "password": "123456"
                                                   },
                                             headers={"accept": "application/json",
                                                      "Content-Type": "application/json"}
                                             )

        assert login_admin_response.status_code == 200

        # Работа со словарем, достаем значение ключа "token"
        token = login_admin_response.json().get("token")

        create_user_request = CreateUserRequest(username=username, password=password, role="ROLE_USER")


        create_user_response = requests.post(
            url="http://localhost:4111/api/admin/create",
            json=create_user_request.model_dump(),
            headers={
                "Content-Type": "application/json",
                # Отправляем токен для авторизации
                "Authorization": f"Bearer {token}"
            }
        )

        assert create_user_response.status_code == 400

