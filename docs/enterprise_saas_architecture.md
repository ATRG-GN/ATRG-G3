# Aetherium Enterprise-Grade Architecture (SaaS/Cloud)

เอกสารนี้เสนอ reference architecture สำหรับยกระดับ Aetherium ไปสู่ production ระดับองค์กร

## 1. Target Characteristics

- Multi-tenant SaaS รองรับ workload หลายองค์กรพร้อมกัน
- Governance-by-default (policy checks before execution)
- High availability + disaster recovery
- End-to-end observability + auditability
- Zero-trust security posture

## 2. Logical Architecture

```text
[Client Apps / SDK / Web Console]
              |
         [API Gateway]
              |
      [AuthN/AuthZ Layer]
              |
      [Intent Ingress Service] ---> [Policy Engine]
              |                          |
              |                          v
              |                    [Decision Store]
              v
      [Orchestrator Service] ---> [Event Bus/Kafka/NATS]
              |                          |
      +-------+--------+                 +--> [Workers/Agents Runtime]
      |                |                 +--> [Notification Service]
      v                v
[OLTP Postgres]   [Immutable Ledger]
      |
      +--> [Analytics ETL] --> [Lakehouse/Warehouse]
```

## 3. Deployment Topology (Cloud)

- **Edge:** WAF + DDoS protection + API Gateway
- **Compute:** Kubernetes (regional multi-AZ)
- **Data:**
  - PostgreSQL (HA) สำหรับ transactional state
  - Redis สำหรับ cache/idempotency locks
  - Object storage สำหรับ artifacts
  - Kafka/NATS สำหรับ event streaming
  - Immutable ledger store (append-only)
- **Control plane:** CI/CD + secrets + config management

## 4. Multi-Tenancy Strategy

ระดับการแยกข้อมูล:

1. **Shared DB + tenant_id column** (เริ่มต้นเร็ว)
2. **Schema per tenant** (เพิ่ม isolation)
3. **Dedicated database/cluster per strategic tenant** (enterprise contract)

แนะนำให้เริ่มแบบ hybrid: shared สำหรับ SMB และ dedicated สำหรับ regulated tenant.

## 5. Core Services (Recommended)

- **API Gateway Service**: auth, quota, routing, TLS termination
- **Identity Service**: OIDC/JWT, service account, key rotation
- **Intent Service**: validate request, idempotency, enqueue orchestration
- **Governance Service**: evaluate policy (RBAC/ABAC + domain rules)
- **Orchestrator Service**: state machine + retry + compensation
- **Agent Runtime Service**: execute approved actions in sandboxed workers
- **Event Service**: query/audit timelines and streaming endpoints
- **Billing/Usage Service**: metering + cost attribution per tenant

## 6. Security Controls

- mTLS ระหว่าง service ภายใน cluster
- Encryption at rest (KMS-backed keys)
- Fine-grained IAM per workload identity
- Secret management via dedicated vault
- Audit log immutable + tamper-evident hashing
- Mandatory trace ID / request ID ทุก transaction

## 7. Reliability & SRE

- SLO examples:
  - API availability >= 99.9%
  - P95 intent acceptance latency < 300ms
  - Governance decision latency P95 < 200ms
- Auto-scaling based on queue depth + CPU/memory
- Retry with exponential backoff + DLQ for poison messages
- Chaos drills + failover tests
- DR objectives:
  - RTO <= 60 minutes
  - RPO <= 5 minutes

## 8. CI/CD and SDLC

- Trunk-based development + protected branches
- Quality gates: unit/integration/contract/security scans
- Progressive delivery: canary then blue/green
- Migration strategy: backward-compatible DB changes first
- Signed container images + SBOM generation

## 9. Observability Blueprint

- **Logs:** JSON structured logs with tenant_id + trace_id + intent_id
- **Metrics:** RED/USE + business KPIs (intent throughput, rejection rate)
- **Tracing:** OpenTelemetry, span links across async event boundaries
- **Alerting:** pager routing by service ownership + severity
- **Dashboards:** executive (SLA/cost) + engineering (latency/errors/saturation)

## 10. Migration Plan from Current Repo

1. Standardize API via `docs/openapi.yaml`
2. Split runtime concerns into services (intent/governance/orchestrator/event)
3. Introduce external message broker instead of in-process queue
4. Add persistent store + audit ledger
5. Roll out tenant-aware auth and quota
6. Establish SRE baselines and incident playbooks
