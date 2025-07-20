from prisma import Prisma
from utils.anylyze_debate import anylyze_Debate
from datetime import datetime, timezone
import json
from prisma import Json

async def end_debate(session_id: str):
    try:
        prisma = Prisma()
        await prisma.connect()

        messages = await prisma.message.find_many(
            where={"sessionId": session_id},
            order={"createdAt": "desc"}
        )

        formatted = "\n".join([f"{m.role}: {m.content}" for m in messages])
        anylysis = await anylyze_Debate(formatted)

        await prisma.debatesession.update(
            where={"id": session_id},
            data = {
                "endTime": datetime.now(timezone.utc),
                "winner": anylysis["winner"],
                "feedback": Json(anylysis)
            }
        )

        return {"message": "Debate end successfully", "status": 200, "data": anylysis}
    except Exception as e:
        print(f"Error in ending the debate: {str(e)}")
        return
