from src.main.api.models.base_model import BaseModel

class GetUsersListResponse(BaseModel):
    id: int
    username: str
    role: str
