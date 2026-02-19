from datetime import datetime


def run_checks(runner, checks):
    results = []
    for item in checks:
        res = runner.run(item["command"])
        results.append({
            "label": item["label"],
            "ok": res.exit_code == 0,
            "output": res.output,
            "ts": datetime.now(),
        })
    return results
