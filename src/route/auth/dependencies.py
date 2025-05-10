from src import util
from . import errors
from src.models import User
from fastapi.params import Depends
from ..errors import user_not_found
from src.route.service import get_user
from ..dependencies import acquire_session
from .schema import SigninSchema, SignupSchema
from sqlalchemy.ext.asyncio import AsyncSession


@util.fastapi.api_errors(errors.already_exists)
async def validate_signup_schema(
    body: SignupSchema,
    session: AsyncSession = Depends(acquire_session),
) -> SignupSchema:
    user = await get_user(session, body.nickname)

    if user is not None:
        raise errors.already_exists

    return body


@util.fastapi.api_errors(errors.invalid_password, user_not_found)
async def validate_signin_schema(
    body: SigninSchema,
    session: AsyncSession = Depends(acquire_session),
) -> User:
    user = await get_user(session, body.nickname)

    if user is None:
        raise user_not_found

    if not util.secrets.verify(body.password, user.password_hash):
        raise errors.invalid_password

    return user
