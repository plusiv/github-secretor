import typer
from . import repos_cli
from rich.console import Console

err_console = Console(stderr=True)
app = typer.Typer()
app.add_typer(repos_cli.app, name='repos')
