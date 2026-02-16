from database.vector_store import load_knowledge
from services.evaluation_service import evaluate

def main():
    print("🌾 Agriculture Tutor Bot\n")

    # Load knowledge (run once per session)
    load_knowledge()

    question = "How can farmers prevent fungal infection in crops?"
    correct_answer = (
        "Farmers should avoid overwatering, maintain proper spacing, "
        "and use preventive fungicides."
    )

    print("Question:", question)
    user_answer = input("\nYour Answer: ")

    print("\n🤖 Evaluating...\n")

    result = evaluate(question, correct_answer, user_answer)

    print("📊 Result:\n")
    print(result)


if __name__ == "__main__":
    main()