# Developer Workflow

## Run the API locally

```bash
cd api
npm start
```

The server starts on `http://localhost:3000`.

## Run a demo

1. Check health:
   ```bash
   curl http://localhost:3000/health
   ```
2. Create a run:
   ```bash
   curl -X POST http://localhost:3000/run \
     -H "Content-Type: application/json" \
     -d '{"demo":"hello-cloud"}'
   ```
3. Copy the `bundle_digest` from response.
4. Query run:
   ```bash
   curl http://localhost:3000/runs/<bundle_digest>
   ```
5. Download ZIP:
   ```bash
   curl -L http://localhost:3000/runs/<bundle_digest>/zip -o runs/<bundle_digest>.zip
   ```
