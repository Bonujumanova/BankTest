from src.main.api.models.base_model import BaseModel

class Transactions(BaseModel):
    transactionId: int
    type: str
    amount: int
    fromAccountId: int
    createdAt: str

class TransactionsHistoryResponse(BaseModel):
    id: int
    number: str
    balance: float
    transactions: list[Transactions]


