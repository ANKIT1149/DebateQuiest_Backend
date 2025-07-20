from models.UserIdModel import UserIdModel
from prisma import Prisma


async def get_user_taken_quiz(request: UserIdModel):
    try:
        prisma = Prisma()
        if not prisma.is_connected:
            await prisma.connect()

        exsistingUser = await prisma.user.find_unique(
            where={"clerk_id": request.userId}
        )

        if not exsistingUser:
            return {"message": "User not exsists", "status": 403}

        quizResult = await prisma.quiz_result.find_many(
            where={"userId": request.userId}
        )

        if not quizResult:
            return {"message": "Quiz not taken by user", "status": 400}

        quizId = [quiz.quizId for quiz in quizResult]
        score = {quiz.quizId: quiz.score for quiz in quizResult}

        print(f"quizId: {quizId}")

        findingQuiz = await prisma.quizzes.find_many(where={"quizId": {"in": quizId}})

        quizData = []
        set_quiz_ids = set()
        for quiz in findingQuiz:
            if quiz.quizId not in set_quiz_ids:
                set_quiz_ids.add(quiz.quizId)
                quizData.append(
                    {
                        "title": quiz.title,
                        "level": quiz.level,
                        "score": score.get(quiz.quizId, 0),
                        "quizId": quiz.quizId,
                    }
                )

        return {"message": "Quiz Taken By User", "status": 200, "data": quizData}
    except Exception as e:
        print(f"Error in finding quiz: {str(e)}")
        return
