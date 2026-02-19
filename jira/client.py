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
        
        if endpoint.startswith("rest/agile/1.0/"):
            url = f"{self.url}/{endpoint}"
        else:
            url = f"{self.url}/rest/api/3/{endpoint}"
        
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()

    def get_agile(self, endpoint, params=None):
        return self.get(f"rest/agile/1.0/{endpoint}", params)
