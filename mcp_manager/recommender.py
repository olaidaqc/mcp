def score_repo(repo):
    stars = int(repo.get("stargazers_count", 0))
    updated_days = int(repo.get("updated_days", 999))
    score = 0
    score += min(stars / 10, 500)
    score += max(0, 100 - updated_days)
    return score


def dedupe_by_capability(repos):
    best = {}
    for r in repos:
        cap = r.get("capability") or "general"
        if cap not in best:
            best[cap] = r
        else:
            if score_repo(r) > score_repo(best[cap]):
                best[cap] = r
    return list(best.values())


def pick_best(repos):
    if not repos:
        return None, []
    scored = sorted(repos, key=score_repo, reverse=True)
    return scored[0], scored[1:3]
