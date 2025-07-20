from fastapi import BackgroundTasks
from prisma import Prisma
from models.StartdebatingAiModel import StartDebatingModel
from utils.anylyze_debate import get_ai_reply

async def start_debate(
    request: StartDebatingModel
):
    try:
        prisma = Prisma()
        await prisma.connect()

        session = await prisma.debatesession.create(
            data={"topic": request.topic, "duration": request.duration, "userId": request.user_id}
        )

        system_message = {"role": "system", "content": f"You are debating the user on: {request.topic} and you have to only discuss {request.topic} related debate"}
        ai_intro = await get_ai_reply([system_message])

        await prisma.message.create_many(data=[
            {"sessionId": session.id, "role": "system", "content": system_message["content"]},
            {"sessionId": session.id, "role": "assistant", "content": ai_intro}
        ])

        data = {
            "ai-Intro": ai_intro,
            "id": session.id,
        }

        return {
            "message": "Debate started",
            "status": 200,
            "data": data
        }

    except Exception as e:
        print(f"Error in starting debate: {str(e)}")
        return
