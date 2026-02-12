import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import base64
from io import BytesIO
from dateutil import parser as date_parser
from datetime import timedelta


def calculate_burndown(work_items, sprint_start_date, sprint_end_date):
    """
    Calculates burndown data from work items using their changelogs.
    Returns a list of (date, remaining_count) tuples for plotting.
    
    Logic:
    - Start with total work items on sprint start date.
    - For each day, subtract items that transitioned to a "done" status.
    - Track the ideal burndown line (linear from total to 0).
    """
    done_statuses = {"done", "resolved", "closed", "completed", "dev complete", 
                     "dev - completed", "in qa"}
    
    total = len(work_items)
    
    # Build a map of date -> number of items completed on that date
    completion_dates = {}
    
    for issue in work_items:
        changelog = issue.get("changelog", {}).get("histories", [])
        done_date = None
        
        for history in changelog:
            created = date_parser.parse(history.get("created", ""))
            for item in history.get("items", []):
                if item.get("field") == "status":
                    to_status = (item.get("toString") or "").lower()
                    if to_status in done_statuses:
                        # Use the latest "done" transition within the sprint
                        if sprint_start_date <= created <= sprint_end_date:
                            done_date = created.date()
        
        if done_date:
            completion_dates[done_date] = completion_dates.get(done_date, 0) + 1
    
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
        "total": total
    }


def generate_burndown_chart(burndown_data, output_path=None):
    """Generates a burndown chart and returns base64 encoded image."""
    dates = burndown_data["dates"]
    actual = burndown_data["actual"]
    ideal = burndown_data["ideal"]
    total = burndown_data["total"]
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Ideal burndown line (dashed gray)
    ax.plot(dates, ideal, linestyle='--', color='#8993a4', linewidth=2, 
            label='Ideal Burndown', alpha=0.8)
    
    # Actual burndown line (solid blue with fill)
    ax.plot(dates, actual, marker='o', markersize=4, linestyle='-', 
            color='#0052cc', linewidth=2.5, label='Actual Remaining')
    ax.fill_between(dates, actual, alpha=0.08, color='#0052cc')
    
    # Styling
    ax.set_xlabel('Sprint Days', fontsize=11, fontweight='bold')
    ax.set_ylabel('Remaining Items', fontsize=11, fontweight='bold')
    ax.set_title('Sprint Burndown', fontsize=14, fontweight='bold', pad=15)
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
