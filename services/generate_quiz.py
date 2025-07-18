import os
from dotenv import load_dotenv
import openai
from prisma import Prisma
import json

from models.PromptGenerateModel import PromptGenerateModel

load_dotenv(dotenv_path=".env")

OpenAI_API_KEY=os.getenv("OPENAI_API_KEY")
openai.api_key = OpenAI_API_KEY

async def openai_client(model: PromptGenerateModel):
    try:

        prisma = Prisma()
        await prisma.connect()

        prompt = f"""
           Generate 10 {model.level}-level debate quiz questions on topic {model.title} for grade {model.grade} class Students. Each question should:
           - Have a title (e.g., "Fallacy Basics").
           - Include a question text.
           - Provide 4 multiple-choice options (label as A, B, C, D).
           - Specify the correct answer (e.g., "A").
           - Include a brief explanation.
           - Set level as "Expert".
           -Generate a quizId same for all question and ensure quizId is in form of uuid not normal
           -Also add the grade, remember grade value is {model.grade} exact same that you recieve not any change
           Return the output as a JSON array of objects with fields: title, question, options, correct_answer, explanation, level, grade, quizId.
           Ensure the response is valid JSON with no additional text.
           """

        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
        )

        raw_response = response.choices[0].message.content.strip()
        print(f"quiz data: {raw_response}")

        try:
            quiz_data = json.loads(raw_response)
        except json.JSONDecodeError as e:
            print(f"JSON Decode Error: {e}, Raw response: {raw_response}")
            raise

        if not isinstance(quiz_data, list):
            raise ValueError("Response is not valid JSON Array")

        formatted_Data=[]
        for quiz in quiz_data:
            option_list = [f"{key}) {value}" for key, value in quiz["options"].items()]
            formatted_Data.append(
                {
                    "title": quiz["title"],
                    "question": quiz["question"],
                    "options": json.dumps(option_list),
                    "correct_answer": quiz["correct_answer"],
                    "explanation": quiz["explanation"],
                    "level": quiz["level"],
                    "quizId": quiz["quizId"],
                    "grade": quiz["grade"]
                }
            )

        await prisma.quizzes.create_many(
                data=formatted_Data
            )
        return {"message": "Quiz Generated Successfully", "status": 200, "data": formatted_Data}
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        await prisma.disconnect()
