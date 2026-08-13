import pytest

import tools
from DB import Database


def test_verify_text_empty():
    assert tools.verifyText("") == "Complete this field please."
    assert tools.verifyText("   ") == "Complete this field please."


def test_verify_text_valid():
    assert tools.verifyText("hello") is True


def test_verify_int_invalid():
    assert tools.verifyInt("abc") == "Please enter an integer number."
    assert tools.verifyInt("") == "Please enter an integer number."


def test_verify_int_valid():
    assert tools.verifyInt("5432") is True


def test_ask_db_creds_builds_database(monkeypatch):
    responses = {
        "dbName": "myapp",
        "dbHost": "localhost",
        "dbPort": "5432",
        "dbAdmin": "admin",
        "dbPassword": "secret",
    }

    class FakeForm:
        def __init__(self, **kwargs):
            self.kwargs = kwargs

        def unsafe_ask(self):
            return responses

    monkeypatch.setattr("tools.quest.form", lambda **kwargs: FakeForm(**kwargs))

    db = tools.askDBCreds()
    assert isinstance(db, Database)
    assert db.makePostgresqlURL() == "postgresql://admin:secret@localhost:5432/myapp"


def test_ask_db_creds_returns_none_on_cancel(monkeypatch):
    class FailingForm:
        def unsafe_ask(self):
            raise KeyboardInterrupt

    monkeypatch.setattr("tools.quest.form", lambda **kwargs: FailingForm())

    assert tools.askDBCreds() is None


def test_create_table_from_tables_in_db(monkeypatch, tmp_path):
    from sqlalchemy import create_engine, text

    sqlite_file = tmp_path / "sample.db"
    engine = create_engine(f"sqlite:///{sqlite_file}")
    with engine.begin() as conn:
        conn.execute(text("CREATE TABLE exercises (id INTEGER PRIMARY KEY)"))
        conn.execute(text("CREATE TABLE users (id INTEGER PRIMARY KEY)"))
    engine.dispose()

    monkeypatch.setattr("tools.create_engine", lambda url: create_engine(f"sqlite:///{sqlite_file}"))

    db = Database(("myapp", "localhost", "5432", "admin", "secret"))
    assert db is not None

    from rich.console import Console
    from io import StringIO

    console = Console(file=StringIO())
    table = tools.createATableFromTablesInDB(console, db)
    assert table.title == "Tables found in myapp"

    rendered = StringIO()
    Console(file=rendered).print(table)
    output = rendered.getvalue()
    assert "users" in output
    assert "exercises" in output
