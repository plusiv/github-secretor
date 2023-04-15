import typer
import .validations
from . import GENERAL_HELPS, REPOS_HELPS
from rich import print
from typing import Optional, List
from utils import utils
from pathlib import Path
from secretor import secretor

# Instance Typer Object
app = typer.Typer()

# Helper to get a tuple with help in first position 
# and rich help in second position
help_info = lambda section, help_obj: (section.get(help_obj).get('help'), section.get(help_obj).get('rich_help_panel')) if section.get(help_obj) else (None, None)

state = validations.ReposCommon()

@app.callback()
def main(
        owner: str = typer.Option("", \
                '--owner', '-o', \
                envvar='GIT_USERNAME', \
                help=help_info(REPOS_HELPS, 'owner')[0], \
                rich_help_panel=help_info(REPOS_HELPS, 'owner')[1]),

        repo_name: str = typer.Option("", \
                '--repo-name', '-r', \
                help=help_info(REPOS_HELPS, 'repo-name')[0], \
                rich_help_panel=help_info(REPOS_HELPS, 'repo-name')[1]),

        token: str = typer.Option("", \
                '--token', '-t', \
                help=help_info(GENERAL_HELPS, 'token')[0], \
                rich_help_panel= help_info(GENERAL_HELPS, 'token')[1]),

        token_file: Optional[Path] = typer.Option(None, \
                '--token-file', '-T', \
                envvar='GIT_TOKEN_PATH', \
                callback=validations.file_exists, \
                help=help_info(GENERAL_HELPS, 'token-file')[0], \
                rich_help_panel=help_info(GENERAL_HELPS, 'token-file')[1]),
        ):

    state.owner = owner
    state.repo_name = repo_name
    state.token = token
    state.token_file = token_file

    # Run validations
    validations.common_options(state=state)


@app.command("add")
def add_secret(
        secret_names: Optional[List[str]] = typer.Option(None, \
                '--secret-name', '-n', \
                help=help_info(GENERAL_HELPS, 'secret-name')[0], \
                rich_help_panel=help_info(GENERAL_HELPS, 'secret-name')[1]),

        value_from_file: Optional[Path] = typer.Option(None, \
                callback=validations.file_exists, \
                help=help_info(GENERAL_HELPS, 'value-from-file')[0], \
                rich_help_panel=help_info(GENERAL_HELPS, 'value-from-file')[1]),

        env_files: Optional[List[Path]] = typer.Option(None, \
                '--env-file', '-f', \
                callback=validations.file_exists, \
                help=help_info(GENERAL_HELPS, 'env-file')[0], \
                rich_help_panel=help_info(GENERAL_HELPS, 'env-file')[1]),

        replace: bool = typer.Option(False, \
                help=help_info(GENERAL_HELPS, 'replace')[0], \
                rich_help_panel=help_info(GENERAL_HELPS, 'replace')[1])
        ):

    secrets = []

    if env_files:
        secrets = utils.parse_env_files(env_files)

    # Construct secrets names and values if not in a env file
    else:
        # Set secret names
        if not secret_names:
            secret_names = typer.prompt("Insert secrets names separated by comma (',')")
            secret_names = secret_names.split(',')

        if value_from_file:
            secret_values = utils.get_content_from_file(value_from_file)
            # TODO: Validations for the len of the the secrets names and values
                
        # Prompt values if there'snt a file with values
        else:
            # Check if there's repeated duplicated secret names
            if validations.non_duplicated(secret_names):
                for secret_name in secret_names:
                    secret_value = typer.prompt(f"Insert secret value for {secret_name}", hide_input=True)
                    secrets.append((secret_name, secret_value))
            else:
                print(":boom:[bold red]Error:[/bold red] Unable to add duplicated values.")
                raise typer.Abort()

    rsm = secretor.RepoSecretsManager(state.owner, state.repo_name, state.token, secrets)
    rsm.push_to_github()

