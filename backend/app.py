"""
Agriculture Quiz Bot - Flask Backend
Uses: Groq (LLM) + Supabase (PostgreSQL online DB)
"""

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from groq import Groq
from supabase import create_client, Client
from dotenv import load_dotenv
import os
import random
import json
from datetime import datetime

load_dotenv()

# Serve frontend from ../frontend folder
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), '..', 'frontend')
app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path='')
CORS(app)

@app.route('/')
def index():
    return send_from_directory(FRONTEND_DIR, 'index.html')

# ─── Clients ───────────────────────────────────────────
groq_client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
supabase: Client = create_client(
    os.environ.get("SUPABASE_URL"),
    os.environ.get("SUPABASE_ANON_KEY")
)

GROQ_MODEL = "llama-3.3-70b-versatile"  # fast & free on Groq

# ─── Farming Knowledge Base ─────────────────────────────
FARMING_TIPS = [
    {"id": "tip_001", "topic": "Soil Health", "content": "Crop rotation prevents nutrient depletion and reduces pest buildup. Rotate legumes with cereals to naturally fix nitrogen in the soil, reducing the need for synthetic fertilizers."},
    {"id": "tip_002", "topic": "Irrigation", "content": "Drip irrigation delivers water directly to plant roots, reducing water usage by up to 60% compared to flood irrigation. It also minimizes weed growth and fungal diseases caused by wet foliage."},
    {"id": "tip_003", "topic": "Pest Management", "content": "Integrated Pest Management (IPM) combines biological, cultural, mechanical, and chemical controls. Using natural predators like ladybugs for aphid control reduces chemical pesticide use significantly."},
    {"id": "tip_004", "topic": "Composting", "content": "Compost improves soil structure, water retention, and microbial activity. A proper compost pile needs a 30:1 carbon-to-nitrogen ratio — mix brown materials (straw, cardboard) with green materials (kitchen scraps, grass)."},
    {"id": "tip_005", "topic": "Seed Selection", "content": "Heirloom seeds are open-pollinated varieties that can be saved and replanted. They often have better flavor and adaptability to local conditions, though hybrid seeds may offer higher yield uniformity."},
    {"id": "tip_006", "topic": "Cover Crops", "content": "Planting cover crops like clover, rye, or vetch during off-season prevents soil erosion, suppresses weeds, and improves soil fertility. They are tilled in before the main crop season as 'green manure'."},
    {"id": "tip_007", "topic": "pH Management", "content": "Most vegetables thrive in soil pH between 6.0–7.0. Add lime to raise pH in acidic soils and sulfur to lower pH in alkaline soils. Test soil pH regularly for best crop performance."},
    {"id": "tip_008", "topic": "Mulching", "content": "Applying 2–4 inches of organic mulch around plants conserves moisture, regulates soil temperature, suppresses weeds, and adds organic matter as it decomposes."},
    {"id": "tip_009", "topic": "Companion Planting", "content": "The 'Three Sisters' — corn, beans, and squash — is a classic companion planting system. Corn provides a trellis for beans; beans fix nitrogen; squash leaves shade the ground, retaining moisture and deterring pests."},
    {"id": "tip_010", "topic": "Harvesting", "content": "Harvest timing significantly impacts flavor and shelf life. Most vegetables should be harvested in the morning after the dew dries. Tomatoes are best harvested at 'breaker stage' for longer shelf life."},
    {"id": "tip_011", "topic": "Water Management", "content": "Overwatering is one of the most common farming mistakes. Signs include yellowing leaves, mold, and root rot. Water deeply but infrequently to encourage deep root growth and drought resilience."},
    {"id": "tip_012", "topic": "Fertilization", "content": "NPK (Nitrogen, Phosphorus, Potassium) are the three macronutrients essential for plant growth. Nitrogen promotes leafy growth, phosphorus supports root development and flowering, and potassium improves overall plant health."},
    {"id": "tip_013", "topic": "Greenhouse Farming", "content": "Greenhouses extend the growing season and protect crops from harsh weather. Proper ventilation is critical to prevent humidity-related diseases. Automated climate control systems optimize temperature and CO2 levels."},
    {"id": "tip_014", "topic": "Organic Farming", "content": "Certified organic farming prohibits synthetic pesticides and fertilizers. It relies on natural inputs, biodiversity, and ecological processes. Organic certification typically requires a 3-year transition period from conventional farming."},
    {"id": "tip_015", "topic": "Precision Agriculture", "content": "Precision agriculture uses GPS, IoT sensors, and data analytics to optimize field management. Variable rate technology (VRT) applies inputs like fertilizer and water only where needed, reducing costs and environmental impact."},
]

