from __future__ import annotations

from dataclasses import dataclass

import httpx

from projektveckor_portal.interfaces.auth import Authenticator, CurrentUser


@dataclass(frozen=True, slots=True)
class IdentityIntrospectionConfig:
    introspect_url: str


class IdentityIntrospectionAuthenticator(Authenticator):
    def __init__(self, *, config: IdentityIntrospectionConfig) -> None:
        self._config = config

    async def authenticate_bearer_token(self, token: str) -> CurrentUser | None:
        if token.strip() == "":
            return None

        async with httpx.AsyncClient(timeout=8.0) as client:
            response = await client.post(self._config.introspect_url, json={"token": token})
            response.raise_for_status()
            payload = response.json()

        if not isinstance(payload, dict):
            return None

        active = payload.get("active")
        if active is not True:
            return None

        sub = payload.get("sub")
        if not isinstance(sub, str) or sub.strip() == "":
            return None

        roles = payload.get("roles", [])
        if not isinstance(roles, list):
            roles = []

        cleaned_roles = frozenset(str(r).strip() for r in roles if str(r).strip())
        org_id = payload.get("org_id") if isinstance(payload.get("org_id"), str) else None
        return CurrentUser(user_id=sub, roles=cleaned_roles, org_id=org_id)
