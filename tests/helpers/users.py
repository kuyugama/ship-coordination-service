import secrets

from sqlalchemy.ext.asyncio import AsyncSession

from src.models import User, Token


async def create_user(session: AsyncSession, nickname: str, password_hash: str):
    user = User(
        nickname=nickname,
        password_hash=password_hash,
    )
    session.add(user)

    await session.commit()

    return user


async def create_token(session: AsyncSession, user: User):
    token = Token(body=secrets.token_hex(16), owner=user)
    session.add(token)

    await session.commit()

    return token
