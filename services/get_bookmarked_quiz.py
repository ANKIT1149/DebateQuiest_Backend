from models.UserIdModel import UserIdModel
from prisma import Prisma

async def get_bookmarked_quiz(request: UserIdModel):
    try:
        prisma = Prisma()
        await prisma.connect()

        exsistingUser = await prisma.user.find_unique(
            where={
                "clerk_id": request.userId
            }
        )

        if not exsistingUser:
            return {"message": "User not exsist", "status": 403}
        
        bookmarkedQuiz=await prisma.bookmark_quiz.find_many(
            where={"userId": request.userId}
        )

        if not bookmarkedQuiz:
            return {"message": "No Bookmarked Quiz", "status": 400}
        
        quizId = [quiz.quizId for quiz in bookmarkedQuiz]
        print(f"quizId: {quizId}")

        gettingQuiz = await prisma.quizzes.find_many(
            where={
                "quizId": {
                    "in": quizId
                }
            }
        )

        if not gettingQuiz:
            return {"message": "quizzes not found", "status": 400}
        
        quizData=[]
        set_quiz_id = set()
        for quiz in gettingQuiz:
            if quiz.quizId not in set_quiz_id:
                set_quiz_id.add(quiz.quizId)
                quizData.append({
                    "title": quiz.title,
                    "level": quiz.level,
                    "quizId": quiz.quizId
                })
        return {"message": "Bookmarked Quiz Find", "status": 200, "data": quizData}
    except Exception as e:
        print(f"Error in geeting bookmarked quiz: {str(e)}")
        return
    finally:
        await prisma.disconnect()

