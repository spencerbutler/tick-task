"""Integration tests for end-to-end workflows."""

from datetime import datetime, timedelta

import pytest
from fastapi import status


class TestTaskLifecycleIntegration:
    """Test complete task lifecycle from creation to archiving."""

    def test_complete_task_workflow(self, client):
        """Test full task lifecycle: create → read → update → complete → archive."""
        # 1. Create a task
        create_data = {
            "title": "Integration Test Task",
            "description": "Testing complete workflow",
            "priority": "high",
            "context": "professional",
            "tags": ["integration", "test"],
        }

        create_response = client.post("/api/v1/tasks", json=create_data)
        assert create_response.status_code == status.HTTP_201_CREATED

        task_data = create_response.json()
        task_id = task_data["id"]

        # Verify creation
        assert task_data["title"] == "Integration Test Task"
        assert task_data["status"] == "todo"
        assert task_data["priority"] == "high"
        assert task_data["context"] == "professional"
        assert task_data["tags"] == ["integration", "test"]
        assert "created_at" in task_data
        assert "updated_at" in task_data

        # 2. Read the task back
        get_response = client.get(f"/api/v1/tasks/{task_id}")
        assert get_response.status_code == status.HTTP_200_OK

        retrieved_task = get_response.json()
        assert retrieved_task["id"] == task_id
        assert retrieved_task["title"] == "Integration Test Task"

        # 3. Update the task
        update_data = {
            "title": "Updated Integration Task",
            "status": "doing",
            "description": "Updated description",
        }

        update_response = client.put(f"/api/v1/tasks/{task_id}", json=update_data)
        assert update_response.status_code == status.HTTP_200_OK

        updated_task = update_response.json()
        assert updated_task["title"] == "Updated Integration Task"
        assert updated_task["status"] == "doing"
        assert updated_task["description"] == "Updated description"

        # 4. Mark as completed
        complete_data = {"status": "done"}
        complete_response = client.put(f"/api/v1/tasks/{task_id}", json=complete_data)
        assert complete_response.status_code == status.HTTP_200_OK

        completed_task = complete_response.json()
        assert completed_task["status"] == "done"
        assert completed_task["completed_at"] is not None

        # 5. Archive the task
        archive_response = client.delete(f"/api/v1/tasks/{task_id}")
        assert archive_response.status_code == status.HTTP_200_OK

        archived_task = archive_response.json()
        assert archived_task["status"] == "archived"

        # 6. Verify archived task can't be updated
        final_update_data = {"title": "Should Fail"}
        final_update_response = client.put(
            f"/api/v1/tasks/{task_id}", json=final_update_data
        )
        assert final_update_response.status_code == status.HTTP_409_CONFLICT


class TestTaskFilteringIntegration:
    """Test advanced filtering and searching capabilities."""

    def test_task_filtering_workflow(self, client):
        """Test comprehensive filtering across multiple tasks."""
        # Create multiple tasks with different attributes
        tasks_data = [
            {
                "title": "Personal Todo",
                "status": "todo",
                "context": "personal",
                "priority": "low",
                "tags": ["personal"],
            },
            {
                "title": "Work In Progress",
                "status": "doing",
                "context": "professional",
                "priority": "high",
                "tags": ["work", "urgent"],
            },
            {
                "title": "Blocked Task",
                "status": "blocked",
                "context": "professional",
                "priority": "medium",
                "tags": ["work", "blocked"],
            },
            {
                "title": "Completed Task",
                "status": "done",
                "context": "personal",
                "priority": "medium",
                "tags": ["personal", "done"],
            },
        ]

        # Create all tasks
        created_tasks = []
        for task_data in tasks_data:
            response = client.post("/api/v1/tasks", json=task_data)
            assert response.status_code == status.HTTP_201_CREATED
            created_tasks.append(response.json())

        # Test status filtering
        todo_response = client.get("/api/v1/tasks?status=todo")
        assert todo_response.status_code == status.HTTP_200_OK
        todo_data = todo_response.json()
        assert len(todo_data["tasks"]) == 1
        assert todo_data["tasks"][0]["status"] == "todo"

        # Test context filtering
        professional_response = client.get("/api/v1/tasks?context=professional")
        assert professional_response.status_code == status.HTTP_200_OK
        professional_data = professional_response.json()
        assert len(professional_data["tasks"]) == 2
        for task in professional_data["tasks"]:
            assert task["context"] == "professional"

        # Test priority filtering (minimum level)
        high_priority_response = client.get("/api/v1/tasks?priority=high")
        assert high_priority_response.status_code == status.HTTP_200_OK
        high_priority_data = high_priority_response.json()
        assert len(high_priority_data["tasks"]) == 1
        assert high_priority_data["tasks"][0]["priority"] == "high"

        # Test multiple status filters
        multiple_status_response = client.get(
            "/api/v1/tasks?status=doing&status=blocked"
        )
        assert multiple_status_response.status_code == status.HTTP_200_OK
        multiple_status_data = multiple_status_response.json()
        assert len(multiple_status_data["tasks"]) == 2
        statuses = [task["status"] for task in multiple_status_data["tasks"]]
        assert "doing" in statuses
        assert "blocked" in statuses