QUIZ_QUESTIONS = [
    {"id": "q001", "topic": "Soil Health", "question": "What is the primary benefit of rotating legumes with cereal crops?", "options": {"A": "It increases water usage efficiency", "B": "It naturally fixes nitrogen in the soil", "C": "It eliminates all soil pests", "D": "It increases soil pH levels"}, "correct_answer": "B", "tip_id": "tip_001", "difficulty": "medium"},
    {"id": "q002", "topic": "Irrigation", "question": "By approximately how much can drip irrigation reduce water usage compared to flood irrigation?", "options": {"A": "10–20%", "B": "30–40%", "C": "Up to 60%", "D": "Up to 90%"}, "correct_answer": "C", "tip_id": "tip_002", "difficulty": "easy"},
    {"id": "q003", "topic": "Pest Management", "question": "In Integrated Pest Management (IPM), what is the role of ladybugs?", "options": {"A": "They pollinate crops", "B": "They fix nitrogen in the soil", "C": "They are natural predators of aphids", "D": "They improve soil drainage"}, "correct_answer": "C", "tip_id": "tip_003", "difficulty": "easy"},
    {"id": "q004", "topic": "Composting", "question": "What is the ideal carbon-to-nitrogen ratio for a proper compost pile?", "options": {"A": "10:1", "B": "20:1", "C": "30:1", "D": "50:1"}, "correct_answer": "C", "tip_id": "tip_004", "difficulty": "hard"},
    {"id": "q005", "topic": "pH Management", "question": "What should you add to raise the pH of acidic soil?", "options": {"A": "Sulfur", "B": "Lime", "C": "Nitrogen fertilizer", "D": "Compost only"}, "correct_answer": "B", "tip_id": "tip_007", "difficulty": "medium"},
    {"id": "q006", "topic": "Companion Planting", "question": "In the 'Three Sisters' system, what does squash primarily do?", "options": {"A": "Provides trellis for climbing plants", "B": "Fixes nitrogen in the soil", "C": "Shades ground to retain moisture and deter pests", "D": "Attracts beneficial pollinators"}, "correct_answer": "C", "tip_id": "tip_009", "difficulty": "medium"},
    {"id": "q007", "topic": "Fertilization", "question": "Which macronutrient primarily supports root development and flowering?", "options": {"A": "Nitrogen (N)", "B": "Potassium (K)", "C": "Phosphorus (P)", "D": "Calcium (Ca)"}, "correct_answer": "C", "tip_id": "tip_012", "difficulty": "medium"},
    {"id": "q008", "topic": "Cover Crops", "question": "What are cover crops tilled into soil called?", "options": {"A": "Mulch", "B": "Green manure", "C": "Compost", "D": "Biochar"}, "correct_answer": "B", "tip_id": "tip_006", "difficulty": "easy"},
    {"id": "q009", "topic": "Organic Farming", "question": "How long is the typical transition period for organic certification?", "options": {"A": "1 year", "B": "2 years", "C": "3 years", "D": "5 years"}, "correct_answer": "C", "tip_id": "tip_014", "difficulty": "hard"},
    {"id": "q010", "topic": "Mulching", "question": "What is the recommended depth for applying organic mulch around plants?", "options": {"A": "Less than 1 inch", "B": "1–2 inches", "C": "2–4 inches", "D": "5–6 inches"}, "correct_answer": "C", "tip_id": "tip_008", "difficulty": "easy"},
    {"id": "q011", "topic": "Precision Agriculture", "question": "What does Variable Rate Technology (VRT) do in precision agriculture?", "options": {"A": "Monitors crop diseases via satellite", "B": "Applies inputs like fertilizer only where needed", "C": "Automates the harvesting process", "D": "Controls greenhouse temperature"}, "correct_answer": "B", "tip_id": "tip_015", "difficulty": "hard"},
    {"id": "q012", "topic": "Harvesting", "question": "When is the best time to harvest most vegetables for maximum freshness?", "options": {"A": "At noon when sun is at peak", "B": "In the evening after sunset", "C": "Morning after dew dries", "D": "Any time during the day"}, "correct_answer": "C", "tip_id": "tip_010", "difficulty": "easy"},
    {"id": "q013", "topic": "Water Management", "question": "Which is NOT a sign of overwatering in plants?", "options": {"A": "Yellowing leaves", "B": "Root rot", "C": "Deep root growth", "D": "Mold presence"}, "correct_answer": "C", "tip_id": "tip_011", "difficulty": "medium"},
    {"id": "q014", "topic": "Seed Selection", "question": "What is a key advantage of heirloom seeds over hybrid seeds?", "options": {"A": "Higher yield uniformity", "B": "Resistance to all diseases", "C": "Seeds can be saved and replanted", "D": "They grow faster in all conditions"}, "correct_answer": "C", "tip_id": "tip_005", "difficulty": "medium"},
    {"id": "q015", "topic": "Greenhouse Farming", "question": "What is the most critical factor to prevent humidity-related diseases in a greenhouse?", "options": {"A": "Soil type", "B": "Proper ventilation", "C": "Lighting intensity", "D": "Plant spacing"}, "correct_answer": "B", "tip_id": "tip_013", "difficulty": "medium"},
]


