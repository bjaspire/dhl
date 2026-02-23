import yaml
import os
import datetime
from dateutil import parser
from jira.client import JiraClient
from jira.sprints import get_sprint_by_name, get_active_sprint, get_sprints
from jira.issues import get_sprint_issues
from reports.people_report import aggregate_people_metrics
from reports.velocity import generate_velocity_chart
from reports.burndown import calculate_burndown, generate_burndown_chart
from reports.sprint_report import SprintReportGenerator

def load_config(config_path="config/config.yaml"):
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

def get_sprint_info(client, board_id, sprint_name=None):
    """Fetches sprint object based on name or active status."""
    if sprint_name:
        sprint = get_sprint_by_name(client, board_id, sprint_name)
    else:
        sprint = get_active_sprint(client, board_id)
    
    if not sprint:
        return None
        
    sprint["startDateParsed"] = parser.parse(sprint["startDate"]) if "startDate" in sprint else None
    sprint["endDateParsed"] = parser.parse(sprint["endDate"]) if "endDate" in sprint else None
    return sprint

def filter_sprint_work_items(raw_issues, sprint_id):
    """Filters issues to strictly include those associated with the sprint and non-overhead types."""
    active_in_sprint = []
    for iss in raw_issues:
        fields = iss.get("fields", {})
        sf = fields.get("customfield_10006") or fields.get("sprint")
        in_sprint = False
        if isinstance(sf, list):
            for s in sf:
                if isinstance(s, dict) and s.get("id") == sprint_id: in_sprint = True; break
        elif isinstance(sf, dict) and sf.get("id") == sprint_id:
            in_sprint = True
        
        if in_sprint: active_in_sprint.append(iss)

    # Work items: Non-subtasks and Non-Epics
    return [iss for iss in active_in_sprint if not iss['fields'].get('issuetype', {}).get('subtask') and iss['fields'].get('issuetype', {}).get('name') != 'Epic']

def calculate_metrics(work_items, sprint_start_date, sp_field, sprint_state="active"):
    """Consolidated pass over work items to calculate all sprint and quality metrics."""
    metrics = {
        "completed_count": 0, "spillover_count": 0, "scope_added_count": 0,
        "total_completed_sp": 0, "total_orig_est": 0,
        "spillover_keys": [], "scope_added_keys": [],
        "bugs_reported": 0, "bugs_resolved": 0, "high_priority_bugs": 0,
        "blocked_issues": 0, "production_incidents": 0,
        "bugs_reported_keys": [], "bugs_resolved_keys": [], "high_priority_keys": [],
        "blocked_keys": [], "production_incident_keys": [],
        "status_map": {}, "status_breakdown": {}
    }

    for issue in work_items:
        fields = issue.get("fields", {})
        key = issue["key"]
        status = fields.get("status", {}).get("name")
        issue_type = fields.get("issuetype", {}).get("name")
        priority = (fields.get("priority") or {}).get("name", "Medium")
        created_date = parser.parse(fields.get("created"))
        
        # Estimate / Story Points
        est_raw = fields.get("timeoriginalestimate") or 0
        est_h = est_raw / 3600.0
        metrics["total_orig_est"] += est_h
        
        sp_raw = fields.get(sp_field) or 0
        sp = sp_raw / 3600.0 if sp_field == "timeoriginalestimate" else sp_raw
        
        # Status Parsing
        is_done = status.lower() in ["done", "resolved", "closed", "completed", "dev complete", "in qa", "dev - completed"]
        metrics["status_map"][key] = status
        
        if is_done:
            metrics["completed_count"] += 1
            metrics["total_completed_sp"] += sp
        elif sprint_state == "closed":
            metrics["spillover_count"] += 1
            metrics["spillover_keys"].append(key)
            
        if sprint_start_date and created_date > sprint_start_date:
            metrics["scope_added_count"] += 1
            metrics["scope_added_keys"].append(key)

        # Quality Parsing
        if issue_type.lower() == "bug":
            metrics["bugs_reported"] += 1
            metrics["bugs_reported_keys"].append(key)
            if is_done:
                metrics["bugs_resolved"] += 1
                metrics["bugs_resolved_keys"].append(key)
            if priority.lower() in ["high", "highest", "critical", "p0", "p1"]:
                metrics["high_priority_bugs"] += 1
                metrics["high_priority_keys"].append(key)
        
        if status.lower() in ["blocked", "on hold"]:
            metrics["blocked_issues"] += 1
            metrics["blocked_keys"].append(key)
        
        if "incident" in issue_type.lower():
            metrics["production_incidents"] += 1
            metrics["production_incident_keys"].append(key)

        # Status Breakdown Data
        if status not in metrics["status_breakdown"]:
            metrics["status_breakdown"][status] = {"count": 0, "hours": 0, "tickets": []}
        metrics["status_breakdown"][status]["count"] += 1
        metrics["status_breakdown"][status]["hours"] += est_h
        metrics["status_breakdown"][status]["tickets"].append(key)

    return metrics

