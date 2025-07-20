from prisma import Prisma

async def save_message(session_id: str, role: str, content: str):
    try:
        prisma = Prisma()
        await prisma.connect()

        await prisma.message.create(
            data={
                "role": role,
                "sessionId": session_id,
                "content": content
            }
        )
    except Exception as e:
        print(f"User Message stored")
        return
