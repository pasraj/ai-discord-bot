from fastapi.security.api_key import APIKeyHeader
from fastapi import Depends, HTTPException, Security
from starlette.status import HTTP_403_FORBIDDEN
from config import get_settings

settings = get_settings()


api_key_header = APIKeyHeader(name="X-API-KEY", auto_error=False)

async def get_api_key(api_key_header: str = Security(api_key_header)):

    if api_key_header == settings.secret_key:
        return api_key_header
    
    raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials")