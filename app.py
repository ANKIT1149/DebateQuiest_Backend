from fastapi import (
    FastAPI,
    HTTPException,
)
from db.postgressConnection import get_connection
from routes.Register_User import register_userdata
from models.RegisterModel import RegisterModel
from fastapi.middleware.cors import CORSMiddleware
from services.get_quizzes import get_quizzes
from services.get_quiz_on_level import get_quiz_on_level
from models.SubmitAnswer import SubmitAnswerModel
from models.UserIdModel import UserIdModel
from services.verify_quiz_answer import submit_quiz_and_verify_results
from services.check_user_id import check_user_id
from services.calculate_quiz import calculate_quiz_and_score
from models.GetQuizesModel import GetQuizes
from models.UserIdModel import UserIdModel
from services.get_user_take_quiz import get_user_taken_quiz
from models.BookmarkModel import BookMarkModel
from services.bookmark_quiz import bookmark_quiz
from services.get_bookmarked_quiz import get_bookmarked_quiz
from models.ProgressModel import ProgressModel
from services.level_calculation_and_store import store_level_and_rewards
from services.start_debate import start_debate
from services.end_debate import end_debate
from utils.send_message import send_message
from models.SendMessageModel import SendMessageModel
from models.StartdebatingAiModel import StartDebatingModel
from services.remove_bookmark_quiz import remove_bookmark_quiz
from models.RemoveBookMarkModel import RemoveBookMarkModel
from services.get_level_and_exp import get_level_and_exp
from services.leaderboard_for_quiz import get_leaderboard_for_quiz
from models.PromptGenerateModel import PromptGenerateModel
from services.generate_quiz import openai_client
import openai
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://debatequiest-frontend.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

get_connection()

@app.get("/")
async def root():
    return {"message": "Welcome to DebateQuest Backend"}


@app.head("/")
async def head_root():
    return {}


@app.post("/register")
async def register_user(User: RegisterModel):
    result = await register_userdata(User)
    if result["status"] == 201:
        return {"message": result["message"], "data": result["data"]}
    raise HTTPException(status_code=result["status"], detail=result["message"])


@app.post("/quizzes")
async def get_quiz(request: GetQuizes):
    result = await get_quizzes(request)
    if result["status"] == 200:
        return {"message": result["message"], "data": result["data"]}
    raise HTTPException(status_code=result["status"], detail=result["message"])


@app.get("/get_quizzes")
async def get_quiz_level(quizId: str):
    result = await get_quiz_on_level(quizId)
    if result["status"] == 200:
        return {"message": result["message"], "data": result["data"]}
    raise HTTPException(status_code=result["status"], detail=result["message"])


@app.post("/submit_quiz")
async def submit_quiz(request: SubmitAnswerModel):
    result = await submit_quiz_and_verify_results(request)
    if result["status"] == 200:
        return {"message": result["message"], "data": result["data"]}
    raise HTTPException(status_code=result["status"], detail=result["message"])


@app.post("/check_userId")
async def check_userId(request: UserIdModel):
    result = await check_user_id(request)
    if result["status"] == 200:
        return {"message": result["message"], "data": result["data"]}
    raise HTTPException(status_code=result["status"], detail=result["message"])


@app.post("/calculate")
async def calculating_score(request: UserIdModel):
    result = await calculate_quiz_and_score(request)
    if result["status"] == 200:
        return {"message": result["message"], "data": result["data"]}
    raise HTTPException(status_code=result["status"], detail=result["message"])


@app.post("/get_taken_quiz")
async def get_taken_quiz(request: UserIdModel):
    result = await get_user_taken_quiz(request)
    if result["status"] == 200:
        return {"message": result["message"], "data": result["data"]}
    raise HTTPException(status_code=result["status"], detail=result["message"])


@app.post("/store_bookmarked_quiz")
async def store_bookmarked_quiz(request: BookMarkModel):
    result = await bookmark_quiz(request)
    if result["status"] == 200:
        return {"message": result["message"], "data": result["data"]}
    raise HTTPException(status_code=result["status"], detail=result["message"])

@app.post("/removed_bookmark_quiz")
async def remove_bookmarked_quiz(request: RemoveBookMarkModel):
    result = await remove_bookmark_quiz(request)
    if result["status"] == 200:
        return {"message": result["message"], "data": result["data"]}
    raise HTTPException(status_code=result["status"], detail=result["message"])


@app.post("/get_bookmarked_quiz")
async def get_bookmarke_quiz(request: UserIdModel):
    result = await get_bookmarked_quiz(request)
    if result["status"] == 200:
        return {"message": result["message"], "data": result["data"]}
    raise HTTPException(status_code=result["status"], detail=result["message"])


@app.post("/store_level")
async def store_level(request: ProgressModel):
    result = await store_level_and_rewards(request)
    if result["status"] == 200:
        return {"message": result["message"], "data": result["data"]}
    raise HTTPException(status_code=result["status"], detail=result["message"])

@app.post("/get_level")
async def get_level(request: UserIdModel):
    result = await get_level_and_exp(request)
    if result["status"] == 200:
        return {"message": result["message"], "data": result["data"]}
    raise HTTPException(status_code=result["status"], detail=result["message"])

@app.get("/get_quiz_leaderboard")
async def get_level(limit: int = 10):
    result = await get_leaderboard_for_quiz(limit)
    if result["status"] == 200:
        return {"message": result["message"], "data": result["data"]}
    raise HTTPException(status_code=result["status"], detail=result["message"])

@app.post("/generate_quiz")
async def generate_quiz(model: PromptGenerateModel):
    result = await openai_client(model)
    if result["status"] == 200:
        return {"message": result["message"], "data": result["data"]}
    raise HTTPException(status_code=result["status"], detail=result["message"])


@app.post("/start_debate")
async def start_debate_with_ai(request: StartDebatingModel):
    result = await start_debate(request)
    if result["status"] == 200:
        return {"message": result["message"], "data": result["data"]}
    raise HTTPException(status_code=result["status"], detail=result["message"])


@app.post("/send_message")
async def send_debate_with_ai(request: SendMessageModel):
    result = await send_message(request)

    if not result:
        raise HTTPException(status_code=500, detail="No response from send_message()")

    if result.get("status") == 200:
        return {"message": result["message"], "data": result["data"]}


    raise HTTPException(
        status_code=result.get("status", 500),
        detail=result.get("error", "Unknown error"),
    )


@app.post("/end-debate/{session_id}")
async def end_debate_with_ai(session_id: str):
    result = await end_debate(session_id)
    if result["status"] == 200:
        return {"message": result["message"], "data": result["data"]}
    raise HTTPException(status_code=result["status"], detail=result["message"])


@app.get("/test-openai")
async def test_openai():
    openai.api_key = os.getenv("OPENAI_API_KEY")
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": "Hello, world!"}]
    )
    return {"result": response.choices[0].message.content}
