from jose import JWTError, jwt
from datetime import datetime,date,timedelta
from typing import Dict
from .schema import TokenData,db
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends,HTTPException,status
from dotenv import load_dotenv
import os
ACCESS_TOKEN_EXPIRE_MINUTES=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(payload: Dict):
    to_encode = payload.copy()
    expiration_time=datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expiration_time})

    jwt_token=jwt.encode(to_encode,key=SECRET_KEY,algorithm=ALGORITHM)
    return jwt_token

def verify_access_token(token:str,credentials_exception):
    try:
        payload=jwt.decode(token,key=SECRET_KEY,algorithms=[ALGORITHM])
        id: str = payload.get("id")
        if not id:
            raise credentials_exception
        token_data=TokenData(id=id)
        return token_data
    
    except JWTError:
        raise credentials_exception

async def get_current_user(token:str=Depends(oauth2_scheme)):
    credentials_exception=HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate":"Bearer"}
        )
    current_user_id=verify_access_token(token,credentials_exception)
    current_user=await db["users"].find_one({"_id":current_user_id.id})
    
    return current_user