# Import des modules standard pour la lecture/écriture de fichiers JSON
import json
from pathlib import Path
# Import de SQLAlchemy pour créer le moteur de connexion et exécuter du SQL brut
from sqlalchemy import create_engine, text
# Import de l'exception levée en cas d'échec de connexion à la base
from sqlalchemy.exc import OperationalError

class Database():
    """Gère la connexion à une base PostgreSQL à partir de ses identifiants."""

    def __new__(cls, DB_CREDS: tuple[str, ...] | None):
        # Si aucun identifiant n'est fourni, aucun objet n'est créé (None)
        if DB_CREDS is None:
            return None
        return super.__new__(cls)
    
    def __init__(self, DB_CREDS: tuple[str, ...]):
        # Décompose le tuple d'identifiants dans des attributs dédiés
        self.dbName = DB_CREDS[0]
        self.dbHost = DB_CREDS[1]
        self.dbPort = DB_CREDS[2]
        self.dbAdmin = DB_CREDS[3]
        self.dbPassword = DB_CREDS[4]

    def makePostgresqlURL(self) -> str:
        # Construit l'URL de connexion PostgreSQL à partir des attributs
        return f"postgresql://{self.dbAdmin}:{self.dbPassword}@{self.dbHost}:{self.dbPort}/{self.dbName}"

    def saveDBToJSON(self, json_file: str) -> None:
        # Enregistre les informations de la base dans un fichier JSON
        path = Path(json_file)

        # Si le fichier existe déjà et n'est pas vide, on charge son contenu
        if path.exists() and path.stat().st_size > 0:
            with open(path, 'r', encoding="utf-8") as f:
                data = json.load(f)
        else:
            # Sinon on part d'un dictionnaire vide
            data = {}

        # Ajoute la base courante avec une clé numérique incrémentale
        data[str(len(data))] = dict(dbName = self.dbName, dbHost = self.dbHost, dbPort = self.dbPort)

        # Réécrit le dictionnaire mis à jour dans le fichier JSON
        with open(json_file, 'w', encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def isConnectable(self, showError: bool = False) -> tuple[bool, OperationalError | None]:
        # Teste si la base est joignable en exécutant une requête simple
        engine = create_engine(self.makePostgresqlURL())
        try:
            # Ouvre une connexion et exécute "SELECT 1" pour valider la liaison
            with engine.connect() as conn:
                conn.execute(text("SELECT 1;"))
            return (True, None)
        except OperationalError as e:
            # En cas d'erreur, renvoie l'exception si le paramètre est activé
            if showError:
                return (False, e)
            return (False, None)
