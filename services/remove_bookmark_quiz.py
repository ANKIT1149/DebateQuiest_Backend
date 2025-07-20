from prisma import Prisma
from models.BookmarkModel import BookMarkModel


async def remove_bookmark_quiz(request: BookMarkModel):
    try:
        prisma = Prisma()
        if not prisma.is_connected:
            await prisma.connect()

        exsistingUser = await prisma.user.find_unique(
            where={"clerk_id": request.userId}
        )

        if not exsistingUser:
            return {"message": "User not exsist", "status": 403}

        checkBookmark = await prisma.bookmark_quiz.find_first(
            where={"quizId": request.quizId}
        )

        storeBookMark = await prisma.bookmark_quiz.delete(
            where={"id": checkBookmark.id}
        )

        return {"message": "Bookmark Quiz Removed", "status": 200, "data": storeBookMark}
    except Exception as e:
        print(f"Error in storing bookmark quiz: {str(e)}")
        return
