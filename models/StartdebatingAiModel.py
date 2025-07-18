from pydantic import BaseModel

class StartDebatingModel(BaseModel):
    user_id: str
    topic: str
    duration: int