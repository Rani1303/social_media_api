from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class Save(BaseModel):
    user_id: str
    post_id: str
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)