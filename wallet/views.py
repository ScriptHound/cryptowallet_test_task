from typing import Annotated, Optional, Dict

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, Path, Body, Header
from fastapi.responses import JSONResponse

from auth.logic import get_current_active_user
from auth.schemas import User
from container import Container
from wallet.schemas import Transaction, Wallet, Currency
from wallet.services import UserWalletService, CurrencyService

router = APIRouter()


@router.get("/wallets")
@inject
async def get_all_wallets(
    current_user: Annotated[User, Depends(get_current_active_user)],
    wallet_usecase: UserWalletService = Depends(Provide(Container.wallet_usecase)),
):
    wallets = await wallet_usecase.get_all_wallets(current_user.id)
    return wallets


@router.post("/")
@inject
async def create_wallet(
    current_user: Annotated[User, Depends(get_current_active_user)],
    wallet_usecase: UserWalletService = Depends(Provide(Container.wallet_usecase)),
    currency_service: CurrencyService = Depends(Provide(Container.currency_service)),
    currencies: list[str] = Body(...),
) -> Wallet:
    currencies = await currency_service.get_currencies(currencies)
    wallet = await wallet_usecase.create_wallet(current_user.id, currencies)
    return wallet


@router.post("/deposit")
@inject
async def deposit_money(
    current_user: Annotated[User, Depends(get_current_active_user)],
    transaction: Transaction = Body(...),
    wallet_id_to: int = Body(...),
    wallet_usecase: UserWalletService = Depends(Provide(Container.wallet_usecase)),
):
    transaction_in = Transaction(
        wallet_id=wallet_id_to,
        currency_id=transaction.currency_id,
        amount=transaction.amount,
        outgoing=False,
    )
    await wallet_usecase.send_money(transaction_in, transaction)
    return JSONResponse({"message": "Money deposited successfully"})


@router.post("/balance")
@inject
async def get_balance(
    current_user: Annotated[User, Depends(get_current_active_user)],
    wallet_usecase: UserWalletService = Depends(Provide(Container.wallet_usecase)),
    currency_id: int = Body(...),
):
    balance = await wallet_usecase.get_balance(current_user.id, currency_id)
    return balance
