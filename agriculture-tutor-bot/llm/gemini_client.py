from google import genai
from config import GEMINI_API_KEY, MODEL_NAME

client = genai.Client(api_key=GEMINI_API_KEY)

def evaluate_answer(question, correct_answer, user_answer, context):
    prompt = f"""
You are an agriculture expert tutor.

Context:
{context}

Question: {question}
Correct Answer: {correct_answer}
Student Answer: {user_answer}

Evaluate the student's answer.

Return:
1. Score (0-10)
2. Verdict (Correct/Partially Correct/Incorrect)
3. Explanation of mistake
4. Correct concept in simple language
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    return response.text