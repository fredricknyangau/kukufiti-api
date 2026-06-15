"""Shared FastAPI dependency functions used across all module routers.

This module provides application-level dependencies (authentication,
current user context) that are not specific to any single module. Module-
specific dependencies (database connections, service construction) live in
each module's own dependencies.py file.
"""
import logging
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

logger = logging.getLogger(__name__)

# HTTPBearer extracts the token from the `Authorization: Bearer <token>` header.
# auto_error=True (default) means FastAPI automatically returns 403 if the
# header is missing, so get_current_user is only called with a valid header present.
_bearer = HTTPBearer(auto_error=True)


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(_bearer)],
) -> dict:
    """Validate the Bearer JWT and return the decoded token payload.

    Used as a router-level dependency on protected routers:

        router = APIRouter(dependencies=[Depends(get_current_user)])

    All routes on that router require a valid JWT. The callback endpoint
    (/mpesa/callback) overrides this by NOT being on the protected router —
    Daraja does not send an Authorization header.

    TOKEN VALIDATION
    ----------------
    Decodes and verifies the JWT using the application's SECRET_KEY and the
    HS256 algorithm. Raises HTTP 401 if:
      - The token is malformed or cannot be decoded.
      - The signature is invalid (wrong secret).
      - The token has expired (exp claim is in the past).

    Returns the decoded payload dict, which typically contains:
      - sub:  the user's UUID (subject)
      - exp:  expiry timestamp
      - type: "access" (to distinguish access from refresh tokens)

    FUTURE
    ------
    When the auth module is fully implemented, this function will also
    look up the user record from the database to verify the user is still
    active and not suspended. For now, a valid token is sufficient.
    """
    # python-jose (python-jose[cryptography]) is used — it's in requirements.txt.
    # Imported lazily here to avoid importing jose at module load time, which
    # keeps the dependency injection light during testing.
    from jose import ExpiredSignatureError, JWTError, jwt
    from app.core.config import settings

    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=["HS256"],
        )
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Reject refresh tokens being used as access tokens.
    # Without this check a long-lived refresh token could be used to call
    # protected endpoints indefinitely, bypassing the short access-token window.
    if payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type — use an access token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    logger.debug("Authenticated request", extra={"user_id": payload.get("sub")})
    return payload
