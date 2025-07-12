from pydantic import BaseModel
from typing import Optional

class RegisterModel(BaseModel):
    clerk_id: str
    username: str
    email: str
    grade: str
    password: Optional[str] = None
    imageUrl: Optional[str] = None
