# LinkedIn URL Finder API

API Vercel pour trouver automatiquement les URLs de profils LinkedIn.

## Endpoint

GET /api/search?prenom=Georges&nom=delaTaille&societe=Actusite&pays=France

## Réponse

{"url": "https://fr.linkedin.com/in/...", "statut": "trouvé", "found": true}

## Stack
- Python (Vercel Serverless)
- Serper.dev API
