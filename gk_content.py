"""
General Knowledge content module.

Uses xAI Grok (OpenAI-compatible API) to:
  1. Generate daily GK questions across varied topics (count depends on profile).
  2. Power a per-question chat tutor that gives hints without answers.

Supports multiple user profiles so questions and tone match each user's age
and knowledge level.
"""

import difflib
import json
import random
import re
from datetime import date

from openai import OpenAI

# ── xAI Grok configuration ──
XAI_BASE_URL = "https://api.x.ai/v1"
XAI_MODEL = "grok-3-mini"

# Post-generation diversity checks (pairwise question text)
_DIVERSITY_MAX_PAIR_SIMILARITY = 0.76
_DIVERSITY_MAX_ADJACENT_SIMILARITY = 0.70
_DIVERSITY_OPENING_WORDS = 5
_DIVERSITY_MIN_ANSWER_LEN_FOR_UNIQUENESS = 5
_DIVERSITY_GENERATION_RETRIES = 3

# ──────────────────────────────────────────────
# User profiles — each defines topics, prompts, and tone
# ──────────────────────────────────────────────

PROFILES = {
    # ── Arjun: 11-year-old kid ──
    "Arjun": {
        "topics": [
            "Science", "Nature", "Animals", "Space", "Geography",
            "History", "Sports", "Inventions", "Food", "Culture",
            "Human Body", "Oceans & Marine Life", "Weather & Climate",
            "World Records", "Famous People", "Countries & Flags",
            "Dinosaurs & Fossils", "Music & Instruments", "Math Fun Facts",
            "Computers & Technology", "Languages of the World", "Mythology",
            "Olympics", "Wonders of the World", "Volcanoes & Earthquakes",
        ],
        "topic_emojis": {
            "Science": "🔬", "Nature": "🌿", "Animals": "🐾", "Space": "🚀",
            "Geography": "🌍", "History": "📜", "Sports": "⚽", "Inventions": "💡",
            "Food": "🍕", "Culture": "🎭", "Human Body": "🫀",
            "Oceans & Marine Life": "🐳", "Weather & Climate": "🌦️",
            "World Records": "🏆", "Famous People": "👤",
            "Countries & Flags": "🏳️", "Dinosaurs & Fossils": "🦕",
            "Music & Instruments": "🎵", "Math Fun Facts": "🔢",
            "Computers & Technology": "💻", "Languages of the World": "🗣️",
            "Mythology": "⚡", "Olympics": "🥇",
            "Wonders of the World": "🏛️", "Volcanoes & Earthquakes": "🌋",
        },
        "question_prompt": """\
You are a quiz maker for an 11-year-old student. Generate exactly 15 \
general knowledge multiple-choice questions.

TOPICS (one question per topic — use 15 DIFFERENT topics, no repeats):
Pick 15 topics randomly from this list (shuffle order — not alphabetical): \
Science, Nature, Animals, Space, Geography, History, Sports, Inventions, \
Food, Culture, Human Body, Oceans & Marine Life, Weather & Climate, World Records, \
Famous People, Countries & Flags, Dinosaurs & Fossils, Music & Instruments, \
Math Fun Facts, Computers & Technology, Languages of the World, Mythology, Olympics, \
Wonders of the World, Volcanoes & Earthquakes.

DIFFICULTY: medium — fun and educational, not too easy and not too hard.

UNIQUENESS — this is mandatory for the whole quiz:
- No two questions may test the same fact, the same answer, the same famous person, \
the same country/city, the same animal species, or the same invention/device.
- "Different topic" is NOT enough: two questions must not feel like the same template. \
Do NOT place similar patterns next to each other (e.g. avoid back-to-back "What is the \
capital of ___" or back-to-back "Which planet ___"). Mix question shapes across the list.
- Vary HOW you ask: use a mix of styles such as Which / Who / What does X mean / \
In which country / Which of these is NOT / What happens when / About how many / \
Which invention helped — not only "What is...".
- For broad topics (e.g. Science), use DIFFERENT sub-areas within that one question \
(life vs physical vs earth vs materials — not two questions about the same sub-area).
- Avoid stuffing the quiz with the same kind of superlative ("largest", "longest", \
"highest", "fastest") — at most two such questions in all 15.
- Skip tired one-line clichés unless the angle is fresh; do not lean on the same \
small set of "famous quiz answers" repeated across quizzes.

FORMAT:
- Each question has exactly 4 options.
- The "answer" field is the 0-based index of the correct option.
- Include a short "explanation" (1-2 sentences) that teaches something interesting.
- Questions should be factual and have one clearly correct answer.

Before you output JSON, verify all 15 questions are pairwise distinct in subject matter \
and in question wording.

Respond with ONLY valid JSON — an array of 15 objects:
[
  {{
    "topic": "Science",
    "question": "What gas do plants breathe in?",
    "options": ["Oxygen", "Carbon Dioxide", "Nitrogen", "Helium"],
    "answer": 1,
    "explanation": "Plants absorb carbon dioxide from the air and use it along with sunlight to make their food through photosynthesis."
  }}
]

Generate 15 NEW, UNIQUE questions now. Respond with ONLY the JSON array.""",
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
        "quiz_description": "15 questions from 25 topics — Science, Space, History, Sports, Dinosaurs, Olympics, and more!",
        "color": "#f59e0b",
        "strict_diversity_post_checks": True,
        "diversity_hint_pool": [
            "This session: lean toward real-world uses and 'how it works', not just names and dates.",
            "Include at least one question about a habitat or ecosystem (not just an animal fact).",
            "Include at least one question where the interesting part is a number, distance, or time span.",
            "Favor lesser-known but kid-appropriate facts over the same famous examples everyone uses.",
            "Ensure Geography and History questions refer to different regions/eras — no duplicate area.",
            "Mix at least one 'Which is NOT true' or 'Which does not belong' style (still one clear answer).",
            "Include one question inspired by everyday experience (kitchen, weather, sports match, phone/map).",
            "Avoid repeating the same opening word for more than two questions in a row (e.g. not all 'What...').",
            "For Space, ask about missions, phases, or distances — not only planet names.",
            "For Sports/Olympics, vary between rules, venues, symbols, and records — not only medal counts.",
            "Use diverse countries and continents across Geography / Culture / Flags — not Europe-only.",
            "Pull one question from a niche angle within a topic (e.g. a festival, a tool, a material).",
        ],
    },

    # ── Sangeetha: 35-year-old adult, building GK habits (India focus) ──
    "Sangeetha": {
        "topics": [
            "States & Capitals", "Languages of India", "Rivers of India",
            "South Indian Rivers", "Mountains & Ranges", "Seas & Coasts",
            "Historical Places", "National Monuments", "Famous Landmarks",
            "Indian Culture & Festivals", "Freedom Struggle", "Important Cities",
        ],
        "topic_emojis": {
            "States & Capitals": "🏛️", "Languages of India": "🗣️",
            "Rivers of India": "🏞️", "South Indian Rivers": "🌊",
            "Mountains & Ranges": "🏔️", "Seas & Coasts": "🌊",
            "Historical Places": "🕌", "National Monuments": "🏗️",
            "Famous Landmarks": "🗺️", "Indian Culture & Festivals": "🪔",
            "Freedom Struggle": "🇮🇳", "Important Cities": "🏙️",
        },
        "question_prompt": """\
You are a friendly quiz creator for an Indian adult who is building a daily \
general knowledge habit. Generate exactly 10 multiple-choice questions — \
ALL questions must be about INDIA.

RULES:
- Each question should be from a DIFFERENT topic. Pick 10 topics from this list: \
States & Capitals, Languages of India, Rivers of India, South Indian Rivers, \
Mountains & Ranges, Seas & Coasts, Historical Places, National Monuments, \
Famous Landmarks, Indian Culture & Festivals, Freedom Struggle, Important Cities.
- EVERY quiz MUST include at least ONE question on National Monuments and at least \
ONE question on South Indian Rivers.
- Difficulty: easy to medium — approachable and interesting, NOT intimidating.
- The goal is to make the quiz feel rewarding and fun, encouraging daily practice. \
Avoid obscure trivia. Stick to well-known facts about India.
- Each question has exactly 4 options.
- The "answer" field is the 0-based index of the correct option.
- Include a short "explanation" (1-2 sentences) with an interesting fact about India.
- Questions should be factual and have one clearly correct answer.

NATIONAL MONUMENTS — use questions about these and similar places:
India Gate, Qutub Minar, Red Fort, Taj Mahal, Sanchi Stupa, Gateway of India, \
Charminar, Hawa Mahal, Victoria Memorial, Konark Sun Temple, Brihadeeswarar Temple, \
Meenakshi Amman Temple, Hampi ruins, Ajanta & Ellora Caves, Khajuraho temples, \
Fatehpur Sikri, Jantar Mantar, Buland Darwaza, Golconda Fort, Mysore Palace, \
Rashtrapati Bhavan, Parliament House, Cellular Jail (Andaman).

SOUTH INDIAN RIVERS — use questions about these:
Kaveri (Cauvery), Tungabhadra, Vaigai, Periyar, Pamba, Bharathappuzha (Nila), \
Chaliyar, Krishna (in AP/Telangana/Karnataka), Godavari (in Telangana/AP), \
Pennar, Chitravathi, Hemavathi, Kabini, Arkavathi, Nethravathi, Sharavathi, \
Moyar, Amaravathi, Tamiraparani, Bhavani.
Include the state(s) they flow through in the explanation.

EXAMPLE TOPICS:
- Which state has X as its capital?
- Which language is the official language of X state?
- Which river flows through X city / originates in X?
- Which South Indian river is a tributary of X?
- Which mountain range is in X region?
- Which sea borders X coast of India?
- Which national monument was built by X ruler?
- In which city is the X monument located?
- Which freedom fighter is known for X?
- Which festival is celebrated for X reason?

IMPORTANT: Each question MUST include BOTH fields:
1. "location" — a specific place name in India related to the question \
(city, monument, river, mountain, etc.). This is used to show the location on a map.
2. "state" — the Indian state where the location is situated (e.g. "Karnataka", \
"Tamil Nadu"). For rivers spanning multiple states, use the most relevant state.

Respond with ONLY valid JSON — an array of 10 objects:
[
  {{
    "topic": "States & Capitals",
    "question": "What is the capital of Karnataka?",
    "options": ["Chennai", "Bengaluru", "Hyderabad", "Mumbai"],
    "answer": 1,
    "explanation": "Bengaluru (formerly Bangalore) is the capital of Karnataka and is known as the Silicon Valley of India.",
    "location": "Bengaluru",
    "state": "Karnataka"
  }}
]

Generate 10 NEW, UNIQUE questions now. Respond with ONLY the JSON array.""",
        "tutor_prompt": """\
You are a warm, supportive learning companion for an Indian adult who is \
building their general knowledge about India. They are working on a daily quiz.

RULES:
- Give helpful HINTS but NEVER reveal the correct answer directly.
- Use clear, conversational language — like a knowledgeable friend.
- You can reference Indian geography, history, and culture to give context.
- Be encouraging — say things like "Good thinking!" or "You're close!"
- Keep responses concise (2-4 sentences).
- If asked for the answer directly, kindly nudge them to think it through and offer a hint.

You are helping with this question:
Topic: {topic}
Question: {question}
Options: {options}

Help them reason through it without giving away the answer.""",
        "subtitle": "Discover India, one question at a time!",
        "quiz_description": "10 questions — states, monuments, rivers, landmarks & more!",
        "color": "#f093fb",
        "has_map": True,
        "strict_diversity_post_checks": False,
    },
    # ── Rakesh: 37-year-old adult, building GK habits (United States focus) ──
    "Rakesh": {
        "topics": [
            "States & Capitals", "US Presidents", "National Parks",
            "Rivers & Lakes", "Mountains & Landscapes", "National Monuments",
            "Famous Landmarks", "American History", "Space & NASA",
            "Sports & Culture", "Inventions & Tech", "Important Cities",
        ],
        "topic_emojis": {
            "States & Capitals": "🏛️", "US Presidents": "🇺🇸",
            "National Parks": "🏕️", "Rivers & Lakes": "🏞️",
            "Mountains & Landscapes": "🏔️", "National Monuments": "🗽",
            "Famous Landmarks": "🗺️", "American History": "📜",
            "Space & NASA": "🚀", "Sports & Culture": "🏈",
            "Inventions & Tech": "💡", "Important Cities": "🏙️",
        },
        "question_prompt": """\
You are a friendly quiz creator for an adult who is building a daily \
general knowledge habit. Generate exactly 10 multiple-choice questions — \
ALL questions must be about the UNITED STATES.

RULES:
- Each question should be from a DIFFERENT topic. Pick 10 topics from this list: \
States & Capitals, US Presidents, National Parks, Rivers & Lakes, \
Mountains & Landscapes, National Monuments, Famous Landmarks, \
American History, Space & NASA, Sports & Culture, Inventions & Tech, Important Cities.
- EVERY quiz MUST include at least ONE question on National Monuments and at least \
ONE question on National Parks.
- Difficulty: easy to medium — approachable and interesting, NOT intimidating.
- The goal is to make the quiz feel rewarding and fun, encouraging daily practice. \
Avoid obscure trivia. Stick to well-known facts about the US.
- Each question has exactly 4 options.
- The "answer" field is the 0-based index of the correct option.
- Include a short "explanation" (1-2 sentences) with an interesting fact about the US.
- Questions should be factual and have one clearly correct answer.

NATIONAL MONUMENTS & LANDMARKS — use questions about these and similar places:
Statue of Liberty, Golden Gate Bridge, White House, Capitol Building, Lincoln Memorial, \
Mount Rushmore, Grand Canyon, Yellowstone, Niagara Falls, Kennedy Space Center, \
Hollywood Sign, Times Square, Alcatraz, Independence Hall, Liberty Bell, \
Gateway Arch, Space Needle, Pearl Harbor, Hoover Dam.

NATIONAL PARKS — use questions about these:
Yellowstone, Yosemite, Grand Canyon, Zion, Glacier, Everglades, Acadia, \
Rocky Mountain, Great Smoky Mountains, Arches, Bryce Canyon, Crater Lake, \
Grand Teton, Olympic, Badlands, Denali, Big Bend.

EXAMPLE TOPICS:
- Which state has X as its capital?
- Which US president is known for X?
- Which national park is located in X state?
- Which river flows through X city?
- Which mountain range is in X region?
- Which landmark was built in X year?
- Which city is known as X?
- In which state is X located?
- Which invention came from X?
- Which team plays in X city?

IMPORTANT: Each question MUST include BOTH fields:
1. "location" — a specific place name in the US related to the question \
(city, monument, river, park, etc.). This is used to show the location on a map.
2. "state" — the US state where the location is situated (e.g. "California", \
"New York"). For DC use "District of Columbia".

Respond with ONLY valid JSON — an array of 10 objects:
[
  {{
    "topic": "States & Capitals",
    "question": "What is the capital of California?",
    "options": ["Los Angeles", "San Francisco", "Sacramento", "San Diego"],
    "answer": 2,
    "explanation": "Sacramento has been the capital of California since 1854. It's located in the Central Valley.",
    "location": "Sacramento",
    "state": "California"
  }}
]

Generate 10 NEW, UNIQUE questions now. Respond with ONLY the JSON array.""",
        "tutor_prompt": """\
You are a warm, supportive learning companion for an adult who is \
building their general knowledge about the United States. They are working on a daily quiz.

RULES:
- Give helpful HINTS but NEVER reveal the correct answer directly.
- Use clear, conversational language — like a knowledgeable friend.
- You can reference US geography, history, and culture to give context.
- Be encouraging — say things like "Good thinking!" or "You're close!"
- Keep responses concise (2-4 sentences).
- If asked for the answer directly, kindly nudge them to think it through and offer a hint.

You are helping with this question:
Topic: {topic}
Question: {question}
Options: {options}

Help them reason through it without giving away the answer.""",
        "subtitle": "Explore the United States, one question at a time!",
        "quiz_description": "10 questions — states, landmarks, parks, history & more!",
        "color": "#3b82f6",
        "has_map": True,
        "map_country": "us",
        "strict_diversity_post_checks": False,
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


def _normalize_for_compare(text: str) -> str:
    text = (text or "").lower().strip()
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def _word_jaccard(a: str, b: str) -> float:
    wa = set(a.split())
    wb = set(b.split())
    if not wa or not wb:
        return 0.0
    return len(wa & wb) / len(wa | wb)


def _question_similarity(q1: str, q2: str) -> float:
    """Blend sequence similarity and word overlap (no extra dependencies)."""
    n1, n2 = _normalize_for_compare(q1), _normalize_for_compare(q2)
    if not n1 or not n2:
        return 0.0
    if n1 == n2:
        return 1.0
    seq = difflib.SequenceMatcher(None, n1, n2).ratio()
    jac = _word_jaccard(n1, n2)
    return max(seq, jac)


def _same_opening_prefix(a: str, b: str, words: int) -> bool:
    wa = _normalize_for_compare(a).split()
    wb = _normalize_for_compare(b).split()
    if len(wa) < words or len(wb) < words:
        return False
    return wa[:words] == wb[:words]


def check_quiz_diversity(
    questions: list[dict],
    *,
    require_unique_topics: bool = True,
    strict: bool = True,
) -> tuple[bool, list[str]]:
    """Return (ok, issues). If strict=False, only topic + duplicate-answer checks."""
    issues: list[str] = []
    n = len(questions)
    texts = [str(q.get("question", "")) for q in questions]

    if require_unique_topics:
        topics = [str(q.get("topic", "")).strip().lower() for q in questions]
        if any(not t for t in topics):
            issues.append("Every question must have a non-empty topic.")
        elif len(topics) != len(set(topics)):
            issues.append(
                "Duplicate topic labels: each question must use a different topic."
            )

    # Duplicate correct answers (substantive strings only)
    seen_ans: dict[str, int] = {}
    for i, q in enumerate(questions):
        opts = q.get("options")
        ans_i = q.get("answer")
        if not isinstance(opts, list) or ans_i is None:
            continue
        if not (0 <= int(ans_i) < len(opts)):
            continue
        key = _normalize_for_compare(str(opts[int(ans_i)]))
        if len(key) >= _DIVERSITY_MIN_ANSWER_LEN_FOR_UNIQUENESS:
            if key in seen_ans:
                issues.append(
                    f"Questions {seen_ans[key] + 1} and {i + 1} share the same correct answer text."
                )
            else:
                seen_ans[key] = i

    if not strict:
        out_light: list[str] = []
        for x in issues:
            if x not in out_light:
                out_light.append(x)
        return (len(out_light) == 0, out_light)

    for i in range(n):
        for j in range(i + 1, n):
            if _same_opening_prefix(texts[i], texts[j], _DIVERSITY_OPENING_WORDS):
                issues.append(
                    f"Questions {i + 1} and {j + 1} use the same first "
                    f"{_DIVERSITY_OPENING_WORDS} words — rewrite one with a different structure."
                )
            sim = _question_similarity(texts[i], texts[j])
            if sim >= _DIVERSITY_MAX_PAIR_SIMILARITY:
                issues.append(
                    f"Questions {i + 1} and {j + 1} are too similar (score {sim:.2f})."
                )

    for i in range(n - 1):
        sim = _question_similarity(texts[i], texts[i + 1])
        if sim >= _DIVERSITY_MAX_ADJACENT_SIMILARITY:
            issues.append(
                f"Consecutive questions {i + 1} and {i + 2} are too similar "
                f"(score {sim:.2f}) — separate their wording more."
            )

    # Dedupe issue strings while preserving order
    out: list[str] = []
    for x in issues:
        if x not in out:
            out.append(x)
    return (len(out) == 0, out)


def _parse_validate_shuffle_questions(raw: str) -> list:
    """Parse model JSON, validate fields, shuffle options. Raises ValueError."""
    json_match = re.search(r"\[[\s\S]*\]", raw)
    if not json_match:
        raise ValueError(f"No JSON array found in response:\n{raw[:500]}")

    questions = json.loads(json_match.group())

    if not isinstance(questions, list) or len(questions) == 0:
        raise ValueError("Expected a non-empty list of questions")

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

        correct_text = q["options"][q["answer"]]
        indices = list(range(4))
        random.shuffle(indices)
        q["options"] = [q["options"][j] for j in indices]
        q["answer"] = q["options"].index(correct_text)

        validated.append(q)

    return validated


def generate_daily_questions(
    xai_api_key: str,
    user_name: str = "Arjun",
    past_questions: list[str] | None = None,
) -> list:
    """Generate daily GK questions using xAI Grok.

    After each successful parse, runs ``check_quiz_diversity`` (see profile flag
    ``strict_diversity_post_checks``). On failure, retries up to
    ``_DIVERSITY_GENERATION_RETRIES`` with automated feedback to the model.

    Args:
        xai_api_key: xAI API key.
        user_name: Name of the user (determines profile/topics/tone).
        past_questions: Optional list of previously asked question strings
            to exclude from generation.

    Returns a list of question dicts, each with:
      topic, question, options (list of 4), answer (int), explanation (str)

    Raises ValueError if generation, parsing, or post-checks fail after retries.
    """
    profile = get_profile(user_name)
    client = _get_client(xai_api_key)

    system_prompt = profile["question_prompt"]

    # Build an exclusion block so the model avoids repeating past questions
    if past_questions:
        pq = list(past_questions)
        random.shuffle(pq)
        sample = pq[: min(100, len(pq))]
        exclusion = "\n".join(f"- {q}" for q in sample)
        system_prompt += (
            "\n\nCRITICAL — do NOT repeat or closely paraphrase any of these previously "
            "asked questions. Each new question must target a different fact than all of these. "
            "If a topic appears here often, choose a different sub-topic or angle for that topic:\n"
            f"{exclusion}"
        )

    # Randomise the user message so the model doesn't cache identical outputs
    today_str = date.today().strftime("%A, %B %d, %Y")
    seed = random.randint(1000, 9999)
    user_msg = (
        f"Generate a fresh set of general knowledge questions for {today_str}. "
        f"(Session {seed}) Make them creative and different from any previous set!"
    )
    hint_pool = profile.get("diversity_hint_pool")
    if hint_pool:
        k = min(5, len(hint_pool))
        picks = random.sample(hint_pool, k=k)
        user_msg += "\n\nSession-specific diversity requirements (follow all):\n" + "\n".join(
            f"- {p}" for p in picks
        )

    require_unique_topics = profile.get("require_unique_topics", True)
    strict_checks = profile.get("strict_diversity_post_checks", False)
    retry_feedback: str | None = None
    last_structural_error: str | None = None
    last_diversity_issues: list[str] = []

    for attempt in range(_DIVERSITY_GENERATION_RETRIES):
        user_attempt = user_msg
        if retry_feedback:
            user_attempt += "\n\n" + retry_feedback
        if attempt > 0 and hint_pool:
            extra = random.sample(hint_pool, k=min(2, len(hint_pool)))
            user_attempt += "\n\nExtra variety nudges:\n" + "\n".join(f"- {p}" for p in extra)

        response = client.chat.completions.create(
            model=XAI_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_attempt},
            ],
            max_tokens=3800,
            temperature=1.0,
        )

        raw = response.choices[0].message.content.strip()

        try:
            validated = _parse_validate_shuffle_questions(raw)
        except ValueError as exc:
            last_structural_error = str(exc)
            if attempt < _DIVERSITY_GENERATION_RETRIES - 1:
                retry_feedback = (
                    "Your last reply was not usable. Fix and return ONLY a valid JSON array "
                    f"of questions. Error: {last_structural_error}"
                )
                continue
            raise

        ok, issues = check_quiz_diversity(
            validated,
            require_unique_topics=require_unique_topics,
            strict=strict_checks,
        )
        if ok:
            return validated

        last_diversity_issues = issues
        if attempt < _DIVERSITY_GENERATION_RETRIES - 1:
            shown = issues[:20]
            retry_feedback = (
                "AUTOMATED DIVERSITY CHECKS FAILED on your last JSON. "
                "Regenerate the ENTIRE quiz from scratch. Fix ALL of the following:\n"
                + "\n".join(f"- {x}" for x in shown)
            )
            continue

    detail = "; ".join(last_diversity_issues[:5]) if last_diversity_issues else "unknown"
    raise ValueError(
        f"Quiz diversity checks failed after {_DIVERSITY_GENERATION_RETRIES} attempts: {detail}"
    )


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
