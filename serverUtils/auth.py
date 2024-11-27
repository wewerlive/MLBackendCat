from fastapi import Security, HTTPException, status, Request
from fastapi.security import APIKeyHeader
from .db import getBusinessFromAPIKey
from fastapi import FastAPI, Depends

api_key_header = APIKeyHeader(name="X-API-Key")

# def get_user(api_key_header: str = Security(api_key_header)):
#     if check_api_key(api_key_header):
#         user = get_user_from_api_key(api_key_header)
#         return user
#     raise HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Missing or invalid API key"
#     )

async def getBusinessUser(request:Request,api_key_header: str = Security(api_key_header)):
    business = await getBusinessFromAPIKey(api_key_header,request.app)
    if business is not None:
        return business
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Missing or invalid API key"
    )