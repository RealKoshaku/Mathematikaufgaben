# Import of the Rich console for colored terminal output
from rich.console import Console


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

def main():
    """Entry point: print the banner and run the main application loop."""
    # TODO: implement the main application loop
    pass

if __name__ == '__main__':
    # Create a Rich console for all program output
    console = Console()
    try:
        # Display the banner then stay in a loop (awaiting implementation)
        banner(console)
        while True:
            continue
    except KeyboardInterrupt:
        # Clean exit from the application on Ctrl+C
        console.print("[bold red]\nUser pressed Ctrl+C. Stopping k-Aufgaben.")
