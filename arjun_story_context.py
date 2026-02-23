"""
Factual story generation for Arjun (age 11).

Uses xAI Grok to create 7-8 page stories based on real-world events,
places, scientific discoveries, and sports milestones. Each story is
followed by 10 comprehension questions.

Stories are educational narratives written at an easy-to-medium vocabulary
level appropriate for an 11-year-old.
"""

import json
import random
import re
import time

from openai import OpenAI

XAI_BASE_URL = "https://api.x.ai/v1"
XAI_MODEL = "grok-3-mini"

COVER_COLORS = [
    "#ef4444", "#f97316", "#eab308", "#22c55e", "#06b6d4",
    "#3b82f6", "#6366f1", "#a855f7", "#ec4899", "#14b8a6",
]

# ── Curated topic pool across categories ──

TOPIC_POOL = {
    "Science": [
        "The Moon Landing — Apollo 11",
        "How Electricity Was Discovered — Benjamin Franklin and Thomas Edison",
        "What Happened to the Dinosaurs — The Great Extinction",
        "The Hubble Space Telescope — Eyes in the Sky",
        "How Vaccines Were Invented — Edward Jenner and Smallpox",
        "The Discovery of Gravity — Isaac Newton and the Apple",
        "Marie Curie and the Discovery of Radioactivity",
        "The Journey of Voyager 1 — Farthest Spacecraft from Earth",
        "Charles Darwin and the Theory of Evolution",
        "The International Space Station — Living in Space",
    ],
    "Social Science": [
        "Ancient Egypt and the Pyramids of Giza",
        "The Silk Road — Trade Route That Connected the World",
        "India's Independence — The Story of Mahatma Gandhi",
        "The American Revolution and the Boston Tea Party",
        "Nelson Mandela and the End of Apartheid",
        "The French Revolution — Liberty, Equality, Fraternity",
        "The Berlin Wall — A City Divided and Reunited",
        "The Renaissance — When Art and Science Flourished",
    ],
    "Places": [
        "The Great Wall of China — The Longest Wall Ever Built",
        "The Amazon Rainforest — Lungs of the Earth",
        "Antarctica — The Coldest Continent on Earth",
        "Machu Picchu — The Lost City of the Incas",
        "The Great Barrier Reef — World's Largest Living Structure",
        "Mount Everest — The Roof of the World",
        "The Sahara Desert — Largest Hot Desert on Earth",
        "The Galápagos Islands — Darwin's Living Laboratory",
    ],
    "Sports": [
        "The First Modern Olympics — Athens 1896",
        "Jesse Owens at the 1936 Berlin Olympics",
        "Sachin Tendulkar — The God of Cricket",
        "The Miracle on Ice — 1980 US Hockey Team",
        "Usain Bolt — The Fastest Man in History",
        "The Story of the FIFA World Cup",
        "Nadia Comăneci — The First Perfect 10 in Gymnastics",
        "Michael Jordan — The Legend of Basketball",
    ],
    "Events": [
        "The Wright Brothers — The First Flight at Kitty Hawk",
        "The Titanic — The Ship That Could Not Sink",
        "The Invention of the Internet — How the World Got Connected",
        "The First Telephone Call — Alexander Graham Bell",
        "The Discovery of Penicillin — Alexander Fleming's Lucky Accident",
        "The Rosetta Stone — Unlocking Ancient Egyptian Writing",
        "The Fall of the Roman Empire",
        "The Story of the Printing Press — Johannes Gutenberg",
    ],
}

TOPIC_EMOJIS = {
    "Science": "🔬",
    "Social Science": "📜",
    "Places": "🌍",
    "Sports": "🏅",
    "Events": "⚡",
    "Current Events": "📰",
}

# Prompt used to fetch fresh, kid-appropriate current event topics from Grok
_CURRENT_EVENTS_PROMPT = """\
Suggest exactly 6 kid-appropriate current event topics (year 2025-2026) that \
an 11-year-old would find interesting. These should be REAL recent events or \
developments — things happening in the world right now.

Good categories: space missions, science breakthroughs, sports tournaments, \
Olympic games, technology milestones, environmental events, world records, \
new discoveries, cultural events.

BAD topics (avoid): war, violence, politics, crime, disasters with casualties.

Return ONLY a JSON array of 6 strings, each in the format:
"Short Title — Brief Description"

Example:
["Winter Olympics 2026 — The Winter Games in Milan-Cortina, Italy", ...]

Return ONLY the JSON array, nothing else."""

