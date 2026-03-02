from __future__ import annotations

from typing import Awaitable, Callable

from .events import Event

RouteHandler = Callable[[Event], Awaitable[None]]


class MessageRouter:
    """Minimal message router that decouples transport from handlers."""

    def __init__(self) -> None:
        self._routes: dict[str, RouteHandler] = {}

    def register(self, route_key: str, handler: RouteHandler) -> None:
        self._routes[route_key] = handler

    async def route(self, route_key: str, event: Event) -> None:
        if route_key not in self._routes:
            raise KeyError(f"No route registered for '{route_key}'")
        await self._routes[route_key](event)
