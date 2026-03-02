# Aetherium MVP Template

Minimal working template สำหรับเริ่ม service ตาม contract ของ Aetherium API

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8080 --reload
```

## Quick test

```bash
curl -H "x-api-key: dev-secret" -H "x-tenant-id: demo" http://localhost:8080/v1/health

curl -X POST http://localhost:8080/v1/agents \
  -H "Content-Type: application/json" \
  -H "x-api-key: dev-secret" \
  -H "x-tenant-id: demo" \
  -d '{"name":"EconomicAgent","type":"economic"}'

curl -X POST http://localhost:8080/v1/intents \
  -H "Content-Type: application/json" \
  -H "x-api-key: dev-secret" \
  -H "x-tenant-id: demo" \
  -d '{"actorId":"AgioSage","action":"allocate_budget","payload":{"amount":1000}}'
```

## Docker

```bash
docker compose up --build
```
