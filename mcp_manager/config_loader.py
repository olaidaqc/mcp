import json
from pathlib import Path


def load_commands(path: str):
    p = Path(path)
    with p.open("r", encoding="utf-8") as f:
        return json.load(f)
