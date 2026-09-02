import requests

from src.main.api.models.create_user_response import CreateUserResponse
from src.main.api.models.transactions_history_response import TransactionsHistoryResponse
from src.main.api.requests.requester import Requester
from requests import Response



class TransactionsHistoryRequester(Requester):
    # get
    def post(self, account_id: int) -> TransactionsHistoryResponse | Response:
        url = f"{self.base_url}/account/transactions/{account_id}"
        print(url)
        response = requests.get(
            url=url,
            headers=self.headers
        )
        self.response_spec(response)
        if response.status_code == 200:
            return TransactionsHistoryResponse(**response.json())
        return response
