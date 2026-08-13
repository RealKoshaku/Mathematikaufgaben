# Import des modules du projet et des dépendances externes
import tools as t
from rich.console import Console
from sqlalchemy import create_engine, Engine
import questionary as quest
from DB import Database

def askDBCredsAndTest(console: Console) -> Database | None:
    # Demande les identifiants à l'utilisateur jusqu'à ce que la connexion réussisse
    while True:
        try:
            # Récupère les identifiants saisis par l'utilisateur
            db = t.askDBCreds()
            # Saisie annulée : on s'arrête
            if db is None:
                return None
            # Teste la connexion et informe l'utilisateur du résultat
            if db.isConnectable()[0]:
                console.print("[bold green]Sucess ! Connection test passed.[/]\n")
                return db
            console.print("[bold red] Fail ! Connection test failed : Invalid data entered.[/]\n")
        except KeyboardInterrupt:
            # Interruption clavier (Ctrl+C) : on s'arrête
            return None

def initializeDB(DB_CREDS: str, console: Console) -> None:
    """Initialize the database schema using the given connection URL."""
    # TODO: initialiser le schéma de la base à l'aide des identifiants fournis
    pass

def connectToNewDB(console: Console, json_file: str):
    """Establish a connection to the database at the given URL.""" 
    # Demande les identifiants et teste la connexion à une nouvelle base
    db : Database | None = askDBCredsAndTest(console)
    if db is None:
        return None
    else:
        # Propose d'enregistrer la configuration dans le fichier JSON
        ok = quest.confirm("Do you want to save this DB in the JSON ?", default = True).ask()
        if ok:
            db.saveDBToJSON(json_file)
            console.print("Sucess ! Credentials saved to JSON.")
        # Crée puis libère un moteur SQLAlchemy (validation finale)
        engine: Engine = create_engine(db.makePostgresqlURL())
        engine.dispose()


def connectToSavedDB() -> None:
    """Connect to a previously saved database configuration."""
    # TODO: lire une configuration enregistrée dans le JSON et s'y connecter
    pass

def quit():
    # TODO: implémenter la sortie propre de l'application
    pass

# Point d'entrée : lance la connexion à une nouvelle base avec la console Rich
connectToNewDB(Console(), 'savedDB.json')
