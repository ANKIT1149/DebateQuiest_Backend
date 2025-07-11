from prisma import Prisma

async def get_quiz_on_level(level: str):
    try:
        prisma = Prisma()
        await prisma.connect()

        print(f"Prisma connected Successfully")

        quizData = await prisma.quizzes.find_many(
            where={"level": level},
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
