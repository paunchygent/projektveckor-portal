from __future__ import annotations

from dataclasses import dataclass

from fastapi import Depends, HTTPException, Request, status

from projektveckor_portal.interfaces.auth import Authenticator, CurrentUser


@dataclass(frozen=True, slots=True)
class AppDependencies:
    authenticator: Authenticator | None


def deps_from_request(request: Request) -> AppDependencies:
    deps = getattr(request.app.state, "deps", None)
    if not isinstance(deps, AppDependencies):
        raise RuntimeError("App dependencies are not configured")
    return deps


async def get_current_user_optional(request: Request) -> CurrentUser | None:
    deps = deps_from_request(request)
    if deps.authenticator is None:
        return None

    auth = request.headers.get("Authorization", "")
    parts = auth.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        return None

    try:
        return await deps.authenticator.authenticate_bearer_token(parts[1])
    except Exception:
        return None


async def require_teacher(
    user: CurrentUser | None = Depends(get_current_user_optional),
) -> CurrentUser:
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Du behöver logga in.")
    if not user.is_teacher:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Åtkomst nekad.")
    return user
