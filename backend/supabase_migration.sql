-- Run this in your Supabase SQL Editor (Dashboard → SQL Editor → New query)

CREATE TABLE IF NOT EXISTS quiz_sessions (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    player_name TEXT NOT NULL DEFAULT 'Anonymous',
    score       INTEGER NOT NULL,
    total       INTEGER NOT NULL,
    percentage  INTEGER NOT NULL,
    topic       TEXT DEFAULT 'Mixed',
    difficulty  TEXT DEFAULT 'Mixed',
    wrong_topics TEXT[] DEFAULT '{}',
    summary     TEXT,
    played_at   TIMESTAMPTZ DEFAULT NOW()
);

-- Enable Row Level Security (optional but recommended)
ALTER TABLE quiz_sessions ENABLE ROW LEVEL SECURITY;

-- Allow public read (for leaderboard)
CREATE POLICY "Public read" ON quiz_sessions FOR SELECT USING (true);

-- Allow public insert (for saving sessions)
CREATE POLICY "Public insert" ON quiz_sessions FOR INSERT WITH CHECK (true);
