# Import of project modules and external dependencies
import json
from pathlib import Path

import questionary as quest
from rich.console import Console
from rich.table import Table
from sqlalchemy import Engine, create_engine

import kaufgaben
import tools as t
from databaseStructure import Base
from DB import Database


def askDBCredsAndTest(console: Console) -> Database | None:
    """Prompt for credentials until the connection succeeds, or None on cancel."""
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
        return
    else:
        # Offer to save the configuration into the JSON file
        t.askSaveDBToJSON(console, db, json_file)
        # Create then release a SQLAlchemy engine (final validation)
        engine: Engine = create_engine(db.makePostgresqlURL())
        kaufgaben.k_aufgaben()
        engine.dispose()

def connectToSavedDB(console: Console, json_file: str) -> Database | None:
    """Connect to a previously saved database configuration, or None on cancel."""
    path = Path(json_file)

    # Load the saved databases from the JSON file
    if not path.exists() or path.stat().st_size == 0:
        console.print(f"[bold red] No databases have been saved in {json_file}.[/]\n")
        return None

    with open(json_file, 'r', encoding="utf-8") as f:
        data: dict[str, dict[str, str]] = json.load(f)

    if not data:
        console.print(f"[bold red] No databases have been saved in {json_file}.[/]\n")
        return None

    # Build and display the table of saved databases
    table = Table(title=f"Saved databases in {json_file}")
    table.add_column("ID", style="cyan", justify="center")
    table.add_column("DB name", style="blue", justify="center")
    table.add_column("DB host", style="green", justify="center")
    table.add_column("DB port", style="yellow", justify="center")

    for db_id, creds in data.items():
        table.add_row(db_id, creds['dbName'], creds['dbHost'], creds['dbPort'])
    console.print(table)

    # Let the user pick a database ID
    while True:
        try:
            db_id = quest.text("Write the ID of the database you want to connect to:").unsafe_ask()
            if db_id not in data:
                console.print("[bold red] Invalid ID. Please try again.[/]\n")
                continue
            break
        except KeyboardInterrupt:
            return None

    creds = data[db_id]

    # Ask for admin credentials and retry until the connection succeeds
    while True:
        try:
            console.print(f"[yellow] Log in to {creds['dbName']}")
            logIn = quest.form(
                dbAdmin = quest.text("Admin of the DB :", validate=t.verifyText),
                dbPassword = quest.password("Password of the DB :", validate=t.verifyText)
            ).unsafe_ask()

            db = Database((creds['dbName'], creds['dbHost'], creds['dbPort']) + tuple(logIn.values()))
            ok, error = db.isConnectable(showError=True)
            if ok:
                console.print("[bold green] success ! Connection established.[/]\n")
                kaufgaben.k_aufgaben()
                return db
            console.print(f"[bold red] An error occured : {error}[/]\n")
        except KeyboardInterrupt:
            return None

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
        print()
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