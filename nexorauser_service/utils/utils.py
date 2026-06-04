from nexorauser_service.config import settings
from fastapi import status
from fastapi.responses import JSONResponse
from datetime import datetime, timezone, timedelta
import jwt

def createSuccessResponse(data):
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content = {
            "data": data,
            "response_code": "SUCCESS"
        }
    )

def createFailedResponse(message):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "detail": message,
            "response_code": "FAILED"
        }
    )

def create_access_token(data: dict):
    to_encode = data.copy()
    to_encode["exp"] = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)