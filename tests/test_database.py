"""Tests for database configuration and connections."""

import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from tick_task.database import get_db
from tick_task.models import Base, Task


class TestDatabaseConnection:
    """Test cases for database connectivity."""

    async def test_database_connection(self, db_session):
        """Test that database connection works."""
        # Execute a simple query to test connection
        result = await db_session.execute("SELECT 1 as test")
        row = result.first()

        assert row is not None
        assert row.test == 1

    async def test_database_session_is_async_session(self, db_session):
        """Test that db_session fixture returns AsyncSession."""
        assert isinstance(db_session, AsyncSession)

    async def test_database_tables_created(self, db_session):
        """Test that database tables are created."""
        # Check if tasks table exists by trying to query it
        result = await db_session.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='tasks'"
        )
        table = result.first()

        assert table is not None
        assert table.name == "tasks"


class TestDatabaseOperations:
    """Test cases for basic database operations."""

    async def test_create_task_in_database(self, db_session):
        """Test creating a task directly in database."""
        task = Task(title="DB Test Task", status="doing")

        db_session.add(task)
        await db_session.commit()
        await db_session.refresh(task)

        assert task.id is not None
        assert task.title == "DB Test Task"
        assert task.status == "doing"

    async def test_query_task_from_database(self, db_session):
        """Test querying a task from database."""
        # Create a task
        task = Task(title="Query Test", priority="high")
        db_session.add(task)
        await db_session.commit()
        await db_session.refresh(task)

        # Query it back
        result = await db_session.get(Task, task.id)

        assert result is not None
        assert result.id == task.id
        assert result.title == "Query Test"
        assert result.priority == "high"

    async def test_update_task_in_database(self, db_session):
        """Test updating a task in database."""
        # Create task
        task = Task(title="Update Test")
        db_session.add(task)
        await db_session.commit()
        await db_session.refresh(task)

        # Update it
        task.title = "Updated Title"
        task.status = "done"
        await db_session.commit()
        await db_session.refresh(task)

        assert task.title == "Updated Title"
        assert task.status == "done"

    async def test_delete_task_from_database(self, db_session):
        """Test deleting a task from database."""
        # Create task
        task = Task(title="Delete Test")
        db_session.add(task)
        await db_session.commit()

        # Delete it
        await db_session.delete(task)
        await db_session.commit()

        # Verify it's gone
        result = await db_session.get(Task, task.id)
        assert result is None
