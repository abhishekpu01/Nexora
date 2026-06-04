import cv2
import os
import numpy as np
from fastapi import status
from fastapi.responses import JSONResponse
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
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

def get_base_color(rgb):
    rgb_np = np.uint8([[rgb]])
    hsv = cv2.cvtColor(rgb_np, cv2.COLOR_RGB2HSV)[0][0]

    h, s, v = hsv

    if v < 50:
        return "black"

    if s < 30 and v > 200:
        return "white"

    if s < 30:
        return "grey"

    # Hue-based mapping
    if (h < 15 or h > 165) and v > 150 and s < 180:
        return "pink"
    if h < 10 or h >= 170:
        return "red"
    elif h < 25:
        return "orange"
    elif h < 35:
        return "yellow"
    elif h < 85:
        return "green"
    elif h < 145:
        return "blue"
    else:
        return "pink"
    
def get_user(token):
    try:
        return jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=[os.getenv("ALGORITHM")])
    except ExpiredSignatureError:
        print("Token has expired")
        return None
    except InvalidTokenError:
        return "Invalid Token"
