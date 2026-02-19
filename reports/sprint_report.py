from jinja2 import Environment, FileSystemLoader
import os

class SprintReportGenerator:
    def __init__(self, template_dir, output_dir):
        self.env = Environment(loader=FileSystemLoader(template_dir))
        self.env.filters["jira_time"] = self.format_jira_time
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def format_jira_time(self, hours):
        if not hours or hours == 0:
            return "0h"
            
        total_minutes = int(round(hours * 60))
        
        # 1d = 8h = 480m
        # 1w = 5d = 40h = 2400m
        
        w = total_minutes // 2400
        r_minutes = total_minutes % 2400
        
        d = r_minutes // 480
        r_minutes = r_minutes % 480
        
        h = r_minutes // 60
        m = r_minutes % 60
        
        parts = []
        if w > 0: parts.append(f"{w}w")
        if d > 0: parts.append(f"{d}d")
        if h > 0: parts.append(f"{h}h")
        if m > 0: parts.append(f"{m}m")
        
        breakdown = " ".join(parts)
        if not breakdown:
            return f"{round(hours, 1)}h"
            
        return f"{round(hours, 1)}h<br><small>( {breakdown} )</small>"

    def generate_html(self, data, template_name, output_filename):
        template = self.env.get_template(template_name)
        html_content = template.render(data)
        
        output_path = os.path.join(self.output_dir, output_filename)
        with open(output_path, "w") as f:
            f.write(html_content)
        return output_path
