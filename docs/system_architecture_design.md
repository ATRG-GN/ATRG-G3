# ATRG-G3 – System Architecture & Design Document

**Aetherium Core Driver – Neural Bridge Architecture**  
**Version:** Draft v1.0  
**Status:** Proposed Refactor Blueprint

## 1. Overview

ATRG-G3 คือระบบแบบ **Event-Driven Modular Platform** ที่ประกอบด้วย:

- Core Controller
- AetherBus (Event Bus)
- Genesis Node
- AI/Neural Engine
- Web Interface
- Governance Layer
- Simulation / Plugin Layer

ระบบออกแบบเพื่อรองรับ:

- Modular extension
- Distributed nodes
- AI orchestration
- High scalability

## 2. High-Level Architecture

```text
Client
  │
  ▼
Web Interface (HTTP/WebSocket)
  │
  ▼
Core Controller
  │
  ▼
AetherBus (Event Bus)
  ├── Genesis Node
  ├── AI Engine
  ├── Governance
  └── Simulation/Plugins
```

## 3. Directory Structure (Proposed Refactor)

```text
atrg_g3/
│
├── core/
│   ├── controller.py
│   ├── lifecycle.py
│   └── config.py
│
├── bus/
│   ├── event.py
│   ├── dispatcher.py
│   └── registry.py
│
├── agents/
│   ├── genesis_node.py
│   └── base_agent.py
│
├── ai/
│   ├── adapter.py
│   ├── prompt_manager.py
│   └── model_client.py
│
├── api/
│   ├── routes.py
│   ├── websocket.py
│   └── schemas.py
│
├── governance/
│   └── policy_engine.py
│
├── simulation/
│   └── simulator.py
│
├── tests/
│
└── main.py
```

## 4. Event Model

### 4.1 Event Schema

```python
# bus/event.py

from dataclasses import dataclass
from typing import Any, Dict
import uuid
import datetime

@dataclass
class Event:
    id: str
    timestamp: str
    type: str
    payload: Dict[str, Any]
    source: str

    @staticmethod
    def create(event_type: str, payload: Dict, source: str):
        return Event(
            id=str(uuid.uuid4()),
            timestamp=datetime.datetime.utcnow().isoformat(),
            type=event_type,
            payload=payload,
            source=source
        )
```

## 5. Event Bus (AetherBus)

```python
# bus/dispatcher.py

from typing import Callable, Dict, List
from bus.event import Event

class EventDispatcher:

    def __init__(self):
        self.subscribers: Dict[str, List[Callable]] = {}

    def subscribe(self, event_type: str, handler: Callable):
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(handler)

    async def publish(self, event: Event):
        handlers = self.subscribers.get(event.type, [])
        for handler in handlers:
            await handler(event)
```

## 6. Core Controller

```python
# core/controller.py

from bus.dispatcher import EventDispatcher
from bus.event import Event

class CoreController:

    def __init__(self, dispatcher: EventDispatcher):
        self.dispatcher = dispatcher

    async def handle_request(self, request_data: dict):
        event = Event.create(
            event_type="USER.REQUEST",
            payload=request_data,
            source="web"
        )
        await self.dispatcher.publish(event)
```

## 7. Base Agent Architecture

```python
# agents/base_agent.py

class BaseAgent:

    def __init__(self, dispatcher):
        self.dispatcher = dispatcher

    def register(self):
        raise NotImplementedError
```

## 8. Genesis Node

```python
# agents/genesis_node.py

from agents.base_agent import BaseAgent

class GenesisNode(BaseAgent):

    def register(self):
        self.dispatcher.subscribe("USER.REQUEST", self.process)

    async def process(self, event):
        print(f"[GenesisNode] Received event: {event.payload}")
```

## 9. AI Adapter Layer

```python
# ai/adapter.py

class AIAdapter:

    def __init__(self, model_client):
        self.model_client = model_client

    async def generate(self, prompt: str):
        response = await self.model_client.call(prompt)
        return response
```

## 10. Governance Layer

```python
# governance/policy_engine.py

class PolicyEngine:

    def validate(self, event):
        if "forbidden" in event.payload:
            raise Exception("Policy violation")
```

Integration inside dispatcher:

```python
async def publish(self, event: Event):
    policy_engine.validate(event)
    handlers = self.subscribers.get(event.type, [])
    for handler in handlers:
        await handler(event)
```

## 11. Web API Example (FastAPI)

```python
# api/routes.py

from fastapi import APIRouter
from core.controller import CoreController

router = APIRouter()

@router.post("/request")
async def user_request(data: dict):
    await controller.handle_request(data)
    return {"status": "accepted"}
```

## 12. Async Upgrade (Recommended)

เปลี่ยน dispatcher เป็น async queue:

```python
import asyncio

class AsyncEventBus:

    def __init__(self):
        self.queue = asyncio.Queue()

    async def publish(self, event):
        await self.queue.put(event)

    async def start(self):
        while True:
            event = await self.queue.get()
            # dispatch logic
```

## 13. Distributed Mode (Future)

Node Communication Protocol:

```text
Node
 ├── Heartbeat
 ├── Leader Election
 ├── Event Replication
```

สามารถต่อยอดด้วย:

- Redis Streams
- NATS
- Kafka
- gRPC

## 14. Security Model

| Layer | Security |
| --- | --- |
| API | JWT |
| Node Communication | TLS |
| Event Validation | Governance Policy |
| Admin Control | RBAC |

## 15. Observability

- Structured Logging (JSON)
- Prometheus metrics endpoint
- Health check endpoint `/health`
- Distributed tracing (OpenTelemetry)

## 16. Deployment Strategy

### Dockerfile (Example)

```dockerfile
FROM python:3.11
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "main.py"]
```

## 17. CI/CD (GitHub Actions)

```yaml
name: ATRG-G3 CI

on: [push]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Install deps
        run: pip install -r requirements.txt
      - name: Run tests
        run: pytest
```

## 18. Testing Strategy

| Test | Description |
| --- | --- |
| Unit | Event, Dispatcher |
| Integration | API + Bus |
| E2E | Full workflow |
| Load | Event throughput |

## 19. Roadmap Summary

- Phase 1 → Modular Core
- Phase 2 → Async Event Bus
- Phase 3 → Distributed Nodes
- Phase 4 → AI Orchestration Layer
- Phase 5 → Production Hardening

## 20. Conclusion

ATRG-G3 ควรพัฒนาเป็น:

- Event-Driven Architecture
- Modular Agent-Based System
- AI-Extensible Platform
- Distributed Ready Infrastructure

หากคุณต้องการ สามารถต่อยอดเป็น:

- README.md แบบ production-ready
- OpenAPI spec เต็มรูปแบบ
- ตัวอย่าง full working minimal version (MVP template)
- Enterprise-grade architecture (ระดับ SaaS/Cloud)
