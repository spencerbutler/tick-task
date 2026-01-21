"""Database models for FIN-tasks."""

from datetime import datetime
from typing import Optional
from uuid import uuid4

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.dialects.sqlite import JSON
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(AsyncAttrs, DeclarativeBase):
    """Base class for all database models."""

    pass


class Task(Base):
    """Task database model."""

    __tablename__ = "tasks"

    # Primary key
    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid4())
    )

    # Core fields
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Status and priority enums
    status: Mapped[str] = mapped_column(
        Enum(
            "todo",
            "doing",
            "blocked",
            "done",
            "archived",
            name="task_status",
        ),
        nullable=False,
        default="todo",
    )

    priority: Mapped[str] = mapped_column(
        Enum(
            "low",
            "medium",
            "high",
            "urgent",
            name="task_priority",
        ),
        nullable=False,
        default="medium",
    )

    # Dates
    due_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    # Tags stored as JSON array
    tags: Mapped[Optional[list[str]]] = mapped_column(
        JSON, nullable=True, default=list
    )

    # Context and workspace
    context: Mapped[str] = mapped_column(
        Enum(
            "personal",
            "professional",
            "mixed",
            name="task_context",
        ),
        nullable=False,
        default="personal",
    )

    workspace: Mapped[Optional[str]] = mapped_column(
        String(100), nullable=True
    )

    # Timestamps (UTC)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
    completed_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime, nullable=True
    )

    def __repr__(self) -> str:
        """String representation of Task."""
        return f"<Task(id={self.id!r}, title={self.title!r}, status={self.status!r})>"
