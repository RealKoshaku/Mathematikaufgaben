# Import of project modules and external dependencies
import tools as t

from rich.console import Console
from rich.table import Table

from sqlalchemy import create_engine, Engine
import questionary as quest
from DB import Database
from databaseStructure import Base

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
                console.print("[bold green]success ! Connection test passed.[/]\n")
                return db
            console.print("[bold red] Fail ! Connection test failed : Invalid data entered.[/]\n")
        except KeyboardInterrupt:
            # Keyboard interruption (Ctrl+C): stop
            return None

def connectToNewDB(console: Console, json_file: str):
    """Establish a connection to the database at the given URL.""" 
    # Prompt for credentials and test the connection to a new database
    db: Database | None = askDBCredsAndTest(console)
    if db is None:
        return None
    else:
        # Offer to save the configuration into the JSON file
        t.askSaveDBToJSON(console, db, json_file)
        # Create then release a SQLAlchemy engine (final validation)
        engine: Engine = create_engine(db.makePostgresqlURL())
        engine.dispose()

def connectToSavedDB(json_file: str) -> None:
    """Connect to a previously saved database configuration."""
    # TODO: read a saved configuration from the JSON and connect to it
    pass

def recreateDBSchema(console: Console, json_file: str) -> Database | None:
    """Recreate the app schema: drop all app tables, recreate them, optionally save."""
    # Ask for credentials and test the connection (cancel -> abort)
    db: Database | None = askDBCredsAndTest(console)
    if db is None:
        console.print("[bold red]No data entered. Operation cancelled.[/]\n")
        return None

    engine: Engine = create_engine(db.makePostgresqlURL())
    try:
        # Show the current tables before anything destructive
        console.print(t.createATableFromTablesInDB(console, db))

        # Confirm BEFORE touching the DB, naming the target database
        ok = quest.confirm(
            f"This action will erase all the tables in '{db.dbName}'. "
            "Are you sure you want to delete all the tables ?",
            default=True,
        ).ask()
        print("")
        if not ok:
            console.print("[bold red]Operation cancelled by user.[/]\n")
            return None

        # Drop only this app's tables (not the whole schema)
        with console.status("Erasing all the tables...", spinner="dots"):
            Base.metadata.drop_all(engine)
        console.print("[bold green]Success ! All tables were erased.[/]\n")

        # Recreate the app tables
        with console.status("Creating the new tables...", spinner="dots"):
            Base.metadata.create_all(engine)
        console.print("[bold green]Success ! All new tables were created.[/]\n")

        # Optionally save the credentials
        t.askSaveDBToJSON(console, db, json_file)
        
        ok = quest.confirm("Do you want to enter in this DB", default=True).ask()
        if ok:
            pass

        return db
    except Exception as e:
        console.print(f"[bold red]Error while configuring the DB : {e}[/]\n")
        return None
    finally:
        engine.dispose()

def quit():
    # TODO: implement a clean exit from the application
    pass