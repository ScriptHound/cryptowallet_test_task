from contextlib import AbstractAsyncContextManager
from typing import Protocol, Coroutine

from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from wallet.models import TransactionModel, WalletModel, BalanceView
from wallet.schemas import Transaction, Balance, Wallet


class WalletRepositoryProtocol(Protocol):
    def __init__(self, session_factory: Coroutine[None, None, AbstractAsyncContextManager[AsyncSession]]) -> None:
        self.session_factory = session_factory

    async def get_transactions(self, user_id: int) -> list[Transaction]:
        pass

    async def get_balance(self, user_id: int, currency_id: int, wallet_id: int) -> Balance:
        pass

    async def create_wallet(self, user_id: int) -> Wallet:
        pass


class WalletRepository(WalletRepositoryProtocol):
    def __init__(self, session_factory: Coroutine[None, None, AbstractAsyncContextManager[AsyncSession]]) -> None:
        super().__init__(session_factory)

    async def create_wallet(self, user_id: int) -> Wallet:
        async with self.session_factory as session:
            async with session.begin():
                wallet = WalletModel(user_id=user_id)
                session.add(wallet)
                session.flush()
                wallet = await session.get(WalletModel, wallet.id)

        typed_wallet = Wallet.from_orm(wallet)
        return typed_wallet

    async def create_transaction(self, transaction: Transaction) -> None:
        async with self.session_factory as session:
            async with session.begin():
                session.add(TransactionModel(**transaction.dict()))

    async def get_transactions(self, user_id: int) -> list[Transaction]:
        async with self.session_factory as session:
            query = (
                select(TransactionModel)
                .join(WalletModel,
                      or_(
                          WalletModel.id == TransactionModel.wallet_id_to,
                          WalletModel.id == TransactionModel.wallet_id_from))
                .where(WalletModel.user_id == user_id)
            )
            transactions = await session.scalars(query)

        typed_transactions = [Transaction.from_orm(transaction) for transaction in transactions]
        return typed_transactions

    async def get_balance(self, user_id: int, currency_id: int, wallet_id: int) -> Balance:
        async with self.session_factory as session:
            query = select(BalanceView).where(BalanceView.user_id == user_id)
            balance = await session.scalar(query)

        typed_balance = Balance.from_orm(balance)
        return typed_balance
