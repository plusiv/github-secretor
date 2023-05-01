from rich import print

def secrets(secrets: list = []) -> None:
    for secret in secrets:
        name = secret.get('name')
        created_at = secret.get('created_at')
        updated_at = secret.get('updated_at')
        print(f":lock: [bold white]Secret Name: [/bold white]{name}")
        print(f":stopwatch: [bold white]Created at: [/bold white]{created_at}")
        print(f":stopwatch: [bold white]Updated at: [/bold white]{updated_at}")
        print("\n")

def deleted_secret(secret_name: str = "") -> None:
        print(f":bomb: [bold red]Secret deleted: [/bold red] {secret_name}.")

def success(message: str = "") -> None:
    print(f":white_check_mark: [bold green]Success:[/bold green] {message}.")

def error(message: str="An error has occured", error_type: str = "normal") -> None:
    if error_type == "fatal":
        print(f":boom::boom: [bold red]Fatal error:[/bold red] {message}.")
        return

    print(f":boom: [bold red]Error:[/bold red] {message}.")

def warning(message: str="") -> None:
    print(f":warning: [bold orange]Warning:[/bold red] {message}.")

def debug(message: str="") -> None:
    print(f"{message}.")
