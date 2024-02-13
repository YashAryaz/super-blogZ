from fastapi import APIRouter, Depends, HTTPException, status
from ..schema import BlogContent,BlogContentResponse,db
from fastapi.encoders import jsonable_encoder

from ..oath2 import get_current_user
from typing import List
from datetime import datetime

router = APIRouter(
    prefix="/blog",
    tags=["Blog Content"]
)

@router.post("/create",response_description="Create a new blog",status_code=status.HTTP_201_CREATED,response_model=BlogContentResponse)
async def create_blog(blog: BlogContent,current_user=Depends(get_current_user)):
    try:
        blog = jsonable_encoder(blog)
        blog["author_name"]=current_user["name"]
        blog["author_id"]=current_user["_id"]
        blog["created_at"]=str(datetime.now())

        new_blog = await db["blogPost"].insert_one(blog)
        created_blog = await db["blogPost"].find_one({"_id": new_blog.inserted_id})
        return created_blog
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=f"Internal Server Error: {e}")

@router.get("/get_all",response_description="Get all blogs",status_code=status.HTTP_200_OK,response_model=List[BlogContentResponse])
async def get_blogs(limit:int=10, orderby:str="created_at",current_user=Depends(get_current_user)):
    try:
        blogs = await db["blogPost"].find({"$query":{},"$orderby":{orderby:-1}}).to_list(limit)
        return blogs
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=f"Internal Server Error: {e}")

@router.get("/{id}",response_description="Get a single blog",status_code=status.HTTP_200_OK,response_model=BlogContentResponse)
async def get_blog(id:str,current_user=Depends(get_current_user)):
    try:
        blog = await db["blogPost"].find_one({"_id": id})
        if blog:
            return blog
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Blog with id {id} not found")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=f"Internal Server Error: {e}")

@router.put("/update/{id}",response_description="Update a blog",status_code=status.HTTP_200_OK,response_model=BlogContentResponse)
async def update_blog(id:str,blog_content:BlogContent,current_user=Depends(get_current_user)):
    if blog_post:=await db["blogPost"].find_one({"_id": id}):
        if blog_post['author_id']==current_user['_id']:
            try:
                blog_content={k:v for k,v in blog_content.dict().items() if v is not None}
                if len(blog_content)>=1:
                    updated_blog=await db["blogPost"].update_one({"_id": id},{"$set":blog_content})
                    if updated_blog.modified_count==1:
                        if (updated_blog:=await db["blogPost"].find_one({"_id": id})) is not None:
                            return updated_blog
                    if (existing_blog:=await db["blogPost"].find_one({"_id": id })) is not None:
                            return existing_blog
                    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Blog not found")
            except Exception as e:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=f"Internal Server Error: {e}")
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Unauthorized to update blog")
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Blog not found")


@router.delete("/delete/{id}",response_description="Delete a blog",status_code=status.HTTP_204_NO_CONTENT)
async def delete_blog(id:str,current_user=Depends(get_current_user)):
    if blog_post:=await db["blogPost"].find_one({"_id": id}):
        if blog_post['author_id']==current_user['_id']:
            try:
                deleted_blog=await db["blogPost"].delete_one({"_id": id})
                if deleted_blog.deleted_count==1:
                    return {"status":f"Blog with id {id} deleted successfully"}
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Blog not found")
            except Exception as e:
                raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail=f"Internal Server Error: {e}")
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Unauthorized to delete blog")
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Blog not found")
                    
            
    
