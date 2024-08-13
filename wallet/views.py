from typing import Annotated

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, Path, Body
from fastapi.responses import JSONResponse

from auth.logic import get_current_active_user
from auth.schemas import User
from wallet.containers import WalletContainer
from wallet.schemas import Transaction, Wallet
from wallet.services import UserWalletService

router = APIRouter()


@router.get("/wallets")
@inject
async def get_all_wallets(
    current_user: Annotated[User, Depends(get_current_active_user)],
    wallet_usecase: UserWalletService = Depends(Provide(WalletContainer.wallet_usecase))
):
    wallets = await wallet_usecase.get_all_wallets(current_user.id)
    return wallets


@router.post("/")
@inject
async def create_wallet(
    current_user: Annotated[User, Depends(get_current_active_user)],
    wallet_usecase: UserWalletService = Depends(Provide(WalletContainer.wallet_usecase))
) -> Wallet:
    wallet = await wallet_usecase.create_wallet(current_user.id)
    return wallet


@router.post("/deposit")
@inject
async def deposit_money(
    current_user: Annotated[User, Depends(get_current_active_user)],
    transaction: Transaction = Body(...),
    wallet_usecase: UserWalletService = Depends(Provide(WalletContainer.wallet_usecase)),
):
    await wallet_usecase.send_money(transaction)
    return JSONResponse({"message": "Money deposited successfully"})
