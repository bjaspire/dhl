import pandas as pd
from jinja2 import Environment, FileSystemLoader
import os

class SprintReportGenerator:
    def __init__(self, template_dir, output_dir):
        self.env = Environment(loader=FileSystemLoader(template_dir))
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def generate_html(self, data, template_name, output_filename):
        template = self.env.get_template(template_name)
        html_content = template.render(data)
        
        output_path = os.path.join(self.output_dir, output_filename)
        with open(output_path, "w") as f:
            f.write(html_content)
        return output_path

    def generate_excel(self, sprint_metrics, people_metrics, output_filename):
        output_path = os.path.join(self.output_dir, output_filename)
        
        # Sprint Summary Sheet
        df_summary = pd.DataFrame([sprint_metrics])
        
        # People Metrics Sheet
        people_data = []
        for name, stats in people_metrics.items():
            people_data.append({
                "Name": name,
                "Role": stats["role"],
                "Hours Logged": round(stats["hours"], 2),
                "Issues Worked Count": stats["issues_count"],
                "Issues List": stats["issues_list"],
                "Comments Count": stats["comments"]
            })
        df_people = pd.DataFrame(people_data)
        
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            df_summary.to_excel(writer, sheet_name='Sprint Summary', index=False)
            df_people.to_excel(writer, sheet_name='People Contribution', index=False)
            
        return output_path
