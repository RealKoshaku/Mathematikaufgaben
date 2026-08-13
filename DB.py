# Import of standard library modules for reading/writing JSON files
import json
from pathlib import Path
# Import of SQLAlchemy to create the connection engine and run raw SQL
from sqlalchemy import create_engine, text
# Import of the exception raised when the database connection fails
from sqlalchemy.exc import OperationalError

class Database():
    """Manages a PostgreSQL connection based on its credentials."""

    def __new__(cls, DB_CREDS: tuple[str, ...] | None):
        # If no credentials are provided, no object is created (None)
        if DB_CREDS is None:
            return None
        return super.__new__(cls)
    
    def __init__(self, DB_CREDS: tuple[str, ...]):
        # Unpack the credentials tuple into dedicated attributes
        self.dbName = DB_CREDS[0]
        self.dbHost = DB_CREDS[1]
        self.dbPort = DB_CREDS[2]
        self.dbAdmin = DB_CREDS[3]
        self.dbPassword = DB_CREDS[4]

    def makePostgresqlURL(self) -> str:
        # Build the PostgreSQL connection URL from the attributes
        return f"postgresql://{self.dbAdmin}:{self.dbPassword}@{self.dbHost}:{self.dbPort}/{self.dbName}"

    def saveDBToJSON(self, json_file: str) -> None:
        # Save the database information into a JSON file
        path = Path(json_file)

        # If the file already exists and is not empty, load its contents
        if path.exists() and path.stat().st_size > 0:
            with open(path, 'r', encoding="utf-8") as f:
                data = json.load(f)
        else:
            # Otherwise start from an empty dictionary
            data = {}

        # Add the current database with an incremental numeric key
        data[str(len(data))] = dict(dbName = self.dbName, dbHost = self.dbHost, dbPort = self.dbPort)

        # Rewrite the updated dictionary into the JSON file
        with open(json_file, 'w', encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def isConnectable(self, showError: bool = False) -> tuple[bool, OperationalError | None]:
        # Test whether the database is reachable by running a simple query
        engine = create_engine(self.makePostgresqlURL())
        try:
            # Open a connection and execute "SELECT 1" to validate the link
            with engine.connect() as conn:
                conn.execute(text("SELECT 1;"))
            return (True, None)
        except OperationalError as e:
            # On error, return the exception if the flag is enabled
            if showError:
                return (False, e)
            return (False, None)
