"""
Fix PyCharm problem with type inference of return type of context managers

Usage:
::
    # Async code
    async def func():
        yield 123

    func = async_manager(func, int)

    async with func() as result:
        print(result.to_bytes())

    # Sync code
    def func():
        yield 123

    func = sync_manager(func, int)

    with func() as result:
        print(result.to_bytes())
"""

import typing
from contextlib import asynccontextmanager, contextmanager

__all__ = [
    "sync_manager",
    "async_manager",
]

T = typing.TypeVar("T")
P = typing.ParamSpec("P")


def async_manager(
    func: typing.Callable[P, typing.Any], _: type[T]
) -> typing.Callable[P, typing.AsyncContextManager[T]]:
    return asynccontextmanager(func)


def sync_manager(
    func: typing.Callable[P, typing.Any], _: type[T]
) -> typing.Callable[P, typing.ContextManager[T]]:
    return contextmanager(func)
