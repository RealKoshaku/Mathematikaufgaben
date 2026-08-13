# Import of project modules and external dependencies
import tools as t

from rich.console import Console
from rich.table import Table

from sqlalchemy import create_engine, Engine, MetaData
import questionary as quest
from DB import Database
from databaseStructure import Base
import time

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
        ok = quest.confirm("Do you want to save this DB in the JSON ?", default = True).ask()
        if ok:
            db.saveDBToJSON(json_file)
            console.print("[bold green]Success ! Credentials saved to JSON.[/]n")
        # Create then release a SQLAlchemy engine (final validation)
        engine: Engine = create_engine(db.makePostgresqlURL())
        engine.dispose()

def connectToSavedDB(json_file: str) -> None:
    """Connect to a previously saved database configuration."""
    # TODO: read a saved configuration from the JSON and connect to it
    pass

def configureDB(console: Console, json_file: str) -> None:
    """Initialize the database schema using the given connection URL."""
    db: Database | None = askDBCredsAndTest(console)
    if db is None:
        console.print("[bold red] Please enter data[/]")
        return None
    else:
        engine: Engine = create_engine(db.makePostgresqlURL())
        metadata: MetaData = MetaData()
        metadata.reflect(bind=engine)

        tablesFound: list = list(metadata.tables.keys())
        table = Table(title=f"Tables found in {db.dbName}")

        table.add_column("ID", style="cyan")
        table.add_column("Table", style="red", justify="center")

        for i, key in enumerate(tablesFound):
            table.add_row(str(i), key)

        console.print(table)

        ok = quest.confirm("This action will erase all the tables in the DB. Sure you want to delete all the tables ?", default=True).ask()
        if ok:
            with console.status("Erasing all the tables...", spinner="dots"):
                metadata.drop_all(bind=engine)
                time.sleep(0.5)
            console.print("[bold green] Success ! All tables were erased.")
            with console.status("Creating the new tables...", spinner="dots"):
                Base.metadata.create_all(engine)
                time.sleep(0.5)
            console.print("[bold green]Success ! All new tables were created.[/]\n")
        else:
            console.print("[bold red] Operation cancelled by user.[/]\n")
            return None
        engine.dispose()

        ok = quest.confirm("Do you want to save this DB in the JSON ?", default = True).ask()
        if ok:
            db.saveDBToJSON(json_file)
            console.print("[bold green]Success ! Credentials saved to JSON.[/]n")

def quit():
    # TODO: implement a clean exit from the application
    pass