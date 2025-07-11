from fastapi import FastAPI, HTTPException
from db.postgressConnection import get_connection
from routes.Register_User import register_userdata
from models.RegisterModel import RegisterModel
from fastapi.middleware.cors import CORSMiddleware
from services.get_quizzes import get_quizzes
from services.get_quiz_on_level import get_quiz_on_level
from models.SubmitAnswer import SubmitAnswerModel
from services.verify_quiz_answer import submit_quiz_and_verify_results
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

get_connection();

@app.get("/")
async def root():
    return {"message": "Welcome to DebateQuest Backend"}


@app.post("/register")
async def register_user(User: RegisterModel):
     result = await register_userdata(User)
     if result["status"] == 201:
        return {"message": result["message"], "data": result["data"]}
     raise HTTPException(status_code=result["status"], detail=result["message"])


@app.get("/quizzes")
async def get_quiz():
    result = await get_quizzes()
    if result["status"] == 200:
        return {"message": result["message"], "data": result["data"]}
    raise HTTPException(status_code=result["status"], detail=result["message"])


@app.get("/get_quizzes")
async def get_quiz_level(level: str):
    result = await get_quiz_on_level(level)
    if result["status"] == 200:
        return {"message": result["message"], "data": result["data"]}
    raise HTTPException(status_code=result["status"], detail=result["message"])

@app.post("/submit_quiz")
async def submit_quiz(request: SubmitAnswerModel):
    result = await submit_quiz_and_verify_results(request)
    if result["status"] == 200:
        return {"message": result["message"], "data": result["data"]}
    raise HTTPException(status_code=result["status"], detail=result["message"])