import uuid

import pytest

from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_repay_request import CreditRepayRequest
from src.main.api.models.credit_request_request import CreditRequestRequest
from src.main.api.requests.create_account_requester import CreateAccountRequester
from src.main.api.requests.create_user_requester import CreateUserRequester
from src.main.api.requests.credit_repay_requester import CreditRepayRequester
from src.main.api.requests.credit_request_requester import CreditRequestRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs


class TestCreditRepay:
    """ проверяет корректность погашения кредита пользователем"""

    # Create User
    # Create Account
    # Take out a loan
    # Pay off a loan
    def test_credit_repay_valid(self):
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

        # Взять кредит
        credit_request = CreditRequestRequest(accountId=account_id, amount=5000, termMonths=12)
        response = CreditRequestRequester(
            request_spec=RequestSpecs.authorization_headers(username=username, password="Pas!w0rd"),
            response_spec=ResponseSpecs.request_created()
        ).post(credit_request)
        credit_id = response.creditId

        # Погасить кредит
        credit_repay_request = CreditRepayRequest(creditId=credit_id, accountId=account_id, amount=5000)
        response = CreditRepayRequester(
            request_spec=RequestSpecs.authorization_headers(username=username, password="Pas!w0rd"),
            response_spec=ResponseSpecs.request_ok()
        ).post(credit_repay_request)

        assert response.amountDeposited == 5000
        

    @pytest.mark.parametrize("amount", [
    1000, 20000
    ])
    def test_credit_repay_invalid_422(self, amount):
        """ Проверяет, что кредит погашается, а не оплачивается частями"""
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

        # Взять кредит
        credit_request = CreditRequestRequest(accountId=account_id, amount=5000, termMonths=12)
        response = CreditRequestRequester(
            request_spec=RequestSpecs.authorization_headers(username=username, password="Pas!w0rd"),
            response_spec=ResponseSpecs.request_created()
        ).post(credit_request)
        credit_id = response.creditId

        # Погасить кредит
        credit_repay_request = CreditRepayRequest(creditId=credit_id, accountId=account_id, amount=amount)
        response = CreditRepayRequester(
            request_spec=RequestSpecs.authorization_headers(username=username, password="Pas!w0rd"),
            response_spec=ResponseSpecs.request_bad_422()
        ).post(credit_repay_request)
