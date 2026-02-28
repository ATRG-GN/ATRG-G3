# Aetherium Architecture Overview & Refactor Blueprint

เอกสารนี้สรุปภาพรวมสถาปัตยกรรมปัจจุบัน พร้อมแผน refactor รายระยะเพื่อพัฒนาแพลตฟอร์มให้เป็น event-driven, modular และรองรับการกระจายระบบ (distributed-ready)

## 1) สถาปัตยกรรมระบบ (Architecture Overview)

องค์ประกอบหลักจากโครงสร้างโปรเจกต์:

- `AetherBus/core`
- `genesis_node.py`
- `main.py`
- `web_interface.py`
- `conesis-core`
- `components/ai-elements`
- `config`
- `governance`
- `nexus`
- `pangenes`
- `simulation`
- `tests`

### High-level Architecture Diagram

```text
                          ┌───────────────────────────┐
                          │        External Users      │
                          │ ┌── Web Browser / API Client│
                          └┬───────────────────────────┘
                           │
                     REST/WebSocket
                           │
                     ┌─────▼────────────────┐
                     │    Web Interface     │   (web_interface.py)
                     │──────────────────────│
                     │  HTTP API, UI Pages  │
                     │  Authentication      │
                     └────────┬─────────────┘
                              │
                     ┌────────▼──────────┐
                     │   Core Controller  │   (main.py)
                     │────────────────────│
                     │  Orchestration     │
                     │  Event Routing     │
                     └────────┬───────────┘
                              │
         ┌────────────────────┴──────────────────────────────────┐
         │                       AetherBus/Core                   │
         │  (Event Bus + Message Routing + Internal Protocols)   │
         └─────────────────▲─────────────────▲───────────────────┘
                           │                 │
                     ┌─────┴─────┐       ┌───┴─────────┐
                     │ Genesis   │       │ Neural/AI   │
                     │ Node      │       │ Engine      │
                     │ (Agent)   │       │ (ai-elements)│
                     └───────────┘       └─────────────┘
                           │                     │
                     ┌─────┴─────┐       ┌───────┴──────┐
                     │ Governance│       │ Simulation   │
                     │ Protocols │       │ & Plugins    │
                     └───────────┘       └──────────────┘
```

### Component Summary

- **Web Interface**
  - รับ HTTP/WebSocket
  - ส่งคำสั่งและแสดงผล
  - แยก UI logic ออกจาก Core เพื่อ modularity
- **Core Controller**
  - จุดศูนย์กลาง orchestration
  - รับ event จาก UI และ Agent
  - ส่ง event เข้าสู่ AetherBus
- **AetherBus (Event Bus)**
  - สถาปัตยกรรมแบบ message-driven ระหว่าง agents
  - รองรับ event routing แบบ asynchronous
- **Genesis Node**
  - bootstrap node เริ่มต้นระบบ
- **Neural/AI Engine**
  - อยู่ใน `components/ai-elements`
  - ประมวลผลแบบ asynchronous
  - แยก AI compute logic ออกจาก Core
- **Governance**
  - จัดเก็บ rules / policies
  - ตรวจสอบ actions ของ agents
- **Simulation & Plugins**
  - ใช้สำหรับ simulation และ extension modules

## 2) Refactor Roadmap (Step-by-Step)

### Phase 1 — Structure & Core Foundation

1. **Requirement & Domain Model**
   - ระบุ use-cases, event types, API contracts
2. **Module Separation**
   - จัดโครงสร้างเป็น subpackages:
     - `core/`
     - `service/api/`
     - `agents/`
     - `bus/`
     - `ai/`
     - `tests/`
3. **Define Event Bus API**
   - กำหนด interface กลางสำหรับ event/message passing
4. **Config Loader**
   - โหลดค่า config จาก `.json` หรือ `.yaml`
5. **Web API Refactoring**
   - แยก Router / Controllers / DTO + Validators

### Phase 2 — Expand into Distributed System

1. แยก networking layer รองรับ gRPC/WebSockets
2. เพิ่ม async event queue (เช่น Redis Streams / NATS)
3. พัฒนา node discovery (leader selection, load balancing)
4. ทำ event persistence เพื่อ audit/trace

### Phase 3 — Modular AI & Plugins

1. AI engine adapter แบบ plugin
2. รองรับโหมด `local` และ `cloud API`
3. กำหนด AI interface ชัดเจน (prompt handling, model selection)

### Phase 4 — Security & Observability

1. **Auth & RBAC**: JWT / OAuth2
2. **Monitoring**: Prometheus + Grafana
3. **Tracing**: OpenTelemetry
4. **CI/CD**: GitHub Actions + automated tests

## 3) System Design Blueprint (Detailed)

### Architectural Principles

| Principle | Description |
| --- | --- |
| Modularity | แยก concerns อย่างชัดเจน |
| Event-Driven | รองรับ event handling ขนาดใหญ่ |
| Extensible | เพิ่ม Agent / Plugin ได้ง่าย |
| Scalable | รองรับ distributed nodes |

### Core Layer Design

```text
Core Controller (main.py)
│
├── Config
├── Router
│   └── EventDispatcher
├── AetherBus (bus/core)
│   ├── EventQueue
│   ├── Subscriber Registry
│   └── Publisher API
├── API Adapters
│   ├── HTTP API
│   ├── WebSocket
│   └── gRPC (future)
└── Lifecycle Management
```

### Event Protocol

```json
{
  "id": "UUID",
  "timestamp": "ISO8601",
  "type": "String",
  "payload": {},
  "source": "String",
  "tags": ["String"]
}
```

- **Publisher API**
  - `bus.publish(event_type, payload)`
- **Subscriber API**
  - `@bus.subscribe("AGENT.ACTION")`
  - `async def handler(event): ...`

### Node & Network

แต่ละ node ควรประกอบด้วย:

- Node ID
- Event Queue
- Heartbeat
- State Sync

### Data Flow

`User -> Web API -> Controller -> AetherBus -> Agents -> Response`

1. Client ส่ง request
2. Controller แปลงเป็น event
3. Event ถูกส่งเข้าสู่ Core
4. Core route ไปยัง subscribed agents
5. Agents ส่งผลลัพธ์กลับ
6. Web UI แจ้งผลให้ผู้ใช้

### AI Integration

```text
AI Adapter
├── Model Client
├── Prompt Manager
└── Response Cache
```

รองรับทั้ง internal LLM และ external APIs

### Security

| Component | Security |
| --- | --- |
| API | JWT/Auth0 |
| Event Bus | TLS encrypted |
| Node Communication | Mutual TLS |
| Governance Rules | Whitelist + RBAC |

### Observability

| Tool | Purpose |
| --- | --- |
| Logs | Logging |
| Metrics | Prometheus |
| Tracing | OpenTelemetry |
| Alerts | Grafana |

### Deployment

- Containerization: Docker
- Orchestration: Kubernetes
- Environment config: `.env` / secrets manager

### Testing Plan

| Test Type | Scope |
| --- | --- |
| Unit | individual modules |
| Integration | API + event bus |
| E2E | UI with backend |
| Load | stress testing |

## สรุป

คุณภาพของระบบจะเพิ่มขึ้นอย่างมีนัยสำคัญเมื่อ:

- เปลี่ยนเป็น event-driven architecture อย่างครบวงจร
- แยก modules ตามแนวทาง domain-driven และ layering ที่ชัดเจน
- รองรับ distributed nodes พร้อม observability/security ตั้งแต่ต้น
- มี AI abstraction layer สำหรับ neural components และ external model providers
