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


@dataclass(frozen=True, slots=True)
class TokenPair:
    access_token: str
    refresh_token: str
    expires_in_seconds: int


@dataclass(frozen=True, slots=True)
class AccessToken:
    access_token: str
    expires_in_seconds: int


@dataclass(frozen=True, slots=True)
class IntrospectResult:
    active: bool
    sub: str | None
    roles: frozenset[str]


class IdentityClient(Protocol):
    async def login(self, *, email: str, password: str) -> TokenPair: ...

    async def refresh(self, *, refresh_token: str) -> AccessToken: ...

    async def introspect(self, *, token: str) -> IntrospectResult: ...

    async def logout(self, *, refresh_token: str) -> None: ...

