import requests

from src.main.api.configs.config import Config
from src.main.api.models.login_user_requests import LoginUserRequest
from src.main.api.models.login_user_response import LoginUserResponse


class RequestSpecs:
    # Заголовки для Post-запросов
    @staticmethod
    def base_headers():
        return  {
            "accept": "application/json",
            "Content-Type": "application/json"
        }

    # Заголовки для авторизации, содержащие токен
    @staticmethod
    def authorization_headers(username: str, password: str):
        request = LoginUserRequest(username=username, password=password)
        url = "http://localhost:4111/api/auth/token/login"
        response = requests.post(
            url=url,
            json = request.model_dump(),
            headers=RequestSpecs.base_headers()
        )

        if response.status_code == 200:
            response_data = LoginUserResponse(**response.json())
            token = response_data.token
            headers = RequestSpecs.base_headers()
            headers["Authorization"] = f"Bearer {token}"
            return {
                "headers": headers,
                "base_url": Config.fetch("backendUrl")
            }
        raise Exception(f"failed to login: {response.status_code} {response.text}")

    @staticmethod
    def unauth_headers():
        return {
            "headers": RequestSpecs.base_headers(),
            "base_url": Config.fetch("backendUrl")
        }
