from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src import schema, util
from src.models import User
from . import service
from .dependencies import require_input_user
from ..dependencies import require_user, require_offset_and_limit, acquire_session

router = APIRouter(prefix="/user")


@router.get(
    "/me", summary="Get own profile", response_model=schema.User, operation_id="user.get_me"
)
async def get_me(user: User = Depends(require_user)):
    return user


@router.get(
    "/{nickname}",
    summary="Get user's profile",
    response_model=schema.User,
    operation_id="user.get_user",
)
async def get_user(user: User = Depends(require_input_user)):
    return user


@router.get(
    "/",
    summary="List users",
    response_model=schema.Paginated[schema.User],
    operation_id="user.list_users",
)
async def list_users(
    pagination: tuple[int, int] = Depends(require_offset_and_limit),
    session: AsyncSession = Depends(acquire_session),
):
    offset, limit = pagination

    total = await service.count_users(session)
    items = await service.list_users(session, offset, limit)

    return util.paginated_response(
        items.all(),
        total,
        offset,
        limit,
    )
