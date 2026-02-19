import subprocess
import time
from dataclasses import dataclass
from typing import Callable, Optional


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
            encoding="utf-8",
            errors="replace",
            timeout=self.timeout_sec,
        )
        output = (proc.stdout or "") + (proc.stderr or "")
        return RunResult(proc.returncode, output)

    def run_stream(self, command: str, on_output: Optional[Callable[[str], None]] = None) -> RunResult:
        proc = subprocess.Popen(
            ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", command],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace",
            bufsize=1,
        )
        output_chunks = []
        start = time.monotonic()
        try:
            while True:
                if proc.stdout is None:
                    break
                line = proc.stdout.readline()
                if line:
                    output_chunks.append(line)
                    if on_output:
                        on_output(line.rstrip("\n"))
                else:
                    if proc.poll() is not None:
                        break
                if time.monotonic() - start > self.timeout_sec:
                    proc.kill()
                    output_chunks.append(f"[timeout after {self.timeout_sec}s]\n")
                    break
        finally:
            if proc.stdout is not None:
                proc.stdout.close()
        exit_code = proc.wait() if proc.returncode is None else proc.returncode
        return RunResult(exit_code, "".join(output_chunks))
