import typer
import os
from rich import print
from pathlib import Path
from .schemas import ReposCommon

def validate_common_options(state: ReposCommon)->bool:
    # Set owner if passed
    if not state.owner:
        state.owner = typer.prompt("Insert repository owner")

    # Set repo name if passed
    if not state.repo_name:
        state.repo_name = typer.prompt("Insert repository name")

    if not state.repo_name or not state.owner:
        print(":boom:[bold red]Error:[/bold red] Repository name ")
        raise typer.Abort()

    return True

def validate_non_duplicated(elements: list)->bool:
    elements_set = set()
    for element in elements:
        elements_set.add(element)
    return len(elements_set) == len(elements)

def validate_file_exists(path_to_file: Path)->Path:
    validation = os.path.isfile(str(path_to_file))
    if not validation:
        typer.BadParameter(f"{path_to_file} is not a valid path to file or not exist.")
    return path_to_file
