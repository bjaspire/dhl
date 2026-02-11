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
from reports.sprint_report import SprintReportGenerator

def load_config(config_path="config/config.yaml"):
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

def run():
    config = load_config()
    jira_cfg = config["jira"]
    roles_cfg = config["roles"]
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
    total_issues = len(raw_issues)
    completed_issues = 0
    spillover_issues = 0
    scope_added = 0
    removed_issues = 0 # Difficult to fetch without full board scan, setting to 0 or logic-based
    total_completed_sp = 0
    total_committed_sp = 0
    
    bugs_reported = 0
    bugs_resolved = 0
    high_priority_bugs = 0
    blocked_issues = 0
    production_incidents = 0 # Map to specific Issue Type if needed

    sp_field = jira_cfg.get("story_points_field", "customfield_10016")
    processed_issues = []

    for issue in raw_issues:
        fields = issue.get("fields", {})
        status = fields.get("status", {}).get("name")
        issue_type = fields.get("issuetype", {}).get("name")
        priority = fields.get("priority", {}).get("name")
        created_date = parser.parse(fields.get("created"))
        
        # Story Points (Handle timeoriginalestimate if used)
        sp_raw = fields.get(sp_field) or 0
        if sp_field == "timeoriginalestimate" and sp_raw > 0:
            sp = sp_raw / 3600.0 # Convert seconds to hours
        else:
            sp = sp_raw
            
        # Estimate will be summed in a clean pass later to avoid double-counting
        
        # Completed vs Spillover
        is_done = status.lower() in ["done", "resolved", "closed", "completed", "dev complete", "in qa"]
        if is_done:
            completed_issues += 1
            total_completed_sp += sp
        else:
            spillover_issues += 1
            
        # Scope Added (Created after sprint start OR added to sprint later)
        is_added = False
        if sprint_start_date and created_date > sprint_start_date:
            scope_added += 1
            is_added = True

        # Quality Metrics
        if issue_type.lower() == "bug":
            bugs_reported += 1
            if is_done:
                bugs_resolved += 1
            if priority.lower() in ["high", "highest", "critical", "p0", "p1"]:
                high_priority_bugs += 1
        
        if status.lower() in ["blocked", "on hold"]:
            blocked_issues += 1
        
        if "incident" in issue_type.lower():
            production_incidents += 1

        # Extract bulk worklogs and comments from the expanded fields
        issue["worklogs"] = fields.get("worklog", {}).get("worklogs", [])
        issue["comments"] = fields.get("comment", {}).get("comments", [])
        
        processed_issues.append(issue)

    completion_rate = round((completed_issues / total_issues * 100), 2) if total_issues > 0 else 0

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
    
    velocity_data = []
    for s in recent_sprints:
        if str(s["id"]) == str(sprint["id"]):
            # Use data already calculated
            actual_worked = sum(p["hours"] for p in people_metrics.values()) if 'people_metrics' in locals() else 0
            # Note: people_metrics is defined after this loop in original code, so I'll move it up or recalculate.
            # I will move people_metrics calculation up.
            velocity_data.append({
                "name": s["name"], 
                "estimated": round(total_committed_sp, 1),
                "worked": round(actual_worked, 1)
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
    people_metrics = aggregate_people_metrics(processed_issues, roles_cfg, sprint_start_date, sprint_end_date)
    # Fix the current sprint data in velocity_data after people_metrics is ready
    for v in velocity_data:
        if v["name"] == sprint["name"]:
            v["worked"] = round(sum(p["hours"] for p in people_metrics.values()), 1)

    chart_base64 = generate_velocity_chart(velocity_data, os.path.join(report_cfg["output_dir"], "velocity.png"))

    # Recalculate total estimated hours (sum of all unique issue estimates in sprint)
    total_committed_sp = sum((iss.get("fields", {}).get(sp_field) or 0) for iss in raw_issues)
    if sp_field == "timeoriginalestimate":
        total_committed_sp = total_committed_sp / 3600.0

    # 6. Generate Reports
    total_worked_hours = sum(p["hours"] for p in people_metrics.values())
    sprint_metrics = {
        "sprint_name": sprint["name"],
        "sprint_goal": sprint_goal,
        "start_date": sprint_start_date.strftime("%Y-%m-%d") if sprint_start_date else "N/A",
        "end_date": sprint_end_date.strftime("%Y-%m-%d") if sprint_end_date else "N/A",
        "total_issues": total_issues,
        "completed_issues": completed_issues,
        "spillover_issues": spillover_issues,
        "scope_added": scope_added,
        "removed_issues": removed_issues,
        "completion_rate": completion_rate,
        "total_estimated_hours": round(total_committed_sp, 1),
        "total_worked_hours": round(total_worked_hours, 1),
        "completed_story_points": round(total_completed_sp, 1),
        "committed_story_points": round(total_committed_sp, 1),
        "bugs_reported": bugs_reported,
        "bugs_resolved": bugs_resolved,
        "high_priority_bugs": high_priority_bugs,
        "blocked_issues": blocked_issues,
        "production_incidents": production_incidents,
        "velocity_chart_base64": chart_base64,
        "people_metrics": people_metrics,
        "generated_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    report_gen = SprintReportGenerator("templates", report_cfg["output_dir"])
    report_slug = sprint["name"].lower().replace(" ", "_").replace("/", "_")
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
