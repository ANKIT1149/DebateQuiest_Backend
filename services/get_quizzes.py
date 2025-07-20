from prisma import Prisma
from models.GetQuizesModel import GetQuizes

async def get_quizzes(request: GetQuizes):
    try:
        prisma = Prisma()
        if not prisma.is_connected:
            await prisma.connect()

        print(f"Prisma connected SuccessFully")

        beginnerquizzes = await prisma.quizzes.find_many(
            where={"grade": request.grade, "level": "Beginner"},
            take=1
        )

        intermediatequizzes = await prisma.quizzes.find_many(
            where={"grade": request.grade, "level": "Intermediate"},
            take=1
        )

        expertquizzes = await prisma.quizzes.find_many(
            where={"grade": request.grade, "level": "Expert"},
            skip=1,
            take=1
        )

        quizData=beginnerquizzes + intermediatequizzes + expertquizzes

        if not quizData:
            return {"message": "No quizzes found", "status": 404}

        return {
            "message": "Quizzes retrieved successfully",
            "status": 200,
            "data": quizData
        }
    except Exception as error:
        print(f"Error retrieving quizzes: {error}")
        return {"message": f"Failed to retrieve quizzes: {error}", "status": 500}
