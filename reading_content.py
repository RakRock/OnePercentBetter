"""
Reading content library for Krish's Reading App.
"I Can Read Level 1" style stories with:
  - Simple, short sentences (4-8 words)
  - Repetitive patterns
  - Page-by-page format with pre-generated cartoon illustrations
  - Easy comprehension questions

Built-in stories live in the STORIES dict below.
User-generated stories are saved as JSON files under  stories/
Both sources are merged by  get_all_stories()  and  get_story().

Images live in  images/<story_id>_<page_num>.png
Run  generate_images.py  to regenerate them.
"""

import glob
import json
import os

_BASE_DIR = os.path.dirname(__file__)
_IMG_DIR = os.path.join(_BASE_DIR, "images")
_STORIES_DIR = os.path.join(_BASE_DIR, "stories")


def get_image_path(story_id: str, page_num: int) -> str:
    """Return the local file path for a story page illustration."""
    return os.path.join(_IMG_DIR, f"{story_id}_{page_num}.png")


STORIES = {
    # ── Story 1: The Big Red Ball ──
    "b1": {
        "id": "b1",
        "title": "The Big Red Ball",
        "cover_emoji": "🔴",
        "color": "#ef4444",
        "pages": [
            {
                "image_prompt": "a cute cartoon puppy standing next to a big shiny red ball on green grass",
                "fallback_emoji": "🐶🔴",
                "text": "Sam has a big red ball.",
            },
            {
                "image_prompt": "a cute cartoon puppy kicking a big red ball high up into the blue sky",
                "fallback_emoji": "🐶⬆️🔴",
                "text": "Sam kicks the ball up, up, up!",
            },
            {
                "image_prompt": "a big red ball stuck in the branches of a tall green tree",
                "fallback_emoji": "🔴🌳",
                "text": "Oh no! The ball is in the tree.",
            },
            {
                "image_prompt": "a cute cartoon puppy sitting sadly looking up at a tree with a ball stuck in it",
                "fallback_emoji": "🐶😢",
                "text": "Sam is sad.",
            },
            {
                "image_prompt": "a cute cartoon orange cat climbing a tall green tree looking at a red ball in the branches",
                "fallback_emoji": "🐱🌳",
                "text": "A cat sees the ball in the tree.",
            },
            {
                "image_prompt": "a cute cartoon cat on a tree branch pushing a big red ball down to the ground",
                "fallback_emoji": "🐱🔴⬇️",
                "text": "The cat pushes the ball down.",
            },
            {
                "image_prompt": "a cute cartoon puppy and an orange cat smiling and standing together happily",
                "fallback_emoji": "🐶🐱😊",
                "text": "Sam is happy! Thank you, cat!",
            },
            {
                "image_prompt": "a cute cartoon puppy and an orange cat playing together with a big red ball on green grass with confetti",
                "fallback_emoji": "🐶🐱🔴🎉",
                "text": "Now Sam and the cat play with the ball.",
            },
        ],
        "questions": [
            {
                "q": "What color is the ball?",
                "options": ["Blue 🔵", "Red 🔴", "Green 🟢"],
                "answer": 1,
            },
            {
                "q": "Where did the ball go?",
                "options": ["In the water 🌊", "In the tree 🌳", "On the roof 🏠"],
                "answer": 1,
            },
            {
                "q": "Who helped Sam?",
                "options": ["A bird 🐦", "A dog 🐕", "A cat 🐱"],
                "answer": 2,
            },
            {
                "q": "How did Sam feel at the end?",
                "options": ["Sad 😢", "Happy 😊", "Scared 😨"],
                "answer": 1,
            },
        ],
    },

    # ── Story 2: I See Bugs ──
    "b2": {
        "id": "b2",
        "title": "I See Bugs!",
        "cover_emoji": "🐛",
        "color": "#22c55e",
        "pages": [
            {
                "image_prompt": "a cute cartoon boy with a magnifying glass looking at bugs in a garden with green plants",
                "fallback_emoji": "👦🔍🌿",
                "text": "I like to look for bugs.",
            },
            {
                "image_prompt": "a cute cartoon green caterpillar sitting on a big green leaf",
                "fallback_emoji": "🐛🍃",
                "text": "I see a green bug on a leaf.",
            },
            {
                "image_prompt": "a cute cartoon red ladybug with black spots sitting on a pink flower",
                "fallback_emoji": "🐞🌸",
                "text": "I see a red bug on a flower.",
            },
            {
                "image_prompt": "a cute cartoon colorful butterfly flying in bright sunshine with blue sky",
                "fallback_emoji": "🦋☀️",
                "text": "I see a butterfly in the sun.",
            },
            {
                "image_prompt": "three cute cartoon ants walking in a line on the ground carrying tiny leaves",
                "fallback_emoji": "🐜🐜🐜",
                "text": "I see one, two, three ants!",
            },
            {
                "image_prompt": "a cute cartoon fuzzy bumblebee sitting on a big yellow sunflower",
                "fallback_emoji": "🐝🌻",
                "text": "I see a bee on a big flower.",
            },
            {
                "image_prompt": "a cute cartoon green cricket sitting on grass at nighttime with moon and stars in the sky singing music notes",
                "fallback_emoji": "🌙⭐🦗",
                "text": "At night, I hear a cricket sing.",
            },
            {
                "image_prompt": "a happy cartoon boy surrounded by cute friendly bugs including a ladybug butterfly and caterpillar in a sunny garden",
                "fallback_emoji": "👦😊🐛🐞🦋",
                "text": "I love bugs! Bugs are fun!",
            },
        ],
        "questions": [
            {
                "q": "Where is the green bug?",
                "options": ["On a rock 🪨", "On a leaf 🍃", "On the ground"],
                "answer": 1,
            },
            {
                "q": "How many ants did he see?",
                "options": ["Two 2️⃣", "Three 3️⃣", "Four 4️⃣"],
                "answer": 1,
            },
            {
                "q": "What does the cricket do at night?",
                "options": ["Sleep 😴", "Sing 🎵", "Eat 🍽️"],
                "answer": 1,
            },
            {
                "q": "What color is the bug on the flower?",
                "options": ["Red 🔴", "Blue 🔵", "Yellow 🟡"],
                "answer": 0,
            },
        ],
    },

    # ── Story 3: My Pet Fish ──
    "b3": {
        "id": "b3",
        "title": "My Pet Fish",
        "cover_emoji": "🐠",
        "color": "#3b82f6",
        "pages": [
            {
                "image_prompt": "a cute cartoon orange goldfish swimming in a round glass fish bowl with water",
                "fallback_emoji": "🐠💧",
                "text": "I have a pet fish.",
            },
            {
                "image_prompt": "a cute cartoon bright orange fish with big eyes swimming happily in clear blue water",
                "fallback_emoji": "🐠🟠",
                "text": "My fish is orange.",
            },
            {
                "image_prompt": "a cute cartoon girl sprinkling fish food into a fish bowl with a happy orange fish inside",
                "fallback_emoji": "👧🍽️🐠",
                "text": "I feed my fish every day.",
            },
            {
                "image_prompt": "a cute cartoon orange fish swimming very fast with speed lines through blue water",
                "fallback_emoji": "🐠💨💨",
                "text": "My fish swims fast!",
            },
            {
                "image_prompt": "a cute cartoon orange fish blowing round bubbles in blue water in a fish bowl",
                "fallback_emoji": "🐠🫧🫧",
                "text": "My fish blows bubbles.",
            },
            {
                "image_prompt": "a cute cartoon orange fish peeking from behind a small rock and a tiny castle decoration in a fish tank",
                "fallback_emoji": "🐠🪨🏰",
                "text": "My fish hides behind a rock.",
            },
            {
                "image_prompt": "a cute cartoon orange fish sleeping peacefully in a fish bowl at nighttime with moon visible through window",
                "fallback_emoji": "🌙🐠😴",
                "text": "At night, my fish sleeps.",
            },
            {
                "image_prompt": "a cute cartoon girl hugging a fish bowl with a happy orange fish inside with a heart above them",
                "fallback_emoji": "👧❤️🐠",
                "text": "I love my pet fish!",
            },
        ],
        "questions": [
            {
                "q": "What pet does she have?",
                "options": ["A cat 🐱", "A dog 🐶", "A fish 🐠"],
                "answer": 2,
            },
            {
                "q": "What color is the fish?",
                "options": ["Blue 🔵", "Orange 🟠", "Pink 🩷"],
                "answer": 1,
            },
            {
                "q": "What does the fish blow?",
                "options": ["Bubbles 🫧", "Wind 💨", "Kisses 💋"],
                "answer": 0,
            },
            {
                "q": "Where does the fish hide?",
                "options": ["Under the bed 🛏️", "Behind a rock 🪨", "In a box 📦"],
                "answer": 1,
            },
        ],
    },

    # ── Story 4: Let's Go to the Park ──
    "b4": {
        "id": "b4",
        "title": "Let's Go to the Park!",
        "cover_emoji": "🏞️",
        "color": "#a855f7",
        "pages": [
            {
                "image_prompt": "a bright sunny day with blue sky white fluffy clouds and a big yellow smiling sun",
                "fallback_emoji": "☀️🌤️",
                "text": "It is a sunny day!",
            },
            {
                "image_prompt": "a cute cartoon boy and his mom walking together on a path toward a colorful playground park",
                "fallback_emoji": "👦👧🚶‍♂️🚶‍♀️",
                "text": "Mom and I go to the park.",
            },
            {
                "image_prompt": "a cute cartoon boy sliding down a big colorful playground slide with a big smile saying whee",
                "fallback_emoji": "🛝😄",
                "text": "I go on the slide. Whee!",
            },
            {
                "image_prompt": "a cute cartoon boy on a playground swing going up high with blue sky behind",
                "fallback_emoji": "🔄👦",
                "text": "I go on the swings. Up and down!",
            },
            {
                "image_prompt": "a cute cartoon boy kicking a soccer ball with a friend on green grass at a park",
                "fallback_emoji": "👦⚽👧",
                "text": "I kick a ball with my friend.",
            },
            {
                "image_prompt": "a cute cartoon happy dog running fast through a park with its tongue out",
                "fallback_emoji": "🐕🏃",
                "text": "A dog runs by. It is fast!",
            },
            {
                "image_prompt": "a cute cartoon boy happily eating a big ice cream cone with his mom at a park bench",
                "fallback_emoji": "🍦😋",
                "text": "Mom gets me ice cream. Yum!",
            },
            {
                "image_prompt": "a cute cartoon boy and his mom walking home together at sunset with orange sky and houses in background",
                "fallback_emoji": "🌅👦👧🏠",
                "text": "We go home. What a fun day!",
            },
        ],
        "questions": [
            {
                "q": "How is the weather?",
                "options": ["Rainy 🌧️", "Sunny ☀️", "Snowy ❄️"],
                "answer": 1,
            },
            {
                "q": "What does he go on first?",
                "options": ["The slide 🛝", "The swings 🔄", "A bike 🚲"],
                "answer": 0,
            },
            {
                "q": "What animal runs by?",
                "options": ["A cat 🐱", "A bird 🐦", "A dog 🐕"],
                "answer": 2,
            },
            {
                "q": "What treat does Mom get?",
                "options": ["A cookie 🍪", "Ice cream 🍦", "Cake 🎂"],
                "answer": 1,
            },
        ],
    },

    # ── Story 5: The Rain Song ──
    "b5": {
        "id": "b5",
        "title": "The Rain Song",
        "cover_emoji": "🌧️",
        "color": "#06b6d4",
        "pages": [
            {
                "image_prompt": "cartoon raindrops falling from grey clouds onto green grass with puddles on the ground",
                "fallback_emoji": "🌧️🌧️🌧️",
                "text": "Drip, drop. It is raining!",
            },
            {
                "image_prompt": "a cute cartoon boy looking out a window at the rain falling outside with raindrops on the glass",
                "fallback_emoji": "👦🪟",
                "text": "I look out the window.",
            },
            {
                "image_prompt": "cartoon raindrops falling gently on colorful red and pink flowers in a garden",
                "fallback_emoji": "💧🌷💧🌷",
                "text": "The rain falls on the flowers.",
            },
            {
                "image_prompt": "a cute cartoon happy green frog sitting on a lily pad in the rain with a big smile",
                "fallback_emoji": "🐸💧😊",
                "text": "A frog sits in the rain. He is happy!",
            },
            {
                "image_prompt": "cartoon scene showing rain clouds parting and a bright yellow sun peeking through with blue sky",
                "fallback_emoji": "🌧️➡️☀️",
                "text": "The rain stops. The sun comes out.",
            },
            {
                "image_prompt": "a big bright colorful rainbow arching across a blue sky with sparkles and sunshine",
                "fallback_emoji": "🌈✨",
                "text": "Look! A rainbow!",
            },
            {
                "image_prompt": "a beautiful rainbow with all seven colors red orange yellow green blue indigo violet across a blue sky",
                "fallback_emoji": "🌈🔴🟠🟡🟢🔵🟣",
                "text": "The rainbow has many colors.",
            },
            {
                "image_prompt": "a cute cartoon happy boy pointing up at a beautiful rainbow in the sky with green grass below",
                "fallback_emoji": "👦🌈😊",
                "text": "I love the rain. It makes rainbows!",
            },
        ],
        "questions": [
            {
                "q": "What is the weather at the start?",
                "options": ["Sunny ☀️", "Rainy 🌧️", "Windy 🌬️"],
                "answer": 1,
            },
            {
                "q": "Who sits in the rain?",
                "options": ["A frog 🐸", "A duck 🦆", "A fish 🐟"],
                "answer": 0,
            },
            {
                "q": "What comes after the rain?",
                "options": ["Snow ❄️", "A rainbow 🌈", "More rain 🌧️"],
                "answer": 1,
            },
            {
                "q": "How does the frog feel?",
                "options": ["Sad 😢", "Happy 😊", "Sleepy 😴"],
                "answer": 1,
            },
        ],
    },

    # ── Story 6: Time for Bed ──
    "b6": {
        "id": "b6",
        "title": "Time for Bed",
        "cover_emoji": "🌙",
        "color": "#6366f1",
        "pages": [
            {
                "image_prompt": "a peaceful cartoon night sky with a bright crescent moon and twinkling stars over a quiet village",
                "fallback_emoji": "🌙⭐⭐",
                "text": "The moon is out. The stars are out.",
            },
            {
                "image_prompt": "a cute cartoon bird sleeping peacefully in a cozy nest on a tree branch at night",
                "fallback_emoji": "🐦🪹😴",
                "text": "The bird goes to its nest to sleep.",
            },
            {
                "image_prompt": "a cute cartoon cat curled up sleeping on a soft couch with a small blanket",
                "fallback_emoji": "🐱🛋️😴",
                "text": "The cat naps on the couch.",
            },
            {
                "image_prompt": "a cute cartoon dog sleeping inside a red dog house at night with a bone nearby",
                "fallback_emoji": "🐶🏠😴",
                "text": "The dog sleeps in its house.",
            },
            {
                "image_prompt": "a cute cartoon brown bear sleeping inside a cozy dark cave at nighttime",
                "fallback_emoji": "🐻🕳️😴",
                "text": "The bear sleeps in its cave.",
            },
            {
                "image_prompt": "a cute cartoon boy in pajamas brushing his teeth in front of a bathroom mirror",
                "fallback_emoji": "👦🪥",
                "text": "I brush my teeth.",
            },
            {
                "image_prompt": "a cute cartoon boy sitting in bed reading a storybook with a bedside lamp glowing",
                "fallback_emoji": "👦📖🛏️",
                "text": "I read a book in bed.",
            },
            {
                "image_prompt": "a cute cartoon boy sleeping peacefully in bed with a blanket and moon visible through the window",
                "fallback_emoji": "👦🛏️😴🌙",
                "text": "Good night! Time to sleep.",
            },
        ],
        "questions": [
            {
                "q": "What is out in the sky?",
                "options": ["The sun ☀️", "The moon and stars 🌙⭐", "Clouds ☁️"],
                "answer": 1,
            },
            {
                "q": "Where does the bird sleep?",
                "options": ["In a tree 🌲", "In its nest 🪹", "On the ground"],
                "answer": 1,
            },
            {
                "q": "What does the boy do before bed?",
                "options": ["Eats food 🍽️", "Brushes his teeth 🪥", "Plays a game 🎮"],
                "answer": 1,
            },
            {
                "q": "Where does the bear sleep?",
                "options": ["In a bed 🛏️", "In a cave 🕳️", "In a house 🏠"],
                "answer": 1,
            },
        ],
    },
}


