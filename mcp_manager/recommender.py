
def score_tool(tool):
    score = 0
    score += max(0, 100 - tool.get("last_update_days", 999))
    score += 50 if tool.get("price", 0) == 0 else 0
    return score
