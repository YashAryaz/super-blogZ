from fastapi import APIRouter,Depends,HTTPException,status
from ..oath2 import get_current_user
from ..schema import db,UserDetail

router = APIRouter(
    prefix="/user",
    tags=["User Detail"]
)

@router.get("/user_detail",response_description="Get user detail",status_code=status.HTTP_200_OK,response_model=UserDetail)
async def get_user_detail(current_user=Depends(get_current_user)):
    try:
        user=await db["users"].find_one({"_id":current_user["_id"]},{"_id": 1, "name": 1, "email": 1})
        
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
        else:
            blog_count=await db["blogPost"].count_documents({"author_id":current_user["_id"]})
            if blog_count is None:
                blog_count=0
            
            user_detail = {
            "id": str(user["_id"]),
            "name": user["name"],
            "email": user["email"],
            "blogs_posted": blog_count
            }
            
            return user_detail
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=f"Internal Server Error: {e}")
    

            
