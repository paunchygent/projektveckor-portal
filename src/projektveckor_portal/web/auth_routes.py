from __future__ import annotations

import secrets
from dataclasses import dataclass

from dishka.integrations.fastapi import DishkaRoute, FromDishka
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from pydantic import BaseModel, ConfigDict, Field

from projektveckor_portal.infrastructure.auth.identity_http_client import (
    IdentityInvalidCredentialsError,
)
from projektveckor_portal.interfaces.auth import IdentityClient
from projektveckor_portal.settings import settings
from projektveckor_portal.web.dependencies import require_csrf

router = APIRouter(prefix="/api/v1/auth", tags=["auth"], route_class=DishkaRoute)


@dataclass(frozen=True, slots=True)
class AuthCookies:
    access_cookie: str
    refresh_cookie: str
    csrf_cookie: str


def _cookies() -> AuthCookies:
    return AuthCookies(
        access_cookie=settings.auth_access_cookie_name,
        refresh_cookie=settings.auth_refresh_cookie_name,
        csrf_cookie=settings.csrf_cookie_name,
    )


def _set_cookie(
    response: Response,
    *,
    key: str,
    value: str,
    max_age: int,
    http_only: bool,
) -> None:
    response.set_cookie(
        key=key,
        value=value,
        max_age=max_age,
        httponly=http_only,
        secure=settings.cookie_secure,
        samesite=settings.cookie_samesite,
        path="/",
    )


def _delete_cookie(response: Response, *, key: str) -> None:
    response.delete_cookie(key=key, path="/")


class LoginRequest(BaseModel):
    model_config = ConfigDict(frozen=True)

    email: str = Field(min_length=1)
    password: str = Field(min_length=1)


class LoginResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    ok: bool = True


class MeResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    authenticated: bool
    user_id: str | None = None
    roles: list[str] = []


class CsrfResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    csrf_token: str


@router.post("/login", response_model=LoginResponse)
async def login(
    payload: LoginRequest,
    response: Response,
    identity: FromDishka[IdentityClient | None],
) -> LoginResponse:
    if identity is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Inloggning är inte konfigurerad i den här miljön.",
        )
    try:
        tokens = await identity.login(email=payload.email, password=payload.password)
    except IdentityInvalidCredentialsError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Fel e-post eller lösenord.",
        ) from None
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Inloggning är tillfälligt otillgänglig.",
        ) from None

    c = _cookies()

    _set_cookie(
        response,
        key=c.access_cookie,
        value=tokens.access_token,
        max_age=tokens.expires_in_seconds,
        http_only=True,
    )

    # Identity Service mintar refresh tokens med ~24h TTL (för närvarande).
    _set_cookie(
        response,
        key=c.refresh_cookie,
        value=tokens.refresh_token,
        max_age=60 * 60 * 24,
        http_only=True,
    )

    csrf_token = secrets.token_urlsafe(32)
    _set_cookie(
        response,
        key=c.csrf_cookie,
        value=csrf_token,
        max_age=60 * 60 * 24,
        http_only=False,
    )

    return LoginResponse()


@router.post(
    "/logout",
    dependencies=[Depends(require_csrf)],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def logout(
    request: Request,
    response: Response,
    identity: FromDishka[IdentityClient | None],
) -> None:
    c = _cookies()
    refresh_token = request.cookies.get(c.refresh_cookie, "")

    if refresh_token and identity is not None:
        try:
            await identity.logout(refresh_token=refresh_token)
        except Exception:
            # Vi rensar alltid cookies lokalt även om Identity inte svarar.
            pass

    _delete_cookie(response, key=c.access_cookie)
    _delete_cookie(response, key=c.refresh_cookie)
    _delete_cookie(response, key=c.csrf_cookie)
    return None


@router.get("/csrf", response_model=CsrfResponse)
async def csrf(request: Request, response: Response) -> CsrfResponse:
    c = _cookies()
    token = request.cookies.get(c.csrf_cookie)
    if not token:
        token = secrets.token_urlsafe(32)
        _set_cookie(
            response,
            key=c.csrf_cookie,
            value=token,
            max_age=60 * 60 * 24,
            http_only=False,
        )
    return CsrfResponse(csrf_token=token)


@router.get("/me", response_model=MeResponse)
async def me(
    request: Request,
    response: Response,
    identity: FromDishka[IdentityClient | None],
) -> MeResponse:
    c = _cookies()
    access_token = request.cookies.get(c.access_cookie)
    refresh_token = request.cookies.get(c.refresh_cookie)

    if not access_token:
        return MeResponse(authenticated=False, user_id=None, roles=[])

    if identity is None:
        return MeResponse(authenticated=False, user_id=None, roles=[])

    try:
        result = await identity.introspect(token=access_token)
    except Exception:
        result = None

    if result is None or not result.active or not result.sub:
        if refresh_token:
            try:
                refreshed = await identity.refresh(refresh_token=refresh_token)
                _set_cookie(
                    response,
                    key=c.access_cookie,
                    value=refreshed.access_token,
                    max_age=refreshed.expires_in_seconds,
                    http_only=True,
                )
                result = await identity.introspect(token=refreshed.access_token)
            except Exception:
                result = None

    if result is None or not result.active or not result.sub:
        return MeResponse(authenticated=False, user_id=None, roles=[])

    return MeResponse(
        authenticated=True,
        user_id=result.sub,
        roles=sorted(result.roles),
    )
