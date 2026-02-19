import re


def classify_tool(tool, rules):
    name = tool.get("name", "").lower()
    for domain, patterns in rules.get("domains", {}).items():
        for p in patterns:
            if re.search(p, name):
                return domain
    return "general"
