from src.main.api.models.base_model import BaseModel


class TransferBetweenAccountsResponse(BaseModel):
    fromAccountIdBalance: int
    toAccountId: int
    fromAccountIdBalance: float
