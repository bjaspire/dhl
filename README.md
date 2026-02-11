# Jira Sprint Report Generator

A Python tool to generate comprehensive Jira sprint reports, including metrics, velocity trends, and individual contribution tracking.

## 🚀 How to Run

1.  **Initialize the Environment**:
    Ensure you have Python 3.11+ installed. Run the following commands in the project root:
    ```bash
    python3 - m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

2.  **Run the Generator**:
    ```bash
    python main.py
    ```

## ⚙️ Configuration (Where the Variables Are)

All variables and credentials are stored in `config/config.yaml`.

### Connection Settings
Open `config/config.yaml` and update the `jira` section:
- `url`: Your Jira instance URL (e.g., `https://your-domain.atlassian.net`).
- `email`: Your Jira login email.
- `token`: Your Jira API token (Generate one at [Atlassian Security](https://id.atlassian.com/manage-profile/security/api-tokens)).
- `board_id`: The numeric ID of your Jira board.
- `sprint_name`: (Optional) The name of the sprint you want to report on. If left blank, it defaults to the active sprint.
- `story_points_field`: The custom field ID for story points (defaults to `customfield_10016`).

### Role Mapping
Update the `roles` section to map display names to roles for the "People Contribution" table:
```yaml
roles:
  developers:
    - "John Doe"
  qa:
    - "Jane Smith"
```

## 📊 Outputs

The reports are generated in the `output/` directory:
- `sprint_report_<id>.html`: A polished HTML report with embedded charts.
- `sprint_report_<id>.xlsx`: A detailed Excel spreadsheet with raw metrics and contribution data.
- `velocity.png`: The velocity trend chart.

## 📁 Project Structure

- `main.py`: Entry point.
- `jira/`: API interaction modules (client, issues, sprints, worklogs, comments).
- `reports/`: Logic for metrics, charts, and report generation.
- `templates/`: HTML templates for the final report.
- `config/`: Configuration files.
