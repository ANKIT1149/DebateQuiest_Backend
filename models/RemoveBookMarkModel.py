from pydantic import BaseModel


class RemoveBookMarkModel(BaseModel):
    userId: str
    quizId: str