def get_velocity_trend(client, board_id, current_sprint, current_est, sp_field, lookback=5):
    """Fetches past sprints and calculates estimation vs actual hours trend."""
    all_sprints = get_sprints(client, board_id, state="closed,active").get("values", [])
    all_sprints = sorted([s for s in all_sprints if s.get("startDate")], 
                        key=lambda x: x.get("startDate", ""), reverse=True)
    
    try:
        curr_idx = next(i for i, s in enumerate(all_sprints) if str(s["id"]) == str(current_sprint["id"]))
    except StopIteration:
        curr_idx = 0
        
    recent = all_sprints[curr_idx : curr_idx + lookback]
    recent.reverse()

    velocity_data = []
    for s in recent:
        if str(s["id"]) == str(current_sprint["id"]):
            velocity_data.append({"name": s["name"], "estimated": round(current_est, 1), "worked": 0})
        else:
            past_issues = get_sprint_issues(client, s["id"])
            p_est, p_worked = 0, 0
            p_start, p_end = parser.parse(s["startDate"]), parser.parse(s["endDate"])
            
            for iss in past_issues:
                f = iss.get("fields", {})
                raw_est = f.get(sp_field) or 0
                p_est += (raw_est / 3600.0 if sp_field == "timeoriginalestimate" else raw_est)
                
                for wl in f.get("worklog", {}).get("worklogs", []):
                    wl_date = parser.parse(wl.get("started"))
                    
                    p_start_bound = p_start.replace(hour=0, minute=0, second=0, microsecond=0)
                    p_end_bound = p_end.replace(hour=23, minute=59, second=59, microsecond=999999)
                    
                    if wl_date.tzinfo and not p_start_bound.tzinfo:
                        p_start_bound = p_start_bound.replace(tzinfo=wl_date.tzinfo)
                        p_end_bound = p_end_bound.replace(tzinfo=wl_date.tzinfo)
                    if p_start_bound <= wl_date <= p_end_bound:
                        p_worked += wl.get("timeSpentSeconds", 0) / 3600.0
            
            velocity_data.append({"name": s["name"], "estimated": round(p_est, 1), "worked": round(p_worked, 1)})
    return velocity_data

