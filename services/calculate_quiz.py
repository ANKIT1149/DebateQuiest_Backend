from prisma import Prisma
from models.UserIdModel import UserIdModel


async def calculate_quiz_and_score(request: UserIdModel):
    try:
        prisma = Prisma()
        await prisma.connect()

        print(f"Prisma connected Successfully")

        exsistsuser = await prisma.user.find_unique(where={"clerk_id": request.userId})
        if not exsistsuser:
            return {"message": "User not Exsist", "status": 403}

        quizdata = await prisma.quiz_result.find_many(where={"userId": request.userId})
        if not quizdata:
            return {"message": "Quiz Results not exsist", "status": 400}

        print(f"quizData: {quizdata}")

        total_score = sum(quiz.score for quiz in quizdata)
        total_marks = sum(quiz.Total_Marks for quiz in quizdata)
        taken_quiz = len(quizdata)
        percentage = round((total_score / total_marks) * 100, 2)

        data = {
            "userId": request.userId,
            "total_score": total_score,
            "total_marks": total_marks,
            "taken_quiz": taken_quiz,
            "percentage": percentage
        }

        return {"message": "Quiz Results  exsist", "status": 200, "data": data}
    except Exception as e:
        print(f"Error in getting score: {str(e)}")
