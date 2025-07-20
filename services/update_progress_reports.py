from prisma import Prisma
import json

BADGES = [
    "New Debater", "Basic Learner", "Argument Starter", "Rebuttal Rookie",
    "Intermediate Champ", "Fallacy Finder", "Persuasion Pro", "Expert Debater",
    "Master Orator", "Debate Legend"
]

async def update_progress_report(userId: str, quizId: str, score: int, level: str):
    try:
        prisma = Prisma()
        if not prisma.is_connected:
            await prisma.connect()

        progress_user = await prisma.user.find_unique(
            where={"clerk_id": userId}
        )

        if not progress_user:
            return {"message": "User not exist", "status": 403}

        progress_field = await prisma.user_progress.find_first(
            where={"userId": userId}
        )

        if not progress_field:
            progress_field = await prisma.user_progress.create(
                data={"userId": userId, "Exp": 0, "Level": 1, "Badges": "[]"}
            )

        if level == "Beginner":
            if score > 5:
                newExp = progress_field.Exp + (score * 8)
            else:
                newExp = progress_field.Exp + (score * 4)
        elif level == "Intermediate":
            if score > 5:
                newExp = progress_field.Exp + (score * 10)             
            else:
                newExp = progress_field.Exp + (score * 5)
        elif level == "Expert":
            if score > 5:
                newExp = progress_field.Exp + (score * 12)
            else:
                newExp = progress_field.Exp + (score * 6)
        else:
            return {"message": "Invalid level", "status": 400}

        new_level = progress_field.Level
        current_badges = json.loads(progress_field.Badges) if progress_field.Badges else []
        new_badges = current_badges.copy()

        if newExp >= 100:
            new_level += 1
            newExp -= 100
            if new_level <= len(BADGES) and BADGES[new_level - 1] not in new_badges:
                new_badges.append(BADGES[new_level - 1])

        update_level = await prisma.user_progress.update(
            where={"id": progress_field.id},
            data={
                "Exp": newExp,
                "Level": new_level,
                "Badges": json.dumps(new_badges),
            }
        )

        return {"message": "Update progress", "status": 200, "data": update_level.model_dump() if hasattr(update_level, 'dict') else update_level}

    except Exception as e:
        print(f"error in updating: {str(e)}")
        return {"message": "Error updating progress", "status": 500}