SYSTEM_PROMPT = """\
You are an educational storyteller who writes engaging, factual stories for \
an 11-year-old reader. Your stories are based on REAL historical events, \
scientific discoveries, famous places, or sports milestones.

RULES for the story:
- Exactly 8 pages (you may use 7 if the story wraps up naturally).
- Each page MUST have 4-5 well-written sentences that form a proper paragraph, \
like a page from a real chapter book. Each sentence should flow into the next. \
Use easy-to-medium vocabulary appropriate for an 11-year-old. No baby language, \
but no complex jargon either.
- The story MUST be based on REAL facts. Do not invent fictional characters \
or events. Use the actual names of people, places, and dates.
- Tell the story as an engaging narrative — like a documentary turned into a \
chapter book. Include interesting details and lesser-known facts.
- Each page should read like a proper book paragraph — NOT like a list of \
facts. Use narrative transitions between sentences ("Meanwhile...", \
"As the days passed...", "Back on Earth...", etc.).
- Each page needs a descriptive image_prompt for an illustrator (realistic \
style, educational, colorful, no text in image).
- Each page needs 1-3 fallback_emoji characters that represent the scene.
- Choose a single cover_emoji that best represents the story theme.

RULES for the quiz:
- Exactly 10 multiple-choice questions about the story AND the real-world \
facts mentioned.
- Each question has exactly 4 options.
- Mix question types: some recall from the story, some factual knowledge, \
some inference/reasoning.
- The "answer" field is the 0-based index of the correct option.
- Questions should reinforce learning — test whether the reader absorbed \
the key facts.

Respond with ONLY valid JSON in this exact structure (no other text):
{
  "title": "Story Title",
  "cover_emoji": "🚀",
  "topic_category": "Science",
  "pages": [
    {
      "image_prompt": "a descriptive scene for the illustrator",
      "fallback_emoji": "🚀🌙",
      "text": "It was a warm July morning in 1969 when three astronauts climbed into their spacecraft at Kennedy Space Center in Florida. Neil Armstrong, Buzz Aldrin, and Michael Collins had trained for years for this moment. The massive Saturn V rocket stood 363 feet tall — taller than the Statue of Liberty. As the countdown reached zero, flames erupted beneath the rocket and it slowly rose into the sky. Millions of people around the world held their breath, watching on television as the rocket disappeared into the clouds."
    }
  ],
  "questions": [
    {
      "q": "What year did this event happen?",
      "options": ["1965", "1969", "1972", "1975"],
      "answer": 1
    }
  ]
}

Now write a NEW factual story about the topic the user gives you. \
Respond with ONLY the JSON."""


def get_random_topic() -> tuple[str, str]:
    """Pick a random topic. Returns (category, topic_string)."""
    category = random.choice(list(TOPIC_POOL.keys()))
    topic = random.choice(TOPIC_POOL[category])
    return category, topic


def get_all_topics() -> dict[str, list[str]]:
    """Return the full topic pool (static categories only)."""
    return TOPIC_POOL


def fetch_current_events(xai_api_key: str) -> list[str]:
    """Ask Grok for 6 kid-appropriate current event topics.

    Returns a list of topic strings. Falls back to an empty list on failure.
    """
    try:
        client = OpenAI(api_key=xai_api_key, base_url=XAI_BASE_URL)
        response = client.chat.completions.create(
            model=XAI_MODEL,
            messages=[
                {"role": "system", "content": _CURRENT_EVENTS_PROMPT},
                {"role": "user", "content": "Give me 6 current event topics for kids."},
            ],
            max_tokens=800,
            temperature=0.8,
        )
        raw = response.choices[0].message.content.strip()
        json_match = re.search(r"\[[\s\S]*\]", raw)
        if json_match:
            topics = json.loads(json_match.group())
            if isinstance(topics, list) and len(topics) >= 1:
                return [str(t) for t in topics[:6]]
    except Exception:
        pass
    return []


def generate_arjun_story(xai_api_key: str, topic: str | None = None) -> dict:
    """Generate a factual story for Arjun using xAI Grok.

    Args:
        xai_api_key: xAI API key.
        topic: Topic string. If None, picks a random one from the pool.

    Returns a story dict ready for save_generated_story().
    Raises ValueError on generation/parsing failure.
    """
    if not topic:
        _, topic = get_random_topic()

    client = OpenAI(api_key=xai_api_key, base_url=XAI_BASE_URL)

    response = client.chat.completions.create(
        model=XAI_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Write a factual story about: {topic}"},
        ],
        max_tokens=5000,
        temperature=0.7,
    )

    raw = response.choices[0].message.content.strip()

    json_match = re.search(r"\{[\s\S]*\}", raw)
    if not json_match:
        raise ValueError(f"No JSON found in response:\n{raw[:500]}")

    story = json.loads(json_match.group())

    for field in ("title", "pages", "questions"):
        if field not in story:
            raise ValueError(f"Story missing required field: {field}")

    if not isinstance(story["pages"], list) or len(story["pages"]) < 7:
        raise ValueError(f"Story must have 7-8 pages, got {len(story.get('pages', []))}")

    for i, page in enumerate(story["pages"]):
        for key in ("image_prompt", "fallback_emoji", "text"):
            if key not in page:
                raise ValueError(f"Page {i+1} missing field: {key}")

    if not isinstance(story["questions"], list) or len(story["questions"]) < 10:
        raise ValueError(f"Story must have 10 questions, got {len(story.get('questions', []))}")

    for i, q in enumerate(story["questions"]):
        for key in ("q", "options", "answer"):
            if key not in q:
                raise ValueError(f"Question {i+1} missing field: {key}")
        if not isinstance(q["options"], list) or len(q["options"]) != 4:
            raise ValueError(f"Question {i+1} must have exactly 4 options")
        if not isinstance(q["answer"], int) or q["answer"] >= len(q["options"]):
            raise ValueError(f"Question {i+1} has invalid answer index")

    story["id"] = f"gen_arjun_{int(time.time())}"
    story["color"] = random.choice(COVER_COLORS)
    if "cover_emoji" not in story or not story["cover_emoji"]:
        story["cover_emoji"] = "📖"
    if "topic_category" not in story:
        story["topic_category"] = "General"

    return story
