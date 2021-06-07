import uuid
from typing import Optional
from datetime import date
from pydantic import BaseModel, Field, EmailStr

class Login(BaseModel):
    username: str = Field(...)
    password: str = Field(...)

class User(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    name: str = Field(...)
    email: EmailStr
    login: Login
    birthday: Optional[date] = None
    disabled: bool = False

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "name": "Brad Gibson",
                "email": "brad.gibson@example.com",
                "login" : {
                    "username": "silverswan131",
                    "password": "rockymountains"
                },
                "birthday": "1993-04-21",
                "disabled": False
            }
        }

class UpdateUser(BaseModel):
    name: Optional[str] = Field(...)
    email: Optional[EmailStr]
    login: Optional[Login]
    disabled: Optional[bool]

    class Config:
        schema_extra = {
            "example": {
                "name": "Brad Gibson",
                "email": "brad.gibson@example.com",
                "login" : {
                    "username": "silverswan131",
                    "password": "rockymountains"
                },
                "disabled": False        
            }
        }

