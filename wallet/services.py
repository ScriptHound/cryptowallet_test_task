from typing import Protocol

from user.repositories import UserRepository
from wallet.repositories import WalletRepository
from wallet.schemas import Transaction, Wallet, Balance


class UserWalletServiceProtocol(Protocol):
    def __init__(self, wallet_repository: WalletRepository, user_repository: UserRepository):
        pass

    async def get_balance(self, user_id: int) -> float:
        pass

    async def send_money(self, transaction: Transaction) -> None:
        pass

    async def create_wallet(self, user_id: int) -> Wallet:
        pass


class UserWalletService(UserWalletServiceProtocol):
    def __init__(self, wallet_repository: WalletRepository, user_repository: UserRepository) -> None:
        self.wallet_repository = wallet_repository
        self.user_repository = user_repository

    async def get_balance(self, user_id: int) -> Balance:
        return await self.wallet_repository.get_balance(user_id)

    async def send_money(self, transaction: Transaction) -> None:
        await self.wallet_repository.create_transaction(transaction)

    async def create_wallet(self, user_id: int) -> Wallet:
        return await self.wallet_repository.create_wallet(user_id)
