from llm.gemini_client import evaluate_answer
from services.rag_service import get_context

def evaluate(question, correct_answer, user_answer):
    context = get_context(question)

    result = evaluate_answer(
        question,
        correct_answer,
        user_answer,
        context
    )

    return result