"""
General Knowledge content module.

Uses xAI Grok (OpenAI-compatible API) to:
  1. Generate 10 daily GK questions across varied topics.
  2. Power a per-question chat tutor that gives hints without answers.

Supports multiple user profiles so questions and tone match each user's age
and knowledge level.
"""

import json
import re

from openai import OpenAI

# ── xAI Grok configuration ──
XAI_BASE_URL = "https://api.x.ai/v1"
XAI_MODEL = "grok-3-mini"

# ──────────────────────────────────────────────
# User profiles — each defines topics, prompts, and tone
# ──────────────────────────────────────────────

PROFILES = {
    # ── Arjun: 10-year-old kid ──
    "Arjun": {
        "topics": [
            "Science", "Nature", "Animals", "Space", "Geography",
            "History", "Sports", "Inventions", "Food", "Culture",
        ],
        "topic_emojis": {
            "Science": "🔬", "Nature": "🌿", "Animals": "🐾", "Space": "🚀",
            "Geography": "🌍", "History": "📜", "Sports": "⚽", "Inventions": "💡",
            "Food": "🍕", "Culture": "🎭",
        },
        "question_prompt": """\
You are a quiz maker for a 10-year-old student. Generate exactly 10 \
general knowledge multiple-choice questions.

RULES:
- Each question should be from a DIFFERENT topic. Use these topics in order: \
Science, Nature, Animals, Space, Geography, History, Sports, Inventions, Food, Culture.
- Difficulty: easy to medium — fun and educational, NOT intimidating.
- Each question has exactly 4 options.
- The "answer" field is the 0-based index of the correct option.
- Include a short "explanation" (1-2 sentences) that teaches something interesting.
- Questions should be factual and have one clearly correct answer.

Respond with ONLY valid JSON — an array of 10 objects:
[
  {{
    "topic": "Science",
    "question": "What gas do plants breathe in?",
    "options": ["Oxygen", "Carbon Dioxide", "Nitrogen", "Helium"],
    "answer": 1,
    "explanation": "Plants absorb carbon dioxide from the air and use it along with sunlight to make their food through photosynthesis."
  }}
]

Generate 10 NEW, UNIQUE questions now. Respond with ONLY the JSON array.""",
        "tutor_prompt": """\
You are a friendly, encouraging tutor helping a 10-year-old learn. \
The student is working on a general knowledge quiz.

RULES:
- Give helpful HINTS but NEVER reveal the correct answer directly.
- Use simple, clear language a 10-year-old would understand.
- Be encouraging and positive — say things like "Great question!" or "You're on the right track!"
- Keep responses short (2-4 sentences).
- If the student asks you to just tell the answer, gently refuse and offer a hint instead.

You are helping with this question:
Topic: {topic}
Question: {question}
Options: {options}

Help the student think through it without giving away the answer.""",
        "subtitle": "Learn something new every day!",
        "quiz_description": "10 questions across Science, Nature, Space, and more!",
        "color": "#f59e0b",
    },

    # ── Sangeetha: 35-year-old adult, building GK habits ──
    "Sangeetha": {
        "topics": [
            "Health & Wellness", "World Cultures", "Famous People",
            "Everyday Science", "Geography", "History",
            "Movies & Entertainment", "Nature & Environment",
            "Food & Cooking", "Books & Literature",
        ],
        "topic_emojis": {
            "Health & Wellness": "💪", "World Cultures": "🌏", "Famous People": "⭐",
            "Everyday Science": "🔬", "Geography": "🗺️", "History": "📜",
            "Movies & Entertainment": "🎬", "Nature & Environment": "🌿",
            "Food & Cooking": "🍳", "Books & Literature": "📖",
        },
        "question_prompt": """\
You are a friendly quiz creator for an adult who is building a daily general \
knowledge habit. Generate exactly 10 multiple-choice questions.

RULES:
- Each question should be from a DIFFERENT topic. Use these topics in order: \
Health & Wellness, World Cultures, Famous People, Everyday Science, Geography, \
History, Movies & Entertainment, Nature & Environment, Food & Cooking, Books & Literature.
- Difficulty: easy to medium — approachable and interesting, NOT intimidating.
- The goal is to make the quiz feel rewarding and fun, so the person looks \
forward to it every day. Avoid obscure trivia.
- Each question has exactly 4 options.
- The "answer" field is the 0-based index of the correct option.
- Include a short "explanation" (1-2 sentences) with a fascinating fact or context.
- Questions should be factual and have one clearly correct answer.

Respond with ONLY valid JSON — an array of 10 objects:
[
  {{
    "topic": "Health & Wellness",
    "question": "Which vitamin is produced by your body when exposed to sunlight?",
    "options": ["Vitamin A", "Vitamin B12", "Vitamin C", "Vitamin D"],
    "answer": 3,
    "explanation": "Your skin produces Vitamin D when exposed to UV rays from sunlight. It helps keep your bones strong and your immune system healthy."
  }}
]

Generate 10 NEW, UNIQUE questions now. Respond with ONLY the JSON array.""",
        "tutor_prompt": """\
You are a warm, supportive learning companion for an adult who is building \
their general knowledge. They are working on a daily quiz.

RULES:
- Give helpful HINTS but NEVER reveal the correct answer directly.
- Use clear, conversational language — like a knowledgeable friend.
- Be encouraging — say things like "Good thinking!" or "You're close!"
- Keep responses concise (2-4 sentences).
- If asked for the answer directly, kindly nudge them to think it through and offer a hint.

You are helping with this question:
Topic: {topic}
Question: {question}
Options: {options}

Help them reason through it without giving away the answer.""",
        "subtitle": "A little learning every day goes a long way!",
        "quiz_description": "10 questions on Health, Culture, History, and more!",
        "color": "#f093fb",
    },
}

