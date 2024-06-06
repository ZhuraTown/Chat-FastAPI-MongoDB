import asyncio

import pytest
from faker import Faker
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from users.tests.config import settings
from users.infrastructure.db.models.users import User

pytest_plugins = [
    "users.tests.infrastructure.fixtures.fixture_user",
]


def get_database_url():

    if settings.infrastructure.db_user and settings.infrastructure.db_password:
        return "mongodb://{}:{}@{}:{}/{}".format(
            *[
                settings.infrastructure.db_user,
                settings.infrastructure.db_password,
                settings.infrastructure.db_host,
                settings.infrastructure.db_port,
                settings.infrastructure.db_name,
            ],
        )

    return "mongodb://{}:{}/{}".format(
            *[
                settings.infrastructure.db_host,
                settings.infrastructure.db_port,
                settings.infrastructure.db_name,
            ],
        )


@pytest.fixture(scope="session", autouse=True)
async def init_db():
    client = AsyncIOMotorClient(get_database_url())
    client.get_io_loop = asyncio.get_event_loop
    db_name = client.chat_test
    await init_beanie(database=db_name, document_models=[User])
    yield client
    await client.drop_database(db_name)


@pytest.fixture()
def faker():
    return Faker("ru_RU")


@pytest.fixture(scope="session")
def event_loop():
    """
    Creates an instance of the default event loop for the test session.
    """
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


def pytest_sessionfinish(session, exitstatus):
    asyncio.get_event_loop().close()
