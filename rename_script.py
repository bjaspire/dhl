import os
import glob
import shutil

# To make the file index.html so it serves correctly on github pages
outputs = glob.glob("output/daily_reports/*.html")
if outputs:
    outputs.sort()
    latest_report = outputs[-1]
    shutil.copy(latest_report, "output/daily_reports/index.html")
    print(f"Copied {latest_report} to index.html")
