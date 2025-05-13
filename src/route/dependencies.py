from fastapi import Query

from src import constants, util


async def require_offset_and_limit(
    page: int = Query(1, ge=1),
    size: int = Query(constants.misc.DEFAULT_PAGE_SIZE, ge=1, le=constants.misc.MAX_PAGE_SIZE),
):
    return util.get_offset_and_limit(page, size)
