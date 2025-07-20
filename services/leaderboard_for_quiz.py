from typing import Dict, List
from prisma import Prisma


async def get_leaderboard_for_quiz(limit: int = 10) -> List[Dict[str, any]]:
    try:
        prisma = Prisma()
        if not prisma.is_connected:
            await prisma.connect()

        quiz_result = await prisma.quiz_result.find_many(
            include={"user": True}
        )

        if not quiz_result: 
            return {"message": "Quiz Result not found", "status": 400}

        user_points = {}
        for quiz in quiz_result:
            user_id = quiz.userId
            username = quiz.user.username
            score = quiz.score

            if user_id not in user_points:
                user_points[user_id] = {"username": username, "total_score": 0}
            user_points[user_id]["total_score"] += score

        leaderboard = [
            {"username": data["username"], "total_score": data["total_score"]}
            for data in user_points.values()
        ]

        leaderboard.sort(key=lambda x:x["total_score"], reverse=True)
        leaderboard_data = leaderboard[:limit]

        return {"message": "Find Successfully", "status": 200, "data": leaderboard_data}
    except Exception as e:
        print(f"error in finding users: {str(e)}")
        return
    finally:
        await prisma.disconnect()