# ─── Helper: get tip content ────────────────────────────
def get_tip_for_question(tip_id: str) -> str:
    for tip in FARMING_TIPS:
        if tip["id"] == tip_id:
            return tip["content"]
    return ""


# ─── API Routes ─────────────────────────────────────────

@app.route("/api/questions", methods=["GET"])
def get_questions():
    """Return random 5 questions, optionally filtered by topic/difficulty."""
    topic = request.args.get("topic")
    difficulty = request.args.get("difficulty")
    count = int(request.args.get("count", 5))

    pool = QUIZ_QUESTIONS.copy()
    if topic:
        pool = [q for q in pool if q["topic"] == topic]
    if difficulty:
        pool = [q for q in pool if q["difficulty"] == difficulty]

    selected = random.sample(pool, min(count, len(pool)))
    # Don't send correct_answer to frontend
    safe = [{k: v for k, v in q.items() if k != "correct_answer"} for q in selected]
    return jsonify({"questions": safe, "total": len(selected)})


@app.route("/api/evaluate", methods=["POST"])
def evaluate_answer():
    """Evaluate a single answer using Groq LLM."""
    data = request.json
    question_id = data.get("question_id")
    user_answer = data.get("answer", "").strip().upper()

    question = next((q for q in QUIZ_QUESTIONS if q["id"] == question_id), None)
    if not question:
        return jsonify({"error": "Question not found"}), 404

    is_correct = user_answer == question["correct_answer"]
    tip_content = get_tip_for_question(question["tip_id"])

    prompt = f"""You are an expert agricultural educator evaluating a student's quiz answer.

QUESTION: {question['question']}
OPTIONS:
A) {question['options']['A']}
B) {question['options']['B']}
C) {question['options']['C']}
D) {question['options']['D']}

CORRECT ANSWER: {question['correct_answer']}) {question['options'][question['correct_answer']]}
STUDENT'S ANSWER: {user_answer}) {question['options'].get(user_answer, 'Invalid')}
RESULT: {"CORRECT" if is_correct else "INCORRECT"}

RELEVANT FARMING TIP: {tip_content}

Provide a response with:
1. {"Brief congratulation and" if is_correct else "Gentle explanation of the mistake and"} why the correct answer is right
2. Real-world farming context (1-2 sentences)
3. A practical tip or memory aid

Keep it under 120 words. Be encouraging and practical."""

    response = groq_client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300,
        temperature=0.7
    )

    explanation = response.choices[0].message.content

    return jsonify({
        "is_correct": is_correct,
        "correct_answer": question["correct_answer"],
        "correct_answer_text": question["options"][question["correct_answer"]],
        "explanation": explanation,
        "topic": question["topic"]
    })