# Fallback profile for unknown users
DEFAULT_PROFILE = "Arjun"


def get_profile(user_name: str) -> dict:
    """Return the GK profile for a user, falling back to default."""
    return PROFILES.get(user_name, PROFILES[DEFAULT_PROFILE])


def _get_client(xai_api_key: str) -> OpenAI:
    """Create an OpenAI client configured for xAI."""
    return OpenAI(api_key=xai_api_key, base_url=XAI_BASE_URL)


def generate_daily_questions(xai_api_key: str, user_name: str = "Arjun") -> list:
    """Generate 10 daily GK questions using xAI Grok.

    Args:
        xai_api_key: xAI API key.
        user_name: Name of the user (determines profile/topics/tone).

    Returns a list of question dicts, each with:
      topic, question, options (list of 4), answer (int), explanation (str)

    Raises ValueError if generation or parsing fails.
    """
    profile = get_profile(user_name)
    client = _get_client(xai_api_key)

    response = client.chat.completions.create(
        model=XAI_MODEL,
        messages=[
            {"role": "system", "content": profile["question_prompt"]},
            {"role": "user", "content": "Generate 10 general knowledge questions for today's quiz."},
        ],
        max_tokens=3000,
        temperature=0.8,
    )

    raw = response.choices[0].message.content.strip()

    # Extract JSON array from response
    json_match = re.search(r"\[[\s\S]*\]", raw)
    if not json_match:
        raise ValueError(f"No JSON array found in response:\n{raw[:500]}")

    questions = json.loads(json_match.group())

    if not isinstance(questions, list) or len(questions) == 0:
        raise ValueError("Expected a non-empty list of questions")

    # Validate each question
    validated = []
    for i, q in enumerate(questions):
        for field in ("topic", "question", "options", "answer"):
            if field not in q:
                raise ValueError(f"Question {i+1} missing field: {field}")
        if not isinstance(q["options"], list) or len(q["options"]) != 4:
            raise ValueError(f"Question {i+1} must have exactly 4 options")
        if not isinstance(q["answer"], int) or q["answer"] not in range(4):
            raise ValueError(f"Question {i+1} has invalid answer index")
        if "explanation" not in q:
            q["explanation"] = ""
        validated.append(q)

    return validated


def chat_with_tutor(
    question: dict,
    user_message: str,
    chat_history: list,
    xai_api_key: str,
    user_name: str = "Arjun",
) -> str:
    """Send a message to the tutor about a specific question.

    Args:
        question: The current question dict (topic, question, options).
        user_message: What the student typed.
        chat_history: List of prior {"role": ..., "content": ...} messages.
        xai_api_key: xAI API key.
        user_name: Name of the user (determines tutor tone).

    Returns:
        The tutor's reply as a string.
    """
    profile = get_profile(user_name)
    client = _get_client(xai_api_key)

    system = profile["tutor_prompt"].format(
        topic=question.get("topic", "General Knowledge"),
        question=question.get("question", ""),
        options=", ".join(question.get("options", [])),
    )

    messages = [{"role": "system", "content": system}]
    messages.extend(chat_history)
    messages.append({"role": "user", "content": user_message})

    response = client.chat.completions.create(
        model=XAI_MODEL,
        messages=messages,
        max_tokens=300,
        temperature=0.7,
    )

    return response.choices[0].message.content.strip()
