from dateutil import parser
import datetime

def aggregate_people_metrics(issues, roles_config, sprint_start_date=None, sprint_end_date=None):
    """
    Aggregates metrics per person: hours logged, issues worked, comments made.
    Only includes worklogs within the sprint date range if provided.
    """
    people_stats = {}

    for issue in issues:
        fields = issue.get("fields", {})
        
        # 1. Attributes Estimation to Assignee
        assignee_data = fields.get("assignee")
        if assignee_data:
            assignee = assignee_data.get("displayName", "Unknown")
            if assignee not in people_stats:
                people_stats[assignee] = {
                    "hours": 0, "estimated_hours": 0, "issues": set(), 
                    "comments": 0, "blockers": 0, "role": "Other"
                }
            
            raw_estimate = fields.get("timeoriginalestimate") or 0
            people_stats[assignee]["estimated_hours"] += raw_estimate / 3600.0

        # 2. Process Worklogs (Spent Effort)
        worklogs = issue.get("worklogs", [])
        for wl in worklogs:
            wl_date_str = wl.get("started")
            if wl_date_str and sprint_start_date and sprint_end_date:
                wl_date = parser.parse(wl_date_str)
                if wl_date.tzinfo and not sprint_start_date.tzinfo:
                    sprint_start_date = sprint_start_date.replace(tzinfo=wl_date.tzinfo)
                    sprint_end_date = sprint_end_date.replace(tzinfo=wl_date.tzinfo)
                elif not wl_date.tzinfo and sprint_start_date.tzinfo:
                    wl_date = wl_date.replace(tzinfo=sprint_start_date.tzinfo)

                if not (sprint_start_date <= wl_date <= sprint_end_date):
                    continue

            author = wl.get("author", {}).get("displayName", "Unknown")
            if author not in people_stats:
                people_stats[author] = {
                    "hours": 0, "estimated_hours": 0, "issues": set(), 
                    "comments": 0, "blockers": 0, "role": "Other"
                }
            
            people_stats[author]["hours"] += wl.get("timeSpentSeconds", 0) / 3600.0
            people_stats[author]["issues"].add(issue.get("key"))

        # 3. Process Comments (Engagement)
        comments = issue.get("comments", [])
        for comm in comments:
            author = comm.get("author", {}).get("displayName", "Unknown")
            body = comm.get("body", "")
            body_str = str(body).lower()

            if author not in people_stats:
                people_stats[author] = {
                    "hours": 0, "estimated_hours": 0, "issues": set(), 
                    "comments": 0, "blockers": 0, "role": "Other"
                }
            
            people_stats[author]["comments"] += 1
            if "blocker" in body_str or "blocked" in body_str:
                people_stats[author]["blockers"] += 1

    # Map Roles
    devs = roles_config.get("developers", [])
    qa = roles_config.get("qa", [])
    
    for name, stats in people_stats.items():
        if name in devs:
            stats["role"] = "Developer"
        elif name in qa:
            stats["role"] = "QA"
        
        # Cleanup temporary tracking
        stats.pop("estimated_issues", None)
            
        # Convert set to count for easier reporting
        stats["issues_count"] = len(stats["issues"])
        stats["issues_list"] = ", ".join(sorted(list(stats["issues"])))

    return people_stats
