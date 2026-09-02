import requests
from requests import Response
from src.main.api.models.get_users_list_response import GetUsersListResponse
from src.main.api.requests.requester import Requester

class GetUsersListRequester(Requester):
    # get
    def post(self, model=None) -> GetUsersListResponse | Response:
        url = f"{self.base_url}/admin/users"
        response = requests.get(
            url=url,
            headers=self.headers
        )
        print(response.json())

        # Возвращаюся данные в таком виде, поэтому нужна распаковка для проверкаи
        # [{'id': 138, 'username': 'admin', 'role': 'ROLE_ADMIN'},
        #  {'id': 139, 'username': 'Max01211', 'role': 'ROLE_USER'}]
        return GetUsersListResponse(**response.json()[0])
