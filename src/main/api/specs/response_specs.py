from requests import Response
from http import HTTPStatus

class ResponseSpecs:
    @staticmethod
    def request_ok():
        def confirm(response: Response):
            print("RESPONSE_STATUS_CODE:  ", response.status_code)
            assert response.status_code == HTTPStatus.OK, response.text
        return confirm

    @staticmethod
    def request_created():
        def confirm(response: Response):
            print("RESPONSE_STATUS_CODE:  ", response.status_code)
            assert response.status_code == HTTPStatus.CREATED, response.text
        return confirm

    @staticmethod
    def request_bad():
        def confirm(response: Response):
            assert response.status_code == HTTPStatus.BAD_REQUEST, response.text
        return confirm

    @staticmethod
    def request_maximum_number_accounts_409():
        def confirm(response: Response):
            assert response.status_code == 409, response.text
        return confirm

    @staticmethod
    def request_unauthorized():
        def confirm(response: Response):
            assert response.status_code == HTTPStatus.UNAUTHORIZED, response.text
        return confirm

    @staticmethod
    def request_bad_401():
        def confirm(response: Response):
            assert response.status_code == 401, response.status_code
        return confirm

    #Уже есть активный кредит на этот или другой счет / Нет прав взять кредит
    @staticmethod
    def request_bad_403():
        def confirm(response: Response):
            assert response.status_code == 403, response.status_code
        return confirm

    # Сумма превышает остаток долга / Суммы недостаточно / Недостаточно средств
    @staticmethod
    def request_bad_422():
        def confirm(response: Response):
            assert response.status_code == 422, response.status_code
        return confirm

    @staticmethod
    def request_bad_404():
        def confirm(response: Response):
            assert response.status_code == 404, response.status_code
        return confirm