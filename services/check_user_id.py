from prisma import Prisma
from models.UserIdModel import UserIdModel

async def check_user_id(request: UserIdModel):
    try:
        prisma = Prisma()
        await prisma.connect()

        userId = await prisma.user.find_first(
               where={"clerk_id": request.userId}
          )

        if userId:
            return {"message": "User exists", "status": 200, "data": userId}
        else:
            return {"message": "User exists", "status": 403, "data": userId}
    except Exception as error:
        print(f"Error checking user ID: {error}")
        return {"message": "Internal server error", "status": 500}
