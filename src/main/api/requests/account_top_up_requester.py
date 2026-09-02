from http import HTTPStatus

import requests

from src.main.api.models.account_to_up_request import AccountTopUpRequest
from src.main.api.models.account_top_up_response import AccountTopUpResponse
from src.main.api.requests.requester import Requester
from requests import Response


class AccountTopUpRequester(Requester):
    def post(self, account_top_up_request: AccountTopUpRequest) -> AccountTopUpResponse | Response:
        url = f"{self.base_url}/account/deposit"
        # post-request
        print("ACCOUNT TOP UP REQUEST INFO(json):", account_top_up_request.model_dump())#(by_alias=True))
        response = requests.post(
            url=url,
            json=account_top_up_request.model_dump(),
            headers=self.headers
        )
        self.response_spec(response)
        if response.status_code in (HTTPStatus.OK, HTTPStatus.CREATED):
            return AccountTopUpResponse(**response.json())
        return response
