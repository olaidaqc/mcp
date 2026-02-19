from dataclasses import dataclass
from pathlib import Path


@dataclass
class ProjectPaths:
    repo_root: Path = Path(__file__).resolve().parents[1]
    user_home: Path = Path.home()
