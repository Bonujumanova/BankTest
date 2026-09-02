from src.main.api.models.create_user_request import CreateUserRequest
from src.main.api.models.delete_user_request import DeleteUserRequest
from src.main.api.requests.create_user_requester import CreateUserRequester
from src.main.api.requests.delete_user_requester import DeleteUserRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs


class TestDeleteUser:
    """ Проверяет корректность удаления одного пользователя админом"""

    def test_delete_user(self):
        # Авторизация администратора
        # Отправка Post-запроса для авторизации
        create_user_request = CreateUserRequest(username="Max1", password="Pas!sw0rd", role="ROLE_USER")
        response = CreateUserRequester(
            request_spec=RequestSpecs.authorization_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_ok()
        ).post(create_user_request)

        assert create_user_request.username == response.username
        assert create_user_request.role == response.role


        delete_user_request = DeleteUserRequest(id=response.id)
        response = DeleteUserRequester(
            request_spec=RequestSpecs.authorization_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_ok()
        ).post(delete_user_request)
        assert response.message == "User deleted successfully"
