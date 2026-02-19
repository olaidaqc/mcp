from dataclasses import dataclass
import subprocess


@dataclass
class CommandResult:
    exit_code: int
    stdout: str
    stderr: str


class CommandRunner:
    def run(self, args, timeout=60):
        proc = subprocess.run(
            args,
            capture_output=True,
            text=True,
            timeout=timeout,
            errors="replace",
        )
        return CommandResult(proc.returncode, proc.stdout, proc.stderr)
