from pydantic import BaseModel

class ProgressModel(BaseModel):
    userId: str
    grade: str
