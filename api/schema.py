from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from dotenv import dotenv_values
from pydantic import BaseModel,Field,EmailStr
import os
from typing import Any, Dict 

from pydantic_core import CoreSchema

from pydantic import BaseModel, GetJsonSchemaHandler


config = dotenv_values(".env")


client=AsyncIOMotorClient(str(config.get("MONGO_URI")))
db=client.blogs

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, values, **kwargs):  # Include `values` and `**kwargs`
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema: Any, handler: GetJsonSchemaHandler) -> Dict[str, Any]:
        json_schema: Dict[str, Any] = {"type": "string"}
        return json_schema


        

 
class User(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str=Field(...)
    email: EmailStr=Field(...)
    password: str=Field(...)
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            "example": {
                "name": "John Doe",
                "email": "joedoe@gmail.com",
                "password": "password"
            }
        }

class UserResponse(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str=Field(...)
    email:EmailStr=Field(...)   
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            "example": {
                "name": "John Doe",
                "email": "joedoe@gmail.com"
            }
        }

class VerifyUser(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    
    email:EmailStr=Field(...) 
    code:int=Field(...)  
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            "example": {
                "email": "joedoe@gmail.com",
                "code": "XXXXXX"
            }
        }

class TokenData(BaseModel):
    id: str

class PasswordReset(BaseModel):
    email:EmailStr=Field(...) 

class NewPassword(BaseModel):
    password:str 

class BlogContent(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    title: str=Field(...)
    body: str=Field(...)
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            "example": {
                "title": "Title",
                "body": "First blog"
            }
        }

class BlogContentResponse(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    title: str=Field(...)
    body: str=Field(...)
    author_name:str=Field(...)
    author_id:PyObjectId=Field(...)
    created_at:str=Field(...)
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            "example": {
                "title": "Title",
                "body": "First blog",
                "author_name":"John Doe",
                "author_id":"XXXXXX",
                "created_at":"20XX-XX-XX"


            }
        }

class UserDetail(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str=Field(...)
    email:EmailStr=Field(...)
    blogs_posted:int=Field(...)
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        json_schema_extra = {
            "example": {
                "name": "John Doe",
                "email": "johndoe@gmail.com",
                "blogs_posted": 2
            }
        }
        