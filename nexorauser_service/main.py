from fastapi import FastAPI, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from dotenv import load_dotenv
from nexorauser_service.db.db import get_db
from nexorauser_service.enum.enum import Role, Permission
from models.models import User
import bcrypt
from nexorauser_service.utils.utils import createSuccessResponse, createFailedResponse, create_access_token
load_dotenv()

from pydantic import BaseModel, EmailStr
from typing import Optional

class UserRegister(BaseModel):
    first_name: str
    middle_name: Optional[str] = None
    last_name: str
    email: EmailStr
    password: str
    role: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

app = FastAPI()

@app.post("/register")
def register(data: UserRegister, db: Session = Depends(get_db)):
    try:
        if data.role not in [role.value for role in Role]:
            return createFailedResponse("No such role is defined in our system")
        permissions = []
        if data.role == 'admin' or data.role == "inventory_manager":
            permissions = [val for val in Permission]
        db_user = User(
            first_name=data.first_name,
            middle_name=data.middle_name,
            last_name=data.last_name,
            email=data.email,
            password=bcrypt.hashpw(data.password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8"), 
            role=data.role,
            permissions=permissions
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return createSuccessResponse(jsonable_encoder(db_user))
    except Exception as e:
        return createFailedResponse(str(e))
    

@app.post("/login")
def login(data: UserLogin, db: Session = Depends(get_db)):
    try:   
        db_user = db.query(User).filter(User.email == data.email).first()
        if not db_user:
            return createFailedResponse("Invalid credentials")

        if not bcrypt.checkpw(data.password.encode("utf-8"), db_user.password.encode("utf-8")):
            return createFailedResponse("Invalid credentials")

        token = create_access_token({
            "user_id": str(db_user.user_id),
            "role": db_user.role,
            "permissions": db_user.permissions
        })

        return createSuccessResponse({"access_token": token, "token_type": "bearer"})
    
    except Exception as e:
        return createFailedResponse(str(e))
    

