import json
import os
from datetime import datetime
from pathlib import Path

from mcp_manager.recommender import dedupe_by_capability, pick_best
from mcp_manager.scanners.catalog import fetch_github
from mcp_manager.aihub_structure import ensure_structure


def _load_config():
    path = Path(__file__).resolve().parents[1] / "config" / "recommendations.json"
    return json.loads(path.read_text(encoding="utf-8"))


def _reports_dir(root):
    return Path(root) / "_reports"


def _normalize_repo(item):
    updated_days = item.get("updated_days")
    if updated_days is None:
        updated_days = 999
    return {
        "name": item.get("name") or item.get("full_name"),
        "html_url": item.get("html_url"),
        "description": item.get("description") or "",
        "topics": item.get("topics") or [],
        "stargazers_count": item.get("stargazers_count", 0),
        "updated_days": updated_days,
        "capability": item.get("capability"),
    }


def refresh_recommendations(hub_root=None, token=None, fetcher=fetch_github):
    hub_root = Path(hub_root) if hub_root else None
    token = token or os.environ.get("GITHUB_TOKEN")
    config = _load_config()
    domains = []
    for domain, spec in config.get("domains", {}).items():
        items = []
        for q in spec.get("queries", []):
            items.extend(fetcher(domain, q, token=token, max_items=config.get("max_results_per_query", 10)))
        normalized = [_normalize_repo(i) for i in items]
        for r in normalized:
            desc = (r.get("description") or "").lower()
            topics = " ".join(r.get("topics") or []).lower()
            if any(k in desc or k in topics for k in spec.get("capability_keywords", [])):
                r["capability"] = spec.get("capability_keywords", [None])[0]
        deduped = dedupe_by_capability(normalized)
        best, alternatives = pick_best(deduped)
        domains.append({"domain": domain, "best": best, "alternatives": alternatives})
    report = {"updated_at": datetime.utcnow().isoformat() + "Z", "domains": domains}
    if hub_root:
        ensure_structure(hub_root)
        _reports_dir(hub_root).mkdir(parents=True, exist_ok=True)
        path = _reports_dir(hub_root) / "recommendations.json"
        path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return report


def load_recommendations(hub_root):
    path = Path(hub_root) / "_reports" / "recommendations.json"
    if not path.exists():
        return {"domains": [], "updated_at": None}
    return json.loads(path.read_text(encoding="utf-8"))
