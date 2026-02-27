from dateutil import parser
import datetime

def aggregate_people_metrics(issues, sprint_id=None, sprint_start_date=None, sprint_end_date=None):
    """
    Aggregates metrics per person based on Jira Sprint UI logic.
    - Standard Work Items: All non-subtasks and non-epics.
    - Estimates: Attributed to assignee for standard work items only.
    - Hours: Strictly filtered by worklog dates.
    """
    people_stats = {}

    def get_person_stats(name):
        if name not in people_stats:
            people_stats[name] = {
                "hours": 0, "estimated_hours": 0, 
                "active_issues": set(),   
                "assigned_issues": set(),
                "issue_hours": {}
            }
        return people_stats[name]

    for issue in issues:
        fields = issue.get("fields", {})
        issue_key = issue.get("key")
        issue_type = fields.get("issuetype", {}).get("name")
        is_subtask = fields.get("issuetype", {}).get("subtask")
        raw_estimate = (fields.get("timeoriginalestimate") or 0) / 3600.0
        
        # Track assignment and Attribute Est (h) for ALL sprint issues
        # (no sprint field check needed — get_sprint_issues already filters by sprint)
        assignee_data = fields.get("assignee")
        assignee = assignee_data.get("displayName") if assignee_data else None
        
        if assignee:
            stats = get_person_stats(assignee)
            stats["assigned_issues"].add(issue_key)
            
            # ONLY attribute estimate for work items (Non-subtask, Non-Epic)
            if not is_subtask and issue_type != "Epic":
                stats["estimated_hours"] += raw_estimate

        # 3. Track worklogs — ALWAYS process for ALL issues (including sub-tasks)
        worklogs = issue.get("worklogs")
        if worklogs is None:
            worklogs = fields.get("worklog", {}).get("worklogs", [])
            
        for wl in worklogs:
            wl_date_str = wl.get("started")
            if wl_date_str and sprint_start_date and sprint_end_date:
                wl_date = parser.parse(wl_date_str)
                s_start, s_end = sprint_start_date, sprint_end_date
                
                # Expand sprint start and end to cover whole days
                s_start = s_start.replace(hour=0, minute=0, second=0, microsecond=0)
                s_end = s_end.replace(hour=23, minute=59, second=59, microsecond=999999)
                
                if wl_date.tzinfo and not s_start.tzinfo:
                    s_start = s_start.replace(tzinfo=wl_date.tzinfo)
                    s_end = s_end.replace(tzinfo=wl_date.tzinfo)
                elif not wl_date.tzinfo and s_start.tzinfo:
                    wl_date = wl_date.replace(tzinfo=s_start.tzinfo)
                
                if s_start <= wl_date <= s_end:
                    author = wl.get("author", {}).get("displayName", "Unknown")
                    hours = wl.get("timeSpentSeconds", 0) / 3600.0
                    stats = get_person_stats(author)
                    stats["hours"] += hours
                    stats["active_issues"].add(issue_key)
                    
                    if issue_key not in stats["issue_hours"]:
                        stats["issue_hours"][issue_key] = 0
                    stats["issue_hours"][issue_key] += hours



    # Finalize stats
    for name, stats in people_stats.items():
        # Use all assigned issues for the list to ensure full transparency
        sorted_keys = sorted(list(stats["assigned_issues"]))
        stats["issues_count"] = len(sorted_keys)
        stats["issues_keys"] = sorted_keys
        stats["issues_list"] = ", ".join(sorted_keys)
        stats["assigned_count"] = len(sorted_keys)
        stats["assigned_list"] = stats["issues_list"]

    return people_stats
