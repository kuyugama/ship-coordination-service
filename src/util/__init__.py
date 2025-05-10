import re
import math
import typing
from functools import lru_cache

from src import constants
from dynaconf import Dynaconf
from . import datetime, secrets, string, fastapi, pydantic, contextmanager


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


@lru_cache
def token_ttl() -> int:
    raw_ttl = settings.token.ttl.replace(" ", "")
    if re.match(r"[1-9][0-9*]+", raw_ttl) is None:
        raise RuntimeError(
            'Cannot parse token ttl expression: must match the format "[1-9][0-9*]+" where * is multiply symbol'
        )

    return eval(raw_ttl, {}, {})


def user_active_for():
    raw_active = settings.user.active_for.replace(" ", "")
    if re.match(r"[1-9][0-9*]+", raw_active) is None:
        raise RuntimeError(
            'Cannot parse user active_for expression: must match the format "[1-9][0-9*]+" where * is multiply symbol'
        )

    return eval(raw_active, {}, {})
