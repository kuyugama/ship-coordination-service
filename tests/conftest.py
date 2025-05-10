import uuid
import pytest
import asyncio
from src import util
from src import make_app
from tests import helpers
from contextlib import ExitStack
from src.models.base import Base
from src.models import User, Token
from pytest_postgresql import factories
from async_asgi_testclient import TestClient
from sqlalchemy import make_url, URL, delete
from src.session_holder import session_holder
from sqlalchemy.ext.asyncio import AsyncSession
from pytest_postgresql.janitor import DatabaseJanitor


test_db = factories.postgresql_proc()


@pytest.fixture(autouse=True)
def _app():
    with ExitStack():
        yield make_app(test_mode=True)


@pytest.fixture
async def client(_app):
    async with TestClient(_app) as client:
        yield client


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


# noinspection PyShadowingNames
@pytest.fixture(scope="session", autouse=True)
async def _connection(test_db, event_loop):
    settings = util.settings

    origin_url = make_url(settings.sqlalchemy.url)

    url = URL.create(
        drivername=origin_url.drivername,
        username=origin_url.username,
        password=origin_url.password,
        host=origin_url.host,
        port=origin_url.port,
        database=uuid.uuid4().hex,
    )

    with DatabaseJanitor(
        user=url.username,
        host=url.host,
        port=url.port,
        dbname=url.database,
        version=test_db.version,
        password=url.password,
    ):
        session_holder.init(url)
        yield
        await session_holder.close()


@pytest.fixture(autouse=True, scope="session")
async def _create_tables():
    async with session_holder.connect() as connection:
        await connection.run_sync(Base.metadata.create_all)


@pytest.fixture(autouse=True, scope="function")
async def _cleanup(_connection):
    yield
    # noinspection PyTestUnpassedFixture
    async with session_holder.session() as session_:
        for table in reversed(Base.metadata.sorted_tables):
            await session_.execute(delete(table))

        await session_.commit()


@pytest.fixture
async def session(_connection) -> AsyncSession:
    async with session_holder.session() as session:
        yield session  # type: ignore


@pytest.fixture(scope="session")
def password() -> str:
    return "super secret"


@pytest.fixture(scope="session", autouse=True)
def hash_password(password):
    return util.secrets.make(password)


@pytest.fixture(scope="session")
def nickname_dummy() -> str:
    return "dummy user"


@pytest.fixture
def timer() -> helpers.timer.DebugBreakpointTimer:  # noqa
    """
    Used to test for slowness of application

    Usage:
    ::
        def test_something(debug_timer):
            with debug_timer.timeit("fibonacci") as timer:
                fib = fibonacci(1024)

            with debug_timer.timeit("sleep") as timer:
                time.sleep(1)

            assert timer.took < 1.01

            # To see timer results in teardown output
            assert debug_timer.echo
    """

    timer = helpers.timer.DebugBreakpointTimer()

    try:
        with timer.timeit("test"):
            yield timer  # noqa
    finally:
        print()
        print("--------------------------- TEST TIMER ".ljust(80, "-"))
        print()
        timer.print()
        print()
        print("--------------------------- TEST TIMER ".ljust(80, "-"))
        print()


@pytest.fixture
async def user(session, nickname_dummy, hash_password) -> User:
    return await helpers.users.create_user(session, nickname_dummy, hash_password)


@pytest.fixture
async def token(session, user) -> Token:
    return await helpers.users.create_token(session, user)
