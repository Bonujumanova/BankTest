from src.main.api.models.login_user_request import LoginUserRequest
import requests

from src.main.api.models.login_user_response import LoginUserResponse


class RequestSpecifications:
    BASE_URL = "http://localhost:4111/api"
    @staticmethod
    def base_headers():
        return {
                "accept": "application/json",
                "Content-Type": "application/json"
            }

    @staticmethod
    def authorization_headers(username: str, password: str):
        request = LoginUserRequest(username=username, password=password)
        response = requests.post(
            url="http://localhost:41111/api/auth/token/login",
            json=request.model_dump(),
            headers=RequestSpecifications.base_headers()
        )
        if response.status_code == 200:
            response_data = LoginUserResponse(**response.json())
            token = response_data.token

            headers = RequestSpecifications.base_headers()
            headers["Authorization"] = f"Bearer {token}"
            return {
                "headers": headers,
                "base_url": RequestSpecifications.BASE_URL
            }
        raise Exception("Failed in login")



