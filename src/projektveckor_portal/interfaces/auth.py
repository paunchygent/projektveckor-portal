from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True, slots=True)
class CurrentUser:
    user_id: str
    roles: frozenset[str]
    org_id: str | None = None

    @property
    def is_teacher(self) -> bool:
        return "teacher" in self.roles or "admin" in self.roles


class Authenticator(Protocol):
    async def authenticate_bearer_token(self, token: str) -> CurrentUser | None: ...

