from pydantic import BaseModel

class GetQuizes(BaseModel):
    grade: str