import yaml
import os
import datetime
from dateutil import parser
from jira.client import JiraClient
from jira.sprints import get_sprint_by_name, get_active_sprint, get_sprints
from jira.issues import get_sprint_issues
from jira.worklogs import get_issue_worklogs
from jira.comments import get_issue_comments
from reports.people_report import aggregate_people_metrics
from reports.velocity import calculate_velocity, generate_velocity_chart
from reports.burndown import calculate_burndown, generate_burndown_chart
from reports.sprint_report import SprintReportGenerator

def load_config(config_path="config/config.yaml"):
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

def run():
    config = load_config()
    jira_cfg = config["jira"]
    report_cfg = config["report"]

    client = JiraClient(jira_cfg["url"], jira_cfg["email"], jira_cfg["token"])
    
    # 1. Fetch Sprint
    board_id = jira_cfg["board_id"]
    sprint_name = jira_cfg.get("sprint_name")
    
    if sprint_name:
        sprint = get_sprint_by_name(client, board_id, sprint_name)
    else:
        sprint = get_active_sprint(client, board_id)
        
    if not sprint:
        print(f"Error: Could not find sprint {sprint_name} on board {board_id}")
        return

    print(f"Generating report for: {sprint['name']} (ID: {sprint['id']})")
    sprint_start_date = parser.parse(sprint["startDate"]) if "startDate" in sprint else None
    sprint_end_date = parser.parse(sprint["endDate"]) if "endDate" in sprint else None
    sprint_goal = sprint.get("goal")

    # 2. Fetch Issues
    raw_issues = get_sprint_issues(client, sprint["id"])
    
    # 3. Process Metrics
    standard_types = ["Story", "Task", "Bug", "New Feature", "New feature"]
    
    # Pre-filter: Issues accurately associated with this sprint
    active_in_sprint = []
    for iss in raw_issues:
        fields = iss.get("fields", {})
        sf = fields.get("customfield_10006") or fields.get("sprint")
        in_sprint = False
        if isinstance(sf, list):
            for s in sf:
                if isinstance(s, dict) and s.get("id") == sprint["id"]: in_sprint = True; break
        elif isinstance(sf, dict) and sf.get("id") == sprint["id"]:
            in_sprint = True
        
        if in_sprint: active_in_sprint.append(iss)

    # The 87 work items: Non-subtasks and Non-Epics
    work_items = [iss for iss in active_in_sprint if not iss['fields'].get('issuetype', {}).get('subtask') and iss['fields'].get('issuetype', {}).get('name') != 'Epic']
    
    total_issues = len(work_items) # Should be 87
    completed_issues = 0
    spillover_issues = 0
    scope_added = 0
    removed_issues = 0
    scope_added_keys = []
    spillover_keys = []
    removed_keys = []
    total_completed_sp = 0
    
    bugs_reported = 0
    bugs_resolved = 0
    high_priority_bugs = 0
    blocked_issues = 0
    production_incidents = 0

    sp_field = jira_cfg.get("story_points_field", "customfield_10016")
    processed_issues = []

    for issue in work_items:
        fields = issue.get("fields", {})
        status = fields.get("status", {}).get("name")
        issue_type = fields.get("issuetype", {}).get("name")
        priority = fields.get("priority", {}).get("name")
        created_date = parser.parse(fields.get("created"))
        
        sp_raw = fields.get(sp_field) or 0
        sp = sp_raw / 3600.0 if sp_field == "timeoriginalestimate" else sp_raw
            
        is_done = status.lower() in ["done", "resolved", "closed", "completed", "dev complete", "in qa", "dev - completed"]
        if is_done:
            completed_issues += 1
            total_completed_sp += sp
        else:
            spillover_issues += 1
            spillover_keys.append(issue.get("key", ""))
            
        if sprint_start_date and created_date > sprint_start_date:
            scope_added += 1
            scope_added_keys.append(issue.get("key", ""))

        if issue_type.lower() == "bug":
            bugs_reported += 1
            if is_done: bugs_resolved += 1
            if priority.lower() in ["high", "highest", "critical", "p0", "p1"]: high_priority_bugs += 1
        
        if status.lower() in ["blocked", "on hold"]:
            blocked_issues += 1
        
        if "incident" in issue_type.lower():
            production_incidents += 1

        issue["worklogs"] = fields.get("worklog", {}).get("worklogs", [])
        issue["comments"] = fields.get("comment", {}).get("comments", [])
        processed_issues.append(issue)

    completion_rate = round((completed_issues / total_issues * 100), 2) if total_issues > 0 else 0

    # 4. Status Breakdown (with hours and ticket keys)
    status_breakdown = {}
    for iss in work_items:
        s = iss["fields"].get("status", {}).get("name")
        key = iss.get("key", "")
        est_raw = iss["fields"].get("timeoriginalestimate") or 0
        est_hours = est_raw / 3600.0

        if s not in status_breakdown:
            status_breakdown[s] = {"count": 0, "hours": 0, "tickets": []}
        status_breakdown[s]["count"] += 1
        status_breakdown[s]["hours"] += est_hours
        status_breakdown[s]["tickets"].append(key)
    
    # Round hours and sort breakdown by count descending
    for s in status_breakdown:
        status_breakdown[s]["hours"] = round(status_breakdown[s]["hours"], 1)
    status_breakdown = dict(sorted(status_breakdown.items(), key=lambda x: x[1]["count"], reverse=True))

    # 4. Velocity Trend (Estimated vs Worked Hours)
    all_sprints = get_sprints(client, board_id, state="closed,active").get("values", [])
    all_sprints = [s for s in all_sprints if s.get("startDate")]
    all_sprints.sort(key=lambda x: x.get("startDate", ""), reverse=True)
    
    current_idx = -1
    for i, s in enumerate(all_sprints):
        if str(s["id"]) == str(sprint["id"]):
            current_idx = i
            break
    
    lookback = report_cfg.get("lookback", 5)
    recent_sprints = all_sprints[max(0, current_idx): current_idx + lookback]
    recent_sprints.reverse() 
    
    # Calculate total committed SP for the CURRENT sprint for the summary
    summary_oe = sum((iss['fields'].get('timeoriginalestimate') or 0) for iss in work_items) / 3600.0
    total_committed_sp = summary_oe

    velocity_data = []
    for s in recent_sprints:
        if str(s["id"]) == str(sprint["id"]):
            velocity_data.append({
                "name": s["name"], 
                "estimated": round(total_committed_sp, 1),
                "worked": 0 # Will be updated after people_metrics
            })
        else:
            past_issues = get_sprint_issues(client, s["id"])
            p_est = 0
            p_worked = 0
            p_start = parser.parse(s["startDate"])
            p_end = parser.parse(s["endDate"])
            
            for iss in past_issues:
                f = iss.get("fields", {})
                raw_est = f.get(sp_field) or 0
                if sp_field == "timeoriginalestimate":
                    p_est += raw_est / 3600.0
                else:
                    p_est += raw_est
                
                wls = f.get("worklog", {}).get("worklogs", [])
                for wl in wls:
                    wl_date = parser.parse(wl.get("started"))
                    if wl_date.tzinfo and not p_start.tzinfo:
                        p_start = p_start.replace(tzinfo=wl_date.tzinfo)
                        p_end = p_end.replace(tzinfo=wl_date.tzinfo)
                    if p_start <= wl_date <= p_end:
                        p_worked += wl.get("timeSpentSeconds", 0) / 3600.0
                        
            velocity_data.append({
                "name": s["name"], 
                "estimated": round(p_est, 1),
                "worked": round(p_worked, 1)
            })

    # Move people_metrics up before chart generation
    # 5. People Metrics
    # Pass raw_issues so it can detect all assignments/worklogs, 
    # and sprint_id/dates for precise filtering.
    people_metrics = aggregate_people_metrics(raw_issues, sprint["id"], sprint_start_date, sprint_end_date)
    
    # Update current sprint velocity data
    for v in velocity_data:
        if v["name"] == sprint["name"]:
            # Recalculate estimated hours for the 86 items ONLY for the summary
            # We already have work_items list from earlier
            summary_oe = sum((iss['fields'].get('timeoriginalestimate') or 0) for iss in work_items) / 3600.0
            v["estimated"] = round(summary_oe, 1)
            v["worked"] = round(sum(p["hours"] for p in people_metrics.values()), 1)

    chart_base64 = generate_velocity_chart(velocity_data)

    # 6. Burndown Chart
    burndown_data = calculate_burndown(work_items, sprint_start_date, sprint_end_date)
    burndown_base64 = generate_burndown_chart(burndown_data)

    total_estimated_hours = sum((iss['fields'].get('timeoriginalestimate') or 0) for iss in work_items) / 3600.0
    total_worked_hours = sum(p["hours"] for p in people_metrics.values())

    sprint_metrics = {
        "sprint_name": sprint["name"],
        "sprint_goal": sprint_goal,
        "start_date": sprint_start_date.strftime("%Y-%m-%d") if sprint_start_date else "N/A",
        "end_date": sprint_end_date.strftime("%Y-%m-%d") if sprint_end_date else "N/A",
        "total_issues": total_issues, # 86
        "completed_issues": completed_issues,
        "spillover_issues": spillover_issues,
        "scope_added": scope_added,
        "scope_added_keys": scope_added_keys,
        "removed_issues": removed_issues,
        "removed_keys": removed_keys,
        "spillover_keys": spillover_keys,
        "completion_rate": completion_rate,
        "total_estimated_hours": round(total_estimated_hours, 1),
        "total_worked_hours": round(total_worked_hours, 1),
        "completed_story_points": round(total_completed_sp, 1),
        "committed_story_points": round(total_estimated_hours, 1), # Same as total_estimated_hours
        "bugs_reported": bugs_reported,
        "bugs_resolved": bugs_resolved,
        "high_priority_bugs": high_priority_bugs,
        "blocked_issues": blocked_issues,
        "production_incidents": production_incidents,
        "status_breakdown": status_breakdown,
        "velocity_chart_base64": chart_base64,
        "burndown_chart_base64": burndown_base64,
        "people_metrics": people_metrics,
        "generated_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "jira_url": jira_cfg["url"]
    }

    report_slug = sprint["name"].lower().replace(" ", "_").replace("/", "_")
    sprint_output_dir = os.path.join(report_cfg["output_dir"], report_slug)
    os.makedirs(sprint_output_dir, exist_ok=True)

    report_gen = SprintReportGenerator("templates", sprint_output_dir)
    html_filename = f"{report_slug}.html"
    excel_filename = f"{report_slug}.xlsx"

    html_path = report_gen.generate_html(sprint_metrics, "report_template.html", html_filename)
    excel_metrics = {k: v for k, v in sprint_metrics.items() if k not in ["people_metrics", "velocity_chart_base64"]}
    excel_path = report_gen.generate_excel(
        excel_metrics,
        people_metrics,
        excel_filename
    )

    print(f"Done! Reports generated:")
    print(f"- HTML: {html_path}")
    print(f"- Excel: {excel_path}")

if __name__ == "__main__":
    try:
        run()
    except Exception as e:
        print(f"An error occurred: {e}")
