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
                "comments": 0, "blockers": 0
            }
        return people_stats[name]

    for issue in issues:
        fields = issue.get("fields", {})
        issue_key = issue.get("key")
        issue_type = fields.get("issuetype", {}).get("name")
        is_subtask = fields.get("issuetype", {}).get("subtask")
        raw_estimate = (fields.get("timeoriginalestimate") or 0) / 3600.0
        
        # 1. Check Sprint Association (only for estimate/assignment gating)
        in_sprint = True
        if sprint_id:
            sf = fields.get("customfield_10006") or fields.get("sprint")
            in_sprint = False
            if isinstance(sf, list):
                for s in sf:
                    if isinstance(s, dict) and s.get("id") == sprint_id: in_sprint = True; break
            elif isinstance(sf, dict) and sf.get("id") == sprint_id:
                in_sprint = True

        # 2. Track assignment and Attribute Est (h) — only for sprint-associated items
        if in_sprint:
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

        # 4. Track comments — ALWAYS process for ALL issues (including sub-tasks)
        comments = issue.get("comments")
        if comments is None:
            comments = fields.get("comment", {}).get("comments", [])
            
        for comm in comments:
            author = comm.get("author", {}).get("displayName", "Unknown")
            body_str = str(comm.get("body", "")).lower()
            created_str = comm.get("created")
            if created_str and sprint_start_date and sprint_end_date:
                created = parser.parse(created_str)
                s_start, s_end = sprint_start_date, sprint_end_date
                if created.tzinfo and not s_start.tzinfo:
                    s_start = s_start.replace(tzinfo=created.tzinfo)
                    s_end = s_end.replace(tzinfo=created.tzinfo)
                if s_start <= created <= s_end:
                    stats = get_person_stats(author)
                    stats["comments"] += 1
                    stats["active_issues"].add(issue_key)
                    if "blocker" in body_str or "blocked" in body_str:
                        stats["blockers"] += 1

    # Finalize stats
    for name, stats in people_stats.items():
        # Use all assigned issues for the list to ensure full transparency
        sorted_keys = sorted(list(stats["assigned_issues"]))
        stats["issues_count"] = len(sorted_keys)
        stats["issues_list"] = ", ".join(sorted_keys)
        stats["assigned_count"] = len(sorted_keys)
        stats["assigned_list"] = stats["issues_list"]

    return people_stats
