"""
Story generation context and LLM integration.

Defines the format rules for "I Can Read Level 1" stories and provides
a function to generate complete stories (text + image prompts + quiz)
from a simple topic using an LLM via the HuggingFace Inference API.
"""

import json
import random
import re
import time

from huggingface_hub import InferenceClient

# ── Palette for randomly assigned book covers ──
COVER_COLORS = [
    "#ef4444", "#f97316", "#eab308", "#22c55e", "#06b6d4",
    "#3b82f6", "#6366f1", "#a855f7", "#ec4899", "#14b8a6",
]

# ── LLM model for text generation ──
TEXT_MODEL = "meta-llama/Llama-3.1-8B-Instruct"

# ── System prompt that defines the story format ──
SYSTEM_PROMPT = """\
You are a children's book author who writes "I Can Read Level 1" stories \
for kids ages 4-6.

RULES for the story:
- Exactly 8 pages.
- Each page has ONE simple sentence (4-8 words maximum).
- Use only common, easy words a 4-year-old knows.
- Use repetitive patterns (e.g. "I see a ___", "The ___ is ___").
- Tell a simple story with a beginning, middle, and happy ending.
- Each page needs a descriptive image_prompt for a cartoon illustrator.
- Each page needs 1-3 fallback_emoji characters that represent the scene.
- Choose a single cover_emoji that best represents the story theme.

RULES for the quiz:
- Exactly 4 multiple-choice questions about the story.
- Each question has exactly 3 options, each option ends with an emoji.
- Questions should be simple recall (who, what, where, how).
- The "answer" field is the 0-based index of the correct option.

Respond with ONLY valid JSON in this exact structure (no other text):
{
  "title": "Story Title",
  "cover_emoji": "🐶",
  "pages": [
    {
      "image_prompt": "a descriptive scene for the cartoon illustrator",
      "fallback_emoji": "🐶🏠",
      "text": "Simple sentence here."
    }
  ],
  "questions": [
    {
      "q": "Simple question?",
      "options": ["Option A 🅰️", "Option B 🅱️", "Option C 🅲️"],
      "answer": 0
    }
  ]
}

FULL EXAMPLE — topic "a puppy at the beach":
{
  "title": "Pup Goes to the Beach",
  "cover_emoji": "🏖️",
  "pages": [
    {"image_prompt": "a cute cartoon puppy riding in a car looking out the window at the ocean", "fallback_emoji": "🐶🚗", "text": "Pup goes to the beach!"},
    {"image_prompt": "a cute cartoon puppy stepping onto golden sand with blue waves behind", "fallback_emoji": "🐶🏖️", "text": "Pup sees the sand."},
    {"image_prompt": "a cute cartoon puppy splashing happily in shallow blue ocean water", "fallback_emoji": "🐶🌊", "text": "Pup runs in the water. Splash!"},
    {"image_prompt": "a cute cartoon puppy digging a hole in the sand at the beach", "fallback_emoji": "🐶⛱️", "text": "Pup digs in the sand."},
    {"image_prompt": "a cute cartoon puppy finding a pretty pink seashell on the beach", "fallback_emoji": "🐶🐚", "text": "Pup finds a shell!"},
    {"image_prompt": "a cute cartoon puppy and a small red crab looking at each other on the beach", "fallback_emoji": "🐶🦀", "text": "Pup meets a crab. Hello!"},
    {"image_prompt": "a cute cartoon puppy eating a treat while sitting on a beach towel", "fallback_emoji": "🐶🍖", "text": "Pup eats a yummy treat."},
    {"image_prompt": "a cute cartoon puppy sleeping on a beach towel at sunset", "fallback_emoji": "🐶😴🌅", "text": "Pup is tired. What a fun day!"}
  ],
  "questions": [
    {"q": "Where does Pup go?", "options": ["The park 🏞️", "The beach 🏖️", "The store 🏪"], "answer": 1},
    {"q": "What does Pup find?", "options": ["A ball ⚽", "A shell 🐚", "A stick 🪵"], "answer": 1},
    {"q": "Who does Pup meet?", "options": ["A cat 🐱", "A bird 🐦", "A crab 🦀"], "answer": 2},
    {"q": "How does Pup feel at the end?", "options": ["Sad 😢", "Tired 😴", "Angry 😠"], "answer": 1}
  ]
}

Now write a NEW story about the topic the user gives you. Respond with ONLY the JSON."""


def generate_story_from_topic(topic: str, hf_token: str) -> dict:
    """Generate a complete story dict from a topic string.

    Uses the HuggingFace Inference API to call an LLM, parses the
    structured JSON response, validates it, and returns a story dict
    that is ready to save and display.

    Raises ``ValueError`` if the LLM response cannot be parsed or
    the story structure is invalid.
    """
    client = InferenceClient(provider="auto", api_key=hf_token)

    response = client.chat_completion(
        model=TEXT_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Write a story about: {topic}"},
        ],
        max_tokens=2000,
        temperature=0.7,
    )

    raw = response.choices[0].message.content.strip()

    # Extract JSON from the response (LLMs sometimes wrap in markdown)
    json_match = re.search(r"\{[\s\S]*\}", raw)
    if not json_match:
        raise ValueError(f"No JSON found in LLM response:\n{raw[:500]}")

    story = json.loads(json_match.group())

    # ── Validate required fields ──
    for field in ("title", "pages", "questions"):
        if field not in story:
            raise ValueError(f"Story missing required field: {field}")

    if not isinstance(story["pages"], list) or len(story["pages"]) == 0:
        raise ValueError("Story must have at least 1 page")

    for i, page in enumerate(story["pages"]):
        for key in ("image_prompt", "fallback_emoji", "text"):
            if key not in page:
                raise ValueError(f"Page {i+1} missing field: {key}")

    if not isinstance(story["questions"], list) or len(story["questions"]) == 0:
        raise ValueError("Story must have at least 1 question")

    for i, q in enumerate(story["questions"]):
        for key in ("q", "options", "answer"):
            if key not in q:
                raise ValueError(f"Question {i+1} missing field: {key}")
        if not isinstance(q["options"], list) or len(q["options"]) < 2:
            raise ValueError(f"Question {i+1} must have at least 2 options")
        if not isinstance(q["answer"], int) or q["answer"] >= len(q["options"]):
            raise ValueError(f"Question {i+1} has invalid answer index")

    # ── Assign generated metadata ──
    story["id"] = f"gen_{int(time.time())}"
    story["color"] = random.choice(COVER_COLORS)
    if "cover_emoji" not in story or not story["cover_emoji"]:
        story["cover_emoji"] = "📖"

    return story
