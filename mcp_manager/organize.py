from pathlib import Path
import os


def get_default_roots(user_home):
    user_home = Path(user_home)
    roots = [str(user_home / "Downloads"), str(user_home / "Desktop"), str(user_home / "Documents")]
    exclude = str(user_home / "Desktop" / "claude").replace("\\", "/")
    return [r for r in roots if r.replace("\\", "/") != exclude]


def get_ai_hub_root():
    return Path(os.environ.get("AI_HUB_ROOT", "C:/Users/11918/AI-Hub"))
