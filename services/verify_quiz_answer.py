from fastapi import HTTPException
from prisma import Prisma
from models.SubmitAnswer import SubmitAnswerModel


async def submit_quiz_and_verify_results(request: SubmitAnswerModel):
    try:
        prisma = Prisma()
        await prisma.connect()

        print(f"Prisma connected Successfully")

        exsistuser = await prisma.user.find_first(where={"clerk_id": request.userId})

        if not exsistuser:
            return {"message": "User not exsist", "status": 403}

        print(
            f"level: {request.quizId}, userID: {request.userId} answer: {request.answer}"
        )
        quizData = await prisma.quizzes.find_many(
            where={"quizId": request.quizId},
        )

        print(f"quiz data: {quizData}")

        if not quizData:
            return {
                "message": "No quizzes found for the specified level",
                "status": 404,
            }

        correct_answers = {str(q.id): q.correct_answer for q in quizData}

        results = {}
        correct_answer = 0
        wrong_answer = 0
        total_question = 10
        total_marks = 0
        score = 0

        for answer in request.answer:
            question_id = answer.i
            user_answer = answer.a.strip()

            if question_id in correct_answers:
                isCorrect = user_answer == correct_answers[question_id]
                results[question_id] = isCorrect

                if isCorrect:
                    correct_answer += 1
                else:
                    wrong_answer += 1
            else:
                results[question_id] = False
                wrong_answer += 1

        if request.level == "Beginner":
            total_marks = total_question * 1
            score = correct_answer * 1

        elif request.level == "Intermediate":
            total_marks = total_question * 2
            score = correct_answer * 2

        elif request.level == "Expert":
            total_marks = total_question * 3
            score = correct_answer * 3
        else:
            raise HTTPException(status_code=400, detail=f"Invalid level: {request.level}")

        percentage = (score / total_marks) * 100 if total_marks > 0 else 0

        submitting_quizzes =  await prisma.quiz_result.create_many(
            data=[
                {
                    "userId": request.userId,
                    "correct_answer": correct_answer,
                    "Wrong_Answer": wrong_answer,
                    "Total_question": total_question,
                    "level": request.level,
                    "Total_Marks": total_marks,
                    "score": score,
                    "percentage": percentage,
                    "quizId": request.quizId
                }
            ]
        )

        quiz_return_data = {
            "score": score,
            "percentage": percentage,
            "correct_answers": correct_answer,
            "wrong_answers": wrong_answer,
            "total_marks": total_marks,
            "results": results,
            "userId": request.userId,
            "submittingQuizzes": submitting_quizzes,
            "answer": request.answer
        }

        return {
            "message": "Quiz results calculated successfully",
            "status": 200,
            "data": quiz_return_data,
        }
    except Exception as error:
        print(f"Error retrieving quizzes: {error}")
        return {"message": f"Failed to retrieve quizzes: {error}", "status": 500}
    finally:
        await prisma.disconnect()
        print(f"Prisma disconnected Successfully")
