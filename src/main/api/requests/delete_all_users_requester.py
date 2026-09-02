import requests
from src.main.api.models.delete_all_users_response import DeleteAllUsersResponse
from src.main.api.requests.requester import Requester
from requests import Response

class DeleteAllUsersRequester(Requester):
    # delete
    # тк нет тела запросы, указывается пустая модель
    def post(self, model=None) -> DeleteAllUsersResponse | Response:
        url = f"{self.base_url}/admin/users"
        # Отправка delete запроса
        response = requests.delete(url=url, headers=self.headers)
        self.response_spec(response)
        return DeleteAllUsersResponse(**response.json())
