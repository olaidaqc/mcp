
def should_run(freq, last_run_days):
    if freq == "daily":
        return last_run_days >= 1
    if freq == "weekly":
        return last_run_days >= 7
    return False
