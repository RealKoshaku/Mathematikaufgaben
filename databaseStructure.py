# Import of Python standard library modules
from datetime import datetime
from typing import List, Optional
import uuid

# Import of SQLAlchemy column types
from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Uuid,
    func,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    """Base class for all ORM models using the declarative base pattern."""


class User(Base):
    """ORM model representing a registered user of the application."""

    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid, primary_key=True, default=uuid.uuid4
    )

    username: Mapped[str] = mapped_column(
        String(50), unique=True, index=True, nullable=False
    )

    # Hashed password (never stored in plain text)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)

    # Personal information about the user
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)

    # Flag indicating whether the user has administrator rights
    is_admin: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )

    # Creation and last-update timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # Relationship: one user can create many exercises.
    # "cascade=all, delete-orphan" deletes their exercises along with the user.
    exercises: Mapped[List["Exercise"]] = relationship(
        "Exercise", back_populates="author", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        """Return a human-readable representation of the User."""
        return f"<User username='{self.username}'>"


class Exercise(Base):
    """ORM model representing a math exercise stored in the database."""

    __tablename__ = "exercises"

    id: Mapped[uuid.UUID] = mapped_column(
        Uuid, primary_key=True, default=uuid.uuid4
    )

    # Exercise title
    title: Mapped[str] = mapped_column(String(255), nullable=False)

    # Main subject (indexed) and optional secondary subject
    principal_subject: Mapped[str] = mapped_column(
        String(100), index=True, nullable=False
    )
    second_subject: Mapped[Optional[str]] = mapped_column(
        String(100), nullable=True
    )

    # School level (indexed)
    level: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    difficulty: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    # Path to the exercise file (unique)
    path_to_file: Mapped[str] = mapped_column(
        String(512), unique=True, nullable=False
    )

    # Foreign key pointing to the creator of the exercise
    created_by: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    # Creation and last-update timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # Optional comment on the exercise
    comment: Mapped[Optional[str]] = mapped_column(
        String(1024),
        nullable = True
    )

    # Inverse relationship: the author (user) of the exercise
    author: Mapped["User"] = relationship("User", back_populates="exercises")

    def __repr__(self) -> str:
        """Return a human-readable representation of the Exercise."""
        return (
            f"<Exercise id={self.id} title={self.title!r} "
            f"subject={self.principal_subject!r} level={self.level!r} "
            f"difficulty={self.difficulty}>"
        )
