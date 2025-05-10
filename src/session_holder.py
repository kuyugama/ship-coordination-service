from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    AsyncConnection,
    async_sessionmaker,
    create_async_engine,
)

from src import util


class SessionHolder:
    def __init__(self):
        self._session_maker: async_sessionmaker | None = None
        self._engine: AsyncEngine | None = None
        self._url: str | None = None

    def init(self, url: str):
        self._url = url
        self._engine = create_async_engine(url, echo=False)
        self._session_maker = async_sessionmaker(
            autocommit=False,
            expire_on_commit=False,
            bind=self._engine,
        )

    async def close(self):
        if self._engine is None:
            raise RuntimeError("SessionHolder is not initialized")

        await self._engine.dispose()

        self._session_maker = None
        self._engine = None

    @property
    def connect(self):
        async def inner():
            if self._engine is None:
                raise RuntimeError("SessionHolder is not initialized")

            async with self._engine.begin() as connection:
                try:
                    yield connection
                except Exception:
                    await connection.rollback()
                    raise

        return util.contextmanager.async_manager(inner, AsyncConnection)

    @property
    def session(self):
        async def inner():
            if self._session_maker is None:
                raise RuntimeError("SessionHolder is not initialized")

            session = self._session_maker()

            try:
                yield session
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()

        return util.contextmanager.async_manager(inner, AsyncSession)


session_holder = SessionHolder()
