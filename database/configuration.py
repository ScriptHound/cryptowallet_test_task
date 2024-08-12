from contextlib import asynccontextmanager, AbstractAsyncContextManager
from logging import getLogger
from typing import Coroutine

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base, scoped_session

from config import Config

logger = getLogger('database_logger')

DATABASE_URL = Config.SQLALCHEMY_DATABASE_URL

Base = declarative_base()


class Database:

    def __init__(self) -> None:
        self._engine = create_async_engine(DATABASE_URL, echo=True)
        self._session_factory = scoped_session(
            async_sessionmaker(
                autocommit=False,
                autoflush=False,
                bind=self._engine,
            ),
        )

    @asynccontextmanager
    async def session(self) -> Coroutine[None, None, AbstractAsyncContextManager[AsyncSession]]:
        session: AsyncSession = self._session_factory()
        try:
            yield session
        except Exception:
            logger.exception("Session rollback because of exception")
            await session.rollback()
            raise
        finally:
            await session.close()
