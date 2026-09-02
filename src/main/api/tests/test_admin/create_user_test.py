from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.requests.create_user_requester import CreateUserRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
import pytest

class TestCreateUser:
    def test_create_user(self):
        # Авторизация администратора
        # Отправка Post-запроса для авторизации
        create_user_request = CreateUserRequest(username="Max01211", password="Pas!sw0rd", role="ROLE_USER")
        response = CreateUserRequester(
            request_spec=RequestSpecs.authorization_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_ok()
        ).post(create_user_request)

        assert create_user_request.username == response.username
        assert create_user_request.role == response.role



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
        create_user_request = CreateUserRequest(username=username, password=password, role="ROLE_USER")
        response = CreateUserRequester(
            request_spec=RequestSpecs.authorization_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_bad()
        ).post(create_user_request)
