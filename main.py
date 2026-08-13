# Import of the Rich console for colored terminal output
from rich.console import Console
import questionary as quest
import firstMenu as fM
from collections.abc import Callable


def banner(console: Console) -> None:
    """
    Print banner of k-Aufgaben software with the connection state of the DB.
    """
    # Display the k-Aufgaben ASCII logo
    console.print("[green]    __                     ____            __             [/green]")
    console.print("[green]   / /__      ____ ___  __/ __/___ _____ _/ /_  ___  ____ [/green]")
    console.print("[green]  / //_/_____/ __ `/ / / / /_/ __ `/ __ `/ __ \\/ _ \\/ __ \\ [/green]")
    console.print("[green] / ,< /_____/ /_/ / /_/ / __/ /_/ / /_/ / /_/ /  __/ / / /[/green]")
    console.print("[green]/_/|_|      \\__,_/\\__,_/_/  \\__, /\\__,_/_.___/\\___/_/ /_/ [/green]")
    # Display the author credit
    console.print("[green]by Adahy de Plas           /____/[/green]\n")

def main(console: Console, json_file: str):
    """Entry point: print the banner and run the main application loop."""
    COMMANDS: dict[str, Callable] = {
        "Connect to a new database" : fM.connectToNewDB,
        "Connect to a saved database" : fM.connectToSavedDB,
        "Configure a database" : fM.configureDB,
        "exit" : fM.quit
    }
    while True:
        asking = quest.select(
            "Select an option :",
            choices=["Connect to a new database", "Connect to a saved databse", "Configure a database", "exit"]
            ).unsafe_ask()

        COMMANDS[asking](console, json_file)
        

if __name__ == '__main__':
    # Create a Rich console for all program output
    console: Console = Console()
    json_file: str = 'savedDB.json'
    try:
        # Display the banner then stay in a loop (awaiting implementation)
        banner(console)
        main(console, json_file)
    except KeyboardInterrupt:
        # Clean exit from the application on Ctrl+C
        console.print("[bold red]\nUser pressed Ctrl+C. Stopping k-Aufgaben.")
