import pytest
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

from DB import Database

FAKE_CREDS = ("myapp", "localhost", "5432", "admin", "secret")


@pytest.fixture
def db() -> Database:
    db = Database(FAKE_CREDS)
    assert db is not None
    return db


def test_make_postgresql_url(db):
    assert db.makePostgresqlURL() == "postgresql://admin:secret@localhost:5432/myapp"


def test_new_returns_none_without_creds():
    assert Database(None) is None


def test_save_to_json_creates_file(db, tmp_path):
    json_file = str(tmp_path / "creds.json")
    db.saveDBToJSON(json_file)
    import json

    with open(json_file, encoding="utf-8") as f:
        data = json.load(f)
    assert data["0"] == {"dbName": "myapp", "dbHost": "localhost", "dbPort": "5432"}


def test_save_to_json_preserves_existing(db, tmp_path):
    json_file = str(tmp_path / "creds.json")
    db.saveDBToJSON(json_file)
    other = Database(("other", "host", "5433", "a", "p"))
    assert other is not None
    other.saveDBToJSON(json_file)
    import json

    with open(json_file, encoding="utf-8") as f:
        data = json.load(f)
    assert len(data) == 2


def test_is_connectable_true_when_engine_ok(db, monkeypatch):
    engine = create_engine("sqlite:///:memory:")
    monkeypatch.setattr("DB.create_engine", lambda url: engine)
    assert db.isConnectable() == (True, None)


def test_is_connectable_false_on_operational_error(db, monkeypatch):
    class BrokenEngine:
        def connect(self):
            raise OperationalError("s", None, Exception("down"))

    monkeypatch.setattr("DB.create_engine", lambda url: BrokenEngine())
    ok, err = db.isConnectable()
    assert ok is False
    assert err is None


def test_is_connectable_returns_error_when_asked(db, monkeypatch):
    class BrokenEngine:
        def connect(self):
            raise OperationalError("s", None, Exception("down"))

    monkeypatch.setattr("DB.create_engine", lambda url: BrokenEngine())
    ok, err = db.isConnectable(showError=True)
    assert ok is False
    assert isinstance(err, OperationalError)
