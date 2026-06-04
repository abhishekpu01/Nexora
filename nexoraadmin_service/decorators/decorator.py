from nexoraadmin_service.utils.utils import get_user
from fastapi import HTTPException
import functools
def check_permissions(permissions: list):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                token = kwargs.get('token')
                user = get_user(token)
                if user:
                    if user == "Invalid Token":
                        raise Exception("Invalid Token")
                    if all(p in user['permissions'] for p in permissions):
                        return await func(*args, **kwargs)
                    else:
                        raise HTTPException(status_code=403, detail="Permission denied")
                else:
                    raise Exception("Token Expired")
                
            except HTTPException as e:
                raise e
            
        return wrapper
    return decorator
