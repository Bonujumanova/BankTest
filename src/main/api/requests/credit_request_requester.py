import requests

from src.main.api.models.credit_request_request import CreditRequestRequest
from src.main.api.models.credit_request_response import CreditRequestResponse
from src.main.api.requests.requester import Requester
from requests import Response

class CreditRequestRequester(Requester):
    def post(self, credit_request: CreditRequestRequest) -> CreditRequestResponse |  Response:
        url = f"{self.base_url}/credit/request"
        response = requests.post(
            url=url,
            headers=self.headers,
            json=credit_request.model_dump()
        )
        self.response_spec(response)
        if response.status_code in (200, 201):
            return CreditRequestResponse(**response.json())
        return response
