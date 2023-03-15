import typer
from typing import Optional, List
from pathlib import Path
from utils import utils
from secretor import secretor

app = typer.Typer()

@app.command("add")
def add_secret(
        secret_names: Optional[List[str]] = typer.Option(None, '--secret-name', '-n'),
        value_from_file: Optional[Path] = typer.Option(None),
        env_file: Optional[Path] = typer.Option(None, '--env-file', '-f'),
        owner: str = typer.Option(..., prompt="Insert Owner", envvar='GIT_USERNAME'),
        repo_name: str = typer.Option(..., prompt="Insert repository name"),
        token: str = typer.Option("", '--token', '-t'),
        token_file: str = typer.Option("", envvar='GIT_TOKEN_FILE'),
        replace: bool = False
        ):

    secrets = []

    # Set github access token if not passed
    if not token and not token_file:
        token = typer.prompt("Insert Github Access Token", hide_input=True)

    # Set secret names
    if not secret_names:
        secret_names = typer.prompt("Insert secret name")
        secret_names = secret_names.split(',')

    if value_from_file:
        secret_value = utils.get_content_from_file(value_from_file)

    else:
        for secret_name in secret_names:
            secret_value = typer.prompt(f"Insert secret value for {secret_name}", hide_input=True)
            secrets.append((secret_name, secret_value))


    rsm = secretor.RepoSecretsManager(owner, repo_name, token, secrets)
    rsm.push_to_github()

    print(secrets)
