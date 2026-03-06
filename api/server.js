const http = require('http');
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const PORT = process.env.PORT || 3000;
const runsDir = path.join(__dirname, '..', 'runs');
const runStore = new Map();

if (!fs.existsSync(runsDir)) {
  fs.mkdirSync(runsDir, { recursive: true });
}

function sendJson(res, statusCode, payload) {
  const body = JSON.stringify(payload, null, 2);
  res.writeHead(statusCode, { 'Content-Type': 'application/json' });
  res.end(body);
}

function parseBody(req) {
  return new Promise((resolve, reject) => {
    let data = '';
    req.on('data', chunk => {
      data += chunk;
      if (data.length > 1_000_000) {
        reject(new Error('Request body too large'));
      }
    });
    req.on('end', () => {
      if (!data) {
        resolve({});
        return;
      }
      try {
        resolve(JSON.parse(data));
      } catch {
        reject(new Error('Invalid JSON body'));
      }
    });
    req.on('error', reject);
  });
}

function createPseudoZip(bundleDigest) {
  const zipPath = path.join(runsDir, `${bundleDigest}.zip`);
  const content = Buffer.from(`PK\u0003\u0004\nDemo bundle for ${bundleDigest}\n`, 'utf8');
  fs.writeFileSync(zipPath, content);
  return zipPath;
}

const server = http.createServer(async (req, res) => {
  const url = new URL(req.url, `http://${req.headers.host}`);

  if (req.method === 'GET' && url.pathname === '/health') {
    return sendJson(res, 200, { status: 'ok', service: 'paygod-cloud-starter-api' });
  }

  if (req.method === 'POST' && url.pathname === '/run') {
    try {
      const input = await parseBody(req);
      const digestSeed = JSON.stringify(input) + Date.now().toString();
      const bundleDigest = crypto.createHash('sha256').update(digestSeed).digest('hex').slice(0, 16);
      createPseudoZip(bundleDigest);

      const run = {
        bundle_digest: bundleDigest,
        status: 'PASS',
        created_at: new Date().toISOString(),
        input
      };
      runStore.set(bundleDigest, run);
      return sendJson(res, 201, run);
    } catch (error) {
      return sendJson(res, 400, { error: error.message });
    }
  }

  const runMatch = url.pathname.match(/^\/runs\/([A-Za-z0-9_-]+)$/);
  if (req.method === 'GET' && runMatch) {
    const bundleDigest = runMatch[1];
    const run = runStore.get(bundleDigest);
    if (!run) {
      return sendJson(res, 404, { error: 'Run not found', bundle_digest: bundleDigest });
    }
    return sendJson(res, 200, run);
  }

  const zipMatch = url.pathname.match(/^\/runs\/([A-Za-z0-9_-]+)\/zip$/);
  if (req.method === 'GET' && zipMatch) {
    const bundleDigest = zipMatch[1];
    const zipPath = path.join(runsDir, `${bundleDigest}.zip`);
    if (!fs.existsSync(zipPath)) {
      return sendJson(res, 404, { error: 'Bundle zip not found', bundle_digest: bundleDigest });
    }

    res.writeHead(200, {
      'Content-Type': 'application/zip',
      'Content-Disposition': `attachment; filename="${bundleDigest}.zip"`
    });
    fs.createReadStream(zipPath).pipe(res);
    return;
  }

  sendJson(res, 404, { error: 'Not found' });
});

server.listen(PORT, () => {
  console.log(`API listening on http://localhost:${PORT}`);
});
