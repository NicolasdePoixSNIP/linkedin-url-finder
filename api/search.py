from flask import Flask, request, jsonify
import requests as req
import json

app = Flask(__name__)

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
        r = req.post(
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

@app.route("/api/search")
def search():
    prenom  = request.args.get("prenom", "")
    nom     = request.args.get("nom", "")
    societe = request.args.get("societe", "")
    pays    = request.args.get("pays", "")
    if not prenom or not nom:
        return jsonify({"error": "prenom et nom requis"}), 400
    result = find_linkedin(prenom, nom, societe, pays)
    return jsonify(result)
