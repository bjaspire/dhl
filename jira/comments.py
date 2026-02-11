def get_issue_comments(client, issue_key):
    """Fetch all comments for a specific issue."""
    return client.get(f"issue/{issue_key}/comment").get("comments", [])
