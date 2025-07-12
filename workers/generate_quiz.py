import os
from dotenv import load_dotenv
import openai
from prisma import Prisma
import json

load_dotenv(dotenv_path=".env")

OpenAI_API_KEY=os.getenv("OPENAI_API_KEY")
openai.api_key = OpenAI_API_KEY

async def openai_client():
    try:

        prisma = Prisma()
        await prisma.connect()

        prompt = """
           Generate 10 expert-level debate quiz questions for grade 10 to 12 class Students. Each question should:
           - Have a title (e.g., "Fallacy Basics").
           - Include a question text.
           - Provide 4 multiple-choice options (label as A, B, C, D).
           - Specify the correct answer (e.g., "A").
           - Include a brief explanation.
           - Set level as "Expert".
           -Generate a quizId same for all question and ensure quizId is in form of uuid not normal
           -Also add the grade for which grade this for
           Return the output as a JSON array of objects with fields: title, question, options, correct_answer, explanation, level, grade, quizId.
           Ensure the response is valid JSON with no additional text.
           """

        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2000,
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
        print(f"Quiz generated Successfully and saved {len(formatted_Data)} quizzess")
    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        await prisma.disconnect()

if __name__ == "__main__":
    import asyncio
    asyncio.run(openai_client())
