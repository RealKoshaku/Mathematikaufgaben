# Import de questionary pour les invites de saisie interactives
import questionary as quest
from questionary import Form
# Import de la classe Database définie dans DB.py
from DB import Database

def verifyText(text: str) -> str | bool:
    """Return an error message if the text is empty, True otherwise."""
    # Renvoie un message d'erreur si la saisie est vide ou ne contient que des espaces
    if not text or not text.strip():
        return "Complete this field please."
    return True

def verifyInt(text: str) -> str | bool:
    """Return an error message if the text is not an integer, True otherwise."""
    # Renvoie un message d'erreur si la saisie n'est pas un nombre entier
    if not text or not text.strip().isdigit():
        return "Please enter an integer number."
    return True

def askDBCreds() -> Database | None:
    """Prompt the user for database credentials and return them as a tuple."""
    try:
        # Affiche un formulaire interactif pour saisir les identifiants de la base
        responses = quest.form(
            dbName = quest.text("Name of the DB :", validate=verifyText),
            dbHost = quest.text("Host of the DB :", validate=verifyText),
            dbPort = quest.text("Port of the DB :", default="5432", validate=verifyInt),
            dbAdmin = quest.text("Admin of the DB :", validate=verifyText),
            dbPassword = quest.text("Password of the DB :", validate=verifyText)
        ).unsafe_ask()
        # Construit un objet Database à partir des réponses du formulaire
        return Database(tuple(responses.values()))
    except:
        # Retourne None en cas d'annulation ou d'erreur de saisie
        return None
