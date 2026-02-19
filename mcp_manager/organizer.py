from pathlib import Path


def classify_path(path):
    ext = Path(path).suffix.lower()
    if ext in {".bat", ".sh", ".ps1"}:
        return "scripts"
    if ext in {".json", ".yml", ".yaml"}:
        return "config"
    if ext in {".log", ".txt"}:
        return "logs"
    return "other"
