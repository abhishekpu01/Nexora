from fastapi import status
from fastapi.responses import JSONResponse
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