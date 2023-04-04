from dataclasses import dataclass

@dataclass
class ReposCommon:
    owner: str = ""
    repository_name: str = ""
    token: str  = ""
    token_file: str = ""
