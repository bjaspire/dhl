import yaml
import os
import datetime
from dateutil import parser
from jira.client import JiraClient
from reports.sprint_report import SprintReportGenerator
import argparse

def load_config(config_path="config/config.yaml"):
    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            return yaml.safe_load(f)
    else:
        print("Config file not found, falling back to environment variables.")
        return {
            "jira": {
                "url": os.environ.get("JIRA_URL", ""),
                "email": os.environ.get("JIRA_EMAIL", ""),
                "token": os.environ.get("JIRA_TOKEN", ""),
                "board_id": os.environ.get("JIRA_BOARD_ID", 193)
            },
            "report": {
                "output_dir": os.environ.get("REPORT_OUTPUT_DIR", "output")
            }
        }

def run():
    parser_arg = argparse.ArgumentParser(description="Generate Daily Hour Log Report")
    parser_arg.add_argument("--date", type=str, help="Target date in YYYY-MM-DD format (default: today)")
    parser_arg.add_argument("--yesterday", action="store_true", help="Generate report for yesterday")
    args = parser_arg.parse_args()

    config = load_config()
    jira_cfg, report_cfg = config["jira"], config["report"]
    client = JiraClient(jira_cfg["url"], jira_cfg["email"], jira_cfg["token"])

    # Target date for the report
    if args.date:
        try:
            target_date = datetime.datetime.strptime(args.date, "%Y-%m-%d").date()
        except ValueError:
            print("Error: Invalid date format. Please use YYYY-MM-DD.")
            return
    elif args.yesterday:
        target_date = datetime.date.today() - datetime.timedelta(days=1)
    else:
        target_date = datetime.date.today()
        
    target_date_str = target_date.strftime("%Y-%m-%d")
    print(f"Generating daily report for: {target_date_str}")
    
    # 1. Fetch Board Info to map board_id to a Project Key
    board_id = jira_cfg.get("board_id")
    project_key = None
    if board_id:
        try:
            board_info = client.get_agile(f"board/{board_id}")
            project_key = board_info.get("location", {}).get("projectKey")
            print(f"Board {board_id} belongs to project: {project_key}")
        except Exception as e:
            print(f"Warning: Could not fetch board info for board_id {board_id}. Proceeding without project filter.")
        
    # JQL to find issues with work logged on the target date
    jql = f'worklogDate = "{target_date_str}"'
    if project_key:
        jql += f' AND project = "{project_key}"'
    elif "project_key" in jira_cfg:
        jql += f' AND project = "{jira_cfg["project_key"]}"'
    
    print(f"Executing JQL: {jql}")
    # Expand worklog and use fields explicitly to get the details
    issues = client.search_issues(jql, fields=["worklog", "summary", "assignee", "issuetype"])
    
    people_stats = {}
    
    # Process issues to aggregate worklogs
    for iss in issues:
        fields = iss.get("fields", {})
        issue_key = iss.get("key")
        
        # We must look at each worklog to see if it matches the target date
        worklogs = fields.get("worklog", {}).get("worklogs", [])
        
        for wl in worklogs:
            wl_start_str = wl.get("started")
            if not wl_start_str:
                continue
                
            wl_date = parser.parse(wl_start_str).date()
            if wl_date == target_date:
                author = wl.get("author", {}).get("displayName", "Unknown")
                hours = wl.get("timeSpentSeconds", 0) / 3600.0
                
                if author not in people_stats:
                    people_stats[author] = {
                        "name": author,
                        "total_hours": 0.0,
                        "tasks": {}
                    }
                
                people_stats[author]["total_hours"] += hours
                if issue_key not in people_stats[author]["tasks"]:
                    people_stats[author]["tasks"][issue_key] = 0.0
                people_stats[author]["tasks"][issue_key] += hours

    # Transform people_stats into a sorted list for easier rendering
    people_list = list(people_stats.values())
    people_list.sort(key=lambda x: x["name"])
    
    # Calculate global totals
    total_hours_all = sum(p["total_hours"] for p in people_list)
    total_people = len(people_list)
    total_tasks = len(set(key for p in people_list for key in p["tasks"].keys()))

    report_data = {
        "report_date": target_date_str,
        "generated_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "jira_url": jira_cfg["url"],
        "people_metrics": people_list,
        "total_hours": round(total_hours_all, 1),
        "total_people": total_people,
        "total_tasks": total_tasks
    }

    # Generate the report
    report_slug = f"daily_report_{target_date_str}"
    output_dir = os.path.join(report_cfg["output_dir"], "daily_reports")
    os.makedirs(output_dir, exist_ok=True)
    
    report_gen = SprintReportGenerator("templates", output_dir)
    html_path = report_gen.generate_html(report_data, "daily_report_template.html", f"{report_slug}.html")
    
    # Duplicate as index.html for GitHub Pages
    index_path = os.path.join(output_dir, "index.html")
    import shutil
    shutil.copy(html_path, index_path)
    
    print(f"Done! Report generated:\n- HTML: {html_path}\n- Index: {index_path}")

if __name__ == "__main__":
    try:
        run()
    except Exception as e:
        print(f"An error occurred: {e}")
