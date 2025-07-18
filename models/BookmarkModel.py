from pydantic import BaseModel

class BookMarkModel(BaseModel):
    userId: str
    quizId: str
    level:str