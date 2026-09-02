import uuid

from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.credit_request_request import CreditRequestRequest
from src.main.api.requests.create_account_requester import CreateAccountRequester
from src.main.api.requests.create_user_requester import CreateUserRequester
from src.main.api.requests.credit_history_requester import CreditHistoryRequester
from src.main.api.requests.credit_request_requester import CreditRequestRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs


class TestCreditHistory:
    def test_get_credit_history(self):
        """ Проверка корректности получения кредитной истории пользователем"""

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

        #Взять кредит
        credit_request = CreditRequestRequest(accountId=account_id, amount=5000, termMonths=12)
        response = CreditRequestRequester(
            request_spec=RequestSpecs.authorization_headers(username=username, password="Pas!w0rd"),
            response_spec=ResponseSpecs.request_created()
        ).post(credit_request)
        credit_id = response.creditId

        # Посмотреть историю кредитов
        CreditHistoryRequester(
            request_spec=RequestSpecs.authorization_headers(username=username, password="Pas!w0rd"),
            response_spec=ResponseSpecs.request_ok()
        ).post()
