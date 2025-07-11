from typing import List
from pydantic import BaseModel

class Answer(BaseModel):
    i: str
    a: str

class SubmitAnswerModel(BaseModel):
    level: str
    answer: List[Answer]
    userId: str

class SubmitAnswerResponse(BaseModel):
    score: int
    percentage: int
    correct_answers: int
    wrong_answers: int