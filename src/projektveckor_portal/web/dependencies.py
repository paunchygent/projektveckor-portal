from __future__ import annotations

from dishka.integrations.fastapi import FromDishka, inject
from fastapi import Depends, Header, HTTPException, Request, status

from projektveckor_portal.interfaces.auth import Authenticator, CurrentUser
from projektveckor_portal.settings import settings


@inject
async def get_current_user_optional(
    request: Request,
    authenticator: FromDishka[Authenticator | None],
) -> CurrentUser | None:
    if authenticator is None:
        return None

    token: str | None = None

    auth = request.headers.get("Authorization", "")
    parts = auth.split()
    if len(parts) == 2 and parts[0].lower() == "bearer":
        token = parts[1]
    else:
        token = request.cookies.get(settings.auth_access_cookie_name)

    if not token:
        return None

    try:
        return await authenticator.authenticate_bearer_token(token)
    except Exception:
        return None


async def require_csrf(
    request: Request,
    csrf_header: str | None = Header(default=None, alias="X-CSRF-Token"),
) -> None:
    method = request.method.upper()
    if method in {"GET", "HEAD", "OPTIONS"}:
        return None

    expected = request.cookies.get(settings.csrf_cookie_name)
    if not expected or not csrf_header or csrf_header != expected:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="CSRF-validering misslyckades.",
        )


async def require_teacher(
    user: CurrentUser | None = Depends(get_current_user_optional),
) -> CurrentUser:
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Du behöver logga in.")
    if not user.is_teacher:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Åtkomst nekad.")
    return user


async def require_admin(
    user: CurrentUser | None = Depends(get_current_user_optional),
) -> CurrentUser:
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Du behöver logga in.")
    if "admin" not in user.roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Åtkomst nekad.")
    return user
