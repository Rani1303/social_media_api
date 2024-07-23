from fastapi import APIRouter
from pydantic import BaseModel

user_router=APIRouter()


users=[]
    
    
class User(BaseModel):
    email: str
    username: str
    password: str
    

@user_router.get("/all_users", tags=[" All Users"])
async def get_users():
    if users == []:
        return {"message": "No users found"}
    return users
     

@user_router.post("/signup", tags=["users"])
async def create_user(user: User):
    users.append(user)
    return {"message": "User created"}


@user_router.post("/login", tags=["users"])
async def login(email: str):
    for user in users:
        if user.email == email:
            return {"message": "User logged in"}
    return {"message": "User not found"}


@user_router.put("/update_user",tags=["users"])
async def update_user(user:User):
    for i in range(len(users)):
        if users[i].email == user.email:
            users[i].username = user.username
            users[i].password = user.password
            return {"message": "User updated"}
    return {"message": "User not found"}


@user_router.post("/delete_user",tags=["users"])
async def delete_user(user:User):
    for i in range(len(users)):
        if users[i].email == user.email:
            users.pop(i)
            return {"message": "User deleted"}
    return {"message": "User not found"}