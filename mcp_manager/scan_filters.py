from pathlib import Path
import os


def _norm(p):
    return str(p).replace("\\", "/").lower()


def is_project_dir(path, markers):
    path = Path(path)
    if (path / ".git").exists():
        return True
    for marker in markers:
        if "*" in marker:
            if any(path.glob(marker)):
                return True
        else:
            if (path / marker).exists():
                return True
    return False


def should_exclude_path(path, rules, user_home):
    norm = _norm(path)
    fragments = [f.lower() for f in rules.get("exclude_path_fragments", [])]
    for frag in fragments:
        if frag in norm:
            return True
    return False


def _is_excluded_dir(path, rules, user_home):
    name = Path(path).name.lower()
    if name in {n.lower() for n in rules.get("exclude_dir_names", [])}:
        return True
    return should_exclude_path(path, rules, user_home)


def iter_scan_files(roots, rules, user_home):
    markers = rules.get("project_markers", [])
    for root in roots:
        root = Path(root)
        if not root.exists():
            continue
        for dirpath, dirnames, filenames in os.walk(root):
            dirpath = Path(dirpath)
            pruned = []
            for d in list(dirnames):
                candidate = dirpath / d
                if _is_excluded_dir(candidate, rules, user_home):
                    continue
                if is_project_dir(candidate, markers):
                    continue
                pruned.append(d)
            dirnames[:] = pruned
            for fname in filenames:
                yield dirpath / fname
