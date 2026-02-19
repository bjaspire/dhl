import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import base64
from io import BytesIO
from dateutil import parser as date_parser
from datetime import timedelta


DONE_STATUSES = {"done", "resolved", "closed", "completed", "dev complete", 
                 "dev - completed", "in qa"}


def _find_completion_date(issue, sprint_start, sprint_end):
    """
    Determine the date an issue was completed within the sprint.
    
    Strategy:
    1. Check changelog for status transitions to a 'done' status within the sprint dates.
    2. If no changelog transition found but the issue is currently in a done status,
       use the 'resolutiondate' or 'statuscategorychangedate' as fallback.
    3. If neither is available, use the 'updated' field as last resort.
    
    Returns the completion date or None if not completed in this sprint.
    """
    # Strategy 1: Look for explicit status transitions in changelog
    changelog = issue.get("changelog", {}).get("histories", [])
    
    best_done_date = None
    for history in changelog:
        # Check if this history contains any status changes to 'done' first
        status_items = [item for item in history.get("items", []) if item.get("field") == "status"]
        if not any((item.get("toString") or "").lower() in DONE_STATUSES for item in status_items):
            continue
            
        created = date_parser.parse(history.get("created", ""))
        # Only proceed if the event is within the sprint timeframe
        if sprint_start <= created <= sprint_end:
            for item in status_items:
                if (item.get("toString") or "").lower() in DONE_STATUSES:
                    if best_done_date is None or created > best_done_date:
                        best_done_date = created
    
    if best_done_date:
        return best_done_date.date()
    
    # Strategy 2: Issue is currently done but no changelog entry found (pagination issue)
    fields = issue.get("fields", {})
    current_status = fields.get("status", {}).get("name", "").lower()
    
    if current_status in DONE_STATUSES:
        # Try resolutiondate first
        resolution_date_str = fields.get("resolutiondate")
        if resolution_date_str:
            res_date = date_parser.parse(resolution_date_str)
            if sprint_start <= res_date <= sprint_end:
                return res_date.date()
        
        # Try statuscategorychangedate
        status_change_str = fields.get("statuscategorychangedate")
        if status_change_str:
            status_date = date_parser.parse(status_change_str)
            if sprint_start <= status_date <= sprint_end:
                return status_date.date()
        
        # Last resort: use 'updated' field
        updated_str = fields.get("updated")
        if updated_str:
            updated_date = date_parser.parse(updated_str)
            if sprint_start <= updated_date <= sprint_end:
                return updated_date.date()
    
    return None


def calculate_burndown(work_items, sprint_start_date, sprint_end_date):
    """
    Calculates burndown data from work items.
    Returns a dict with dates, actual remaining, and ideal remaining for plotting.
    """
    total = len(work_items)
    
    # Build a map of date -> number of items completed on that date
    completion_dates = {}
    
    for issue in work_items:
        done_date = _find_completion_date(issue, sprint_start_date, sprint_end_date)
        if done_date:
            completion_dates[done_date] = completion_dates.get(done_date, 0) + 1
    
    total_completed = sum(completion_dates.values())
    
    # Generate day-by-day burndown
    start = sprint_start_date.date()
    end = sprint_end_date.date()
    num_days = (end - start).days
    
    dates = []
    actual_remaining = []
    ideal_remaining = []
    
    remaining = total
    
    for i in range(num_days + 1):
        current_date = start + timedelta(days=i)
        dates.append(current_date)
        
        # Subtract completions for this day
        completed_today = completion_dates.get(current_date, 0)
        remaining -= completed_today
        actual_remaining.append(remaining)
        
        # Ideal: linear decrease from total to 0
        ideal = total - (total * i / num_days) if num_days > 0 else 0
        ideal_remaining.append(round(ideal, 1))
    
    return {
        "dates": dates,
        "actual": actual_remaining,
        "ideal": ideal_remaining,
        "total": total,
        "completed": total_completed
    }


def generate_burndown_chart(burndown_data, output_path=None):
    """Generates a burndown chart and returns base64 encoded image."""
    dates = burndown_data["dates"]
    actual = burndown_data["actual"]
    ideal = burndown_data["ideal"]
    total = burndown_data["total"]
    completed = burndown_data["completed"]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Ideal burndown line (dashed gray)
    ax.plot(dates, ideal, linestyle='--', color='#8993a4', linewidth=2, 
            label='Ideal Burndown', alpha=0.8)
    
    # Actual burndown line (solid blue with fill)
    ax.plot(dates, actual, marker='o', markersize=4, linestyle='-', 
            color='#0052cc', linewidth=2.5, label=f'Actual Remaining ({completed} completed)')
    ax.fill_between(dates, actual, alpha=0.08, color='#0052cc')
    
    # Styling
    ax.set_xlabel('Sprint Days', fontsize=11, fontweight='bold')
    ax.set_ylabel('Remaining Items', fontsize=11, fontweight='bold')
    ax.set_title(f'Sprint Burndown ({total} items)', fontsize=14, fontweight='bold', pad=15)
    ax.legend(loc='upper right', framealpha=0.9)
    ax.grid(True, linestyle='--', alpha=0.4)
    ax.set_ylim(bottom=0, top=total + 2)
    
    # Format x-axis dates
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d'))
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=max(1, len(dates) // 10)))
    plt.xticks(rotation=45, ha='right')
    
    plt.tight_layout()
    
    if output_path:
        plt.savefig(output_path, dpi=150)
    
    # Return base64 for HTML embedding
    buffer = BytesIO()
    plt.savefig(buffer, format='png', dpi=150)
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close()
    
    return image_base64
