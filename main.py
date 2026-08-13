# Import de la console Rich pour un affichage coloré dans le terminal
from rich.console import Console


def banner(console: Console) -> None:
    """
    Print banner of k-Aufgaben software with the connection state of the DB.
    """
    # Affiche le logo ASCII de k-Aufgaben
    console.print("[green]    __                     ____            __             [/green]")
    console.print("[green]   / /__      ____ ___  __/ __/___ _____ _/ /_  ___  ____ [/green]")
    console.print("[green]  / //_/_____/ __ `/ / / / /_/ __ `/ __ `/ __ \\/ _ \\/ __ \\ [/green]")
    console.print("[green] / ,< /_____/ /_/ / /_/ / __/ /_/ / /_/ / /_/ /  __/ / / /[/green]")
    console.print("[green]/_/|_|      \\__,_/\\__,_/_/  \\__, /\\__,_/_.___/\\___/_/ /_/ [/green]")
    # Affiche le crédit de l'auteur
    console.print("[green]by Adahy de Plas           /____/[/green]\n")

def main():
    """Entry point: print the banner and run the main application loop."""
    # TODO: implémenter la boucle principale de l'application
    pass

if __name__ == '__main__':
    # Crée une console Rich pour tous les affichages du programme
    console = Console()
    try:
        # Affiche la bannière puis reste en boucle (en attente d'implémentation)
        banner(console)
        while True:
            continue
    except KeyboardInterrupt:
        # Arrêt propre de l'application lors d'un Ctrl+C
        console.print("[bold red]\nUser pressed Ctrl+C. Stopping k-Aufgaben.")
