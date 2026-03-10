import os
import json
import datetime
import urllib.request
from dateutil import parser
from jira.client import JiraClient
import yaml

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
                "board_id": os.environ.get("JIRA_BOARD_ID") or 193,
                "webhook_url": os.environ.get("GCHAT_WEBHOOK_URL", "")
            }
        }

def get_report_data():
    config = load_config()
    jira_cfg = config["jira"]
    client = JiraClient(jira_cfg["url"], jira_cfg["email"], jira_cfg["token"])

    today = datetime.date.today()
    if today.weekday() == 0:  # Monday
        target_date = today - datetime.timedelta(days=3)
    elif today.weekday() == 5 or today.weekday() == 6: # Saturday or Sunday
        print("Today is the weekend. No daily report runs scheduled for yesterday.")
        return None
    else:
        target_date = today - datetime.timedelta(days=1)
        
    target_date_str = target_date.strftime("%Y-%m-%d")
    print(f"Generating chat notification for: {target_date_str}")
    
    board_id = jira_cfg.get("board_id")
    project_key = None
    if board_id:
        try:
            board_info = client.get_agile(f"board/{board_id}")
            project_key = board_info.get("location", {}).get("projectKey")
        except Exception as e:
            print(f"Warning: Could not fetch board info for board_id {board_id}.")
        
    jql = f'worklogDate = "{target_date_str}"'
    if project_key:
        jql += f' AND project = "{project_key}"'
    elif "project_key" in jira_cfg:
        jql += f' AND project = "{jira_cfg["project_key"]}"'
    
    issues = client.search_issues(jql, fields=["worklog", "summary", "assignee", "issuetype"])
    
    people_stats = {}
    for iss in issues:
        fields = iss.get("fields", {})
        issue_key = iss.get("key")
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
                    people_stats[author] = {"name": author, "total_hours": 0.0, "tasks": {}}
                
                people_stats[author]["total_hours"] += hours
                if issue_key not in people_stats[author]["tasks"]:
                    people_stats[author]["tasks"][issue_key] = 0.0
                people_stats[author]["tasks"][issue_key] += hours

    people_list = list(people_stats.values())
    people_list.sort(key=lambda x: x["name"])
    total_hours_all = sum(p["total_hours"] for p in people_list)

    return {
        "report_date": target_date_str,
        "jira_url": jira_cfg["url"],
        "people_metrics": people_list,
        "total_hours": round(total_hours_all, 1)
    }

def send_google_chat_notification(report_data, webhook_url):
    widgets = []
    jira_base_url = report_data["jira_url"].rstrip('/')
    
    for person in report_data["people_metrics"]:
        tasks_text = []
        sorted_tasks = sorted(person["tasks"].items(), key=lambda x: x[0])
        for task_key, hours in sorted_tasks:
            task_url = f"{jira_base_url}/browse/{task_key}"
            tasks_text.append(f'• <a href="{task_url}">{task_key}</a> ({hours:.1f}h)')
        
        tasks_html = "<br>".join(tasks_text)
        
        text = f'<b>{person["name"]}</b><br>{tasks_html}<br><b>Total: {person["total_hours"]:.1f}h</b>'
        
        widgets.append({"textParagraph": {"text": text}})
        widgets.append({"divider": {}})
    
    widgets.append({
        "decoratedText": {
            "topLabel": "Project Summary",
            "text": f'<b>GRAND TOTAL: {report_data["total_hours"]:.1f}h</b>',
            "startIcon": {
                "iconUrl": "https://fonts.gstatic.com/s/e/notoemoji/17.0/1f646/512.png=s64"
            }
        }
    })
    
    payload = {
        "cardsV2": [{
            "cardId": "worklog_report",
            "card": {
                "header": {
                    "title": "Project Work Log Summary",
                    "subtitle": f'Daily Task Breakdown ({report_data["report_date"]})',
                    "imageUrl": "https://fonts.gstatic.com/s/e/notoemoji/17.0/1f647/512.png=s64"
                },
                "sections": [{"header": "Team Contributions", "widgets": widgets}]
            }
        }]
    }
    
    try:
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(webhook_url, data=data, headers={'Content-Type': 'application/json'})
        urllib.request.urlopen(req)
        print("Successfully sent Google Chat notification.")
    except Exception as e:
        print(f"Failed to send Google Chat notification: {e}")

if __name__ == "__main__":
    config = load_config()
    webhook_url = config.get("jira", {}).get("webhook_url") or os.environ.get("GCHAT_WEBHOOK_URL")
    
    if not webhook_url:
        print("Error: Webhook URL not found in config.yaml or GCHAT_WEBHOOK_URL environment variable.")
        exit(1)

    report_data = get_report_data()
    if report_data:
        send_google_chat_notification(report_data, webhook_url)
