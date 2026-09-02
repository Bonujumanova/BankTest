import uuid

import pytest

from src.main.api.models.account_to_up_request import AccountTopUpRequest
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.requests.account_top_up_requester import AccountTopUpRequester
from src.main.api.requests.create_account_requester import CreateAccountRequester
from src.main.api.requests.create_user_requester import CreateUserRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs


class TestAccountTopUp:
    """ Проверяет корректность пополнения счета"""
    # переменная для калькуляции баланса
    BALANCE: int = 0

    def test_account_top_up_valid(self):
        """ Проверяет корректность пополнения баланса"""

        # create user
        username = f"Santa{uuid.uuid4().hex[:5]}"
        create_user_request = CreateUserRequest(username=username, password="Pas!sw0rd", role="ROLE_USER")
        CreateUserRequester(
            request_spec=RequestSpecs.authorization_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_ok()
        ).post(create_user_request)

        # Create Bank account
        response = CreateAccountRequester(
            request_spec=RequestSpecs().authorization_headers(username=username, password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_created()
        ).post()
        account_id = response.id

        # Top up account
        account_top_up_request = AccountTopUpRequest(accountId=account_id, amount=8000)
        response = AccountTopUpRequester(
            request_spec=RequestSpecs.authorization_headers(username=username, password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_ok()
        ).post(account_top_up_request)

        TestAccountTopUp.BALANCE += response.balance

        assert response.id == account_id
        assert response.balance == TestAccountTopUp.BALANCE


    @pytest.mark.parametrize(
        "amount",
        [
            999,
            9001,
            90.1,
            0
        ]
    )
    def test_account_top_up_invalid(self, amount):
        """ Проверяет корректность входных данных(ниже минимальных и максимальных значений(1000 - 9000"""

        # Из-за parametrize код работает x раз, поэтому необходимо генерить имя, чтобы не было ошибок
        username = f"Santa{uuid.uuid4().hex[:5]}"
        # create user
        create_user_request = CreateUserRequest(username=username, password="Pas!sw0rd", role="ROLE_USER")
        CreateUserRequester(
            request_spec=RequestSpecs.authorization_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_ok()
        ).post(create_user_request)

        # Create Bank account
        response = CreateAccountRequester(
            request_spec=RequestSpecs().authorization_headers(username=username, password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_created()
        ).post()
        account_id = response.id

        # Top up account
        account_top_up_request = AccountTopUpRequest(accountId=account_id, amount=amount)
        AccountTopUpRequester(
            request_spec=RequestSpecs.authorization_headers(username=username, password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_bad()
        ).post(account_top_up_request)
