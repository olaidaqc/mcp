from pathlib import Path
import hashlib
import json
import shutil
from datetime import datetime


def _sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def apply_plan(plan, root):
    root = Path(root)
    (root / "_reports").mkdir(parents=True, exist_ok=True)
    index_path = root / "_reports" / "index.jsonl"
    for item in plan:
        src = Path(item["path"])
        category = item["category"]
        dest_dir = root / category
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest = dest_dir / src.name
        if dest.exists():
            dest = dest_dir / f"{src.stem}_dup1{src.suffix}"
        shutil.move(str(src), str(dest))
        sidecar = dest_dir / f"{dest.name}.aiinfo.txt"
        data = {
            "original_path": str(src),
            "target_path": str(dest),
            "size_bytes": dest.stat().st_size,
            "sha256": _sha256(dest),
            "matched_rules": item.get("matched_rules", []),
            "detected_family": item.get("family"),
            "moved_at": datetime.utcnow().isoformat() + "Z",
        }
        sidecar.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        with open(index_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(data, ensure_ascii=False) + "\n")
