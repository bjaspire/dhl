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
        new_issues = response.get("issues", [])
        
        for issue in new_issues:
            wl = issue.get("fields", {}).get("worklog", {})
            if wl.get("total", 0) > len(wl.get("worklogs", [])):
                try:
                    full_wl = client.get(f"issue/{issue['key']}/worklog")
                    if full_wl and "worklogs" in full_wl:
                        issue["fields"]["worklog"] = full_wl
                except Exception as e:
                    print(f"Failed to fetch full worklogs for {issue['key']}: {e}")
                    
        issues.extend(new_issues)
        
        if len(issues) >= response.get("total", 0):
            break
        start_at += max_results
        
    return issues

def get_issue_details(client, issue_key):
    """Fetch full details for a single issue."""
    return client.get(f"issue/{issue_key}")
