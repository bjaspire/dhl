import matplotlib.pyplot as plt
import base64
from io import BytesIO

def calculate_velocity(sprints_data):
    """
    sprints_data: list of dicts with {'name': sprint_name, 'completed_sp': story_points}
    """
    if not sprints_data:
        return 0
    total_sp = sum(s['completed_sp'] for s in sprints_data)
    return total_sp / len(sprints_data)

def generate_velocity_chart(sprints_data, output_path=None):
    """Generates a line chart for velocity trend (Estimated vs Worked Hours)."""
    names = [s['name'] for s in sprints_data]
    estimated = [s.get('estimated', 0) for s in sprints_data]
    worked = [s.get('worked', 0) for s in sprints_data]
    
    plt.figure(figsize=(10, 6))
    
    # Plot Estimated Hours
    plt.plot(names, estimated, marker='o', linestyle='--', color='#6b778c', linewidth=2, label='Estimated Effort (h)')
    
    # Plot Worked Hours
    plt.plot(names, worked, marker='s', linestyle='-', color='#0052cc', linewidth=2, label='Actual Worked (h)')
    plt.fill_between(names, worked, color='#0052cc', alpha=0.1)
    
    plt.xlabel('Sprints')
    plt.ylabel('Effort (Hours)')
    plt.title('Velocity Trend: Estimation vs Actuals')
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    if output_path:
        plt.savefig(output_path)
    
    # Also return base64 for embedding in HTML
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close()
    
    return image_base64
