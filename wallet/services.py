from abc import ABC
from typing import List

from user.repositories import UserRepository
from wallet.repositories import IWalletRepository, CurrencyRepository, WalletRepository
from wallet.schemas import Transaction, Wallet, Balance, Currency


class IUserWalletService(ABC):
    def __init__(self, wallet_repository: WalletRepository, user_repository: UserRepository):
        pass

    async def get_balance(self, user_id: int, currency_id: int) -> Balance:
        pass

    async def send_money(self, transaction_in: Transaction, transaction_out: Transaction) -> None:
        pass

    async def create_wallet(self, user_id: int, currencies: list[Currency]) -> Wallet:
        pass


class UserWalletService(IUserWalletService):
    def __init__(
        self,
        wallet_repository: WalletRepository,
        user_repository: UserRepository,
    ) -> None:
        super().__init__(wallet_repository, user_repository)
        self.wallet_repository = wallet_repository
        self.user_repository = user_repository

    async def get_balance(self, user_id: int, currency_id: int) -> Balance:
        wallet = (await self.wallet_repository.get_all_wallets(user_id))[0]
        return await self.wallet_repository.get_balance(user_id, currency_id, wallet.id)

    async def send_money(self, transaction_in: Transaction, transaction_out: Transaction) -> None:
        await self.wallet_repository.create_transaction(transaction_in)
        await self.wallet_repository.create_transaction(transaction_out)

    async def create_wallet(self, user_id: int, currencies: list[Currency]) -> Wallet:
        return await self.wallet_repository.create_wallet(user_id, currencies)

    async def get_all_wallets(self, user_id: int) -> list[Wallet]:
        return await self.wallet_repository.get_all_wallets(user_id)


class ICurrencyService(ABC):
    def __init__(self, currency_repository: CurrencyRepository):
        pass

    async def get_currency(self, currency_name: str) -> Currency:
        pass

    async def create_currency(self, currency: Currency) -> None:
        pass


class CurrencyService(ICurrencyService):
    def __init__(self, currency_repository: CurrencyRepository) -> None:
        self.currency_repository = currency_repository

    async def get_currency(self, currency_name: str) -> Currency:
        return await self.currency_repository.get_currency(currency_name)

    async def get_currencies(self, currencies_names: List[str]) -> list[Currency]:
        return await self.currency_repository.get_currencies(currencies_names)

    async def create_currency(self, currency: Currency) -> None:
        await self.currency_repository.create_currency(currency)
