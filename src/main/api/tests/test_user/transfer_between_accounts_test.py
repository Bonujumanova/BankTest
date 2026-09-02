import uuid

import pytest

from src.main.api.models.account_to_up_request import AccountTopUpRequest
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.transfer_between_accounts_request import TransferBetweenAccountsRequest
from src.main.api.requests.account_top_up_requester import AccountTopUpRequester
from src.main.api.requests.create_account_requester import CreateAccountRequester
from src.main.api.requests.create_user_requester import CreateUserRequester
from src.main.api.requests.transfer_netween_accounts_requester import TransferBetweenAccountsRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs


class TestTransferBetweenAccounts:
    """ Проверят корректность переводов между счетами"""
    def test_transfer_between_accounts_valid(self):
        """ Проверят корректность переводов между двумя счетами"""

        # Генерирует двух пользователей
        users: list[str] = [f"Santa{uuid.uuid4().hex[:5]}" for _ in range(2)]

        # Создание пользователя User1
        create_user_request = CreateUserRequest(username=users[0], password="Pas!sw0rd", role="ROLE_USER")
        CreateUserRequester(
            request_spec=RequestSpecs.authorization_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_ok()
        ).post(create_user_request)

        # Создание банковского аккаунта User1
        response = CreateAccountRequester(
            request_spec=RequestSpecs.authorization_headers(username=users[0], password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_created()
        ).post()
        user1_account_id = response.id

        # Пополнение баланса User1
        account_top_up_request = AccountTopUpRequest(accountId=user1_account_id, amount=8000)
        AccountTopUpRequester(
            request_spec=RequestSpecs.authorization_headers(username=users[0], password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_ok()
        ).post(account_top_up_request)

        # Создание пользователя User2
        create_user_request = CreateUserRequest(username=users[1], password="Pas!sw0rd", role="ROLE_USER")
        CreateUserRequester(
            request_spec=RequestSpecs.authorization_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_ok()
        ).post(create_user_request)

        # Создание банковского аккаунта User2
        response = CreateAccountRequester(
            request_spec=RequestSpecs.authorization_headers(username=users[1], password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_created()
        ).post()
        user2_account_id = response.id

        # Перевод от User1 к User2
        transfer_between_accounts = TransferBetweenAccountsRequest(
            fromAccountId=user1_account_id, toAccountId=user2_account_id, amount=500
        )
        response = TransferBetweenAccountsRequester(
            request_spec=RequestSpecs().authorization_headers(username=users[0], password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_ok()
        ).post(transfer_between_accounts)
        assert response.fromAccountIdBalance >= 0

    @pytest.mark.parametrize(
        "amount", [
            499, 100000, 0
        ]
    )
    def test_transfer_between_accounts_invalid_400(self, amount):
        """ Проверят корректность тела запроса(сумму перевода, она не должна быть превышена или принижена(500- 10000))"""

        # Генерирует двух пользователей
        users: list[str] = [f"Santa{uuid.uuid4().hex[:5]}" for _ in range(2)]

        # Создание пользователя User1
        create_user_request = CreateUserRequest(username=users[0], password="Pas!sw0rd", role="ROLE_USER")
        CreateUserRequester(
            request_spec=RequestSpecs.authorization_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_ok()
        ).post(create_user_request)

        # Создание банк аккаунта User1
        response = CreateAccountRequester(
            request_spec=RequestSpecs.authorization_headers(username=users[0], password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_created()
        ).post()
        user1_account_id = response.id

        # Пополнение баланса User1
        account_top_up_request = AccountTopUpRequest(accountId=user1_account_id, amount=8000)
        AccountTopUpRequester(
            request_spec=RequestSpecs.authorization_headers(username=users[0], password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_ok()
        ).post(account_top_up_request)

        # Создание пользователя User2
        create_user_request = CreateUserRequest(username=users[1], password="Pas!sw0rd", role="ROLE_USER")
        CreateUserRequester(
            request_spec=RequestSpecs.authorization_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_ok()
        ).post(create_user_request)

        # Создание банковского аккаунта User2
        response = CreateAccountRequester(
            request_spec=RequestSpecs.authorization_headers(username=users[1], password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_created()
        ).post()
        user2_account_id = response.id

        # Перевод от User1 к User2
        transfer_between_accounts = TransferBetweenAccountsRequest(
            fromAccountId=user1_account_id, toAccountId=user2_account_id, amount=amount
        )
        TransferBetweenAccountsRequester(
            request_spec=RequestSpecs().authorization_headers(username=users[0], password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_bad()
        ).post(transfer_between_accounts)



    def test_transfer_between_accounts_invalid_404(self):
        """ Проверка перевода, когда один из счетов не существует"""

        # Генерирует двух пользователей
        users: list[str] = [f"Santa{uuid.uuid4().hex[:5]}" for _ in range(2)]

        # Создание пользователя User1
        create_user_request = CreateUserRequest(username=users[0], password="Pas!sw0rd", role="ROLE_USER")
        CreateUserRequester(
            request_spec=RequestSpecs.authorization_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_ok()
        ).post(create_user_request)

        # Создание банк. аккаунта User1
        response = CreateAccountRequester(
            request_spec=RequestSpecs.authorization_headers(username=users[0], password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_created()
        ).post()
        user1_account_id = response.id

        # Пополнение баланса User1
        account_top_up_request = AccountTopUpRequest(accountId=user1_account_id, amount=8000)
        AccountTopUpRequester(
            request_spec=RequestSpecs.authorization_headers(username=users[0], password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_ok()
        ).post(account_top_up_request)

        # Перевод на несуществующий счет
        transfer_between_accounts = TransferBetweenAccountsRequest(
            fromAccountId=user1_account_id, toAccountId=122, amount=5000
        )
        TransferBetweenAccountsRequester(
            request_spec=RequestSpecs().authorization_headers(username=users[0], password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_bad_404()
        ).post(transfer_between_accounts)


    @pytest.mark.parametrize(
        "amount", [
            7000, 6000, 7777, 10000, 9999
        ]
    )
    def test_transfer_between_accounts_invalid_422(self, amount):
        """ Проверка перевода при недостатке средств"""

        # Генерирует двух пользователей
        users: list[str] = [f"Santa{uuid.uuid4().hex[:5]}" for _ in range(2)]

        # Создание пользователя User1
        create_user_request = CreateUserRequest(username=users[0], password="Pas!sw0rd", role="ROLE_USER")
        CreateUserRequester(
            request_spec=RequestSpecs.authorization_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_ok()
        ).post(create_user_request)

        # Создание банк аккаунта User1
        response = CreateAccountRequester(
            request_spec=RequestSpecs.authorization_headers(username=users[0], password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_created()
        ).post()
        user1_account_id = response.id

        # Пополнение баланса User1
        account_top_up_request = AccountTopUpRequest(accountId=user1_account_id, amount=5000)
        AccountTopUpRequester(
            request_spec=RequestSpecs.authorization_headers(username=users[0], password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_ok()
        ).post(account_top_up_request)

        # Создание пользователя User2
        create_user_request = CreateUserRequest(username=users[1], password="Pas!sw0rd", role="ROLE_USER")
        CreateUserRequester(
            request_spec=RequestSpecs.authorization_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_ok()
        ).post(create_user_request)

        # Создание банковского аккаунта User2
        response = CreateAccountRequester(
            request_spec=RequestSpecs.authorization_headers(username=users[1], password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_created()
        ).post()
        user2_account_id = response.id

        # Перевод от User1 к User2
        transfer_between_accounts = TransferBetweenAccountsRequest(
            fromAccountId=user1_account_id, toAccountId=user2_account_id, amount=amount
        )
        TransferBetweenAccountsRequester(
            request_spec=RequestSpecs().authorization_headers(username=users[0], password="Pas!sw0rd"),
            response_spec=ResponseSpecs.request_bad_422()
        ).post(transfer_between_accounts)
