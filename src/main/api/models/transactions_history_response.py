from src.main.api.models.base_model import BaseModel


class TransactionsHistoryResponse(BaseModel):
    id: int
    number: str
    balance: float
    transactions: list[Transactions]

class Transactions(BaseModel):
    transactionId: int
    type: str
    amount: int
    fromAccountId: int
    createdAt: str
