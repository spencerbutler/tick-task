"""Pytest configuration and fixtures for FIN-tasks tests."""

"""Pytest configuration and fixtures for FIN-tasks tests."""

import asyncio
import os
from typing import AsyncGenerator, Generator

import pytest
import pytest_asyncio
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from fin_tasks.config import settings
from fin_tasks.database import get_db
from fin_tasks.models import Base
from fin_tasks.main import app
from fin_tasks.models import Task


@pytest_asyncio.fixture(scope="session")
async def test_engine():
    """Create test database engine with in-memory SQLite."""
    # Use in-memory SQLite for tests
    database_url = "sqlite+aiosqlite:///:memory:"

    # Create async engine
    engine = create_async_engine(
        database_url,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    # Cleanup
    await engine.dispose()


@pytest_asyncio.fixture
async def db_session(test_engine) -> AsyncGenerator[AsyncSession, None]:
    """Create database session for tests."""
    # Create session
    async_session = sessionmaker(
        test_engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session() as session:
        # Clear any existing data
        await session.execute("DELETE FROM tasks")

        yield session

        # Rollback any uncommitted changes
        await session.rollback()


@pytest.fixture
def client(db_session) -> Generator[TestClient, None, None]:
    """Create FastAPI test client with database session."""

    def override_get_db():
        yield db_session

    # Override the database dependency
    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    # Clear overrides
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def sample_task(db_session) -> Task:
    """Create a sample task for testing."""
    task = Task(
        title="Sample Task",
        description="A test task",
        status="todo",
        priority="medium",
        context="personal",
        tags=["test", "sample"],
    )

    db_session.add(task)
    await db_session.commit()
    await db_session.refresh(task)

    return task


@pytest_asyncio.fixture
async def completed_task(db_session) -> Task:
    """Create a completed task for testing."""
    from datetime import datetime

    task = Task(
        title="Completed Task",
        description="A completed test task",
        status="done",
        priority="high",
        context="professional",
        tags=["completed", "test"],
        completed_at=datetime.utcnow(),
    )

    db_session.add(task)
    await db_session.commit()
    await db_session.refresh(task)

    return task


@pytest_asyncio.fixture
async def archived_task(db_session) -> Task:
    """Create an archived task for testing."""
    task = Task(
        title="Archived Task",
        description="An archived test task",
        status="archived",
        priority="low",
        context="personal",
    )

    db_session.add(task)
    await db_session.commit()
    await db_session.refresh(task)

    return task