def run():
    config = load_config()
    jira_cfg, report_cfg = config["jira"], config["report"]
    client = JiraClient(jira_cfg["url"], jira_cfg["email"], jira_cfg["token"])
    board_id = jira_cfg["board_id"]
    sp_field = jira_cfg.get("story_points_field", "customfield_10016")

    # 1. Fetch Sprint & Issues
    sprint = get_sprint_info(client, board_id, jira_cfg.get("sprint_name"))
    if not sprint:
        print(f"Error: Could not find sprint on board {board_id}")
        return

    print(f"Generating report for: {sprint['name']} (ID: {sprint['id']})")
    raw_issues = get_sprint_issues(client, sprint["id"])
    work_items = filter_sprint_work_items(raw_issues, sprint["id"])

    # 2. Process Metrics
    m = calculate_metrics(work_items, sprint.get("startDateParsed"), sp_field, sprint.get("state", "active"))
    
    # Finalize Status Breakdown Sorting — fetch board column order from Jira
    def get_board_status_order(client, board_id):
        """Fetch status order from the Jira board's column configuration.
        
        Uses /rest/agile/1.0/board/{boardId}/configuration which returns
        columns in the exact left-to-right order as displayed on the board,
        with each column mapping to its associated statuses.
        """
        try:
            data = client.get_agile(f"board/{board_id}/configuration")
            columns = data.get("columnConfig", {}).get("columns", [])
            
            ordered = []
            for col in columns:
                for status in col.get("statuses", []):
                    # Each status has an 'id'; we need the name.
                    # Fetch from the status API to get the name.
                    try:
                        status_data = client.get(f"status/{status['id']}")
                        name = status_data.get("name", "")
                        if name:
                            ordered.append(name)
                    except Exception:
                        pass
            return ordered
        except Exception as e:
            print(f"Warning: Could not fetch board configuration: {e}")
            return []

    STATUS_ORDER = get_board_status_order(client, board_id)
    
    # Ensure all board statuses are present, even with 0 tasks
    for status in STATUS_ORDER:
        if status not in m["status_breakdown"]:
            m["status_breakdown"][status] = {"count": 0, "hours": 0, "tickets": []}
    sorted_breakdown = dict(sorted(m["status_breakdown"].items(), 
        key=lambda x: next((i for i, s in enumerate(STATUS_ORDER) if x[0].lower() == s.lower()), len(STATUS_ORDER))))
    for s in sorted_breakdown.values(): s["hours"] = round(s["hours"], 1)

    # 3. People & Velocity
    people_metrics = aggregate_people_metrics(raw_issues, sprint["id"], sprint.get("startDateParsed"), sprint.get("endDateParsed"))
    total_worked = sum(p["hours"] for p in people_metrics.values())
    
    velocity_data = get_velocity_trend(client, board_id, sprint, m["total_orig_est"], sp_field, report_cfg.get("lookback", 5))
    for v in velocity_data:
        if v["name"] == sprint["name"]: v["worked"] = round(total_worked, 1)

    # 4. Final Assembly
    sprint_metrics = {
        "sprint_name": sprint["name"], "sprint_goal": sprint.get("goal"),
        "start_date": sprint.get("startDate", "N/A")[:10], "end_date": sprint.get("endDate", "N/A")[:10],
        "total_issues": len(work_items), "completed_issues": m["completed_count"],
        "spillover_issues": m["spillover_count"] if sprint.get("state") == "closed" else "N/A", 
        "spillover_keys": m["spillover_keys"],
        "scope_added": m["scope_added_count"], "scope_added_keys": m["scope_added_keys"],
        "completion_rate": round((m["completed_count"] / len(work_items) * 100), 2) if work_items else 0,
        "total_estimated_hours": round(m["total_orig_est"], 1), "total_worked_hours": round(total_worked, 1),
        "completed_story_points": round(m["total_completed_sp"], 1),
        "bugs_reported": m["bugs_reported"], "bugs_reported_keys": m["bugs_reported_keys"],
        "bugs_resolved": m["bugs_resolved"], "bugs_resolved_keys": m["bugs_resolved_keys"],
        "high_priority_bugs": m["high_priority_bugs"], "high_priority_bugs_keys": m["high_priority_keys"],
        "blocked_issues": m["blocked_issues"], "blocked_keys": m["blocked_keys"],
        "production_incidents": m["production_incidents"], "production_incident_keys": m["production_incident_keys"],
        "ticket_status_map": m["status_map"], "status_breakdown": sorted_breakdown,
        "velocity_chart_base64": generate_velocity_chart(velocity_data),
        "burndown_chart_base64": generate_burndown_chart(calculate_burndown(work_items, sprint["startDateParsed"], sprint["endDateParsed"])),
        "people_metrics": people_metrics, "jira_url": jira_cfg["url"],
        "generated_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    report_slug = sprint["name"].lower().replace(" ", "_").replace("/", "_")
    sprint_output_dir = os.path.join(report_cfg["output_dir"], report_slug)
    os.makedirs(sprint_output_dir, exist_ok=True)
    
    report_gen = SprintReportGenerator("templates", sprint_output_dir)
    html_path = report_gen.generate_html(sprint_metrics, "report_template.html", f"{report_slug}.html")
    pdf_path = report_gen.generate_pdf(sprint_metrics, "pdf_people_template.html", f"{report_slug}_people.pdf")
    
    print(f"Done! Report generated:\n- HTML: {html_path}\n- PDF:  {pdf_path}")

if __name__ == "__main__":
    try:
        run()
    except Exception as e:
        print(f"An error occurred: {e}")
