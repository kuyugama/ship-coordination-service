import hashlib
import secrets
from src import util
from src.models import User, Token
from src.route.auth.schema import SignupSchema
from sqlalchemy.ext.asyncio import AsyncSession


async def create_user(session: AsyncSession, body: SignupSchema) -> User:
    user = User(
        nickname=body.nickname,
        password_hash=util.secrets.make(body.password),
    )

    session.add(user)
    await session.commit()

    return user


async def create_token(session: AsyncSession, user: User) -> Token:
    now = util.datetime.now()
    user.login_at = now
    user.active_at = now

    user_hash = hashlib.sha256(user.nickname.encode()).hexdigest()

    token = Token(
        body=user_hash[16:] + secrets.token_hex(32) + user_hash[-16:],
        owner=user,
        created_at=now,
    )

    session.add(token)
    await session.commit()

    return token
