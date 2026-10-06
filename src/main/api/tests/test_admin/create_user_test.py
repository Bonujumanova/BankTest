import uuid

import allure

from src.main.api.configs.config import Config
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.requests.create_user_requester import CreateUserRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs
import pytest

class TestCreateUser:

    # Интегрирование allure в тест (Посмотреть отчет: allure serve allure-results)
    @allure.feature("Admin")
    @allure.story("Create user")
    @allure.title("Admin can create user")
    def test_create_user(self):
        # Авторизация администратора
        # Отправка Post-запроса для авторизации

        username = f"Grinch{uuid.uuid4().hex[:3]}"
        print(f"URL: {Config.fetch('backendUrl')}")
        create_user_request = CreateUserRequest(username=username, password="Pas!sw0rd", role="ROLE_USER")
        with allure.step(f"POST {Config.fetch('backendUrl')}{"/admin/create"}"):
            # Прикрепляет скриншот, файл, текст или лог-файлы к отчету
            allure.attach(
                str(create_user_request.model_dump()),
                "Request body",
                allure.attachment_type.JSON
            )

            response = CreateUserRequester(
                request_spec=RequestSpecs.authorization_headers(username="admin", password="123456"),
                response_spec=ResponseSpecs.request_ok()
            ).post(create_user_request)

            # Прикрепляет скриншот, файл, текст или лог-файлы к отчету
            allure.attach(
                str(response.model_dump()),
                "Request body",
                allure.attachment_type.JSON
            )


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
