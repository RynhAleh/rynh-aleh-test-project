import asyncio

import pytest
from app.database import Base
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

# Test DB
TEST_DATABASE_URL = "postgresql+asyncpg://user:password@db:5432/test_db"


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def test_engine():
    """Engine for test DB"""
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)

    # Create a table once for all tests
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    # Cleanup after all tests
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest.fixture
async def db_session(test_engine):
    """BD session with transaction for every test"""
    async for engine in test_engine:
        connection = await engine.connect()
        transaction = await connection.begin()

        AsyncSessionLocal = async_sessionmaker(connection, expire_on_commit=False)
        session = AsyncSessionLocal()

        yield session

        # Rollback transaction after test
        await transaction.rollback()
        await connection.close()


@pytest.fixture
async def client(db_session, test_engine):
    from app.db.sessions import get_db
    from app.main import app

    async for session in db_session:
        async for engine in test_engine:
            # Redefine dependency DB for tests
            async def override_get_db():
                yield session

            app.dependency_overrides[get_db] = override_get_db

            # Clean tables before EVERY test
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.drop_all)
                await conn.run_sync(Base.metadata.create_all)

            async with AsyncClient(app=app, base_url="http://test") as test_client:
                yield test_client

            app.dependency_overrides.clear()
