# 🌾 FarmWise - Agriculture Quiz Bot Web App

A full-stack web application for agricultural education.  
**Stack: Groq (LLaMA 3 LLM) + Supabase (PostgreSQL online DB) + Flask + Vanilla JS**

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        FarmWise Web App                         │
├──────────────┬──────────────────────────┬───────────────────────┤
│   Frontend   │        Backend           │    External Services  │
│  (HTML/CSS/  │      (Flask API)         │                       │
│      JS)     │                          │  🟣 Groq API          │
│              │  /api/questions          │   LLaMA 3 8B (free)   │
│  • Quiz UI   │  /api/evaluate     ────► │   - Answer eval       │
│  • Results   │  /api/session/save       │   - Explanations      │
│  • Leaderbd  │  /api/leaderboard  ────► │   - Summaries         │
│  • Tips      │  /api/topics             │                       │
│  • Ask AI    │  /api/tips               │  🟢 Supabase          │
│              │  /api/ask                │   PostgreSQL (free)   │
│              │                          │   - Sessions stored   │
│              │                          │   - Leaderboard       │
└──────────────┴──────────────────────────┴───────────────────────┘
```

---

## ⚙️ Setup Instructions

### Step 1: Get Free API Keys

**Groq API** (free — fast LLM inference):
1. Go to https://console.groq.com
2. Sign up → API Keys → Create API Key
3. Copy your key

**Supabase** (free online PostgreSQL):
1. Go to https://supabase.com
2. Create a new project (free tier available)
3. Go to **Settings → API**
4. Copy:
   - `Project URL` → `SUPABASE_URL`
   - `anon/public key` → `SUPABASE_ANON_KEY`

---

### Step 2: Create Supabase Database Table

1. In Supabase Dashboard → **SQL Editor** → **New Query**
2. Paste and run the contents of `backend/supabase_migration.sql`

---

### Step 3: Configure Environment Variables

```bash
cd backend
cp .env.example .env
```

Edit `.env`:
```
GROQ_API_KEY=gsk_your_actual_groq_key
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_ANON_KEY=your_anon_key_here
```

---

### Step 4: Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

---

### Step 5: Run the Backend

```bash
python app.py
```

Server starts at: `http://localhost:5000`

---

### Step 6: Open the Frontend

Simply open `frontend/index.html` in your browser.

> **Tip**: Use VS Code's Live Server extension, or run:
> ```bash
> cd frontend
> python -m http.server 3000
> ```
> Then visit `http://localhost:3000`

---

## 📁 File Structure

```
agri_quiz_webapp/
├── backend/
│   ├── app.py                  ← Flask API (Groq + Supabase)
│   ├── requirements.txt
│   ├── .env.example
│   └── supabase_migration.sql  ← Run this in Supabase SQL Editor
└── frontend/
    └── index.html              ← Full SPA (no build step needed)
```

---

## 🎮 Features

| Feature | Tech | Details |
|---|---|---|
| MCQ Quiz | Flask + JS | 15 questions, 3 difficulties |
| AI Evaluation | Groq (LLaMA 3 8B) | Real-time answer feedback |
| Explanations | Groq | Deep contextual farming tips |
| Personalized Summary | Groq | End-of-quiz AI coaching |
| Score Persistence | Supabase | PostgreSQL in the cloud |
| Leaderboard | Supabase | Top 10 scores, real-time |
| Ask AI | Groq | Free-text farming Q&A |
| Topic Filtering | Flask | Filter by topic/difficulty |

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/questions` | Get quiz questions (`?count=5&topic=X&difficulty=easy`) |
| POST | `/api/evaluate` | Evaluate an answer with Groq AI |
| POST | `/api/session/save` | Save session to Supabase |
| GET | `/api/leaderboard` | Top 10 scores from Supabase |
| GET | `/api/topics` | List all available topics |
| GET | `/api/tips` | All farming tips |
| POST | `/api/ask` | Free-text Q&A with Groq |

---

## 📄 Supabase Table Schema

```sql
quiz_sessions (
  id UUID PRIMARY KEY,
  player_name TEXT,
  score INTEGER,
  total INTEGER,
  percentage INTEGER,
  topic TEXT,
  difficulty TEXT,
  wrong_topics TEXT[],
  summary TEXT,
  played_at TIMESTAMPTZ
)
```
