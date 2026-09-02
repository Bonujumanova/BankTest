import uuid
import pytest

from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_request_request import CreditRequestRequest
from src.main.api.requests.create_account_requester import CreateAccountRequester
from src.main.api.requests.create_user_requester import CreateUserRequester
from src.main.api.requests.credit_request_requester import CreditRequestRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs


class TestCreditRequest:
    """ Проверяет корректность отправки запроса на получение кредита пользователем"""

    def test_credit_request_valid(self):
        # Создать пользователя
        username = f"Grinch{uuid.uuid4().hex[:3]}"
        create_account_request = CreateUserRequest(username=username, password="Pas!w0rd", role="ROLE_CREDIT_SECRET")
        CreateUserRequester(
            request_spec=RequestSpecs.authorization_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_ok()
        ).post(create_account_request)

        # Создать счет
        response = CreateAccountRequester(
            request_spec=RequestSpecs.authorization_headers(username=username, password="Pas!w0rd"),
            response_spec=ResponseSpecs.request_created()
        ).post()
        account_id = response.id

        # Отправить запрос на получение кредита
        credit_request = CreditRequestRequest(accountId=account_id, amount=5000, termMonths=12)
        response = CreditRequestRequester(
            request_spec=RequestSpecs.authorization_headers(username=username, password="Pas!w0rd"),
            response_spec=ResponseSpecs.request_created()
        ).post(credit_request)

        assert response.amount == 5000
        assert response.id == account_id



    @pytest.mark.parametrize("amount", [
        4900, 15001, 0, -1
    ])
    def test_credit_request_invalid(self, amount):
        """ Проверяет корректность входных данных, ниже минимального и выше максимального значенийю
         сумма кредита - в пределах(5000 - 15000 """

        # Создать пользователя
        username = f"Grinch{uuid.uuid4().hex[:3]}"
        create_account_request = CreateUserRequest(username=username, password="Pas!w0rd", role="ROLE_CREDIT_SECRET")
        CreateUserRequester(
            request_spec=RequestSpecs.authorization_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_ok()
        ).post(create_account_request)

        # Создать счет
        response = CreateAccountRequester(
            request_spec=RequestSpecs.authorization_headers(username=username, password="Pas!w0rd"),
            response_spec=ResponseSpecs.request_created()
        ).post()
        account_id = response.id

        # Отправить запрос на кредит
        credit_request = CreditRequestRequest(accountId=account_id, amount=amount, termMonths=12)
        response = CreditRequestRequester(
            request_spec=RequestSpecs.authorization_headers(username=username, password="Pas!w0rd"),
            response_spec=ResponseSpecs.request_bad()
        ).post(credit_request)

    def test_credit_request_invalid_404(self):
        """ Проверка, что пользователь может отправить запрос на получение кредита только ОДИН раз"""


        # Создать пользователя
        username = f"Grinch{uuid.uuid4().hex[:3]}"
        create_account_request = CreateUserRequest(username=username, password="Pas!w0rd", role="ROLE_CREDIT_SECRET")
        CreateUserRequester(
            request_spec=RequestSpecs.authorization_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_ok()
        ).post(create_account_request)

        # Создать счет
        response = CreateAccountRequester(
            request_spec=RequestSpecs.authorization_headers(username=username, password="Pas!w0rd"),
            response_spec=ResponseSpecs.request_created()
        ).post()
        account_id = response.id

        # Запрос на кредит 1
        credit_request = CreditRequestRequest(accountId=account_id, amount=5000, termMonths=12)
        response = CreditRequestRequester(
            request_spec=RequestSpecs.authorization_headers(username=username, password="Pas!w0rd"),
            response_spec=ResponseSpecs.request_created()
        ).post(credit_request)

        # Запрос на кредит 2
        credit_request = CreditRequestRequest(accountId=account_id, amount=9000, termMonths=12)
        response = CreditRequestRequester(
            request_spec=RequestSpecs.authorization_headers(username=username, password="Pas!w0rd"),
            response_spec=ResponseSpecs.request_bad_404()
        ).post(credit_request)
