from src.main.api.models.base_model import BaseModel


class CreditHistoryResponse(BaseModel):
    userId: int
    credits: list[CreditInfo]

class CreditInfo(BaseModel):
    creditId: int
    accountId: int
    amount: int
    termMonths: int
    balance: int
    createdAt: str
