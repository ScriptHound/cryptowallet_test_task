from contextlib import AbstractAsyncContextManager
from typing import Protocol, Coroutine

from auth.models import UserModel
from auth.schemas import User


class UserRepositoryProtocol(Protocol):
    def __init__(self, session_factory: Coroutine[..., AbstractAsyncContextManager[AsyncSession]]) -> None:
        self.session_factory = session_factory

    async def create_user(self, user: User) -> None:
        async with self.session_factory as session:
            async with session.begin():
                session.add(UserModel(**user.dict()))
                session.flush()
