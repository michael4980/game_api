from os import getenv
from typing import Optional

from fastapi import Depends, HTTPException
from fastapi.security.http import HTTPAuthorizationCredentials, HTTPBearer
from starlette import status


async def check_static_token(
    auth: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False)),
) -> str:
    client_token = getenv("CLIENT_TOKEN")
    if auth is None or (token := auth.credentials) != client_token:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bearer token missing or unknown")
    return token
