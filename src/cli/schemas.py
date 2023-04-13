from dataclasses import dataclass
from typing import Optional
from pathlib import Path

@dataclass
class ReposCommon:
    owner: str = ""
    repo_name: str = ""
    token: str  = ""
    token_file: Optional[Path] = None
