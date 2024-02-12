from fastapi import APIRouter, Depends, HTTPException,Response, Cookie,Request
from ..schema import User, db, UserResponse ,VerifyUser
import secrets
from ..utils import get_password_hash
from fastapi.encoders import jsonable_encoder
from dotenv import load_dotenv
from ..sender_email import send_email_async
import os
from fastapi import Query
from typing import Optional
import random
# import redis
import json
load_dotenv()
router = APIRouter(

    tags=["users"],
)
@router.post("/registeration", response_description="Register a user")
async def register_user(user_info: User, response: Response):
    user_info = jsonable_encoder(user_info)
    user_name=await db.users.find_one({"name":user_info["name"]})
    user_email=await db.users.find_one({"email":user_info["email"]})
    if user_name:
        raise HTTPException(status_code=409, detail="Username already exists")
    if user_email:
        raise HTTPException(status_code=409, detail="Email already exists")
    
    user_info['password']=get_password_hash(user_info['password']) 
    user_info['api_key']=secrets.token_hex(30)
    verification_code = str(random.randint(100000, 999999))
    response.set_cookie(key=verification_code, value=json.dumps(user_info))  # Set a cookie
    try:
        await send_email_async("Welcome to our blog",user_info['email'],{
        "title":"Here is your verification code",
        "code":verification_code,
        "name":user_info['name']
        })
    except Exception as e:
        print(e)
        raise HTTPException(status_code=400, detail="Email not sent")

    return {"detail": "Verification email sent"}

@router.get("/verify", response_description="Verify a user", response_model=UserResponse)
async def verify_user(request: Request,code: int = Query(...)):
    user_info = request.cookies.get(str(code))
    if not user_info:
        raise HTTPException(status_code=404, detail="Invalid code")
    user_info = json.loads(user_info)
    new_user = await db.users.insert_one(user_info)  # Insert user data into database
    created_user = await db.users.find_one({"_id": new_user.inserted_id})
    return created_user

    