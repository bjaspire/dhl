import requests
from requests.auth import HTTPBasicAuth

class JiraClient:
    def __init__(self, url, email, token):
        self.url = url.rstrip('/')
        self.session = requests.Session()
        self.session.auth = HTTPBasicAuth(email, token)
        self.session.headers.update({
            "Accept": "application/json",
            "Content-Type": "application/json"
        })

    def get(self, endpoint, params=None):
        # Handle cases where endpoint already starts with a slash
        endpoint = endpoint.lstrip('/')
        
        if endpoint.startswith("rest/agile/1.0/") or endpoint.startswith("rest/api/2/"):
            url = f"{self.url}/{endpoint}"
        else:
            url = f"{self.url}/rest/api/3/{endpoint}"
        
        response = self.session.get(url, params=params)
        
        # If 410 Gone, try v2 API
        if response.status_code == 410 and not endpoint.startswith("rest/api/2/"):
            return self.get(f"rest/api/2/{endpoint}", params)
            
        response.raise_for_status()
        return response.json()

    def get_agile(self, endpoint, params=None):
        return self.get(f"rest/agile/1.0/{endpoint}", params)

    def post(self, endpoint, payload=None):
        endpoint = endpoint.lstrip('/')
        
        if endpoint.startswith("rest/agile/1.0/") or endpoint.startswith("rest/api/2/"):
            url = f"{self.url}/{endpoint}"
        else:
            url = f"{self.url}/rest/api/3/{endpoint}"
            
        response = self.session.post(url, json=payload)
        
        if response.status_code == 410 and not endpoint.startswith("rest/api/2/"):
            return self.post(f"rest/api/2/{endpoint}", payload)
            
        response.raise_for_status()
        return response.json()
    def search_issues(self, jql, fields=None, expand=None, max_results=1000):
        payload = {
            "jql": jql,
            "maxResults": max_results
        }
        if fields:
            payload["fields"] = fields
        if expand:
            payload["expand"] = expand
        
        try:
            issues = self.post("search/jql", payload).get("issues", [])

            # Handle worklog pagination (Jira only returns first 20 worklogs per issue)
            if fields and "worklog" in fields:
                for issue in issues:
                    wl = issue.get("fields", {}).get("worklog", {})
                    if wl.get("total", 0) > len(wl.get("worklogs", [])):
                        try:
                            full_wl = self.get(f"issue/{issue['key']}/worklog")
                            if full_wl and "worklogs" in full_wl:
                                issue["fields"]["worklog"] = full_wl
                        except Exception as e:
                            print(f"Failed to fetch full worklogs for {issue['key']}: {e}")

            return issues
        except Exception as e:
            print(f"Error searching issues: {e}")
            return []
