import requests
from requests import Response
from src.main.api.models.credit_history_response import CreditHistoryResponse
from src.main.api.requests.requester import Requester


class CreditHistoryRequester(Requester):
    # get-request!!!!
    def post(self, model=None) -> CreditHistoryResponse | Response:
        url = f"{self.base_url}/credit/history"
        print("url: ", url)
        response = requests.get(
            url=url,
            headers=self.headers
        )
        self.response_spec(response)
        print(response.text)
        if response.status_code in (200, 201):
            return CreditHistoryResponse(**response.json())
        return response
