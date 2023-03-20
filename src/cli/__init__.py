from utils import utils
from os import path
from pathlib import Path
HELP_TEXT_FILE = Path(path.dirname(__file__)) / 'help_text.json'


GENERAL_HELPS = utils.get_help_info(HELP_TEXT_FILE, 'general')
REPOS_HELPS = utils.get_help_info(HELP_TEXT_FILE, 'repos')
ORGS_HELPS = utils.get_help_info(HELP_TEXT_FILE, 'orgs')
