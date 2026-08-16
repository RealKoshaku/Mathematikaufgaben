# Import of the Rich console for colored terminal output
from collections.abc import Callable
from random import choice

import questionary as quest
from rich.color import ANSI_COLOR_NAMES
from rich.console import Console

import firstMenu as fM


def random_color() -> str:
    """Return a random Rich color name, excluding near-black and white ones for readability."""
    return choice([name for name in ANSI_COLOR_NAMES if name not in {"white", "black", "gray0", "grey0", "gray3", "grey3", "gray7", "grey7"}])

def banner(console: Console) -> None:
    """
    Print banner of k-Aufgaben software with the connection state of the DB.
    """
    # Pick one random color for the whole banner
    color = random_color()
    # Display the k-Aufgaben ASCII logo
    console.print(f"[{color}]    __                     ____            __             [/{color}]")
    console.print(f"[{color}]   / /__      ____ ___  __/ __/___ _____ _/ /_  ___  ____ [/{color}]")
    console.print(f"[{color}]  / //_/_____/ __ `/ / / / /_/ __ `/ __ `/ __ \\/ _ \\/ __ \\ [/{color}]")
    console.print(f"[{color}] / ,< /_____/ /_/ / /_/ / __/ /_/ / /_/ / /_/ /  __/ / / /[/{color}]")
    console.print(f"[{color}]/_/|_|      \\__,_/\\__,_/_/  \\__, /\\__,_/_.___/\\___/_/ /_/ [/{color}]")
    # Display the author credit
    console.print(f"[{color}]by Adahy de Plas           /____/[/{color}]\n")

def main(console: Console, json_file: str):
    """Entry point: print the banner and run the main application loop."""
    # Map each menu label to the function handling it
    COMMANDS: dict[str, Callable] = {
        "Connect to a new database" : fM.connectToNewDB,
        "Connect to a saved database" : fM.connectToSavedDB,
        "Recreate database schema" : fM.recreateDBSchema,
        "Exit" : lambda: None
    }
    # Loop forever so the user can keep choosing actions
    while True:
        # Let the user pick one of the available commands
        asking = quest.select(
            "Select an option :",
            choices=[key for key in COMMANDS]
            ).unsafe_ask()

        # Run the function associated with the chosen command
        if asking == "Exit":
            console.print("[bold blue]Goodbye ![/]\n")
            break
        else:
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
    except Exception as e:
        # Show the real error instead of silently swallowing it
        console.print(f"[bold red]An error occured : {e}[/]\n")
