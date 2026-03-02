from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class AccessToken:
    subject: str
    role: str


def enforce_rbac(token: AccessToken, allowed_roles: set[str]) -> bool:
    return token.role in allowed_roles