def _load_generated_stories() -> dict:
    """Scan stories/*.json and return them as {id: story_dict}."""
    generated = {}
    if not os.path.isdir(_STORIES_DIR):
        return generated
    for path in glob.glob(os.path.join(_STORIES_DIR, "*.json")):
        try:
            with open(path, "r", encoding="utf-8") as f:
                story = json.load(f)
            if "id" in story:
                generated[story["id"]] = story
        except (json.JSONDecodeError, OSError):
            continue
    return generated


def save_generated_story(story: dict) -> str:
    """Save a generated story dict to stories/<id>.json. Returns the file path."""
    os.makedirs(_STORIES_DIR, exist_ok=True)
    path = os.path.join(_STORIES_DIR, f"{story['id']}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(story, f, ensure_ascii=False, indent=2)
    return path


def get_all_stories() -> list:
    """Get all stories (built-in + generated) as a list."""
    merged = dict(STORIES)
    merged.update(_load_generated_stories())
    return list(merged.values())


def get_story(story_id: str) -> dict | None:
    """Get a story by its ID (checks built-in first, then generated)."""
    if story_id in STORIES:
        return STORIES[story_id]
    generated = _load_generated_stories()
    return generated.get(story_id)


def get_all_story_ids() -> list:
    """Get all story IDs (built-in + generated)."""
    merged = dict(STORIES)
    merged.update(_load_generated_stories())
    return list(merged.keys())
