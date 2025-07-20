from prisma import Prisma
from datetime import datetime, timedelta, timezone
from models.SendMessageModel import SendMessageModel
from utils.anylyze_debate import get_ai_reply

async def send_message(request:SendMessageModel):
    try:
        prisma = Prisma()
        if not prisma.is_connected:
            await prisma.connect()

        session = await prisma.debatesession.find_unique(where={"id": request.session_id})
        if not session:
            return {"error": "Session not found."}

        start_time = session.createdAt
        duration_minutes = session.duration
        end_time = start_time + timedelta(minutes=duration_minutes)

        if datetime.now(timezone.utc) > end_time:
            return {"error": "Debate time is over. Please end the debate to see feedback."}

        await prisma.message.create(
                data={"sessionId": request.session_id, "role": "user", "content": request.user_message}
        )

        messages = await prisma.message.find_many(
                where={"sessionId": request.session_id}, order={"createdAt": "asc"}
        )
        formatted = [{"role": m.role, "content": m.content} for m in messages]

        ai_response = await get_ai_reply(formatted)

        await prisma.message.create(
                data={"sessionId": request.session_id, "role": "assistant", "content": ai_response}
            )

        return {"message": "Ai Feedback", "status" : 200, "data": ai_response}
    
    except Exception as e:
        print(f"Error in sending message: {str(e)}")
        return {"error": str(e), "status": 500}
    finally:
        await prisma.disconnect()

