import typer
from . import repos_cli
from rich.console import Console

err_console = Console(stderr=True)
app = typer.Typer()

# Add sub commands
app.add_typer(repos_cli.app, name='repos')
app.add_typer(repos_cli.app, name='orgs')
