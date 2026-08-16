import questionary as quest
from rich.console import Console
from rich.table import Table
from sqlalchemy import Engine, MetaData, create_engine

from DB import Database


def verifyText(text: str) -> str | bool:
    """Return an error message if the text is empty, True otherwise."""
    # Return an error message if the input is empty or whitespace-only
    if not text or not text.strip():
        return "Complete this field please."
    return True

def verifyInt(text: str) -> str | bool:
    """Return an error message if the text is not an integer, True otherwise."""
    # Return an error message if the input is not an integer
    if not text or not text.strip().isdigit():
        return "Please enter an integer number."
    return True

def askDBCreds() -> Database | None:
    """Prompt the user for database credentials and return them as a tuple."""
    try:
        # Display an interactive form to collect the database credentials
        responses = quest.form(
            dbName = quest.text("Name of the DB :", validate=verifyText),
            dbHost = quest.text("Host of the DB :", validate=verifyText),
            dbPort = quest.text("Port of the DB :", default="5432", validate=verifyInt),
            dbAdmin = quest.text("Admin of the DB :", validate=verifyText),
            dbPassword = quest.password("Password of the DB :", validate=verifyText)
        ).unsafe_ask()
        # Build a Database object from the form responses
        return Database(tuple(responses.values()))
    except (KeyboardInterrupt, EOFError):
        # Return None if the input was cancelled or failed
        return None

def createATableFromTablesInDB(console: Console, db : Database) -> Table:
    """Build a Rich table listing all tables currently present in the database."""
    # Create an engine and introspect the database schema
    engine: Engine = create_engine(db.makePostgresqlURL())
    metadata: MetaData = MetaData()
    metadata.reflect(bind=engine)

    # Collect the names of all existing tables
    tablesFound: list = list(metadata.tables.keys())
    table = Table(title=f"Tables found in {db.dbName}")

    # Add an ID column and the table name column
    table.add_column("ID", style="cyan")
    table.add_column("Table", style="red", justify="center")

    # Fill the table with one row per existing table
    for i, key in enumerate(tablesFound):
        table.add_row(str(i), key)

    engine.dispose()

    return table

def askSaveDBToJSON(console: Console, db: Database, json_file: str) -> None:
    """Ask the user whether to save the database credentials into a JSON file."""
    # Only save if the user confirms
    ok = quest.confirm("Do you want to save this DB in the JSON ?", default = True).ask()
    if ok:
        db.saveDBToJSON(json_file)
        console.print("[bold green]Success ! Credentials saved to JSON.[/]\n")
