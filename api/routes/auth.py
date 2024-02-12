from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from ..schema import db
from ..import utils
from ..oath2 import create_access_token
from jose import JWTError, jwt
from passlib.context import CryptContext

router = APIRouter(
    prefix="/login",
    tags=["Authentication"]
)



@router.post("/",status_code=status.HTTP_200_OK)
async def login(user_credentials: OAuth2PasswordRequestForm = Depends()):
    

    user=await db["users"].find_one({"name":user_credentials.username})
    
    if user and utils.verify_password(user_credentials.password,user["password"]):
        access_token=create_access_token({"id":user["_id"]})
        return ({'access_token':access_token,'token_type':'bearer'})
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Incorrect username or password")