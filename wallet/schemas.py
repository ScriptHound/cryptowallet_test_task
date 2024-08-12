from typing import Optional

from pydantic import BaseModel


class Balance(BaseModel):
    user_id: int
    wallet_id: int
    currency_name: str
    balance: float

    class Config:
        from_attributes = True


class Transaction(BaseModel):
    id: Optional[int] = None
    wallet_id_from: int
    wallet_id_to: int
    currency_id: int
    amount: float
    transaction_type: str

    class Config:
        from_attributes = True


class Currency(BaseModel):
    id: int
    name: str
    symbol: str

    class Config:
        from_attributes = True


class Wallet(BaseModel):
    id: int
    balance: float
    user_id: int
    currencies: list[Currency]
    transactions: list[Transaction]

    class Config:
        from_attributes = True

