from .paths import ProjectPaths


def get_log_path():
    return ProjectPaths().repo_root / "runtime.log"
