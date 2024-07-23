# Basic fastapi app
from fastapi import FastAPI
from crud.user import user_router
app = FastAPI()
# User router in app
app.include_router(user_router)
