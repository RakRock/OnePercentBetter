"""
Problem Solver content module for Arjun.

Uses xAI Grok to generate real-world scenarios that teach structured
problem-solving through a 6-step breakdown, each presented as a
multiple-choice question.
"""

import json
import re

from openai import OpenAI

XAI_BASE_URL = "https://api.x.ai/v1"
XAI_MODEL = "grok-3-mini"

CATEGORIES = {
    "planning": {
        "name": "Planning Events",
        "emoji": "🎪",
        "color": "#f59e0b",
        "examples": "school fair, birthday party, camping trip, talent show",
    },
    "building": {
        "name": "Building Things",
        "emoji": "🔧",
        "color": "#3b82f6",
        "examples": "design a board game, build a treehouse, create a school newspaper",
    },
    "how_it_works": {
        "name": "How Things Work",
        "emoji": "⚙️",
        "color": "#8b5cf6",
        "examples": "food delivery service, airport operations, library system",
    },
    "everyday": {
        "name": "Solving Everyday Problems",
        "emoji": "💡",
        "color": "#10b981",
        "examples": "reduce lunch line wait, organize a messy room, plan a road trip",
    },
    "community": {
        "name": "Community Projects",
        "emoji": "🤝",
        "color": "#ec4899",
        "examples": "neighborhood cleanup, fundraiser, school garden",
    },
}

STEP_FRAMEWORK = [
    {"name": "Understand the Goal", "icon": "🎯", "description": "What is the main goal or problem?"},
    {"name": "Identify Key Areas", "icon": "🔍", "description": "What are the important areas to think about?"},
    {"name": "Break It Down", "icon": "🧩", "description": "How can we split this into smaller tasks?"},
    {"name": "Prioritize", "icon": "📋", "description": "What should we tackle first?"},
    {"name": "Think About Risks", "icon": "⚠️", "description": "What could go wrong and how do we handle it?"},
    {"name": "Put It Together", "icon": "✅", "description": "Combine everything into a clear plan."},
]

_SYSTEM_PROMPT = """\
You are a problem-solving coach for an 11-year-old student named Arjun. \
Your job is to create a real-world scenario and guide the student through \
breaking it down step by step using multiple-choice questions.

RULES:
- The scenario must be age-appropriate, relatable, and fun for an 11-year-old.
- Difficulty: medium — make the student think, but keep it approachable.
- Generate EXACTLY 6 steps following this framework:
  Step 1: Understand the Goal — What is the main goal or problem?
  Step 2: Identify Key Areas — What are the important areas to think about?
  Step 3: Break It Down — How can we split this into smaller tasks?
  Step 4: Prioritize — What should we tackle first?
  Step 5: Think About Risks — What could go wrong and how do we handle it?
  Step 6: Put It Together — Combine everything into a clear plan.
- Each step MUST have exactly 4 options and 1 correct answer.
- The "answer" field is the 0-based index of the correct option.
- Explanations should teach WHY the approach works — help the student learn \
the thinking process, not just memorize answers.
- Keep language simple and encouraging.

Respond with ONLY valid JSON in this exact structure:
{{
  "title": "Planning a School Science Fair",
  "description": "Your school principal just announced that your class will \
organize this year's science fair! You've been chosen as the lead organizer. \
How would you plan this event from start to finish?",
  "category": "Planning Events",
  "steps": [
    {{
      "step_name": "Understand the Goal",
      "step_icon": "🎯",
      "question": "What is the MAIN goal you need to focus on?",
      "options": [
        "Make sure every student wins a prize",
        "Organize a fun and educational science fair that runs smoothly",
        "Spend as little money as possible",
        "Finish planning in one day"
      ],
      "answer": 1,
      "explanation": "The main goal is to create an event that is both fun \
AND educational while running smoothly. Focusing too narrowly on cost or \
speed misses the bigger picture."
    }}
  ]
}}

Generate EXACTLY 6 steps. Respond with ONLY the JSON object."""


def _get_client(xai_api_key: str) -> OpenAI:
    return OpenAI(api_key=xai_api_key, base_url=XAI_BASE_URL)


def generate_scenario(xai_api_key: str, category: str | None = None) -> dict:
    """Generate a complete problem-solving scenario with 6 MCQ steps.

    Args:
        xai_api_key: xAI API key.
        category: Optional category key from CATEGORIES. If None, AI picks one.

    Returns a dict with: title, description, category, steps (list of 6).
    Raises ValueError if generation or parsing fails.
    """
    client = _get_client(xai_api_key)

    if category and category in CATEGORIES:
        cat_info = CATEGORIES[category]
        user_msg = (
            f"Generate a problem-solving scenario in the category "
            f'"{cat_info["name"]}". Example scenarios: {cat_info["examples"]}. '
            f"Pick something creative and different from the examples."
        )
    else:
        user_msg = (
            "Generate a fun, creative problem-solving scenario for an 11-year-old. "
            "Pick from any of these categories: Planning Events, Building Things, "
            "How Things Work, Solving Everyday Problems, Community Projects."
        )

    response = client.chat.completions.create(
        model=XAI_MODEL,
        messages=[
            {"role": "system", "content": _SYSTEM_PROMPT},
            {"role": "user", "content": user_msg},
        ],
        max_tokens=3000,
        temperature=0.85,
    )

    raw = response.choices[0].message.content.strip()

    json_match = re.search(r"\{[\s\S]*\}", raw)
    if not json_match:
        raise ValueError(f"No JSON object found in response:\n{raw[:500]}")

    scenario = json.loads(json_match.group())

    for field in ("title", "description", "steps"):
        if field not in scenario:
            raise ValueError(f"Missing required field: {field}")

    steps = scenario["steps"]
    if not isinstance(steps, list) or len(steps) < 6:
        raise ValueError(f"Expected 6 steps, got {len(steps) if isinstance(steps, list) else 'non-list'}")

    steps = steps[:6]
    for i, step in enumerate(steps):
        for f in ("question", "options", "answer", "explanation"):
            if f not in step:
                raise ValueError(f"Step {i + 1} missing field: {f}")
        if not isinstance(step["options"], list) or len(step["options"]) != 4:
            raise ValueError(f"Step {i + 1} must have exactly 4 options")
        if not isinstance(step["answer"], int) or step["answer"] not in range(4):
            raise ValueError(f"Step {i + 1} has invalid answer index")
        if "step_name" not in step:
            step["step_name"] = STEP_FRAMEWORK[i]["name"]
        if "step_icon" not in step:
            step["step_icon"] = STEP_FRAMEWORK[i]["icon"]

    scenario["steps"] = steps
    if "category" not in scenario:
        scenario["category"] = "General"

    return scenario
