from abc import ABC
from contextlib import AbstractAsyncContextManager
from typing import Coroutine

from sqlalchemy.ext.asyncio import AsyncSession

from auth.models import UserModel
from auth.schemas import User


class IUserRepository(ABC):
    def __init__(self, session_factory: Coroutine[None, None, AbstractAsyncContextManager[AsyncSession]]) -> None:
        self.session_factory = session_factory

    async def get_user_by_id(self, user_id: int) -> User:
        pass

    async def create_user(self, user: User) -> None:
        pass


class UserRepository(IUserRepository):
    def __init__(self, session_factory: Coroutine[None, None, AbstractAsyncContextManager[AsyncSession]]) -> None:
        super().__init__(session_factory)

    async def get_user_by_id(self, user_id: int) -> User:
        async with self.session_factory as session:
            user = await session.get(UserModel, user_id)

        if user is None:
            raise ValueError(f"User with id {user_id} not found")

        typed_user = User.from_orm(user)
        return typed_user

    async def create_user(self, user: User) -> None:
        async with self.session_factory() as session:
            async with session.begin():
                session.add(UserModel(**user.dict()))
                session.flush()
                await session.commit()
