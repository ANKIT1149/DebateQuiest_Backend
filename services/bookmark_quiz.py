from prisma import Prisma
from models.BookmarkModel import BookMarkModel

async def bookmark_quiz(request: BookMarkModel):
    try:
        prisma = Prisma()
        if not prisma.is_connected:
            await prisma.connect()

        exsistingUser = await prisma.user.find_unique(where={"clerk_id": request.userId})

        if not exsistingUser:
            return {"message": "User not exsist", "status": 403}

        storeBookMark = await prisma.bookmark_quiz.create_many(data=[
            {
              "level": request.level,
              "quizId": request.quizId,
              "userId": request.userId  
            }
        ])

        return {"message": "Bookmark Quiz Stored", "status": 200, "data": storeBookMark}
    except Exception as e:
        print(f"Erro in storing bookmark quiz: {str(e)}")
        return
