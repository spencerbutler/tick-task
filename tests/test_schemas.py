"""Tests for Pydantic schemas."""

import pytest
from datetime import datetime
from pydantic import ValidationError

from tick_task.schemas import (
    TaskCreate,
    TaskUpdate,
    Task,
    TaskList,
    HealthResponse,
    ErrorResponse,
)


class TestTaskCreateSchema:
    """Test cases for TaskCreate schema."""

    def test_task_create_minimal_valid(self):
        """Test creating a task with minimal valid data."""
        data = {"title": "Test Task"}
        task = TaskCreate(**data)

        assert task.title == "Test Task"
        assert task.status == "todo"
        assert task.priority == "medium"
        assert task.context == "personal"
        assert task.description is None
        assert task.due_at is None
        assert task.tags == []
        assert task.workspace is None

    def test_task_create_full_valid(self):
        """Test creating a task with all fields."""
        due_date = datetime(2024, 12, 31, 23, 59, 59)

        data = {
            "title": "Full Task",
            "description": "Complete description",
            "status": "doing",
            "priority": "high",
            "due_at": due_date,
            "tags": ["urgent", "important"],
            "context": "professional",
            "workspace": "Project Alpha",
        }
        task = TaskCreate(**data)

        assert task.title == "Full Task"
        assert task.description == "Complete description"
        assert task.status == "doing"
        assert task.priority == "high"
        assert task.due_at == due_date
        assert task.tags == ["urgent", "important"]
        assert task.context == "professional"
        assert task.workspace == "Project Alpha"

    def test_task_create_title_validation(self):
        """Test title validation rules."""
        # Valid title
        task = TaskCreate(title="Valid Title")
        assert task.title == "Valid Title"

        # Title with whitespace (should be stripped)
        task = TaskCreate(title="  Spaced Title  ")
        assert task.title == "Spaced Title"

        # Empty title after strip
        with pytest.raises(ValidationError) as exc_info:
            TaskCreate(title="   ")
        assert "Title cannot be empty" in str(exc_info.value)

        # Completely empty title
        with pytest.raises(ValidationError):
            TaskCreate(title="")

    def test_task_create_title_length_limits(self):
        """Test title length constraints."""
        # Valid length
        task = TaskCreate(title="x" * 200)
        assert len(task.title) == 200

        # Too long title
        with pytest.raises(ValidationError):
            TaskCreate(title="x" * 201)

    def test_task_create_status_validation(self):
        """Test status enum validation."""
        valid_statuses = ["todo", "doing", "blocked", "done", "archived"]

        for status in valid_statuses:
            task = TaskCreate(title="Test", status=status)
            assert task.status == status

        # Invalid status
        with pytest.raises(ValidationError):
            TaskCreate(title="Test", status="invalid")

    def test_task_create_priority_validation(self):
        """Test priority enum validation."""
        valid_priorities = ["low", "medium", "high", "urgent"]

        for priority in valid_priorities:
            task = TaskCreate(title="Test", priority=priority)
            assert task.priority == priority

        # Invalid priority
        with pytest.raises(ValidationError):
            TaskCreate(title="Test", priority="invalid")

    def test_task_create_context_validation(self):
        """Test context enum validation."""
        valid_contexts = ["personal", "professional", "mixed"]

        for context in valid_contexts:
            task = TaskCreate(title="Test", context=context)
            assert task.context == context

        # Invalid context
        with pytest.raises(ValidationError):
            TaskCreate(title="Test", context="invalid")

    def test_task_create_tags_validation(self):
        """Test tags validation."""
        # Valid tags
        task = TaskCreate(title="Test", tags=["tag1", "tag2", "TAG3"])
        assert task.tags == ["tag1", "tag2", "tag3"]  # Should be lowercased

        # Empty tags list
        task = TaskCreate(title="Test", tags=[])
        assert task.tags == []

        # Tags with whitespace (should be stripped)
        task = TaskCreate(title="Test", tags=["  spaced  ", "  tag  "])
        assert task.tags == ["spaced", "tag"]

        # Empty tag
        with pytest.raises(ValidationError) as exc_info:
            TaskCreate(title="Test", tags=[""])
        assert "Tag cannot be empty" in str(exc_info.value)

        # Whitespace-only tag
        with pytest.raises(ValidationError) as exc_info:
            TaskCreate(title="Test", tags=["   "])
        assert "Tag cannot be empty" in str(exc_info.value)

        # Tag too long
        with pytest.raises(ValidationError) as exc_info:
            TaskCreate(title="Test", tags=["x" * 51])
        assert "Tag must be 50 characters" in str(exc_info.value)

    def test_task_create_workspace_length_limit(self):
        """Test workspace length constraints."""
        # Valid length
        task = TaskCreate(title="Test", workspace="x" * 100)
        assert len(task.workspace) == 100

        # Too long workspace
        with pytest.raises(ValidationError):
            TaskCreate(title="Test", workspace="x" * 101)


