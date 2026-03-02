"""
Sight Words Practice for Krish (ages 4-6)

Based on the Dolch Sight Word lists — the most widely used sight word
curriculum in early childhood education.  Three progressive levels:
  Pre-K  (Dolch Pre-Primer)  — 40 words
  Kindergarten (Dolch Primer) — 52 words
  First Grade  (Dolch Grade 1) — 41 words

Each word includes a kid-friendly example sentence and a visual emoji cue.
"""

import random

LEVELS = [
    {
        "id": "prek",
        "title": "Pre-K",
        "subtitle": "First sight words",
        "emoji": "🌟",
        "color": "#10b981",
        "words_per_round": 8,
    },
    {
        "id": "kinder",
        "title": "Kindergarten",
        "subtitle": "Growing your words",
        "emoji": "🌈",
        "color": "#3b82f6",
        "words_per_round": 10,
    },
    {
        "id": "grade1",
        "title": "First Grade",
        "subtitle": "Big kid words",
        "emoji": "🚀",
        "color": "#8b5cf6",
        "words_per_round": 10,
    },
]

WORD_BANK = {
    "prek": [
        {"word": "a", "sentence": "I see a cat.", "emoji": "🐱"},
        {"word": "and", "sentence": "Mom and Dad.", "emoji": "👨‍👩‍👦"},
        {"word": "away", "sentence": "Run away!", "emoji": "🏃"},
        {"word": "big", "sentence": "A big bear.", "emoji": "🐻"},
        {"word": "blue", "sentence": "The sky is blue.", "emoji": "🔵"},
        {"word": "can", "sentence": "I can do it!", "emoji": "💪"},
        {"word": "come", "sentence": "Come here!", "emoji": "👋"},
        {"word": "down", "sentence": "Sit down.", "emoji": "⬇️"},
        {"word": "find", "sentence": "Find the ball.", "emoji": "🔍"},
        {"word": "for", "sentence": "This is for you.", "emoji": "🎁"},
        {"word": "funny", "sentence": "That is funny!", "emoji": "😂"},
        {"word": "go", "sentence": "Let's go!", "emoji": "🚗"},
        {"word": "help", "sentence": "Can you help me?", "emoji": "🤝"},
        {"word": "here", "sentence": "Come here.", "emoji": "📍"},
        {"word": "I", "sentence": "I am happy.", "emoji": "😊"},
        {"word": "in", "sentence": "The cat is in the box.", "emoji": "📦"},
        {"word": "is", "sentence": "It is fun.", "emoji": "⭐"},
        {"word": "it", "sentence": "Look at it!", "emoji": "👀"},
        {"word": "jump", "sentence": "Jump up high!", "emoji": "🤸"},
        {"word": "little", "sentence": "A little bird.", "emoji": "🐦"},
        {"word": "look", "sentence": "Look at me!", "emoji": "👁️"},
        {"word": "make", "sentence": "Let's make a cake.", "emoji": "🎂"},
        {"word": "me", "sentence": "Play with me.", "emoji": "🙋"},
        {"word": "my", "sentence": "This is my toy.", "emoji": "🧸"},
        {"word": "not", "sentence": "I am not sad.", "emoji": "🚫"},
        {"word": "one", "sentence": "I have one apple.", "emoji": "🍎"},
        {"word": "play", "sentence": "Let's play!", "emoji": "🎮"},
        {"word": "red", "sentence": "A red flower.", "emoji": "🌹"},
        {"word": "run", "sentence": "Run fast!", "emoji": "🏃‍♂️"},
        {"word": "said", "sentence": 'Mom said "yes!"', "emoji": "🗣️"},
        {"word": "see", "sentence": "I can see you.", "emoji": "👀"},
        {"word": "the", "sentence": "The dog is big.", "emoji": "🐕"},
        {"word": "three", "sentence": "Three little pigs.", "emoji": "🐷"},
        {"word": "to", "sentence": "Go to bed.", "emoji": "🛏️"},
        {"word": "two", "sentence": "Two eyes.", "emoji": "👀"},
        {"word": "up", "sentence": "Look up!", "emoji": "⬆️"},
        {"word": "we", "sentence": "We are friends.", "emoji": "👫"},
        {"word": "where", "sentence": "Where is it?", "emoji": "❓"},
        {"word": "yellow", "sentence": "A yellow sun.", "emoji": "🌞"},
        {"word": "you", "sentence": "I like you!", "emoji": "💛"},
    ],
    "kinder": [
        {"word": "all", "sentence": "We are all here.", "emoji": "👥"},
        {"word": "am", "sentence": "I am tall.", "emoji": "🧍"},
        {"word": "are", "sentence": "You are nice.", "emoji": "😊"},
        {"word": "at", "sentence": "Look at the bird.", "emoji": "🐦"},
        {"word": "ate", "sentence": "I ate lunch.", "emoji": "🍽️"},
        {"word": "be", "sentence": "Be kind.", "emoji": "💗"},
        {"word": "black", "sentence": "A black cat.", "emoji": "🐈‍⬛"},
        {"word": "brown", "sentence": "A brown dog.", "emoji": "🐕"},
        {"word": "but", "sentence": "I tried, but I fell.", "emoji": "😅"},
        {"word": "came", "sentence": "She came home.", "emoji": "🏠"},
        {"word": "did", "sentence": "I did it!", "emoji": "✅"},
        {"word": "do", "sentence": "What do you want?", "emoji": "🤔"},
        {"word": "eat", "sentence": "Let's eat!", "emoji": "🍕"},
        {"word": "four", "sentence": "Four dogs.", "emoji": "🐕"},
        {"word": "get", "sentence": "Get the ball!", "emoji": "⚽"},
        {"word": "good", "sentence": "Good job!", "emoji": "👍"},
        {"word": "have", "sentence": "I have a book.", "emoji": "📚"},
        {"word": "he", "sentence": "He is fast.", "emoji": "🏃‍♂️"},
        {"word": "into", "sentence": "Jump into the pool.", "emoji": "🏊"},
        {"word": "like", "sentence": "I like ice cream.", "emoji": "🍦"},
        {"word": "must", "sentence": "You must be nice.", "emoji": "☝️"},
        {"word": "new", "sentence": "I got new shoes.", "emoji": "👟"},
        {"word": "no", "sentence": "No, thank you.", "emoji": "🙅"},
        {"word": "now", "sentence": "Do it now!", "emoji": "⏰"},
        {"word": "on", "sentence": "Sit on the chair.", "emoji": "🪑"},
        {"word": "our", "sentence": "This is our house.", "emoji": "🏡"},
        {"word": "out", "sentence": "Go out and play.", "emoji": "🌳"},
        {"word": "please", "sentence": "Please help me.", "emoji": "🙏"},
        {"word": "pretty", "sentence": "A pretty butterfly.", "emoji": "🦋"},
        {"word": "ran", "sentence": "The dog ran fast.", "emoji": "🐕‍🦺"},
        {"word": "ride", "sentence": "Ride the bike.", "emoji": "🚲"},
        {"word": "saw", "sentence": "I saw a rainbow.", "emoji": "🌈"},
        {"word": "say", "sentence": "What did you say?", "emoji": "💬"},
        {"word": "she", "sentence": "She is my friend.", "emoji": "👧"},
        {"word": "so", "sentence": "I am so happy!", "emoji": "😄"},
        {"word": "soon", "sentence": "We will go soon.", "emoji": "🕐"},
        {"word": "that", "sentence": "Look at that!", "emoji": "👉"},
        {"word": "there", "sentence": "Over there!", "emoji": "👈"},
        {"word": "they", "sentence": "They are playing.", "emoji": "👦👧"},
        {"word": "this", "sentence": "I like this.", "emoji": "👍"},
        {"word": "too", "sentence": "Me too!", "emoji": "✌️"},
        {"word": "under", "sentence": "Under the table.", "emoji": "🪑"},
        {"word": "want", "sentence": "I want a cookie.", "emoji": "🍪"},
        {"word": "was", "sentence": "It was fun.", "emoji": "🎉"},
        {"word": "well", "sentence": "I feel well.", "emoji": "😌"},
        {"word": "went", "sentence": "We went to the park.", "emoji": "🌳"},
        {"word": "what", "sentence": "What is that?", "emoji": "❓"},
        {"word": "white", "sentence": "White snow.", "emoji": "❄️"},
        {"word": "who", "sentence": "Who is there?", "emoji": "🔎"},
        {"word": "will", "sentence": "I will try.", "emoji": "💪"},
        {"word": "with", "sentence": "Come with me.", "emoji": "🤝"},
        {"word": "yes", "sentence": "Yes, I can!", "emoji": "✅"},
    ],
    "grade1": [
        {"word": "after", "sentence": "After school, we play.", "emoji": "🏫"},
        {"word": "again", "sentence": "Do it again!", "emoji": "🔄"},
        {"word": "an", "sentence": "I ate an apple.", "emoji": "🍎"},
        {"word": "any", "sentence": "Do you have any?", "emoji": "🤷"},
        {"word": "ask", "sentence": "Ask your teacher.", "emoji": "🙋"},
        {"word": "as", "sentence": "Fast as a cheetah!", "emoji": "🐆"},
        {"word": "by", "sentence": "Sit by me.", "emoji": "🪑"},
        {"word": "could", "sentence": "Could you help?", "emoji": "🤝"},
        {"word": "every", "sentence": "Every day I read.", "emoji": "📖"},
        {"word": "fly", "sentence": "Birds can fly.", "emoji": "🕊️"},
        {"word": "from", "sentence": "A gift from Dad.", "emoji": "🎁"},
        {"word": "give", "sentence": "Give me a hug.", "emoji": "🤗"},
        {"word": "going", "sentence": "We are going home.", "emoji": "🏠"},
        {"word": "had", "sentence": "I had fun.", "emoji": "🎉"},
        {"word": "has", "sentence": "She has a pet.", "emoji": "🐹"},
        {"word": "her", "sentence": "This is her book.", "emoji": "📕"},
        {"word": "him", "sentence": "Help him up.", "emoji": "🤝"},
        {"word": "his", "sentence": "That is his hat.", "emoji": "🎩"},
        {"word": "how", "sentence": "How are you?", "emoji": "👋"},
        {"word": "just", "sentence": "I just woke up.", "emoji": "🌅"},
        {"word": "know", "sentence": "I know the answer.", "emoji": "💡"},
        {"word": "let", "sentence": "Let me try.", "emoji": "✋"},
        {"word": "live", "sentence": "I live here.", "emoji": "🏡"},
        {"word": "may", "sentence": "May I have some?", "emoji": "🙏"},
        {"word": "of", "sentence": "A cup of milk.", "emoji": "🥛"},
        {"word": "old", "sentence": "An old tree.", "emoji": "🌳"},
        {"word": "once", "sentence": "Once upon a time.", "emoji": "📖"},
        {"word": "open", "sentence": "Open the door.", "emoji": "🚪"},
        {"word": "over", "sentence": "Jump over it.", "emoji": "🤸"},
        {"word": "put", "sentence": "Put it away.", "emoji": "📥"},
        {"word": "round", "sentence": "A round ball.", "emoji": "⚽"},
        {"word": "some", "sentence": "I want some water.", "emoji": "💧"},
        {"word": "stop", "sentence": "Stop and look.", "emoji": "🛑"},
        {"word": "take", "sentence": "Take my hand.", "emoji": "🤲"},
        {"word": "thank", "sentence": "Thank you!", "emoji": "🙏"},
        {"word": "them", "sentence": "Give it to them.", "emoji": "👫"},
        {"word": "then", "sentence": "Then we went home.", "emoji": "🏠"},
        {"word": "think", "sentence": "Let me think.", "emoji": "🤔"},
        {"word": "walk", "sentence": "Let's walk to school.", "emoji": "🚶"},
        {"word": "were", "sentence": "We were happy.", "emoji": "😊"},
        {"word": "when", "sentence": "When is lunch?", "emoji": "🕛"},
    ],
}

