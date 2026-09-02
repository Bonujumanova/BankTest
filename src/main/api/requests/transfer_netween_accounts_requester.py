import requests
from requests import Response
from src.main.api.models.transfer_between_accounts_request import TransferBetweenAccountsRequest
from src.main.api.models.transfer_between_accounts_response import TransferBetweenAccountsResponse
from src.main.api.requests.requester import Requester



class TransferBetweenAccountsRequester(Requester):
    def post(self, transfer_between_accounts_request:
    TransferBetweenAccountsRequest) -> TransferBetweenAccountsResponse | Response:
        url = f"{self.base_url}/account/transfer"
        response = requests.post(
            url=url,
            json=transfer_between_accounts_request.model_dump(),
            headers=self.headers
        )
        self.response_spec(response)
        if response.status_code in (200, 201):
            return TransferBetweenAccountsResponse(**response.json())
        return response
