from fastapi import APIRouter, Depends, HTTPException, status
from ..schema import PasswordReset,db,NewPassword
from ..sender_email import password_reset_async
from ..oath2 import create_access_token,get_current_user
from ..utils import get_password_hash
router = APIRouter(
    prefix="/password_reset",
    tags=["Password Reset"]
)

@router.post("",response_description="Reset Request",status_code=status.HTTP_200_OK)
async def reset_request(user_email:PasswordReset):
    user=await db["users"].find_one({"email":user_email.email})
    if user is not None:
        token=create_access_token({"id":user["_id"]})

        reset_link=f"http://localhost:8000/password_reset/token={token}"
        await password_reset_async("Password Reset",user["email"],{
            "title":"Password Reset",
            "name":user["name"],
            "reset_link":reset_link
        })
    
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    
@router.put("",response_description="Reset Password",status_code=status.HTTP_200_OK)
async def reset(token:str,new_password:NewPassword):
    request_data={k:v for k,v in new_password.model_dump().items() if v is not None}
    request_data["password"]=get_password_hash(request_data["password"])

    if(len(request_data["password"])>=1):
        user=await get_current_user(token)
        update_result=await db["users"].update_one({"_id":user["_id"]},{"$set":request_data})
        if update_result.modified_count==1:
            updated_user=await db["users"].find_one({"_id":user["_id"]})
            if (updated_user) is not None:
                return updated_user
    existing_user=await db["users"].find_one({"_id":user["_id"]})
    if (existing_user) is not None:
        return existing_user
    
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Password Reset Failed")



