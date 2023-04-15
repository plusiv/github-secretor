from rich import print

def success(message: str = ""):
    print(f":white_check_mark:[bold green]Success:[/bold green] {message}.")


def error(message: str="An error has occured", error_type: str = "normal") -> None:
    if error_type == "fatal":
        print(f":boom::boom:[bold red]Fatal error:[/bold red] {message}.")
        return

    print(f":boom:[bold red]Error:[/bold red] {message}.")


def warning(message: str="") -> None:
    print(f":warning:[bold orange]Warning:[/bold red] {message}.")


def debug(message: str="") -> None:
    print(f"{message}.")
