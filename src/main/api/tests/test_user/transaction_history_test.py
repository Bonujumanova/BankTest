import uuid

from src.main.api.models.create_account_response import CreateAccountResponse
from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.requests.create_account_requester import CreateAccountRequester
from src.main.api.requests.create_user_requester import CreateUserRequester
from src.main.api.requests.transactions_history_requester import TransactionsHistoryRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs


class TestTransactionsHistory:
    """ Проверяет корректность получения истории кредитов пользователя"""

    def test_transactions_history_valid(self):
        # Создать User
        username = f"Grinch{uuid.uuid4().hex[:3]}"
        create_account_request = CreateUserRequest(username=username, password="Pas!w0rd", role="ROLE_USER")
        response = CreateUserRequester(
            request_spec=RequestSpecs.authorization_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_ok()
        ).post(create_account_request)

        # Создать счет
        response = CreateAccountRequester(
            request_spec=RequestSpecs.authorization_headers(username=username, password="Pas!w0rd"),
            response_spec=ResponseSpecs.request_created()
        ).post()
        user_account_id = response.id

        # Получить инфу о счете
        response = TransactionsHistoryRequester(
            request_spec=RequestSpecs.authorization_headers(username=username,password="Pas!w0rd"),
            response_spec=ResponseSpecs.request_ok()
        ).post(user_account_id)

        assert response.id == user_account_id