class TestTaskConcurrencyIntegration:
    """Test concurrent operations and data consistency."""

    def test_concurrent_task_operations(self, client):
        """Test that multiple operations work correctly together."""
        # Create initial task
        create_response = client.post(
            "/api/v1/tasks", json={"title": "Concurrency Test"}
        )
        assert create_response.status_code == status.HTTP_201_CREATED
        task_id = create_response.json()["id"]

        # Perform multiple operations rapidly
        operations = [
            {"title": "Update 1", "status": "doing"},
            {"title": "Update 2", "priority": "high"},
            {"title": "Update 3", "status": "done"},
        ]

        for op_data in operations:
            response = client.put(f"/api/v1/tasks/{task_id}", json=op_data)
            assert response.status_code == status.HTTP_200_OK

        # Verify final state
        final_response = client.get(f"/api/v1/tasks/{task_id}")
        assert final_response.status_code == status.HTTP_200_OK
        final_task = final_response.json()

        assert final_task["title"] == "Update 3"  # Last update
        assert final_task["status"] == "done"  # Last status update
        assert final_task["priority"] == "high"  # Priority update persisted
        assert final_task["completed_at"] is not None


class TestDataPersistenceIntegration:
    """Test that data persists correctly across operations."""

    def test_data_persistence_across_operations(self, client):
        """Test that all task data is correctly persisted and retrieved."""
        # Create a comprehensive task
        complex_task = {
            "title": "Complex Persistence Test",
            "description": "Testing all fields persist correctly",
            "status": "doing",
            "priority": "urgent",
            "due_at": "2024-12-31T23:59:59Z",
            "tags": ["complex", "persistence", "test"],
            "context": "professional",
            "workspace": "Integration Testing",
        }

        # Create task
        create_response = client.post("/api/v1/tasks", json=complex_task)
        assert create_response.status_code == status.HTTP_201_CREATED
        created_task = create_response.json()

        # Verify all fields were saved (note: due_at gets parsed and may be reformatted)
        for key, expected_value in complex_task.items():
            if key == "due_at":
                # datetime gets parsed and may lose 'Z' suffix in serialization
                assert created_task[key].startswith("2024-12-31T23:59:59")
            else:
                assert created_task[key] == expected_value

        # Retrieve task separately
        task_id = created_task["id"]
        get_response = client.get(f"/api/v1/tasks/{task_id}")
        assert get_response.status_code == status.HTTP_200_OK
        retrieved_task = get_response.json()

        # Verify all fields match (due_at gets reformatted)
        for key, expected_value in complex_task.items():
            if key == "due_at":
                # datetime gets parsed and may lose 'Z' suffix in serialization
                assert retrieved_task[key].startswith("2024-12-31T23:59:59")
            else:
                assert retrieved_task[key] == expected_value

        # Check that metadata fields exist
        assert "id" in retrieved_task
        assert "created_at" in retrieved_task
        assert "updated_at" in retrieved_task
        assert retrieved_task["completed_at"] is None
