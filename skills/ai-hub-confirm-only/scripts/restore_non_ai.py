import argparse
import json
from pathlib import Path
import shutil
from datetime import datetime


def load_rules(hub):
    rules_path = hub / "_rules" / "rules.json"
    if rules_path.exists():
        return json.loads(rules_path.read_text(encoding="utf-8"))
    return {}


def restore_non_ai(hub, keep, dry_run):
    hub = Path(hub)
    index_path = hub / "_reports" / "index.jsonl"
    if not index_path.exists():
        raise SystemExit(f"index.jsonl missing at {index_path}")

    rules = load_rules(hub)
    exclude_exts = set(rules.get("exclude_exts", []))
    report_path = hub / "_reports" / f"restore-{datetime.utcnow().strftime('%Y%m%d-%H%M%S')}Z.jsonl"

    restored = 0
    missing = 0
    conflicts = 0
    kept = 0

    with index_path.open("r", encoding="utf-8") as f, report_path.open("w", encoding="utf-8") as out:
        for line in f:
            line = line.strip()
            if not line:
                continue
            data = json.loads(line)
            target = Path(data["target_path"])
            original = Path(data["original_path"])
            category = target.parent.name
            ext = target.suffix.lower()

            should_restore = category not in keep or ext in exclude_exts
            if not should_restore:
                kept += 1
                continue
            if not target.exists():
                missing += 1
                continue

            original.parent.mkdir(parents=True, exist_ok=True)
            final = original
            if final.exists():
                conflicts += 1
                i = 1
                while True:
                    final = original.with_name(f"{original.stem}_restored{i}{original.suffix}")
                    if not final.exists():
                        break
                    i += 1
            if not dry_run:
                shutil.move(str(target), str(final))
            restored += 1
            out.write(json.dumps({
                "from": str(target),
                "to": str(final),
                "original_path": str(original),
                "dry_run": dry_run,
            }, ensure_ascii=False) + "\n")

    return restored, kept, missing, conflicts, report_path


def main():
    parser = argparse.ArgumentParser(description="Restore non-AI files from AI-Hub index.jsonl")
    parser.add_argument("--hub", default="C:/Users/11918/AI-Hub", help="AI-Hub root path")
    parser.add_argument(
        "--keep",
        default="Models,Tools,Plugins,Datasets,Docs,Code",
        help="Comma-separated categories to keep in AI-Hub",
    )
    parser.add_argument("--dry-run", action="store_true", help="Do not move files")
    args = parser.parse_args()

    keep = {item.strip() for item in args.keep.split(",") if item.strip()}
    restored, kept, missing, conflicts, report = restore_non_ai(args.hub, keep, args.dry_run)
    print(f"restored {restored}")
    print(f"kept {kept}")
    print(f"missing {missing}")
    print(f"conflicts {conflicts}")
    print(f"report {report}")


if __name__ == "__main__":
    main()
