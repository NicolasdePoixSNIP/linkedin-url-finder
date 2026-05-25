from http.server import BaseHTTPRequestHandler
import json
import requests
import urllib.parse

SERPER_KEY = "8cf636c6d6a5485b7e87f40c8ee0f8c9053a2edf"

def find_linkedin(prenom, nom, societe, pays=""):
    headers = {
        "X-API-KEY": SERPER_KEY,
        "Content-Type": "application/json"
    }
    attempts = [
        f'site:linkedin.com/in "{prenom} {nom}" "{societe}"' + (f' "{pays}"' if pays else ""),
        f'site:linkedin.com/in "{prenom} {nom}" "{societe}"',
        f'site:linkedin.com/in "{prenom} {nom}"',
    ]
    labels = ["trouvé", "trouvé (sans pays)", "trouvé (sans société)"]
    for query, label in zip(attempts, labels):
        r = requests.post(
            "https://google.serper.dev/search",
            headers=headers,
            data=json.dumps({"q": query, "num": 3, "gl": "fr", "hl": "fr"}),
            timeout=10
        )
        for result in r.json().get("organic", []):
            link = result.get("link", "")
            if "linkedin.com/in/" in link:
                return {"url": link, "statut": label, "found": True}
    return {"url": "", "statut": "non trouvé", "found": False}

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)
        prenom  = params.get("prenom",  [""])[0]
        nom     = params.get("nom",     [""])[0]
        societe = params.get("societe", [""])[0]
        pays    = params.get("pays",    [""])[0]
        if not prenom or not nom:
            self.send_response(400)
            self.send_header("Content-Type", "application/json")
            self.send_header("Access-Control-Allow-Origin", "*")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "prenom et nom requis"}).encode())
            return
        result = find_linkedin(prenom, nom, societe, pays)
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(result).encode())

    def log_message(self, format, *args):
        pass
