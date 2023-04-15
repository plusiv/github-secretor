from dotenv import dotenv_values
import requests
import json
from pathlib import Path
from typing import List
from collections import ChainMap

def parse_secrets(keys: list = [], values: list = [])->List[tuple]:
    return list(zip(keys, values))

def parse_env_files(paths: List[Path]) -> List[tuple]:
    # Creates a List of dicts of env values 
    key_values = list(map(dotenv_values,paths))

    # Merges all dicts using the built-in module ChainMap.
    # To understand why ChainMap was used instead of implementing
    # some straightforward logic with dict.update()
    # see https://stackoverflow.com/questions/23392976/what-is-the-purpose-of-collections-chainmap
    key_values = dict(ChainMap(*key_values))

    # Return a list of tuples
    return list(key_values.items())

def get_content_from_file(path: Path) -> list:
    content = ''
    with path.open() as f:
        content = f.readlines()

    return content

def http_exception_handler(func) -> callable:
    def inner_function(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except requests.ConnectionError as ce:
            print('A connection error has occured: ', ce)
        except requests.HTTPError as he:
            print('Unssuccesful response from Github: ', he)
        except requests.Timeout as te:
            print('Operation timeout: ', te)
        except requests.TooManyRedirects as tmre:
            print('Too many redirects from Github resource: ', tmre)

    return inner_function

def get_help_info(path: Path, section: str = 'general') -> dict:
    help_obj = dict()
    with path.open() as f:
        helps = json.load(f)
        return helps.get(section)


