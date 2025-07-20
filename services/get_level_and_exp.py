from prisma import Prisma
from models.UserIdModel import UserIdModel

async def get_level_and_exp(request: UserIdModel):
    try:
        prisma = Prisma()
        await prisma.connect()

        exsistingUser = await prisma.user.find_unique(
            where={"clerk_id": request.userId}
        )

        if not exsistingUser:
            return {"message": "User not exsist", "status": 403}

        find_progress_report = await prisma.user_progress.find_first(
            where={"userId": request.userId},
            order={"updated_at": "desc"}
        )

        return {
            "message": "Progress found",
            "status": 200,
            "data": find_progress_report,
        }

    except Exception as e:
        print(f"Error in getting progress report, {str(e)}")
        return
