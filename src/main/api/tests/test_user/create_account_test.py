import uuid

from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.requests.create_account_requester import CreateAccountRequester
from src.main.api.requests.create_user_requester import CreateUserRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs


class TestCreateBankAccount:
    """ Проверяет корректность создания пользователя"""

    def test_create_bank_account_valid(self):
        """ Проверяет корректность создания пользователя"""

        # Создание пользователя, авторизация админа
        create_user_request = CreateUserRequest(username="Max107", password="Pas!sw0rd", role="ROLE_USER")
        response = CreateUserRequester(
            request_spec=RequestSpecs.authorization_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_ok()
        ).post(create_user_request)

        assert create_user_request.username == response.username
        assert create_user_request.role == response.role


        # Создание банк. аккаунта
        response = CreateAccountRequester(
            request_spec=RequestSpecs.authorization_headers(username="Max107", password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_created()
        ).post()
        assert response.balance == 0



    def test_create_bank_account_invalid_409(self):
        """
        Проверяет максимальное число банковских аккаунтов
        Пользователь может иметь только 2 аккаунта
        """
        # Создание пользователя, авторизация админа
        username = f"Santa{uuid.uuid4().hex[:5]}"
        create_user_request = CreateUserRequest(username=username, password="Pas!sw0rd", role="ROLE_USER")
        response = CreateUserRequester(
            request_spec=RequestSpecs.authorization_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_ok()
        ).post(create_user_request)

        assert create_user_request.username == response.username
        assert create_user_request.role == response.role

        # Создание аккаунта 1
        CreateAccountRequester(
            request_spec=RequestSpecs.authorization_headers(username=username, password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_created()
        ).post()

        # Создание аккаунта 2
        CreateAccountRequester(
            request_spec=RequestSpecs.authorization_headers(username=username, password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_created()
        ).post()

        # Создание аккаунта 3
        CreateAccountRequester(
            request_spec=RequestSpecs.authorization_headers(username=username, password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_maximum_number_accounts_409()
        ).post()
