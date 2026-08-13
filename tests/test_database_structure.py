import uuid

import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from databaseStructure import Base, Exercise, User


@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    with Session(engine) as s:
        yield s
    engine.dispose()


def make_user(username="alice", **kwargs) -> User:
    return User(
        username=username,
        hashed_password="hashed",
        first_name="Alice",
        last_name="Example",
        **kwargs,
    )


def test_create_user(session):
    user = make_user()
    session.add(user)
    session.commit()

    stored = session.execute(select(User)).scalar_one()
    assert stored.username == "alice"
    assert stored.is_admin is False
    assert isinstance(stored.id, uuid.UUID)
    assert stored.created_at is not None


def test_username_is_unique(session):
    session.add(make_user())
    session.commit()
    session.add(make_user(username="alice"))
    with pytest.raises(IntegrityError):
        session.commit()


def test_create_exercise(session):
    user = make_user()
    session.add(user)
    session.commit()

    exercise = Exercise(
        title="Derivatives",
        principal_subject="Analysis",
        level="Bac1",
        difficulty=3,
        path_to_file="/exercises/derivatives.pdf",
        created_by=user.id,
    )
    session.add(exercise)
    session.commit()

    stored = session.execute(select(Exercise)).scalar_one()
    assert stored.title == "Derivatives"
    assert stored.author.username == "alice"


def test_path_to_file_is_unique(session):
    user = make_user()
    session.add(user)
    session.commit()

    def add(path):
        session.add(
            Exercise(
                title="T",
                principal_subject="Analysis",
                level="Bac1",
                difficulty=2,
                path_to_file=path,
                created_by=user.id,
            )
        )

    add("/exercises/a.pdf")
    session.commit()
    add("/exercises/a.pdf")
    with pytest.raises(IntegrityError):
        session.commit()


def test_deleting_user_deletes_exercises(session):
    user = make_user()
    session.add(user)
    session.commit()

    session.add(
        Exercise(
            title="Derivatives",
            principal_subject="Analysis",
            level="Bac1",
            difficulty=3,
            path_to_file="/exercises/derivatives.pdf",
            created_by=user.id,
        )
    )
    session.commit()

    session.delete(user)
    session.commit()

    assert session.execute(select(Exercise)).all() == []
