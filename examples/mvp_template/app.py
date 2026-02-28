from datetime import datetime, timezone
from typing import Dict, List, Optional
from uuid import uuid4

from fastapi import Depends, FastAPI, Header, HTTPException, Query
from pydantic import BaseModel, Field

app = FastAPI(title="Aetherium MVP Template", version="0.1.0")

API_KEY = "dev-secret"

agents: Dict[str, dict] = {}
intents: Dict[str, dict] = {}
events: List[dict] = []


class CreateAgentRequest(BaseModel):
    name: str
    type: str
    config: Dict = Field(default_factory=dict)


class SubmitIntentRequest(BaseModel):
    actorId: str
    action: str
    payload: Dict = Field(default_factory=dict)
    priority: str = "normal"
    idempotencyKey: Optional[str] = None


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def auth(x_api_key: str = Header(...), x_tenant_id: str = Header(...)) -> str:
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="invalid api key")
    return x_tenant_id


@app.get("/v1/health")
def health(tenant: str = Depends(auth)):
    return {
        "status": "ok",
        "service": "aetherium-mvp",
        "version": "0.1.0",
        "timestamp": now_iso(),
        "tenant": tenant,
    }


@app.get("/v1/agents")
def list_agents(status: Optional[str] = Query(default=None), tenant: str = Depends(auth)):
    result = [a for a in agents.values() if a["tenantId"] == tenant]
    if status:
        result = [a for a in result if a["status"] == status]
    return {"data": result, "meta": {"total": len(result)}}


@app.post("/v1/agents", status_code=201)
def create_agent(req: CreateAgentRequest, tenant: str = Depends(auth)):
    agent_id = f"agt_{uuid4().hex[:12]}"
    doc = {
        "id": agent_id,
        "tenantId": tenant,
        "name": req.name,
        "type": req.type,
        "status": "active",
        "config": req.config,
        "createdAt": now_iso(),
        "updatedAt": now_iso(),
    }
    agents[agent_id] = doc
    return {"data": doc}


@app.post("/v1/intents", status_code=202)
def submit_intent(req: SubmitIntentRequest, tenant: str = Depends(auth)):
    intent_id = f"int_{uuid4().hex[:12]}"
    decision = {
        "result": "approved",
        "reason": "passed MVP baseline policy",
        "policiesEvaluated": ["default_allowlist"],
        "decidedAt": now_iso(),
    }
    doc = {
        "id": intent_id,
        "tenantId": tenant,
        "actorId": req.actorId,
        "action": req.action,
        "payload": req.payload,
        "status": "approved",
        "governanceDecision": decision,
        "createdAt": now_iso(),
        "updatedAt": now_iso(),
    }
    intents[intent_id] = doc

    evt = {
        "id": f"evt_{uuid4().hex[:12]}",
        "tenantId": tenant,
        "type": "intent.approved",
        "source": "governance-mvp",
        "intentId": intent_id,
        "payload": {"action": req.action, "actorId": req.actorId},
        "occurredAt": now_iso(),
    }
    events.append(evt)

    return {"data": doc}


@app.get("/v1/intents/{intent_id}")
def get_intent(intent_id: str, tenant: str = Depends(auth)):
    doc = intents.get(intent_id)
    if not doc or doc["tenantId"] != tenant:
        raise HTTPException(status_code=404, detail="intent not found")
    return {"data": doc}


@app.get("/v1/events")
def list_events(event_type: Optional[str] = Query(default=None), tenant: str = Depends(auth)):
    result = [e for e in events if e["tenantId"] == tenant]
    if event_type:
        result = [e for e in result if e["type"] == event_type]
    return {"data": result, "meta": {"total": len(result)}}
