from src.main.api.models.base_model import BaseModel

class LoginUserResponse:
    id: int
    username: str
    password: str
    role: str