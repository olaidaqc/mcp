from pathlib import Path


class LogSink:
    def __init__(self, path: Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def write(self, text: str):
        with self.path.open("a", encoding="utf-8") as f:
            f.write(text + "\n")
