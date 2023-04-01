import configparser
import requests
import json
from pathlib import Path

def parse_ini(config_file) -> list:
    config = configparser.ConfigParser()
    config.read_file(config_file)

    sections = config.sections()

    secrets = []
    if sections:
        for section in sections:
            for item in config.items(section):
                secrets.append([item[0].upper(), item[1]])

    return secrets

def get_content_from_file(path: Path):
    content = ''
    with path.open() as f:
        content = f.readlines()

    return content

def http_exception_handler(func):
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

def get_help_info(path: Path, section: str = 'general'):
    help_obj = dict()
    with path.open() as f:
        helps = json.load(f)
        return helps.get(section)


