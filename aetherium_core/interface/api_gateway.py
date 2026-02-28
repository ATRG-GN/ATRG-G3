from __future__ import annotations

from dataclasses import dataclass

from aetherium_core.application.orchestrator import GenesisOrchestrator


@dataclass
class APIGateway:
    """Interface layer facade for REST/WebSocket/gRPC endpoints."""

    orchestrator: GenesisOrchestrator

    async def rest_infer(self, prompt: str) -> dict[str, str]:
        return {"answer": await self.orchestrator.handle_prompt(prompt)}

    async def websocket_infer(self, prompt: str) -> str:
        return await self.orchestrator.handle_prompt(prompt)

    async def grpc_infer(self, prompt: str) -> str:
        return await self.orchestrator.handle_prompt(prompt)
