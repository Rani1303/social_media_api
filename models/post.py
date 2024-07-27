from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Post(BaseModel):
    title: str
    description: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None