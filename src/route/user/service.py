from sqlalchemy import Select, select, func, ScalarResult
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import User


def filter_users_list(query: Select) -> Select:
    return query


def options_users_list(query: Select) -> Select:
    return query


async def count_users(session: AsyncSession) -> int:
    return await session.scalar(filter_users_list(select(func.count(User.id))))


async def list_users(session: AsyncSession, offset: int, limit: int) -> ScalarResult[User]:
    return await session.scalars(
        options_users_list(filter_users_list(select(User).offset(offset).limit(limit)))
    )
