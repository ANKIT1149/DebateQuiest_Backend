from prisma import Prisma
from models.ProgressModel import ProgressModel
import json

async def store_level_and_rewards(request: ProgressModel):
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
        
        if exsistingUser.grade != request.grade:
            return {"message": "Grade not exsist", "status": 403}
        
        store_level = await prisma.user_progress.create(
            data={
                    
                    "userId": request.userId,
                    "grade": request.grade,
                    "Level": 1,
                    "Exp": 0,
                    "Badges": json.dumps([])
                }
        )

        return {"message": "Progress Bar Created", "status": 200, "data": store_level}
    
    except Exception as e:
        print(f"Error in storing level: {str(e)}")
        return
    
    finally:
        await prisma.disconnect()
