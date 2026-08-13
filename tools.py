# Import of questionary for interactive input prompts
import questionary as quest
# Import of the Database class defined in DB.py
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
    except:
        # Return None if the input was cancelled or failed
        return None

