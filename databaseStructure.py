# Import des modules Python standard
from datetime import datetime, timezone
from typing import List, Optional
import uuid

# Import des types de colonnes SQLAlchemy
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

    # Identifiants de connexion : email et nom d'utilisateur (uniques)
    email: Mapped[str] = mapped_column(
        String(255), unique=True, index=True, nullable=False
    )
    username: Mapped[str] = mapped_column(
        String(50), unique=True, index=True, nullable=False
    )

    # Mot de passe haché (jamais stocké en clair)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)

    # Informations personnelles de l'utilisateur
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)

    # Drapeau indiquant si l'utilisateur a les droits administrateur
    is_admin: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )

    # Horodatage de création et de dernière modification
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # Relation : un utilisateur peut créer plusieurs exercices.
    # "cascade=all, delete-orphan" supprime ses exercices avec lui.
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

    # Titre de l'exercice
    title: Mapped[str] = mapped_column(String(255), nullable=False)

    # Matière principale (indexée) et matière secondaire optionnelle
    principal_subject: Mapped[str] = mapped_column(
        String(100), index=True, nullable=False
    )
    second_subject: Mapped[Optional[str]] = mapped_column(
        String(100), nullable=True
    )

    # Niveau scolaire (indexé) et difficulté comprise entre 1 et 5
    level: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    difficulty: Mapped[int] = mapped_column(
        Integer,
        CheckConstraint("difficulty >= 1 AND difficulty <= 5"),
        nullable=False,
    )

    # Chemin vers le fichier de l'exercice (unique)
    path_to_file: Mapped[str] = mapped_column(
        String(512), unique=True, nullable=False
    )

    # Clé étrangère vers le créateur de l'exercice
    created_by: Mapped[uuid.UUID] = mapped_column(
        Uuid, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    # Horodatage de création et de dernière modification
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # Commentaire facultatif sur l'exercice
    comment: Mapped[Optional[str]] = mapped_column(
        String(1024),
        nullable = True
    )

    # Relation inverse : l'auteur (utilisateur) de l'exercice
    author: Mapped["User"] = relationship("User", back_populates="exercises")

    def __repr__(self) -> str:
        """Return a human-readable representation of the Exercise."""
        return (
            f"<Exercise id={self.id} title={self.title!r} "
            f"subject={self.principal_subject!r} level={self.level!r} "
            f"difficulty={self.difficulty}>"
        )
