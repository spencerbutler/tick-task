"""Pydantic schemas for API validation."""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field, validator


class TaskBase(BaseModel):
    """Base task schema with common fields."""

    title: str = Field(..., min_length=1, max_length=200, description="Task title")
    description: Optional[str] = Field(None, max_length=2000, description="Task description")
    status: str = Field("todo", description="Task status", regex=r"^(todo|doing|blocked|done|archived)$")
    priority: str = Field("medium", description="Task priority", regex=r"^(low|medium|high|urgent)$")
    due_at: Optional[datetime] = Field(None, description="Due date and time in ISO format")
    tags: list[str] = Field(default_factory=list, description="List of tags")
    context: str = Field("personal", description="Task context", regex=r"^(personal|professional|mixed)$")
    workspace: Optional[str] = Field(None, max_length=100, description="Workspace name")

    @validator("tags", each_item=True)
    def validate_tag(cls, v):
        """Validate individual tag constraints."""
        if len(v) > 50:
            raise ValueError("Tag must be 50 characters or less")
        if not v.strip():
            raise ValueError("Tag cannot be empty or whitespace-only")
        return v.strip().lower()

    @validator("title")
    def validate_title(cls, v):
        """Validate title is not empty after stripping."""
        if not v.strip():
            raise ValueError("Title cannot be empty or whitespace-only")
        return v.strip()

    class Config:
        """Pydantic configuration."""
        json_encoders = {
            datetime: lambda v: v.isoformat(),
        }


class TaskCreate(TaskBase):
    """Schema for creating a new task."""
    pass


class TaskUpdate(BaseModel):
    """Schema for updating an existing task."""

    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=2000)
    status: Optional[str] = Field(None, regex=r"^(todo|doing|blocked|done|archived)$")
    priority: Optional[str] = Field(None, regex=r"^(low|medium|high|urgent)$")
    due_at: Optional[datetime] = None
    tags: Optional[list[str]] = None
    context: Optional[str] = Field(None, regex=r"^(personal|professional|mixed)$")
    workspace: Optional[str] = Field(None, max_length=100)

    @validator("tags", each_item=True)
    def validate_tag(cls, v):
        """Validate individual tag constraints."""
        if len(v) > 50:
            raise ValueError("Tag must be 50 characters or less")
        if not v.strip():
            raise ValueError("Tag cannot be empty or whitespace-only")
        return v.strip().lower()

    @validator("title")
    def validate_title(cls, v):
        """Validate title is not empty after stripping."""
        if v is not None and not v.strip():
            raise ValueError("Title cannot be empty or whitespace-only")
        return v.strip() if v is not None else v

    class Config:
        """Pydantic configuration."""
        json_encoders = {
            datetime: lambda v: v.isoformat(),
        }


class Task(TaskBase):
    """Full task schema for responses."""

    id: str = Field(..., description="Task UUID")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    completed_at: Optional[datetime] = Field(None, description="Completion timestamp")

    class Config:
        """Pydantic configuration."""
        orm_mode = True
        json_encoders = {
            datetime: lambda v: v.isoformat(),
        }


class TaskList(BaseModel):
    """Schema for task list responses with pagination."""

    tasks: list[Task] = Field(..., description="List of tasks")
    pagination: dict = Field(..., description="Pagination metadata")

    class Config:
        """Pydantic configuration."""
        json_encoders = {
            datetime: lambda v: v.isoformat(),
        }


class HealthResponse(BaseModel):
    """Schema for health check responses."""

    status: str = Field(..., description="Service status")
    version: str = Field(..., description="Application version")
    database: str = Field(..., description="Database status")
    timestamp: datetime = Field(..., description="Response timestamp")

    class Config:
        """Pydantic configuration."""
        json_encoders = {
            datetime: lambda v: v.isoformat(),
        }


class ErrorResponse(BaseModel):
    """Schema for error responses."""

    error: dict = Field(..., description="Error details")

    class Config:
        """Pydantic configuration."""
        json_encoders = {
            datetime: lambda v: v.isoformat(),
        }
