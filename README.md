# AETHERIUM PLATFORM

Production-ready blueprint สำหรับระบบ Multi-Agent + Governance-first orchestration ที่ออกแบบให้เติบโตจาก MVP ไปสู่ Enterprise SaaS/Cloud ได้จริง

![python](https://img.shields.io/badge/Python-3.11%2B-blue)
![fastapi](https://img.shields.io/badge/API-FastAPI-009688)
![architecture](https://img.shields.io/badge/Architecture-Event--Driven-purple)
![governance](https://img.shields.io/badge/Governance-GEP%20Enforced-success)

---

## 1) Project Overview

Aetherium คือแพลตฟอร์ม orchestration สำหรับ **agent-based workflows** ที่เน้น 3 แกนหลัก:

- **Reliability:** Event-driven core + audit trail
- **Governance:** Policy enforcement (GEP/Inspira-Firma) ก่อน execute ทุก intent
- **Scalability:** พร้อมยกระดับไปสู่ multi-tenant SaaS deployment

เหมาะกับ use-cases เช่น autonomous operations, AI workflow governance, simulation-to-production transition.

---

## 2) Repository Structure

```text
.
├─ core/                        # Runtime core (bus, envelope, conductor, identity, records)
├─ agents/                      # Domain agents (analysis, economic, governance, etc.)
├─ governance/                  # Governance protocol and enforcement logic
├─ aetherium_core/              # Microkernel + plugin-ready next-gen core
├─ tests/                       # Unit + integration tests
├─ docs/
│  ├─ openapi.yaml              # Full OpenAPI 3.1 spec (production contract)
│  └─ enterprise_saas_architecture.md
├─ examples/
│  └─ mvp_template/             # Full working minimal template (FastAPI)
├─ web_interface.py             # Real-time web console API/websocket
└─ main.py                      # Basic orchestration entry point
```

---

## 3) Quick Start (Current Repo)

### 3.1 Prerequisites

- Python 3.11+
- pip / venv

### 3.2 Install

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3.3 Run tests

```bash
pytest -q
```

### 3.4 Run web console (development)

```bash
uvicorn web_interface:app --host 0.0.0.0 --port 8000 --reload
```

Open `http://localhost:8000`.

---

## 4) API Contract (OpenAPI)

เอกสาร OpenAPI ฉบับ production อยู่ที่:

- `docs/openapi.yaml`

Scope ครอบคลุม:

- Authentication + Tenant headers
- Agent lifecycle
- Intent submission + approval flow
- Event query
- WebSocket handshake contract
- Health/readiness/liveness probes
- Standard error model + tracing fields

สามารถ validate ได้ด้วย:

```bash
python -c "import yaml; yaml.safe_load(open('docs/openapi.yaml'))"
```

---

## 5) Full Working MVP Template

ตัวอย่างพร้อมรันจริงอยู่ที่:

- `examples/mvp_template/`

จุดเด่น:

- FastAPI app ที่ implement endpoint หลัก (health/agents/intents/events)
- In-memory event store สำหรับ onboarding เร็ว
- API key auth แบบง่าย
- Dockerfile + docker-compose พร้อมใช้งาน
- OpenAPI-compatible shape สำหรับต่อยอด production

Run MVP:

```bash
cd examples/mvp_template
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8080 --reload
```

Health check:

```bash
curl -H "x-api-key: dev-secret" http://localhost:8080/v1/health
```

---

## 6) Enterprise-Grade Architecture (SaaS/Cloud)

เอกสารฉบับเต็ม:

- `docs/enterprise_saas_architecture.md`

หัวข้อสำคัญที่ครอบคลุม:

- Multi-tenant isolation strategy (shared vs pooled vs dedicated)
- API Gateway + AuthN/AuthZ + policy enforcement pipeline
- Event bus + workflow orchestrator + plugin runtime
- Data topology (OLTP, immutable ledger, analytics lakehouse)
- Observability (logs/metrics/traces), SLOs, and incident workflow
- Security controls (secrets, KMS, key rotation, audit)
- CI/CD, blue/green/canary, and DR strategy (RTO/RPO)

---

## 7) Production Readiness Checklist

- [ ] API contract versioned and backward-compatible policy defined
- [ ] Tenant boundary tests + policy regression tests
- [ ] End-to-end traceability from request -> intent -> action -> record
- [ ] SLO dashboard + alert routing configured
- [ ] Backup/restore drills completed
- [ ] Security scans (SAST, dependency, container) integrated in CI
- [ ] Threat model + runbooks updated

---

## 8) Suggested Next Steps

1. Generate server/client stubs จาก `docs/openapi.yaml`
2. Map existing `core/` และ `aetherium_core/` เข้ากับ endpoint contract
3. Replace in-memory store ใน MVP ด้วย PostgreSQL + Redis + message broker
4. Add OIDC/JWT + RBAC/ABAC policy engine
5. Enable distributed tracing + governance decision audit viewer

---

## 9) License & Security

- Security policy: `SECURITY.md`
- Dependency updates: `dependabot.yml`
