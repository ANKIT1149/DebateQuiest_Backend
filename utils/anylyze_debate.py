import openai
import os
from dotenv import load_dotenv
import json

load_dotenv(dotenv_path=".env")

OpenAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OpenAI_API_KEY

async def anylyze_Debate(chat_text):
    prompt = f"""
            Act as a debate evaluator. Analyze the following debate transcript and provide:
            - Score for user (0-10) based on clarity, logic, rebuttals, and evidence
            - Score for AI (0-10) on same criteria
            - Who won and why
            - Best point made by user
            - Weakest argument by user
            - Any logical fallacies made by user
            - Suggestions for improvement

            Debate:
            {chat_text}

            Return result in JSON format with keys: user_score, ai_score, winner, best_point, weak_argument, fallacies, suggestions
        """

    response = openai.chat.completions.create(
        model="gpt-4", messages=[{"role": "user", "content": prompt}]
    )

    return json.loads(response.choices[0].message.content)


async def get_ai_reply(messages):
    response = openai.chat.completions.create(
        model="gpt-4", messages=messages, temperature=0.7
    )
    return response.choices[0].message.content
