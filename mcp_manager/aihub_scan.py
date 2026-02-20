from pathlib import Path

DOC_EXTS = {".pdf", ".md", ".docx", ".pptx", ".txt"}
CODE_EXTS = {".py", ".ipynb", ".js", ".ts", ".go", ".rs"}
TOOL_EXTS = {".exe", ".msi", ".zip", ".7z", ".bat", ".ps1"}
DATA_EXTS = {".csv", ".parquet", ".jsonl"}


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


def _detect_family(text, families):
    for family, keywords in families.items():
        if _match_any(text, keywords):
            return family
    return None


def classify_ai_path(path, rules):
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

    if _match_any(text, rules.get("ai_keywords", [])):
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
        match = classify_ai_path(f, rules)
        if not match:
            continue
        category, family, matched_rules = match
        plan.append({
            "path": str(f),
            "category": category,
            "family": family,
            "matched_rules": matched_rules,
        })
    return plan
