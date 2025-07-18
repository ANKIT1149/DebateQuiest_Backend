from pydantic import BaseModel

class CustomeDebateModel(BaseModel):
    topic:str
    duration_minutes: int
    userId: str
    level: str