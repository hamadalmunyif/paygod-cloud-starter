# API Reference

Base URL (local): `http://localhost:3000`

## Endpoints

### `GET /health`
Returns service health.

Example response:
```json
{
  "status": "ok",
  "service": "paygod-cloud-starter-api"
}
```

### `POST /run`
Creates a minimal demo run and returns a `bundle_digest`.

Example request:
```json
{
  "demo": "hello-cloud"
}
```

Example response:
```json
{
  "bundle_digest": "abc123...",
  "status": "PASS",
  "created_at": "2026-01-01T00:00:00.000Z",
  "input": {
    "demo": "hello-cloud"
  }
}
```

### `GET /runs/:bundle_digest`
Returns metadata for a run by digest.

### `GET /runs/:bundle_digest/zip`
Downloads the generated demo ZIP artifact.
