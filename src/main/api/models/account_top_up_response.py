from src.main.api.models.base_model import BaseModel


class AccountTopUpResponse(BaseModel):
    id: int
    balance: float
