from src.main.api.requests.delete_all_users_requester import DeleteAllUsersRequester
from src.main.api.specs.request_specs import RequestSpecs
from src.main.api.specs.response_specs import ResponseSpecs


class TestDeleteAllUsers:
    """ Проверяет корректность удаления всех пользоветелей админом"""
    def test_delete_all_users(self):
        response = DeleteAllUsersRequester(
            request_spec=RequestSpecs.authorization_headers(username="admin", password="123456"),
            response_spec=ResponseSpecs.request_ok()
        ).post()

        assert response.message == "All users except current admin deleted successfully"
        # range(1, 100) возможное количество удаляемых элементов, эта цифра завист от числа созданных пользователей
        # число, созданных пользователей НЕ константно!!!
        assert response.deleted_count in range(0,1000)
