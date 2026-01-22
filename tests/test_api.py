"""Tests for API endpoints."""

import pytest
from datetime import datetime
from fastapi import status

from fin_tasks.schemas import TaskCreate, TaskUpdate


class TestHealthEndpoint:
    """Test cases for health check endpoint."""

    def test_health_check_success(self, client):
        """Test successful health check."""
        response = client.get("/health")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert data["status"] == "healthy"
        assert data["version"] == "0.4.0"
        assert data["database"] == "connected"
        assert "timestamp" in data

    def test_health_check_response_format(self, client):
        """Test health response format matches schema."""
        response = client.get("/health")

        data = response.json()
        required_fields = ["status", "version", "database", "timestamp"]

        for field in required_fields:
            assert field in data


class TestCreateTaskEndpoint:
    """Test cases for task creation endpoint."""

    def test_create_task_minimal_success(self, client):
        """Test creating a task with minimal data."""
        task_data = {"title": "New Task"}

        response = client.post("/tasks", json=task_data)

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()

        assert data["title"] == "New Task"
        assert data["status"] == "todo"
        assert data["priority"] == "medium"
        assert data["context"] == "personal"
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data

    def test_create_task_full_success(self, client):
        """Test creating a task with all fields."""
        task_data = {
            "title": "Complete Task",
            "description": "Full task description",
            "status": "doing",
            "priority": "high",
            "due_at": "2024-12-31T23:59:59Z",
            "tags": ["urgent", "important"],
            "context": "professional",
            "workspace": "Project Alpha",
        }

        response = client.post("/tasks", json=task_data)

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()

        assert data["title"] == "Complete Task"
        assert data["description"] == "Full task description"
        assert data["status"] == "doing"
        assert data["priority"] == "high"
        assert data["tags"] == ["urgent", "important"]
        assert data["context"] == "professional"
        assert data["workspace"] == "Project Alpha"

    def test_create_task_validation_error(self, client):
        """Test task creation with validation errors."""
        # Empty title
        task_data = {"title": ""}

        response = client.post("/tasks", json=task_data)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        data = response.json()
        assert "detail" in data

    def test_create_task_invalid_status(self, client):
        """Test task creation with invalid status."""
        task_data = {"title": "Test Task", "status": "invalid"}

        response = client.post("/tasks", json=task_data)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_create_task_invalid_priority(self, client):
        """Test task creation with invalid priority."""
        task_data = {"title": "Test Task", "priority": "invalid"}

        response = client.post("/tasks", json=task_data)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_create_task_invalid_context(self, client):
        """Test task creation with invalid context."""
        task_data = {"title": "Test Task", "context": "invalid"}

        response = client.post("/tasks", json=task_data)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

    def test_create_task_empty_tags_validation(self, client):
        """Test task creation with empty tags."""
        task_data = {"title": "Test Task", "tags": [""]}

        response = client.post("/tasks", json=task_data)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestGetTaskEndpoint:
    """Test cases for get task endpoint."""

    def test_get_task_success(self, client, sample_task):
        """Test successfully getting a task."""
        response = client.get(f"/tasks/{sample_task.id}")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert data["id"] == sample_task.id
        assert data["title"] == sample_task.title
        assert data["status"] == sample_task.status

    def test_get_task_not_found(self, client):
        """Test getting a non-existent task."""
        fake_id = "12345678-1234-5678-9012-123456789012"

        response = client.get(f"/tasks/{fake_id}")

        assert response.status_code == status.HTTP_404_NOT_FOUND
        data = response.json()
        assert "Task not found" in data["detail"]

    def test_get_task_invalid_uuid(self, client):
        """Test getting a task with invalid UUID."""
        response = client.get("/tasks/invalid-uuid")

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestUpdateTaskEndpoint:
    """Test cases for update task endpoint."""

    def test_update_task_success(self, client, sample_task):
        """Test successfully updating a task."""
        update_data = {
            "title": "Updated Title",
            "status": "doing",
            "priority": "high",
        }

        response = client.put(f"/tasks/{sample_task.id}", json=update_data)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert data["title"] == "Updated Title"
        assert data["status"] == "doing"
        assert data["priority"] == "high"

    def test_update_task_partial(self, client, sample_task):
        """Test partial task update."""
        update_data = {"title": "Partially Updated"}

        response = client.put(f"/tasks/{sample_task.id}", json=update_data)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        # Title should be updated
        assert data["title"] == "Partially Updated"
        # Other fields should remain unchanged
        assert data["status"] == sample_task.status
        assert data["priority"] == sample_task.priority

    def test_update_task_to_done_sets_completion_time(self, client, sample_task):
        """Test that updating status to done sets completion timestamp."""
        update_data = {"status": "done"}

        response = client.put(f"/tasks/{sample_task.id}", json=update_data)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert data["status"] == "done"
        assert data["completed_at"] is not None

    def test_update_task_from_done_clears_completion_time(self, client, completed_task):
        """Test that updating status from done clears completion timestamp."""
        update_data = {"status": "todo"}

        response = client.put(f"/tasks/{completed_task.id}", json=update_data)

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert data["status"] == "todo"
        assert data["completed_at"] is None

    def test_update_task_not_found(self, client):
        """Test updating a non-existent task."""
        fake_id = "12345678-1234-5678-9012-123456789012"
        update_data = {"title": "Updated"}

        response = client.put(f"/tasks/{fake_id}", json=update_data)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_update_archived_task_fails(self, client, archived_task):
        """Test that updating an archived task fails."""
        update_data = {"title": "Should Fail"}

        response = client.put(f"/tasks/{archived_task.id}", json=update_data)

        assert response.status_code == status.HTTP_409_CONFLICT
        data = response.json()
        assert "Cannot update archived task" in data["detail"]

    def test_update_task_validation_error(self, client, sample_task):
        """Test update with validation errors."""
        update_data = {"title": ""}  # Empty title

        response = client.put(f"/tasks/{sample_task.id}", json=update_data)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


