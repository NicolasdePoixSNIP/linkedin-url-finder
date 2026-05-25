Voici le contenu complet de api/search.js :
javascriptconst https = require('https');

const SERPER_KEY = process.env.SERPER_KEY || "8cf636c6d6a5485b7e87f40c8ee0f8c9053a2edf";

function serperSearch(query) {
  return new Promise((resolve, reject) => {
    const data = JSON.stringify({ q: query, num: 3, gl: "fr", hl: "fr" });
    const options = {
      hostname: 'google.serper.dev',
      path: '/search',
      method: 'POST',
      headers: {
        'X-API-KEY': SERPER_KEY,
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(data)
      }
    };
    const req = https.request(options, (res) => {
      let body = '';
      res.on('data', chunk => body += chunk);
      res.on('end', () => {
        try { resolve(JSON.parse(body)); }
        catch(e) { reject(e); }
      });
    });
    req.on('error', reject);
    req.write(data);
    req.end();
  });
}

async function findLinkedin(prenom, nom, societe, pays) {
  const attempts = [
    { q: `site:linkedin.com/in "${prenom} ${nom}" "${societe}"${pays ? ` "${pays}"` : ''}`, label: 'trouvé' },
    { q: `site:linkedin.com/in "${prenom} ${nom}" "${societe}"`, label: 'trouvé (sans pays)' },
    { q: `site:linkedin.com/in "${prenom} ${nom}"`, label: 'trouvé (sans société)' },
  ];
  for (const attempt of attempts) {
    const result = await serperSearch(attempt.q);
    const organic = result.organic || [];
    for (const item of organic) {
      if (item.link && item.link.includes('linkedin.com/in/')) {
        return { url: item.link, statut: attempt.label, found: true };
      }
    }
  }
  return { url: '', statut: 'non trouvé', found: false };
}

module.exports = async (req, res) => {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', '*');
  if (req.method === 'OPTIONS') { return res.status(200).end(); }
  res.setHeader('Content-Type', 'application/json');

  const { prenom, nom, societe = '', pays = '' } = req.query;
  if (!prenom || !nom) {
    return res.status(400).json({ error: 'prenom et nom requis' });
  }
  try {
    const result = await findLinkedin(prenom, nom, societe, pays);
    return res.status(200).json(result);
  } catch(e) {
    return res.status(500).json({ error: e.message });
  }
};
