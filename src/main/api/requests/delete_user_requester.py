import requests

from src.main.api.models.delete_user_request import DeleteUserRequest
from src.main.api.models.delete_user_response import DeleteUserResponse
from src.main.api.requests.requester import Requester
from requests import Response


class DeleteUserRequester(Requester):
    def post(self, delete_user_request: DeleteUserRequest) -> DeleteUserResponse | Response:
        url = f"{self.base_url}/admin/users/{delete_user_request.id}"
        print(url)
        # delete запрос
        response = requests.delete(
            url=url,
            headers=self.headers,
            json=delete_user_request.model_dump()
        )
        self.response_spec(response)
        return DeleteUserResponse(**response.json())
