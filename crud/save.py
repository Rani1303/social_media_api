from fastapi import APIRouter, HTTPException
from schemas.save import serializeSaveDict, serializeSaveList
from models.save import Save
from config.database import collection
from bson import ObjectId
from datetime import datetime

save_router = APIRouter()

@save_router.post("/save_post", tags=["Saves"])
async def save_post(save: Save):
    existing_save = await collection.find_one({
        "user_id": save.user_id,
        "post_id": save.post_id
    })
    if existing_save:
        raise HTTPException(status_code=400, detail="Post already saved by this user")
    
    save_dict = dict(save)
    save_dict["created_at"] = datetime.utcnow()
    new_save = await collection.insert_one(save_dict)
    created_save = await collection.find_one({"_id": new_save.inserted_id})
    return serializeSaveDict(created_save)

@save_router.delete("/unsave_post", tags=["Saves"])
async def unsave_post(user_id: str, post_id: str):
    delete_result = await collection.delete_one({
        "user_id": user_id,
        "post_id": post_id
    })
    if delete_result.deleted_count:
        return {"message": "Post unsaved successfully"}
    raise HTTPException(status_code=404, detail="Saved post not found")

@save_router.get("/saved_posts/{user_id}", tags=["Saves"])
async def get_saved_posts(user_id: str):
    saved_posts = await collection.find({"user_id": user_id}).to_list(length=None)
    if not saved_posts:
        return {"message": "No saved posts found for this user"}
    return serializeSaveList(saved_posts)