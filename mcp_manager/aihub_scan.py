from pathlib import Path

DOC_EXTS = {".pdf", ".md", ".docx", ".pptx", ".txt"}
CODE_EXTS = {".py", ".ipynb", ".js", ".ts", ".go", ".rs"}
TOOL_EXTS = {".exe", ".msi", ".zip", ".7z", ".bat", ".ps1"}
DATA_EXTS = {".csv", ".parquet", ".jsonl"}
TEXT_EXTS = {
    ".txt", ".md", ".json", ".yaml", ".yml", ".toml",
    ".csv", ".jsonl",
    ".py", ".ipynb", ".js", ".ts", ".go", ".rs",
    ".ps1", ".bat", ".sh",
}


def _match_any(text, keywords):
    return any(k in text for k in keywords)


def _is_excluded(path, rules):
    text = str(path).lower().replace("/", "\\")
    ext = Path(path).suffix.lower()
    if ext in set(rules.get("exclude_exts", [])):
        return True
    for pat in rules.get("exclude_paths", []):
        if pat.lower() in text:
            return True
    return False


def _is_text_file(path, rules):
    ext = Path(path).suffix.lower()
    text_exts = set(rules.get("text_exts", []))
    if text_exts:
        return ext in text_exts
    return ext in TEXT_EXTS


def _match_content_keywords(path, rules):
    if not _is_text_file(path, rules):
        return False
    try:
        size = Path(path).stat().st_size
    except OSError:
        return False
    max_bytes = int(rules.get("text_max_bytes", 2 * 1024 * 1024))
    if size > max_bytes:
        return False
    keywords = rules.get("content_keywords") or rules.get("ai_keywords", [])
    if not keywords:
        return False
    try:
        text = Path(path).read_text(encoding="utf-8", errors="ignore").lower()
    except OSError:
        return False
    return any(k in text for k in keywords)


def _detect_family(text, families):
    for family, keywords in families.items():
        if _match_any(text, keywords):
            return family
    return None


def classify_ai_path(path, rules, content_match=False):
    text = str(path).lower()
    ext = Path(path).suffix.lower()
    matched = []

    if ext in set(rules.get("core_exts", [])):
        matched.append(ext)
        family = _detect_family(text, rules.get("model_families", {}))
        return "Models", family, matched

    if _match_any(text, rules.get("plugin_keywords", [])):
        matched.append("plugin_keywords")
        return "Plugins", None, matched

    if _match_any(text, rules.get("tool_keywords", [])):
        matched.append("tool_keywords")
        family = _detect_family(text, rules.get("tool_families", {}))
        return "Tools", family, matched

    if ext in DATA_EXTS and _match_any(text, rules.get("dataset_keywords", [])):
        matched.append("dataset_keywords")
        return "Datasets", None, matched

    if ext in DOC_EXTS and _match_any(text, rules.get("doc_keywords", [])):
        matched.append("doc_keywords")
        return "Docs", None, matched

    if ext in CODE_EXTS and _match_any(text, rules.get("code_keywords", [])):
        matched.append("code_keywords")
        return "Code", None, matched

    if _match_any(text, rules.get("ai_keywords", [])) or content_match:
        matched.append("ai_keywords")
        if ext in DOC_EXTS:
            return "Docs", None, matched
        if ext in CODE_EXTS:
            return "Code", None, matched
        if ext in DATA_EXTS:
            return "Datasets", None, matched
        if ext in TOOL_EXTS:
            return "Tools", None, matched
        return "_incoming", None, matched

    return None


def build_plan(files, rules, root):
    plan = []
    for f in files:
        if _is_excluded(f, rules):
            continue
        content_match = _match_content_keywords(f, rules)
        match = classify_ai_path(f, rules, content_match=content_match)
        if not match:
            continue
        category, family, matched_rules = match
        if content_match and "content_keywords" not in matched_rules:
            matched_rules = list(matched_rules) + ["content_keywords"]
        size_bytes = 0
        try:
            size_bytes = Path(f).stat().st_size
        except OSError:
            size_bytes = 0
        plan.append({
            "path": str(f),
            "category": category,
            "family": family,
            "matched_rules": matched_rules,
            "size_bytes": size_bytes,
        })
    return plan
