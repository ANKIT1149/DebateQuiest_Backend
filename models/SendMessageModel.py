from pydantic import BaseModel

class SendMessageModel(BaseModel):
    session_id: str
    user_message: str