WORD_COLORS = [
    "#ef4444", "#f59e0b", "#10b981", "#3b82f6", "#8b5cf6",
    "#ec4899", "#14b8a6", "#f97316", "#6366f1", "#84cc16",
]


def get_level(level_id):
    for lvl in LEVELS:
        if lvl["id"] == level_id:
            return lvl
    return None


def generate_round(level_id):
    """
    Generate a round of sight word practice questions.

    Each question shows a target word and 4 options.  The child must
    pick the correct word from the choices.
    """
    lvl = get_level(level_id)
    if not lvl:
        return []

    bank = WORD_BANK.get(level_id, [])
    if not bank:
        return []

    count = min(lvl["words_per_round"], len(bank))
    selected = random.sample(bank, count)
    questions = []

    for entry in selected:
        correct = entry["word"]
        distractors_pool = [w["word"] for w in bank if w["word"] != correct]
        distractors = random.sample(distractors_pool, min(3, len(distractors_pool)))

        options = [correct] + distractors
        random.shuffle(options)
        answer_idx = options.index(correct)
        word_color = random.choice(WORD_COLORS)

        questions.append({
            "word": correct,
            "sentence": entry["sentence"],
            "emoji": entry["emoji"],
            "options": options,
            "answer": answer_idx,
            "color": word_color,
        })

    return questions
