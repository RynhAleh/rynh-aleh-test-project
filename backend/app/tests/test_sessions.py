import pytest
from app.db.sessions import get_db


@pytest.mark.asyncio
class TestSessions:
    async def test_get_db_session(self):
        generator = get_db()

        async for session in generator:
            assert session is not None

    async def test_get_db_session_cleanup(self, db_session):
        async for session in db_session:
            assert not session.closed