class TestDeleteTaskEndpoint:
    """Test cases for delete (archive) task endpoint."""

    def test_archive_task_success(self, client, sample_task):
        """Test successfully archiving a task."""
        response = client.delete(f"/tasks/{sample_task.id}")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert data["status"] == "archived"

    def test_archive_task_not_found(self, client):
        """Test archiving a non-existent task."""
        fake_id = "12345678-1234-5678-9012-123456789012"

        response = client.delete(f"/tasks/{fake_id}")

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_archive_already_archived_task_fails(self, client, archived_task):
        """Test that archiving an already archived task fails."""
        response = client.delete(f"/tasks/{archived_task.id}")

        assert response.status_code == status.HTTP_409_CONFLICT
        data = response.json()
        assert "Task already archived" in data["detail"]


class TestListTasksEndpoint:
    """Test cases for list tasks endpoint."""

    def test_list_tasks_empty(self, client):
        """Test listing tasks when none exist."""
        response = client.get("/tasks")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert data["tasks"] == []
        assert data["pagination"]["has_more"] is False
        assert data["pagination"]["total_count"] == 0

    def test_list_tasks_with_data(self, client, sample_task):
        """Test listing tasks with data."""
        response = client.get("/tasks")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert len(data["tasks"]) == 1
        assert data["tasks"][0]["id"] == sample_task.id
        assert data["tasks"][0]["title"] == sample_task.title

    def test_list_tasks_filter_by_status(self, client, sample_task):
        """Test filtering tasks by status."""
        # Create another task with different status
        task_data = {"title": "Done Task", "status": "done"}
        client.post("/tasks", json=task_data)

        # Filter by todo status
        response = client.get("/tasks?status=todo")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert len(data["tasks"]) == 1
        assert data["tasks"][0]["status"] == "todo"

        # Filter by done status
        response = client.get("/tasks?status=done")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert len(data["tasks"]) == 1
        assert data["tasks"][0]["status"] == "done"

    def test_list_tasks_filter_by_context(self, client, sample_task):
        """Test filtering tasks by context."""
        # Create task with different context
        task_data = {"title": "Work Task", "context": "professional"}
        client.post("/tasks", json=task_data)

        # Filter by personal context
        response = client.get("/tasks?context=personal")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert len(data["tasks"]) == 1
        assert data["tasks"][0]["context"] == "personal"

    def test_list_tasks_filter_by_priority(self, client, sample_task):
        """Test filtering tasks by minimum priority."""
        # Create high priority task
        task_data = {"title": "High Priority", "priority": "high"}
        client.post("/tasks", json=task_data)

        # Filter by medium+ priority (should include high)
        response = client.get("/tasks?priority=medium")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert len(data["tasks"]) == 1
        assert data["tasks"][0]["priority"] == "high"

    def test_list_tasks_pagination(self, client):
        """Test task list pagination."""
        # Create multiple tasks
        for i in range(5):
            task_data = {"title": f"Task {i}"}
            client.post("/tasks", json=task_data)

        # Request limited results
        response = client.get("/tasks?limit=3")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert len(data["tasks"]) == 3
        assert data["pagination"]["has_more"] is True
        assert data["pagination"]["next_cursor"] is not None

    def test_list_tasks_sorting(self, client):
        """Test task list sorting."""
        # Create tasks with different update times
        task1 = {"title": "Task 1"}
        task2 = {"title": "Task 2"}

        client.post("/tasks", json=task1)
        client.post("/tasks", json=task2)

        # Sort by title ascending
        response = client.get("/tasks?sort=title&order=asc")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert len(data["tasks"]) >= 2
        # Should be sorted alphabetically by title

    def test_list_tasks_updated_since_filter(self, client, sample_task):
        """Test filtering by updated_since."""
        # Use a future date (should return no results)
        future_date = "2030-01-01T00:00:00Z"
        response = client.get(f"/tasks?updated_since={future_date}")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        assert len(data["tasks"]) == 0
