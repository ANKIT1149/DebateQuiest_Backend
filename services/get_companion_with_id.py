from fastapi import HTTPException
from prisma import Prisma
from models.GetCompanionMOdel import GetCompanionModel

async def get_companion_with_id(request:GetCompanionModel):
    try:
        prisma = Prisma()
        await prisma.connect()
        
        exsistingUser = await prisma.user.find_unique(
            where={"clerk_id": request.userId}
        )

        if not exsistingUser:
            raise HTTPException(status_code=403, detail="user not Exsist")
        
        companion = await prisma.companion_create.find_unique(
            where={"id": request.companion_id}
        )

        if not companion:
            raise HTTPException(status_code=400, detail="Companion not Found")
        
        return {"message": "Companion data found", "status": 200, "data": companion}
    
    except Exception as e:
        print(f"Error in getting companion: {str(e)}")
        return
    finally:
        await prisma.disconnect()
    
        
