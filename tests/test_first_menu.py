import json
from io import StringIO

import pytest
from rich.console import Console

import firstMenu as fM
from DB import Database

FAKE_CREDS = ("myapp", "localhost", "5432", "admin", "secret")


def make_db():
    db = Database(FAKE_CREDS)
    assert db is not None
    return db


@pytest.fixture
def sqlite_engine(monkeypatch, tmp_path):
    from sqlalchemy import create_engine

    db_file = tmp_path / "app.db"
    engine = create_engine(f"sqlite:///{db_file}")
    monkeypatch.setattr("firstMenu.create_engine", lambda url: engine)
    return engine


def run_configure(monkeypatch, tmp_path, confirm_result=True):
    console = Console(file=StringIO())
    json_file = str(tmp_path / "creds.json")
    monkeypatch.setattr(fM, "askDBCredsAndTest", lambda c: make_db())
    monkeypatch.setattr(fM.t, "createATableFromTablesInDB", lambda c, db: None)
    monkeypatch.setattr(fM.quest, "confirm", lambda *a, **k: type("C", (), {"ask": lambda s: confirm_result})())
    result = fM.recreateDBSchema(console, json_file)
    return result, json_file


def test_configure_aborts_without_credentials(monkeypatch, sqlite_engine, tmp_path):
    console = Console(file=StringIO())
    monkeypatch.setattr(fM, "askDBCredsAndTest", lambda c: None)
    assert fM.recreateDBSchema(console, str(tmp_path / "creds.json")) is None


def test_configure_aborts_when_cancelled(monkeypatch, sqlite_engine, tmp_path):
    result, _ = run_configure(monkeypatch, tmp_path, confirm_result=False)
    assert result is None
    from sqlalchemy import inspect

    assert not inspect(sqlite_engine).get_table_names()


def test_configure_creates_tables_and_saves_json(monkeypatch, sqlite_engine, tmp_path):
    from sqlalchemy import inspect

    result, json_file = run_configure(monkeypatch, tmp_path, confirm_result=True)
    assert result is not None
    assert set(inspect(sqlite_engine).get_table_names()) >= {"users", "exercises"}

    with open(json_file, encoding="utf-8") as f:
        data = json.load(f)
    assert data["0"] == {"dbName": "myapp", "dbHost": "localhost", "dbPort": "5432"}
