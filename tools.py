import questionary as quest
from sqlalchemy import create_engine, text
from sqlalchemy.exc import OperationalError
from pathlib import Path
import json

def verifyText(text: str) -> str | bool:
    """Return an error message if the text is empty, True otherwise."""
    if not text or not text.strip():
        return "Complete this field please."
    return True

def verifyInt(text: str) -> str | bool:
    """Return an error message if the text is not an integer, True otherwise."""
    if not text or not text.strip().isdigit():
        return "Please enter an integer number."
    return True

def askDBCreds() -> tuple[str, ...]:
    """Prompt the user for database credentials and return them as a tuple."""
    dbName = quest.text(
        "Name of the DB : ",
        validate = verifyText).unsafe_ask()

    dbHost = quest.text(
        "Host of the DB : ",
        validate = verifyText).unsafe_ask()

    dbPort = quest.text(
        "Port of the DB : ",
        default = "5432",
        validate = verifyInt).unsafe_ask()

    dbAdmin = quest.text(
        "Admin of the DB : ",
        validate = verifyText).unsafe_ask()

    dbPassword = quest.password("Password of the DB : ").unsafe_ask()

    return dbName, dbHost, dbPort, dbAdmin, dbPassword

def makePostgresqlURL(DB_CREDS: tuple[str, ...]) -> str:
    """Build a PostgreSQL connection URL from a credentials tuple."""
    return f"postgresql://{DB_CREDS[3]}:{DB_CREDS[4]}@{DB_CREDS[1]}:{DB_CREDS[2]}/{DB_CREDS[0]}"

def isDBConnectable(DB_URL: str, showError: bool = False) -> tuple[bool, OperationalError | None]:
    """Check if the database is reachable, returning success and optional error."""
    engine = create_engine(DB_URL)
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1;"))
        return (True, None)
    except OperationalError as e:
        if showError:
            return (False, e)
        return (False, None)

def saveDBCredsToJSON(DB_CREDS: tuple[str, ...], json_file: str) -> None:
    """Save database credentials into the given JSON file, appending to existing data."""
    path = Path(json_file)

    if path.exists() and path.stat().st_size > 0:
        with open(path, 'r', encoding="utf-8") as f:
            data = json.load(f)
    else:
        data = {}

    data[str(len(data))] = dict(dbName = DB_CREDS[0], dbHost = DB_CREDS[1], dbPort = DB_CREDS[2])

    with open(json_file, 'w', encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    
