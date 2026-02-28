# Aetherium: Modular / Microkernel Refactor Blueprint

เอกสารนี้เพิ่มโครงสร้างอ้างอิงสำหรับการแยก `Aetherium Core` ออกจากส่วนเสริมแบบ plug-in พร้อมรากฐานสำหรับ distributed/event-driven system

## สิ่งที่เพิ่มในโค้ด

- `aetherium_core/kernel/core_engine.py`
  - Core engine แบบ minimal: lifecycle management, event bus, message routing, plugin registry
  - รองรับ dynamic loading ผ่าน `module:ClassName`
- `aetherium_core/kernel/events.py`
  - Event envelope + async event bus
- `aetherium_core/kernel/routing.py`
  - Message router สำหรับ route key -> handler
- `aetherium_core/kernel/plugins.py`
  - Plugin contract กลาง
- `aetherium_core/plugins/*`
  - ตัวอย่างปลั๊กอิน: Neural / Genesis Node / Web UI
- Layer separation:
  - `interface/` API gateway facade
  - `application/` orchestration use-case
  - `domain/` AI adapter abstraction
  - `infrastructure/` message broker abstraction
- Cross-cutting:
  - `security/auth.py` สำหรับ RBAC entry point
  - `observability/telemetry.py` สำหรับ structured JSON log

## Mapping กับแนวทาง 1–9

1. **Modular/Microkernel**: kernel + plugins + dynamic loading
2. **Event-driven**: async event bus + broker interface
3. **Layered architecture**: interface/application/domain/infrastructure แยกชัด
4. **API Gateway + REST/WebSocket/gRPC**: facade methods แยก transport
5. **Distributed node readiness**: Genesis plugin + broker abstraction รองรับต่อยอด leader election/discovery
6. **AI abstraction**: AIAdapter แยก model backend ออกจาก business flow
7. **Security hardening hooks**: RBAC enforcement entry point
8. **Observability**: structured logging utility
9. **DevOps readiness**: test ใหม่ตรวจ kernel behavior

## แนวทางต่อยอดทันที

- เพิ่ม Redis Streams/NATS/Kafka adapter ใน `infrastructure/message_broker.py`
- เพิ่ม JWT/OAuth2 verifier ใน `security/`
- ผูก OpenTelemetry span ใน event publish/route paths
- แยก plugin manifests (yaml/json) เพื่อให้โหลด plugin ตาม environment
