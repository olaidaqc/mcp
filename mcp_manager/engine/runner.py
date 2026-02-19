import subprocess
from dataclasses import dataclass


@dataclass
class RunResult:
    exit_code: int
    output: str


class CommandRunner:
    def __init__(self, timeout_sec: int = 60):
        self.timeout_sec = timeout_sec

    def run(self, command: str) -> RunResult:
        proc = subprocess.run(
            ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", command],
            capture_output=True,
            text=True,
            timeout=self.timeout_sec,
        )
        output = (proc.stdout or "") + (proc.stderr or "")
        return RunResult(proc.returncode, output)
