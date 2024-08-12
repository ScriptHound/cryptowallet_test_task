from typing import Protocol

from auth.schemas import User
from user.repositories import UserRepository


class UserUseCaseProtocol(Protocol):
    def __init__(self, user_repository: UserRepository) -> None:
        pass

    async def create_user(self, user: User) -> None:
        pass


class UserUseCase(UserUseCaseProtocol):
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    async def create_user(self, user: User) -> None:
        await self.user_repository.create_user(user)
