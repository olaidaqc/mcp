from mcp_manager.organize import run_scan
from mcp_manager.recommendations import refresh_recommendations


def startup_run(env=None, fetcher=None):
    plan = run_scan(env or {})
    recommendations = refresh_recommendations(
        hub_root=None if env is None else env.get("AI_HUB_ROOT"),
        fetcher=fetcher,
    )
    return {"plan": plan, "recommendations": recommendations}


if __name__ == "__main__":
    startup_run()
