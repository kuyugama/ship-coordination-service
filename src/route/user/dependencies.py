from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..service import get_user
from ..errors import user_not_found
from ..dependencies import acquire_session


async def require_input_user(nickname: str, session: AsyncSession = Depends(acquire_session)):
    user = await get_user(session, nickname)
    if not user:
        raise user_not_found

    return user