class TestTaskUpdateSchema:
    """Test cases for TaskUpdate schema."""

    def test_task_update_empty(self):
        """Test updating with no fields set."""
        update = TaskUpdate()
        assert update.title is None
        assert update.description is None
        assert update.status is None
        assert update.priority is None
        assert update.due_at is None
        assert update.tags is None
        assert update.context is None
        assert update.workspace is None

    def test_task_update_partial(self):
        """Test updating with some fields."""
        update = TaskUpdate(title="New Title", status="done")
        assert update.title == "New Title"
        assert update.status == "done"
        assert update.description is None

    def test_task_update_validation_same_as_create(self):
        """Test that TaskUpdate has same validation as TaskCreate."""
        # Title validation
        with pytest.raises(ValidationError):
            TaskUpdate(title="")

        with pytest.raises(ValidationError):
            TaskUpdate(title="   ")

        # Status validation
        with pytest.raises(ValidationError):
            TaskUpdate(status="invalid")

        # Tags validation
        with pytest.raises(ValidationError):
            TaskUpdate(tags=[""])


class TestTaskSchema:
    """Test cases for Task response schema."""

    def test_task_response_schema(self):
        """Test full task response schema."""
        task_data = {
            "id": "12345678-1234-5678-9012-123456789012",
            "title": "Response Task",
            "description": "Task description",
            "status": "doing",
            "priority": "high",
            "due_at": datetime(2024, 12, 31, 23, 59, 59),
            "tags": ["response", "test"],
            "context": "professional",
            "workspace": "Test Workspace",
            "created_at": datetime(2024, 1, 1, 12, 0, 0),
            "updated_at": datetime(2024, 1, 2, 12, 0, 0),
            "completed_at": None,
        }

        task = Task(**task_data)
        assert task.id == "12345678-1234-5678-9012-123456789012"
        assert task.title == "Response Task"
        assert task.status == "doing"
        assert task.completed_at is None

    def test_task_from_orm_compatibility(self):
        """Test that Task schema works with from_attributes=True."""
        # This tests the Config.from_attributes setting
        # which allows ORM objects to be converted to Pydantic models
        assert Task.__config__.from_attributes is True


class TestTaskListSchema:
    """Test cases for TaskList schema."""

    def test_task_list_empty(self):
        """Test empty task list."""
        task_list = TaskList(tasks=[], pagination={"has_more": False, "next_cursor": None})
        assert task_list.tasks == []
        assert task_list.pagination["has_more"] is False

    def test_task_list_with_tasks(self):
        """Test task list with tasks."""
        task_data = {
            "id": "12345678-1234-5678-9012-123456789012",
            "title": "List Task",
            "created_at": datetime(2024, 1, 1, 12, 0, 0),
            "updated_at": datetime(2024, 1, 2, 12, 0, 0),
        }

        tasks = [Task(**task_data)]
        pagination = {"has_more": True, "next_cursor": "cursor123"}

        task_list = TaskList(tasks=tasks, pagination=pagination)
        assert len(task_list.tasks) == 1
        assert task_list.tasks[0].title == "List Task"
        assert task_list.pagination["has_more"] is True


class TestHealthResponseSchema:
    """Test cases for HealthResponse schema."""

    def test_health_response(self):
        """Test health response schema."""
        response = HealthResponse(
            status="healthy",
            version="0.4.0",
            database="connected",
            timestamp=datetime(2024, 1, 1, 12, 0, 0),
        )

        assert response.status == "healthy"
        assert response.version == "0.4.0"
        assert response.database == "connected"
        assert isinstance(response.timestamp, datetime)


class TestErrorResponseSchema:
    """Test cases for ErrorResponse schema."""

    def test_error_response(self):
        """Test error response schema."""
        error_data = {"message": "Task not found", "code": 404}
        response = ErrorResponse(error=error_data)

        assert response.error["message"] == "Task not found"
        assert response.error["code"] == 404


class TestSchemaSerialization:
    """Test cases for schema JSON serialization."""

    def test_datetime_serialization(self):
        """Test that datetime fields are properly serialized to ISO format."""
        dt = datetime(2024, 12, 31, 23, 59, 59, 123456)

        task = TaskCreate(title="Test", due_at=dt)
        json_data = task.json()

        # Should contain ISO format datetime
        assert "2024-12-31T23:59:59.123456" in json_data

    def test_task_list_serialization(self):
        """Test TaskList serialization with datetime fields."""
        task_data = {
            "id": "12345678-1234-5678-9012-123456789012",
            "title": "Serialize Task",
            "created_at": datetime(2024, 1, 1, 12, 0, 0),
            "updated_at": datetime(2024, 1, 2, 12, 0, 0),
        }

        task_list = TaskList(
            tasks=[Task(**task_data)],
            pagination={"has_more": False}
        )

        json_data = task_list.json()
        # Should contain ISO format datetimes
        assert "2024-01-01T12:00:00" in json_data
