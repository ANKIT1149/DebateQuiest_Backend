from prisma import Prisma

async def get_quiz_on_level(quizId: str):
    try:
        prisma = Prisma()
        if not prisma.is_connected:
            await prisma.connect()

        print(f"Prisma connected Successfully")

        quizData = await prisma.quizzes.find_many(
            where={"quizId": quizId},
            take=10
        )

        if not quizData:
            return {"message": "No quizzes found for the specified level", "status": 404}

        return {
            "message": "Quizzes retrieved successfully",
            "status": 200,
            "data": quizData
        }
    except Exception as error:
        print(f"Error retrieving quizzes: {error}")
        return {"message": f"Failed to retrieve quizzes: {error}", "status": 500}
