from fastapi import APIRouter, HTTPException
from schemas.post import serializeDict, serializeList
from models.post import Post
from config.database import collection
from bson import ObjectId
from datetime import datetime

post_router = APIRouter()



@post_router.get("/all_posts", tags=["Posts"])
async def get_posts():
    posts = await collection.find().to_list(length=None)
    if not posts:
        return {"message": "No posts found"}
    return serializeList(posts)


@post_router.post("/create_post", tags=["Posts"])
async def create_post(post: Post):
    post_dict= dict(post)
    post_dict["created_at"] = datetime.utcnow()
    post_dict["updated_at"] = post_dict["created_at"]
    new_post = await collection.insert_one(dict(post_dict))
    created_post = await collection.find_one({"_id": new_post.inserted_id})
    return serializeDict(created_post)

@post_router.put("/update_post", tags=["Posts"])
async def update_post(id: str, post: Post):
    update_dict = dict(post)
    update_dict["updated_at"] = datetime.utcnow()
    update_result = await collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": update_dict}
    )
    if update_result.modified_count:
        updated_post = await collection.find_one({"_id": ObjectId(id)})
        return serializeDict(updated_post)
    raise HTTPException(status_code=404, detail="Post not found")


@post_router.delete("/delete_post", tags= ["Posts"])
async def delete_post(id: str):
    delete_result = await collection.delete_one({"_id": ObjectId(id)})
    if delete_result.deleted_count:
        return {"message": "Post deleted"}
    raise HTTPException(status_code=404, detail="Post not found")