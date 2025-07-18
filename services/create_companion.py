from prisma import Prisma
from models.CompanionModel import CompanionCreate

async def create_companion(companion: CompanionCreate):
    try:
        prisma = Prisma()
        await prisma.connect()

        exsistgUser = await prisma.user.find_unique({"clerk_id": companion.userId})

        if not exsistgUser:
            return {"message": "user not exsist", "status": 403}
        
        companion_data = await prisma.companion_create.create(
            data={
                "userId": companion.userId,
                "duration": companion.duration,
                "level": companion.level,
                "topic": companion.topic,
                "tone": companion.tone,
                "voice": companion.voice
            }
        )

        if not companion_data:
            return {"message": "Unable to make companion", "status": 400}
        
        return {"message": "Companion Create", "status": 200, "data": companion_data}
    except Exception as e:
        print(F"Error in creating companion {str(e)}")
        return
    finally:
        await prisma.disconnect()
        
