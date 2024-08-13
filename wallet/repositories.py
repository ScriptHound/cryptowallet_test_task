from abc import ABC
from contextlib import AbstractAsyncContextManager
from typing import Protocol, Coroutine, List

from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from wallet.models import TransactionModel, WalletModel, BalanceView, CurrencyModel, WalletCurrencyModel
from wallet.schemas import Transaction, Balance, Wallet, Currency


class IWalletRepository(ABC):
    def __init__(self, session_factory: Coroutine[None, None, AbstractAsyncContextManager[AsyncSession]]) -> None:
        self.session_factory = session_factory

    async def get_transactions(self, user_id: int) -> list[Transaction]:
        pass

    async def get_balance(self, user_id: int, currency_id: int, wallet_id: int) -> Balance:
        pass

    async def create_wallet(self, user_id: int, currencies: list[Currency]) -> Wallet:
        pass


class WalletRepository(IWalletRepository):
    def __init__(self, session_factory: Coroutine[None, None, AbstractAsyncContextManager[AsyncSession]]) -> None:
        super().__init__(session_factory)

    async def create_wallet(self, user_id: int, currencies: list[Currency]) -> Wallet:
        wallet = WalletModel(
            user_id=user_id,
            balance=0
        )


        async with self.session_factory() as session:
            session.add(wallet)
            await session.commit()
            await session.refresh(wallet)

        async with self.session_factory() as session:
            wallet_currencies = []
            for currency in currencies:
                wallet_currency = WalletCurrencyModel(
                    wallet_id=wallet.id,
                    currency_id=currency.id,
                )
                wallet_currencies.append(wallet_currency)
            session.add_all(wallet_currencies)
            await session.commit()

        async with self.session_factory() as session:
            walley_query = (
                select(WalletModel)
                .where(WalletModel.id == wallet.id)
                .options(
                    joinedload(WalletModel.currencies),
                    joinedload(WalletModel.transactions),
                )
            )
            wallet = await session.scalar(walley_query)
            typed_wallet = Wallet.from_orm(wallet)
            await session.commit()
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


class ICurrencyRepository(ABC):
    def __init__(self, session_factory: Coroutine[None, None, AbstractAsyncContextManager[AsyncSession]]) -> None:
        self.session_factory = session_factory

    async def get_currency(self, currency_name: str) -> Currency:
        pass

    async def create_currency(self, currency: Currency) -> None:
        pass

    async def get_currencies(self, currencies_names: List[str]) -> list[Currency]:
        pass


class CurrencyRepository(ICurrencyRepository):
    def __init__(self, session_factory: Coroutine[None, None, AbstractAsyncContextManager[AsyncSession]]) -> None:
        super().__init__(session_factory)

    async def get_currency(self, currency_name: str) -> Currency:
        async with self.session_factory as session:
            query = select(CurrencyModel).where(CurrencyModel.name == currency_name)
            currency = await session.scalar(query)

        typed_currency = Currency.from_orm(currency)
        return typed_currency

    async def get_currencies(self, currencies_names: List[str]) -> list[Currency]:
        async with self.session_factory() as session:
            query = select(CurrencyModel).where(CurrencyModel.name.in_(currencies_names))
            currencies = (await session.scalars(query)).all()

        typed_currencies = [Currency.from_orm(currency) for currency in currencies]
        return typed_currencies

    async def create_currency(self, currency: Currency) -> None:
        async with self.session_factory as session:
            async with session.begin():
                session.add(CurrencyModel(**currency.dict()))
                session.flush()
                await session.commit()
