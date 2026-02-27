from __future__ import annotations

from dataclasses import dataclass

import httpx

from projektveckor_portal.interfaces.auth import AccessToken, IntrospectResult, TokenPair


class IdentityInvalidCredentialsError(RuntimeError):
    pass


@dataclass(frozen=True, slots=True)
class IdentityConfig:
    base_url: str


class IdentityHttpClient:
    def __init__(self, *, config: IdentityConfig) -> None:
        self._config = config

    async def login(self, *, email: str, password: str) -> TokenPair:
        url = f"{self._config.base_url.rstrip('/')}/v1/auth/login"
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.post(url, json={"email": email, "password": password})
            if response.status_code == 401:
                raise IdentityInvalidCredentialsError("Ogiltiga inloggningsuppgifter.")
            response.raise_for_status()
            payload = response.json()

        access_token = str(payload.get("access_token", "")).strip()
        refresh_token = str(payload.get("refresh_token", "")).strip()
        expires_in = int(payload.get("expires_in", 0) or 0)
        if not access_token or not refresh_token or expires_in <= 0:
            raise RuntimeError("Ogiltigt svar från Identity Service (login).")
        return TokenPair(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in_seconds=expires_in,
        )

    async def refresh(self, *, refresh_token: str) -> AccessToken:
        url = f"{self._config.base_url.rstrip('/')}/v1/auth/refresh"
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.post(url, json={"refresh_token": refresh_token})
            if response.status_code == 401:
                raise IdentityInvalidCredentialsError("Ogiltig refresh token.")
            response.raise_for_status()
            payload = response.json()

        access_token = str(payload.get("access_token", "")).strip()
        expires_in = int(payload.get("expires_in", 0) or 0)
        if not access_token or expires_in <= 0:
            raise RuntimeError("Ogiltigt svar från Identity Service (refresh).")
        return AccessToken(access_token=access_token, expires_in_seconds=expires_in)

    async def introspect(self, *, token: str) -> IntrospectResult:
        url = f"{self._config.base_url.rstrip('/')}/v1/auth/introspect"
        async with httpx.AsyncClient(timeout=8.0) as client:
            response = await client.post(url, json={"token": token})
            if response.status_code == 401:
                raise IdentityInvalidCredentialsError("Ogiltig access token.")
            response.raise_for_status()
            payload = response.json()

        active = bool(payload.get("active", False))
        sub_raw = payload.get("sub")
        sub = str(sub_raw).strip() if isinstance(sub_raw, str) and sub_raw.strip() else None
        roles_raw = payload.get("roles") if isinstance(payload, dict) else []
        roles: frozenset[str] = frozenset(
            str(r).strip()
            for r in (roles_raw or [])
            if isinstance(r, (str, int)) and str(r).strip()
        )
        return IntrospectResult(active=active, sub=sub, roles=roles)

    async def logout(self, *, refresh_token: str) -> None:
        url = f"{self._config.base_url.rstrip('/')}/v1/auth/logout"
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(url, json={"refresh_token": refresh_token})
            if response.status_code == 401:
                raise IdentityInvalidCredentialsError("Ogiltig refresh token.")
            response.raise_for_status()
