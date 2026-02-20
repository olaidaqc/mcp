from pathlib import Path
import json
import re

CATEGORIES = ["Models", "Tools", "Plugins", "Datasets", "Docs", "Code"]


def _learned_path(root):
    return Path(root) / "_rules" / "learned_keywords.json"


def _default_learned():
    return {name: [] for name in CATEGORIES}


def load_learned(root):
    path = _learned_path(root)
    if not path.exists():
        return _default_learned()
    return json.loads(path.read_text(encoding="utf-8"))


def save_learned(root, data):
    path = _learned_path(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def extract_tokens(path):
    text = str(path).lower()
    tokens = re.split(r"[^a-z0-9]+", text)
    cleaned = []
    for token in tokens:
        if len(token) < 3:
            continue
        if token.isdigit():
            continue
        cleaned.append(token)
    return cleaned


def learn_from_confirmed(root, items):
    learned = load_learned(root)
    for item in items:
        category = item.get("category")
        if category not in learned:
            learned[category] = []
        tokens = extract_tokens(item.get("path", ""))
        current = set(learned.get(category, []))
        current.update(tokens)
        learned[category] = sorted(current)
    save_learned(root, learned)
