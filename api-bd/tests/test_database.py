import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

@pytest.mark.asyncio
async def test_engine_is_async():
    from database import engine
    assert isinstance(engine, AsyncEngine)

@pytest.mark.asyncio
async def test_session_is_async():
    from database import SessionLocal
    async with SessionLocal() as session:
        assert isinstance(session, AsyncSession)
