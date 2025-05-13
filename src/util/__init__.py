import math
import typing

from src import constants
from dynaconf import Dynaconf
from . import datetime, string, fastapi, pydantic, contextmanager


settings = Dynaconf(
    envvar_prefix="DYNACONF",
    settings_files=["settings.yaml", ".secrets.yaml"],
)


def get_offset_and_limit(page: int, size: int = constants.misc.DEFAULT_PAGE_SIZE):
    return (page - 1) * size, size


def paginated_response(
    items: typing.Sequence[typing.Any],
    total: int,
    offset: int,
    limit: int,
):
    return {
        "items": items,
        "pagination": {
            "total": total,
            "page": (offset / limit) + 1,
            "pages": math.ceil(total / limit),
        },
    }
