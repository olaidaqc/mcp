from pathlib import Path

DOC_EXTS = {".pdf", ".md", ".docx", ".pptx", ".txt"}
CODE_EXTS = {".py", ".ipynb", ".js", ".ts", ".go", ".rs"}
TOOL_EXTS = {".exe", ".msi", ".zip", ".7z", ".bat", ".ps1"}
DATA_EXTS = {".csv", ".parquet", ".jsonl"}


def _match_keyword(path, rules):
    text = str(path).lower()
    return any(k in text for k in rules.get("keywords", []))


def build_plan(files, rules, root):
    plan = []
    for f in files:
        path = Path(f)
        ext = path.suffix.lower()
        if ext in set(rules.get("core_exts", [])):
            category = "Models"
        elif ext in DOC_EXTS and _match_keyword(path, rules):
            category = "Docs"
        elif ext in CODE_EXTS and _match_keyword(path, rules):
            category = "Code"
        elif ext in TOOL_EXTS and _match_keyword(path, rules):
            category = "Tools"
        elif ext in DATA_EXTS and _match_keyword(path, rules):
            category = "Datasets"
        else:
            category = "_incoming"
        plan.append({"path": str(path), "category": category})
    return plan
