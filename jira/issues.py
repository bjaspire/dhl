def get_sprint_issues(client, sprint_id):
    """Fetch all issues for a specific sprint."""
    issues = []
    start_at = 0
    max_results = 100
    
    while True:
        response = client.get_agile(f"sprint/{sprint_id}/issue", params={
            "startAt": start_at,
            "maxResults": max_results,
            "expand": "changelog,worklog,comment" 
        })
        issues.extend(response.get("issues", []))
        
        if len(issues) >= response.get("total", 0):
            break
        start_at += max_results
        
    return issues

def get_issue_details(client, issue_key):
    """Fetch full details for a single issue."""
    return client.get(f"issue/{issue_key}")
