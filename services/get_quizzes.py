from prisma import Prisma

async def get_quizzes():
    try:
        prisma = Prisma()
        await prisma.connect()

        print(f"Prisma connected SuccessFully")

        beginnerquizzes = await prisma.quizzes.find_many(
            where={"level": "Beginner"}, take=1
        )

        intermediatequizzes = await prisma.quizzes.find_many(
            where={"level": "Intermediate"}, take=1
        )

        expertquizzes = await prisma.quizzes.find_many(
            where={"level": "Expert"}, take=1, skip=1
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
    finally:
        await prisma.disconnect()
