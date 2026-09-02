from src.main.api.requests.get_users_list_requester import GetUsersListRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs


class TestGetUsersList:
    """ проверяет корректность получения списка всех пользователей """
    def test_get_users_list_valid(self):
        # Авторизация админа
        response = GetUsersListRequester(
            request_spec=RequestSpecs.authorization_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_ok()
        ).post()

        assert response.username == "admin"
        assert response.role == "ROLE_ADMIN"
