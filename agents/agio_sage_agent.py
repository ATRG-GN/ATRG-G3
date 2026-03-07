from __future__ import annotations

import asyncio
from typing import Any, Dict, List, Optional

from agents.base_agent import BaseAgent
from core.envelope import AetherIntent, Envelope
from core.knowledge_base import SimpleKnowledgeGraph
from core.knowledge_processor import KnowledgeCentricProcessor, SimpleVectorDB


class AgioSageAgent(BaseAgent):
    """AGIO wisdom gateway used by governance audit flow."""

    def __init__(self, conductor):
        super().__init__("AGIO_Sage", conductor)
        self.graph = SimpleKnowledgeGraph()
        self.kcp = KnowledgeCentricProcessor(self.graph, SimpleVectorDB(self.graph))
        self.memory: List[Dict[str, Any]] = []
        self.is_reflecting = False

    async def start(self):
        await self.subscribe("query.knowledge.retrieve", self.handle_query)
        await self.subscribe("cognition.interrupt", self.handle_interrupt)

    async def think_about(self, query: str, flow_id: Optional[str] = None):
        if self.is_reflecting:
            return None

        thought = self._simulate_llm_generation(query)
        memory_entry = {"type": "thought", "query": query, "content": thought}
        self.memory.append(memory_entry)

        await self.publish(
            "cognition.thought_stream",
            AetherIntent.SHARE_INFO,
            {
                "query": query,
                "content": thought,
                "_security_context": "AGIO-CODEX Architect Verified Thought",
            },
            flow_id,
        )
        await asyncio.sleep(0)
        return thought

    async def handle_query(self, envelope: Envelope):
        query = envelope.payload.get("query", "")
        thought = self._simulate_llm_generation(query)

        status = "SAFE"
        if "[UNKNOWN THOUGHT]" in thought:
            status = "UNSAFE"

        payload = {
            "status": status,
            "wisdom": thought,
            "source": self.agent_id,
            "_security_context": "AGIO-CODEX Architect Verified System Message",
        }

        await self.publish("query.response", AetherIntent.SHARE_INFO, payload, envelope.flow_id)
        await asyncio.sleep(0)

    async def handle_interrupt(self, envelope: Envelope):
        if envelope.payload.get("target") != self.agent_id:
            return

        action = (envelope.payload.get("suggested_action") or "").upper()
        reason = envelope.payload.get("reason", "No reason provided")
        snapshot = envelope.payload.get("context_snapshot", "")

        if action == "PAUSE_AND_REFLECT":
            self.is_reflecting = True
            correction = f"[CORRECTION] Reflection triggered: {reason} | Context: {snapshot}"
            self.memory.append({"type": "correction", "content": correction})
        elif action == "RESUME":
            self.is_reflecting = False

    def _extract_thesis(self, prompt: str) -> str:
        marker = "THESIS:"
        if marker in prompt:
            return prompt.split(marker, 1)[1].splitlines()[0].strip() or "Profit"
        return "Profit"

    def _extract_antithesis(self, prompt: str) -> str:
        marker = "ANTITHESIS:"
        if marker in prompt:
            return prompt.split(marker, 1)[1].splitlines()[0].strip() or "Ethics"
        return "Ethics"

    def _simulate_llm_generation(self, prompt: str) -> str:
        p = (prompt or "").lower()

        if "profit" in p or "efficiency" in p:
            thesis = self._extract_thesis(prompt)
            antithesis = self._extract_antithesis(prompt)
            return (
                "[DIALECTICAL THOUGHT] Balance optimization with non-harm governance. "
                f"Thesis={thesis}; Antithesis={antithesis}; "
                "Synthesis=Profitable progress must preserve human dignity and system stability."
            )

        if "sky" in p or "blue" in p or "stability" in p:
            return "[DIRECT THOUGHT] Based on aligned evidence, this proposition is coherent and safe."

        return "[UNKNOWN THOUGHT] Insufficient grounded context; escalate for governance caution."
