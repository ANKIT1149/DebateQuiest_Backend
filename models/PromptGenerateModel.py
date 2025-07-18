from pydantic import BaseModel

class PromptGenerateModel(BaseModel):
    title: str
    level: str
    grade: str