def get_issue_worklogs(client, issue_key):
    """Fetch all worklogs for a specific issue."""
    return client.get(f"issue/{issue_key}/worklog").get("worklogs", [])

def get_total_hours_for_issue(client, issue_key):
    """Calculate total hours logged on an issue."""
    worklogs = get_issue_worklogs(client, issue_key)
    total_seconds = sum(w.get("timeSpentSeconds", 0) for w in worklogs)
    return total_seconds / 3600.0
