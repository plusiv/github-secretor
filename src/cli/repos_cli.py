import typer
from . import GENERAL_HELPS, REPOS_HELPS, validations, printing as print
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

        values_from_file: Optional[Path] = typer.Option(None, \
                callback=validations.file_exists, \
                help=help_info(GENERAL_HELPS, 'values-from-file')[0], \
                rich_help_panel=help_info(GENERAL_HELPS, 'values-from-file')[1]),

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

    # Construct secrets names and values if not in an env file
    else:
        # Set secret names
        if not secret_names:
            secret_names = typer.prompt("Insert secrets names separated by comma (',')")
            secret_names = secret_names.split(',')

        if values_from_file:
            secret_values = utils.get_content_from_file(value_from_file)
            # Validations for the len of the the secrets names and values
            if not validations.secrets_size(secret_names, secret_values):
                print.error("Secret names and values doesn't have the same length")
                raise typer.Abort()
                
        # Prompt values if there'snt a file with values
        else:
            secret_values = []
            # Check if there's repeated duplicated secret names
            if validations.non_duplicated(secret_names):
                for secret_name in secret_names:
                    secret_value = typer.prompt(f"Insert secret value for {secret_name}", hide_input=True)
                    secrets_values.append(secret_value)
            else:
                print.error("Unable to add duplicated values")
                raise typer.Abort()

        secrets = utils.parse_secrets(secret_names, secret_values)

    try:
        rsm = secretor.RepoSecretsManager(state.owner, state.repo_name, state.token)
        rsm.push_to_github(secrets)
        print.success(f"Secrets successfully pushed to Github. Open https://github.com/{state.owner}/{state.repo_name}/settings/secrets/actions to validate.")
    
    except Exception as e:
        print.error(f"An error has occured while pusing secrets to Github. {e}", error_type="fatal")
        raise typer.Abort()


@app.command("get")
def get_secrets(
        get_all_secrets: bool = typer.Option(None, \
                '--all', '-a', \
                help=help_info(GENERAL_HELPS, 'get_all_secrets')[0], \
                rich_help_panel=help_info(GENERAL_HELPS, 'get_all_secrets')[1]),
        secret_names: Optional[List[str]] = typer.Option(None, \
                '--secret-name', '-n', \
                help=help_info(GENERAL_HELPS, 'secret-name')[0], \
                rich_help_panel=help_info(GENERAL_HELPS, 'secret-name')[1]),
        ):
    
        rsm = secretor.RepoSecretsManager(state.owner, state.repo_name, state.token)
        if get_all_secrets:
            secrets = rsm.get_all_secrets()
            print.secrets(secrets)
        else:
            for secret_name in secret_names:
                secret = rsm.get_secret(secret_name)
                if not secret:
                    print.error(f"Seems like {secret_name} does not exist on the repository {state.repo_name}")
                    continue
                print.secrets([secret])
                
    