@app.route("/api/session/save", methods=["POST"])
def save_session():
    """Save completed quiz session to Supabase."""
    data = request.json
    player_name = data.get("player_name", "Anonymous")
    score = data.get("score", 0)
    total = data.get("total", 0)
    topic = data.get("topic", "Mixed")
    difficulty = data.get("difficulty", "Mixed")
    wrong_topics = data.get("wrong_topics", [])

    # Generate personalized summary with Groq
    pct = round((score / total) * 100) if total > 0 else 0
    prompt = f"""You are an agricultural education coach. Write a 2-3 sentence personalized summary for a student.

Student: {player_name}
Score: {score}/{total} ({pct}%)
Weak topics: {', '.join(wrong_topics) if wrong_topics else 'None — perfect score!'}

Give warm feedback, mention knowledge gaps if any, and end with a short farming motivational line. Max 60 words."""

    summary_response = groq_client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150,
        temperature=0.8
    )
    summary = summary_response.choices[0].message.content

    # Save to Supabase
    record = {
        "player_name": player_name,
        "score": score,
        "total": total,
        "percentage": pct,
        "topic": topic,
        "difficulty": difficulty,
        "wrong_topics": wrong_topics,
        "summary": summary,
        "played_at": datetime.utcnow().isoformat()
    }
    result = supabase.table("quiz_sessions").insert(record).execute()

    return jsonify({"summary": summary, "saved": True, "id": result.data[0]["id"] if result.data else None})


@app.route("/api/leaderboard", methods=["GET"])
def get_leaderboard():
    """Fetch top scores from Supabase."""
    result = supabase.table("quiz_sessions")\
        .select("player_name, score, total, percentage, topic, played_at")\
        .order("percentage", desc=True)\
        .order("played_at", desc=True)\
        .limit(10)\
        .execute()

    return jsonify({"leaderboard": result.data})


@app.route("/api/topics", methods=["GET"])
def get_topics():
    topics = sorted(list(set(q["topic"] for q in QUIZ_QUESTIONS)))
    return jsonify({"topics": topics})


@app.route("/api/tips", methods=["GET"])
def get_tips():
    return jsonify({"tips": FARMING_TIPS})


@app.route("/api/ask", methods=["POST"])
def ask_question():
    """Free-text Q&A about farming."""
    question = request.json.get("question", "")
    if not question:
        return jsonify({"error": "No question provided"}), 400

    # Find most relevant tips (simple keyword match)
    relevant_tips = []
    q_lower = question.lower()
    for tip in FARMING_TIPS:
        if any(word in tip["content"].lower() or word in tip["topic"].lower()
               for word in q_lower.split() if len(word) > 3):
            relevant_tips.append(tip)
    if not relevant_tips:
        relevant_tips = FARMING_TIPS[:3]
    context = "\n".join([f"[{t['topic']}]: {t['content']}" for t in relevant_tips[:3]])

    response = groq_client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[{
            "role": "system",
            "content": "You are an expert agricultural advisor. Answer farming questions clearly and practically."
        }, {
            "role": "user",
            "content": f"Question: {question}\n\nRelevant knowledge:\n{context}\n\nGive a practical, farmer-friendly answer in 3-4 sentences."
        }],
        max_tokens=250,
        temperature=0.7
    )

    return jsonify({"answer": response.choices[0].message.content})


if __name__ == "__main__":
    app.run(debug=True, port=5000)