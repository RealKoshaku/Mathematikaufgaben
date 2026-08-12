from rich.console import Console


def banner(console: Console) -> None:
    """
    Print banner of k-Aufgaben software with the connection state of the DB.
    """
    console.print("[green]    __                     ____            __             [/green]")
    console.print("[green]   / /__      ____ ___  __/ __/___ _____ _/ /_  ___  ____ [/green]")
    console.print("[green]  / //_/_____/ __ `/ / / / /_/ __ `/ __ `/ __ \\/ _ \\/ __ \\ [/green]")
    console.print("[green] / ,< /_____/ /_/ / /_/ / __/ /_/ / /_/ / /_/ /  __/ / / /[/green]")
    console.print("[green]/_/|_|      \\__,_/\\__,_/_/  \\__, /\\__,_/_.___/\\___/_/ /_/ [/green]")
    console.print("[green]by Adahy de Plas           /____/[/green]\n")

def main():
    """Entry point: print the banner and run the main application loop."""
    pass

if __name__ == '__main__':
    console = Console()
    try:
        banner(console)
        while True:
            continue
    except KeyboardInterrupt:
        console.print("[bold red]\nUser pressed Ctrl+C. Stopping k-Aufgaben.")