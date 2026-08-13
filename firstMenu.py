# Import of project modules and external dependencies
import tools as t
from rich.console import Console
from sqlalchemy import create_engine, Engine
import questionary as quest
from DB import Database

def askDBCredsAndTest(console: Console) -> Database | None:
    # Prompt for credentials until the connection succeeds
    while True:
        try:
            # Get the credentials entered by the user
            db = t.askDBCreds()
            # Input cancelled: stop
            if db is None:
                return None
            # Test the connection and inform the user of the result
            if db.isConnectable()[0]:
                console.print("[bold green]Sucess ! Connection test passed.[/]\n")
                return db
            console.print("[bold red] Fail ! Connection test failed : Invalid data entered.[/]\n")
        except KeyboardInterrupt:
            # Keyboard interruption (Ctrl+C): stop
            return None

def initializeDB(DB_CREDS: str, console: Console) -> None:
    """Initialize the database schema using the given connection URL."""
    # TODO: initialize the database schema using the provided credentials
    pass

def connectToNewDB(console: Console, json_file: str):
    """Establish a connection to the database at the given URL.""" 
    # Prompt for credentials and test the connection to a new database
    db : Database | None = askDBCredsAndTest(console)
    if db is None:
        return None
    else:
        # Offer to save the configuration into the JSON file
        ok = quest.confirm("Do you want to save this DB in the JSON ?", default = True).ask()
        if ok:
            db.saveDBToJSON(json_file)
            console.print("Sucess ! Credentials saved to JSON.")
        # Create then release a SQLAlchemy engine (final validation)
        engine: Engine = create_engine(db.makePostgresqlURL())
        engine.dispose()


def connectToSavedDB() -> None:
    """Connect to a previously saved database configuration."""
    # TODO: read a saved configuration from the JSON and connect to it
    pass

def quit():
    # TODO: implement a clean exit from the application
    pass

# Entry point: connect to a new database using the Rich console
connectToNewDB(Console(), 'savedDB.json')
