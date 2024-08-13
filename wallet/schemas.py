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
    id: Optional[int] = None
    name: str
    symbol: str

    class Config:
        from_attributes = True


class Wallet(BaseModel):
    id: Optional[int] = None
    balance: float
    user_id: int
    currencies: list[Currency]
    transactions: Optional[list[Transaction]] = None

    class Config:
        from_attributes = True
