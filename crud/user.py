from fastapi import APIRouter, HTTPException
from schemas.user import serializeList, serializeDict
from models.user import User
from config.database import collection
from bson import ObjectId

user_router = APIRouter()

@user_router.get("/all_users", tags=["All Users"])
async def get_users():
    users = await collection.find().to_list(length=None)
    if not users:
        return {"message": "No users found"}
    return serializeList(users)

@user_router.post("/signup", tags=["users"])
async def create_user(user: User):
    existing_user = await collection.find_one({"email": user.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = await collection.insert_one(dict(user))
    created_user = await collection.find_one({"_id": new_user.inserted_id})
    return serializeDict(created_user)

@user_router.post("/login", tags=["users"])
async def login(email: str):
    user = await collection.find_one({"email": email})
    if user:
        return serializeDict(user)
    raise HTTPException(status_code=400, detail="User not found")

@user_router.put("/update_user", tags=["users"])
async def update_user(id: str, user: User):
    update_result = await collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": dict(user)}
    )
    if update_result.modified_count:
        updated_user = await collection.find_one({"_id": ObjectId(id)})
        return serializeDict(updated_user)
    raise HTTPException(status_code=404, detail="User not found")

@user_router.delete("/delete_user", tags=["users"])
async def delete_user(id: str):
    delete_result = await collection.delete_one({"_id": ObjectId(id)})
    if delete_result.deleted_count:
        return {"message": "User deleted"}
    raise HTTPException(status_code=404, detail="User not found")