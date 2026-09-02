from src.main.api.models.base_model import BaseModel
from pydantic import Field


class AccountTopUpRequest(BaseModel):
    accountId: int #= Field(alias="accountId")
    amount: float
