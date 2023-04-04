import typer
from . import GENERAL_HELPS, REPOS_HELPS
from typing import Optional, List
from utils import utils
from pathlib import Path
from secretor import secretor

# Instance Typer Object
app = typer.Typer()

# Helper to get a tuple with help in first position 
# and rich help in second position
help_info = lambda section, help_obj: (section.get(help_obj).get('help'), section.get(help_obj).get('rich_help_panel')) if section.get(help_obj) else (None, None)

@app.command("add")
def add_secret(
        owner: str = typer.Option(..., \
                prompt="Insert Owner", \
                envvar='GIT_USERNAME', \
                help=help_info(GENERAL_HELPS, 'owner')[0], \
                rich_help_panel=help_info(GENERAL_HELPS, 'owner')[1]),

        repo_name: str = typer.Option(..., \
                prompt="Insert repository name", \
                help=help_info(GENERAL_HELPS, 'repo-name')[0], \
                rich_help_panel=help_info(GENERAL_HELPS, 'repo-name')[1]),

        token: str = typer.Option("", \
                '--token', '-t', \
                help=help_info(GENERAL_HELPS, 'token')[0], \
                rich_help_panel= help_info(GENERAL_HELPS, 'token')[1]),

        token_file: Optional[Path] = typer.Option("", envvar='GIT_TOKEN_PATH', \
                help=help_info(GENERAL_HELPS, 'token-file')[0], \
                rich_help_panel=help_info(GENERAL_HELPS, 'token-file')[1]),

        secret_names: Optional[List[str]] = typer.Option(None, \
                '--secret-name', '-n', \
                help=help_info(GENERAL_HELPS, 'secret-name')[0], \
                rich_help_panel=help_info(GENERAL_HELPS, 'secret-name')[1]),

        value_from_file: Optional[Path] = typer.Option(None, \
                help=help_info(GENERAL_HELPS, 'value-from-file')[0], \
                rich_help_panel=help_info(GENERAL_HELPS, 'value-from-file')[1]),

        env_file: Optional[Path] = typer.Option(None, \
                '--env-file', '-f', \
                help=help_info(GENERAL_HELPS, 'env-file')[0], \
                rich_help_panel=help_info(GENERAL_HELPS, 'env-file')[1]),

        replace: bool = typer.Option(False, \
                help=help_info(GENERAL_HELPS, 'replace')[0], \
                rich_help_panel=help_info(GENERAL_HELPS, 'replace')[1])
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

