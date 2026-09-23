"""Vocabulary from Arjun's Realidades / Auténtico *Para empezar* school packet.

Cards keep school accents and articles. Extra beginner packs (colors, family)
grow the daily mix beyond the first homework set.
"""

from __future__ import annotations

from typing import Any

QUIZ_SIZE = 8
FLASH_SIZE = 12
TYPE_SIZE = 8
MATCH_PAIRS = 5
LIKES_SIZE = 8
DESCRIBE_SIZE = 8
SENTENCE_SIZE = 8
DEFAULT_SESSION_COUNT = 12
SESSION_UNIT_OFFSET = 9100
RECENT_SESSIONS_TO_AVOID = 4
LEARNING_DAYS = 3

TOPICS: list[dict[str, Any]] = [
    {
        "id": "greetings",
        "title": "Greetings",
        "subtitle": "Hola, names, and meeting people",
        "emoji": "👋",
        "color": "#c2410c",
        "source": "school",
    },
    {
        "id": "feelings",
        "title": "How are you?",
        "subtitle": "¿Cómo estás? — formal and informal",
        "emoji": "😊",
        "color": "#ea580c",
        "source": "school",
    },
    {
        "id": "goodbyes",
        "title": "Titles & goodbyes",
        "subtitle": "Señor, adiós, hasta luego",
        "emoji": "🙌",
        "color": "#d97706",
        "source": "school",
    },
    {
        "id": "numbers",
        "title": "Numbers",
        "subtitle": "Cero to treinta",
        "emoji": "🔢",
        "color": "#ca8a04",
        "source": "school",
    },
    {
        "id": "time",
        "title": "Telling time",
        "subtitle": "¿Qué hora es?",
        "emoji": "🕐",
        "color": "#65a30d",
        "source": "school",
    },
    {
        "id": "classroom",
        "title": "Classroom objects",
        "subtitle": "Books, pencils, desks",
        "emoji": "✏️",
        "color": "#059669",
        "source": "school",
    },
    {
        "id": "calendar",
        "title": "Calendar",
        "subtitle": "Days, months, and dates",
        "emoji": "📅",
        "color": "#0d9488",
        "source": "school",
    },
    {
        "id": "phrases",
        "title": "Classroom phrases",
        "subtitle": "How do you say…? How many?",
        "emoji": "💬",
        "color": "#0891b2",
        "source": "school",
    },
    {
        "id": "weather",
        "title": "Weather & seasons",
        "subtitle": "Hace sol, llueve, el verano",
        "emoji": "☀️",
        "color": "#0284c7",
        "source": "school",
    },
    {
        "id": "body",
        "title": "Body & feelings",
        "subtitle": "Me duele… body parts",
        "emoji": "💪",
        "color": "#2563eb",
        "source": "school",
    },
    {
        "id": "commands",
        "title": "Class commands",
        "subtitle": "Sit, stand, take out paper",
        "emoji": "📣",
        "color": "#4f46e5",
        "source": "school",
    },
    {
        "id": "colors",
        "title": "Colors",
        "subtitle": "New words beyond the packet",
        "emoji": "🎨",
        "color": "#7c3aed",
        "source": "extra",
    },
    {
        "id": "family",
        "title": "Family",
        "subtitle": "People at home",
        "emoji": "👨‍👩‍👧",
        "color": "#db2777",
        "source": "extra",
    },
    {
        "id": "gustar",
        "title": "What I like",
        "subtitle": "1A — Me gusta + activities",
        "emoji": "⭐",
        "color": "#e11d48",
        "source": "chapter1",
    },
    {
        "id": "personality",
        "title": "How I am",
        "subtitle": "1B — Soy, eres, es + adjectives",
        "emoji": "🪞",
        "color": "#9333ea",
        "source": "chapter1",
    },
]

DAILY_TOPIC = {
    "id": "daily",
    "title": "Daily mix",
    "subtitle": "A little from every topic",
    "emoji": "🔥",
    "color": "#c2410c",
    "source": "mix",
}


def _card(
    topic: str,
    spanish: str,
    english: str,
    *,
    emoji: str = "",
    hint: str = "",
    slug: str = "",
) -> dict[str, str]:
    key = slug or spanish
    return {
        "id": f"{topic}:{key}",
        "topic": topic,
        "spanish": spanish,
        "english": english,
        "emoji": emoji,
        "hint": hint,
    }


CARDS: list[dict[str, str]] = [
    # --- Greetings ---
    _card("greetings", "Buenos días.", "Good morning.", emoji="🌅", hint="Use until about noon."),
    _card("greetings", "Buenas tardes.", "Good afternoon.", emoji="🌇", hint="After lunch until evening."),
    _card("greetings", "Buenas noches.", "Good evening. / Good night.", emoji="🌙"),
    _card("greetings", "¡Hola!", "Hello! / Hi!", emoji="👋"),
    _card("greetings", "¿Cómo te llamas?", "What's your name?", emoji="🪪", hint="Informal — talking to a friend."),
    _card("greetings", "Me llamo…", "My name is…", emoji="✍️"),
    _card("greetings", "Encantado.", "Pleased to meet you. (said by a boy)", emoji="🤝", slug="encantado"),
    _card("greetings", "Encantada.", "Pleased to meet you. (said by a girl)", emoji="🤝", slug="encantada"),
    _card("greetings", "Igualmente.", "Likewise. / Same here.", emoji="↔️"),
    _card("greetings", "Mucho gusto.", "Nice to meet you.", emoji="😊"),
    # --- How are you ---
    _card("feelings", "¿Cómo está usted?", "How are you? (formal)", emoji="🎩", hint="Use with adults / teachers. Ud. = usted."),
    _card("feelings", "¿Cómo estás?", "How are you? (informal)", emoji="🙂", hint="Use with friends and classmates."),
    _card("feelings", "¿Qué pasa?", "What's happening? / What's up?", emoji="❓"),
    _card("feelings", "¿Qué tal?", "How's it going?", emoji="✌️"),
    _card("feelings", "¿Y tú?", "And you? (informal)", emoji="👉"),
    _card("feelings", "¿Y usted?", "And you? (formal)", emoji="👉", hint="Ud. is the abbreviation for usted."),
    _card("feelings", "muy bien", "very well", emoji="😄"),
    _card("feelings", "bien", "well / fine", emoji="🙂"),
    _card("feelings", "regular", "so-so / okay", emoji="😐"),
    _card("feelings", "mal", "badly / not well", emoji="😟"),
    _card("feelings", "gracias", "thank you", emoji="🙏"),
    _card("feelings", "nada", "nothing", emoji="🚫"),
    # --- Titles & goodbyes ---
    _card("goodbyes", "señor (Sr.)", "sir / Mr.", emoji="👔"),
    _card("goodbyes", "señora (Sra.)", "madam / Mrs.", emoji="👗"),
    _card("goodbyes", "señorita (Srta.)", "miss / Miss", emoji="🎀"),
    _card("goodbyes", "¡Adiós!", "Good-bye!", emoji="👋"),
    _card("goodbyes", "Hasta luego.", "See you later.", emoji="👋"),
    _card("goodbyes", "Hasta mañana.", "See you tomorrow.", emoji="🌅"),
    _card("goodbyes", "¡Nos vemos!", "See you!", emoji="👀"),
    # --- Numbers 0–30 ---
    _card("numbers", "cero", "zero", emoji="0️⃣", slug="0"),
    _card("numbers", "uno", "one", emoji="1️⃣", slug="1"),
    _card("numbers", "dos", "two", emoji="2️⃣", slug="2"),
    _card("numbers", "tres", "three", emoji="3️⃣", slug="3"),
    _card("numbers", "cuatro", "four", emoji="4️⃣", slug="4"),
    _card("numbers", "cinco", "five", emoji="5️⃣", slug="5"),
    _card("numbers", "seis", "six", emoji="6️⃣", slug="6"),
    _card("numbers", "siete", "seven", emoji="7️⃣", slug="7"),
    _card("numbers", "ocho", "eight", emoji="8️⃣", slug="8"),
    _card("numbers", "nueve", "nine", emoji="9️⃣", slug="9"),
    _card("numbers", "diez", "ten", emoji="🔟", slug="10"),
    _card("numbers", "once", "eleven", emoji="1️⃣1️⃣", slug="11"),
    _card("numbers", "doce", "twelve", emoji="1️⃣2️⃣", slug="12"),
    _card("numbers", "trece", "thirteen", emoji="1️⃣3️⃣", slug="13"),
    _card("numbers", "catorce", "fourteen", emoji="1️⃣4️⃣", slug="14"),
    _card("numbers", "quince", "fifteen", emoji="1️⃣5️⃣", slug="15"),
    _card("numbers", "dieciséis", "sixteen", emoji="1️⃣6️⃣", slug="16"),
    _card("numbers", "diecisiete", "seventeen", emoji="1️⃣7️⃣", slug="17"),
    _card("numbers", "dieciocho", "eighteen", emoji="1️⃣8️⃣", slug="18"),
    _card("numbers", "diecinueve", "nineteen", emoji="1️⃣9️⃣", slug="19"),
    _card("numbers", "veinte", "twenty", emoji="2️⃣0️⃣", slug="20"),
    _card("numbers", "veintiuno", "twenty-one", emoji="2️⃣1️⃣", slug="21"),
    _card("numbers", "veintidós", "twenty-two", emoji="2️⃣2️⃣", slug="22"),
    _card("numbers", "veintitrés", "twenty-three", emoji="2️⃣3️⃣", slug="23"),
    _card("numbers", "veinticuatro", "twenty-four", emoji="2️⃣4️⃣", slug="24"),
    _card("numbers", "veinticinco", "twenty-five", emoji="2️⃣5️⃣", slug="25"),
    _card("numbers", "treinta", "thirty", emoji="3️⃣0️⃣", slug="30"),
    # --- Time ---
    _card("time", "¿Qué hora es?", "What time is it?", emoji="🕐"),
    _card("time", "Es la una.", "It's one o'clock.", emoji="🕐", hint="Use Es (singular) only for 1:00."),
    _card("time", "Son las dos.", "It's two o'clock.", emoji="🕑", hint="Use Son las for 2:00 and later."),
    _card("time", "Son las tres.", "It's three o'clock.", emoji="🕒"),
    _card("time", "Son las cuatro.", "It's four o'clock.", emoji="🕓"),
    _card("time", "Son las cinco.", "It's five o'clock.", emoji="🕔"),
    _card("time", "Son las seis.", "It's six o'clock.", emoji="🕕"),
    _card("time", "Son las siete.", "It's seven o'clock.", emoji="🕖"),
    _card("time", "Son las ocho.", "It's eight o'clock.", emoji="🕗"),
    _card("time", "Son las nueve.", "It's nine o'clock.", emoji="🕘"),
    _card("time", "Son las diez.", "It's ten o'clock.", emoji="🕙"),
    _card("time", "Son las once.", "It's eleven o'clock.", emoji="🕚"),
    _card("time", "Son las doce.", "It's twelve o'clock.", emoji="🕛"),
    _card("time", "y cuarto", "quarter past (:15)", emoji="🕒"),
    _card("time", "y media", "half past (:30)", emoji="🕕"),
    _card("time", "menos cuarto", "quarter to (:45)", emoji="🕘"),
    _card("time", "de la mañana", "in the morning", emoji="🌅"),
    _card("time", "de la tarde", "in the afternoon", emoji="🌇"),
    _card("time", "de la noche", "in the evening / at night", emoji="🌙"),
    # --- Classroom ---
    _card("classroom", "el bolígrafo", "the pen", emoji="🖊️"),
    _card("classroom", "la carpeta", "the folder", emoji="📁"),
    _card("classroom", "el cuaderno", "the notebook", emoji="📓"),
    _card("classroom", "el estudiante", "the student (boy)", emoji="👦", slug="estudiante-m"),
    _card("classroom", "la estudiante", "the student (girl)", emoji="👧", slug="estudiante-f"),
    _card("classroom", "la hoja de papel", "the sheet of paper", emoji="📄"),
    _card("classroom", "el lápiz", "the pencil", emoji="✏️"),
    _card("classroom", "el libro", "the book", emoji="📖"),
    _card("classroom", "el profesor", "the teacher (man)", emoji="👨‍🏫"),
    _card("classroom", "la profesora", "the teacher (woman)", emoji="👩‍🏫"),
    _card("classroom", "el pupitre", "the student desk", emoji="🪑"),
    _card("classroom", "la sala de clases", "the classroom", emoji="🏫"),
    _card("classroom", "la mochila", "the backpack", emoji="🎒"),
    _card("classroom", "la pizarra", "the board", emoji="⬛"),
    _card("classroom", "la silla", "the chair", emoji="💺"),
    _card("classroom", "la mesa", "the table", emoji="🪵"),
    _card("classroom", "la puerta", "the door", emoji="🚪"),
    _card("classroom", "la ventana", "the window", emoji="🪟"),
    # --- Calendar ---
    _card("calendar", "el año", "the year", emoji="📆"),
    _card("calendar", "el día", "the day", emoji="☀️"),
    _card("calendar", "el mes", "the month", emoji="🗓️"),
    _card("calendar", "la semana", "the week", emoji="📅"),
    _card("calendar", "hoy", "today", emoji="📍"),
    _card("calendar", "mañana", "tomorrow", emoji="➡️"),
    _card("calendar", "ayer", "yesterday", emoji="⬅️"),
    _card("calendar", "¿Qué día es hoy?", "What day is today?", emoji="❓"),
    _card("calendar", "¿Cuál es la fecha?", "What's the date?", emoji="❓", slug="fecha"),
    _card("calendar", "lunes", "Monday", emoji="1️⃣"),
    _card("calendar", "martes", "Tuesday", emoji="2️⃣"),
    _card("calendar", "miércoles", "Wednesday", emoji="3️⃣"),
    _card("calendar", "jueves", "Thursday", emoji="4️⃣"),
    _card("calendar", "viernes", "Friday", emoji="5️⃣"),
    _card("calendar", "sábado", "Saturday", emoji="6️⃣"),
    _card("calendar", "domingo", "Sunday", emoji="7️⃣"),
    _card("calendar", "enero", "January", emoji="❄️"),
    _card("calendar", "febrero", "February", emoji="💝"),
    _card("calendar", "marzo", "March", emoji="🌱"),
    _card("calendar", "abril", "April", emoji="🌧️"),
    _card("calendar", "mayo", "May", emoji="🌸"),
    _card("calendar", "junio", "June", emoji="☀️"),
    _card("calendar", "julio", "July", emoji="🎆"),
    _card("calendar", "agosto", "August", emoji="🏖️"),
    _card("calendar", "septiembre", "September", emoji="🍎"),
    _card("calendar", "octubre", "October", emoji="🎃"),
    _card("calendar", "noviembre", "November", emoji="🍂"),
    _card("calendar", "diciembre", "December", emoji="🎄"),
    _card(
        "calendar",
        "Es el primero de enero.",
        "It's the first of January.",
        emoji="1️⃣",
        hint="Use primero for the 1st; other days use the number (el dos, el tres…).",
        slug="primero",
    ),
    # --- Classroom phrases ---
    _card("phrases", "¿Cuántos?", "How many? (masculine)", emoji="🔢", slug="cuantos"),
    _card("phrases", "¿Cuántas?", "How many? (feminine)", emoji="🔢", slug="cuantas"),
    _card("phrases", "hay", "there is / there are", emoji="👉"),
    _card("phrases", "por favor", "please", emoji="🙏"),
    _card("phrases", "¿Cómo se dice…?", "How do you say…?", emoji="🗣️"),
    _card("phrases", "Se dice…", "You say… / It's said…", emoji="💬"),
    _card("phrases", "¿Cómo se escribe…?", "How do you write/spell…?", emoji="✍️"),
    _card("phrases", "Se escribe…", "It's written…", emoji="📝"),
    _card("phrases", "¿Qué quiere decir…?", "What does … mean?", emoji="🤔"),
    _card("phrases", "Quiere decir…", "It means…", emoji="💡"),
    # --- Weather ---
    _card("weather", "¿Qué tiempo hace?", "What's the weather like?", emoji="🌤️"),
    _card("weather", "Hace calor.", "It's hot.", emoji="🥵"),
    _card("weather", "Hace frío.", "It's cold.", emoji="🥶"),
    _card("weather", "Hace sol.", "It's sunny.", emoji="☀️"),
    _card("weather", "Hace viento.", "It's windy.", emoji="💨"),
    _card("weather", "Llueve.", "It's raining.", emoji="🌧️"),
    _card("weather", "Nieva.", "It's snowing.", emoji="❄️"),
    _card("weather", "Está nublado.", "It's cloudy.", emoji="☁️"),
    _card("weather", "la estación", "the season", emoji="🌍"),
    _card("weather", "el invierno", "winter", emoji="❄️"),
    _card("weather", "la primavera", "spring", emoji="🌸"),
    _card("weather", "el verano", "summer", emoji="☀️"),
    _card("weather", "el otoño", "fall / autumn", emoji="🍂"),
    # --- Body ---
    _card("body", "la cabeza", "the head", emoji="🧠"),
    _card("body", "el ojo", "the eye", emoji="👁️"),
    _card("body", "la boca", "the mouth", emoji="👄"),
    _card("body", "la mano", "the hand", emoji="✋"),
    _card("body", "el dedo", "the finger", emoji="☝️"),
    _card("body", "el brazo", "the arm", emoji="💪"),
    _card("body", "la pierna", "the leg", emoji="🦵"),
    _card("body", "el pie", "the foot", emoji="🦶"),
    _card("body", "el estómago", "the stomach", emoji="🤢"),
    _card("body", "Me duele…", "… hurts (one thing)", emoji="😣", hint="Me duele la cabeza. = My head hurts."),
    _card("body", "Me duelen…", "… hurt (more than one)", emoji="😣", hint="Me duelen los pies. = My feet hurt."),
    # --- Commands ---
    _card("commands", "Siéntense, por favor.", "Sit down, please.", emoji="🪑"),
    _card("commands", "Levántense, por favor.", "Stand up, please.", emoji="🧍"),
    _card("commands", "Saquen una hoja de papel.", "Take out a sheet of paper.", emoji="📄"),
    _card("commands", "Repitan, por favor.", "Repeat, please.", emoji="🔁"),
    _card("commands", "¡Silencio, por favor!", "Silence, please!", emoji="🤫"),
    _card("commands", "Escuchen, por favor.", "Listen, please.", emoji="👂"),
    _card("commands", "Abran el libro.", "Open the book.", emoji="📖"),
    _card("commands", "Cierren el libro.", "Close the book.", emoji="📕"),
    _card("commands", "Levanten la mano.", "Raise your hand.", emoji="✋"),
    # --- Colors (extra vocab) ---
    _card("colors", "rojo", "red", emoji="🔴"),
    _card("colors", "azul", "blue", emoji="🔵"),
    _card("colors", "verde", "green", emoji="🟢"),
    _card("colors", "amarillo", "yellow", emoji="🟡"),
    _card("colors", "naranja", "orange", emoji="🟠"),
    _card("colors", "morado", "purple", emoji="🟣"),
    _card("colors", "rosa", "pink", emoji="🩷"),
    _card("colors", "negro", "black", emoji="⚫"),
    _card("colors", "blanco", "white", emoji="⚪"),
    _card("colors", "gris", "gray", emoji="🩶"),
    _card("colors", "marrón", "brown", emoji="🤎"),
    # --- Family (extra vocab) ---
    _card("family", "la madre", "the mother", emoji="👩"),
    _card("family", "el padre", "the father", emoji="👨"),
    _card("family", "el hermano", "the brother", emoji="👦"),
    _card("family", "la hermana", "the sister", emoji="👧"),
    _card("family", "el abuelo", "the grandfather", emoji="👴"),
    _card("family", "la abuela", "the grandmother", emoji="👵"),
    _card("family", "la familia", "the family", emoji="👨‍👩‍👧"),
    _card("family", "el hijo", "the son", emoji="👦"),
    _card("family", "la hija", "the daughter", emoji="👧"),
    # --- Capítulo 1A: ¿Qué te gusta hacer? ---
    _card("gustar", "nadar", "to swim", emoji="🏊"),
    _card("gustar", "cantar", "to sing", emoji="🎤"),
    _card("gustar", "bailar", "to dance", emoji="💃"),
    _card("gustar", "correr", "to run", emoji="🏃"),
    _card("gustar", "dibujar", "to draw", emoji="✏️"),
    _card("gustar", "leer", "to read", emoji="📖"),
    _card("gustar", "escribir", "to write", emoji="✍️"),
    _card("gustar", "escuchar música", "to listen to music", emoji="🎧"),
    _card("gustar", "hablar por teléfono", "to talk on the phone", emoji="📱"),
    _card("gustar", "montar en bicicleta", "to ride a bike", emoji="🚲"),
    _card("gustar", "patinar", "to skate", emoji="⛸️"),
    _card("gustar", "ver la tele", "to watch TV", emoji="📺"),
    _card("gustar", "Me gusta…", "I like… (to do)", emoji="👍", hint="Me gusta + infinitive: Me gusta nadar."),
    _card("gustar", "No me gusta…", "I don't like… (to do)", emoji="👎", hint="No me gusta + infinitive."),
    _card("gustar", "¿Qué te gusta hacer?", "What do you like to do?", emoji="❓"),
    _card("gustar", "también", "also / too", emoji="➕", hint="Use after a yes: A mí también."),
    _card("gustar", "tampoco", "neither / either", emoji="🚫", hint="Use after a no: A mí tampoco."),
    # --- Capítulo 1B: Y tú, ¿cómo eres? ---
    _card("personality", "atlético", "athletic (boy)", emoji="🏅", slug="atletico-m"),
    _card("personality", "atlética", "athletic (girl)", emoji="🏅", slug="atletico-f"),
    _card("personality", "estudioso", "studious (boy)", emoji="📚", slug="estudioso-m"),
    _card("personality", "estudiosa", "studious (girl)", emoji="📚", slug="estudioso-f"),
    _card("personality", "simpático", "nice / friendly (boy)", emoji="😊", slug="simpatico-m"),
    _card("personality", "simpática", "nice / friendly (girl)", emoji="😊", slug="simpatico-f"),
    _card("personality", "serio", "serious (boy)", emoji="😐", slug="serio-m"),
    _card("personality", "seria", "serious (girl)", emoji="😐", slug="serio-f"),
    _card("personality", "ordenado", "organized (boy)", emoji="📁", slug="ordenado-m"),
    _card("personality", "ordenada", "organized (girl)", emoji="📁", slug="ordenado-f"),
    _card("personality", "talentoso", "talented (boy)", emoji="🌟", slug="talentoso-m"),
    _card("personality", "talentosa", "talented (girl)", emoji="🌟", slug="talentoso-f"),
    _card("personality", "soy", "I am", emoji="1️⃣", hint="Yo soy atlético."),
    _card("personality", "eres", "you are (informal)", emoji="2️⃣", hint="Tú eres seria."),
    _card("personality", "es", "he/she is", emoji="3️⃣", hint="Ella es estudiosa."),
    _card("personality", "¿Cómo eres?", "What are you like?", emoji="❓"),
    _card("personality", "un", "a / an (masculine)", emoji="🔷"),
    _card("personality", "una", "a / an (feminine)", emoji="🔶"),
]


_CARDS_BY_ID = {c["id"]: c for c in CARDS}
_CARDS_BY_TOPIC: dict[str, list[dict[str, str]]] = {}
for _card_row in CARDS:
    _CARDS_BY_TOPIC.setdefault(_card_row["topic"], []).append(_card_row)


def topic_by_id(topic_id: str) -> dict[str, Any]:
    if topic_id == "daily":
        return dict(DAILY_TOPIC)
    for topic in TOPICS:
        if topic["id"] == topic_id:
            return topic
    raise KeyError(topic_id)


def cards_for_topic(topic_id: str) -> list[dict[str, str]]:
    if topic_id == "daily":
        return list(CARDS)
    return list(_CARDS_BY_TOPIC.get(topic_id, []))


def get_card(card_id: str) -> dict[str, str]:
    return _CARDS_BY_ID[card_id]


def total_cards() -> int:
    return len(CARDS)


def school_topic_ids() -> list[str]:
    return [t["id"] for t in TOPICS if t["source"] == "school"]


def chapter1_topic_ids() -> list[str]:
    return [t["id"] for t in TOPICS if t["source"] == "chapter1"]


GUSTAR_ACTIVITIES: list[dict[str, str]] = [
    {"id": "nadar", "infinitive": "nadar", "english": "to swim", "emoji": "🏊"},
    {"id": "cantar", "infinitive": "cantar", "english": "to sing", "emoji": "🎤"},
    {"id": "bailar", "infinitive": "bailar", "english": "to dance", "emoji": "💃"},
    {"id": "correr", "infinitive": "correr", "english": "to run", "emoji": "🏃"},
    {"id": "dibujar", "infinitive": "dibujar", "english": "to draw", "emoji": "✏️"},
    {"id": "leer", "infinitive": "leer", "english": "to read", "emoji": "📖"},
    {"id": "escribir", "infinitive": "escribir", "english": "to write", "emoji": "✍️"},
    {
        "id": "escuchar",
        "infinitive": "escuchar música",
        "english": "to listen to music",
        "emoji": "🎧",
    },
    {
        "id": "telefono",
        "infinitive": "hablar por teléfono",
        "english": "to talk on the phone",
        "emoji": "📱",
    },
    {
        "id": "bici",
        "infinitive": "montar en bicicleta",
        "english": "to ride a bike",
        "emoji": "🚲",
    },
    {"id": "patinar", "infinitive": "patinar", "english": "to skate", "emoji": "⛸️"},
    {"id": "tele", "infinitive": "ver la tele", "english": "to watch TV", "emoji": "📺"},
]


PERSONALITY_ADJECTIVES: list[dict[str, str]] = [
    {"id": "atletico", "m": "atlético", "f": "atlética", "english": "athletic"},
    {"id": "estudioso", "m": "estudioso", "f": "estudiosa", "english": "studious"},
    {"id": "simpatico", "m": "simpático", "f": "simpática", "english": "nice / friendly"},
    {"id": "serio", "m": "serio", "f": "seria", "english": "serious"},
    {"id": "ordenado", "m": "ordenado", "f": "ordenada", "english": "organized"},
    {"id": "talentoso", "m": "talentoso", "f": "talentosa", "english": "talented"},
    {"id": "reservado", "m": "reservado", "f": "reservada", "english": "reserved"},
    {"id": "perezoso", "m": "perezoso", "f": "perezosa", "english": "lazy"},
    {"id": "gracioso", "m": "gracioso", "f": "graciosa", "english": "funny"},
    {"id": "trabajador", "m": "trabajador", "f": "trabajadora", "english": "hard-working"},
]


def _sentence(
    sid: str,
    english: str,
    spanish: str,
    *,
    topic: str,
    hint: str = "",
    variants: tuple[str, ...] = (),
    emoji: str = "",
) -> dict[str, Any]:
    return {
        "id": sid,
        "english": english,
        "spanish": spanish,
        "topic": topic,
        "hint": hint,
        "variants": list(variants),
        "emoji": emoji,
        "card_id": f"sentence:{sid}",
    }


SENTENCE_PROMPTS: list[dict[str, Any]] = [
    _sentence(
        "time-330",
        "It's three-thirty in the afternoon.",
        "Son las tres y media de la tarde.",
        topic="time",
        hint="Son las + y media + de la tarde.",
        emoji="🕒",
    ),
    _sentence(
        "time-115",
        "It's a quarter past one in the morning.",
        "Es la una y cuarto de la mañana.",
        topic="time",
        hint="Use Es (not Son) only for 1:00.",
        emoji="🕐",
    ),
    _sentence(
        "head",
        "My head hurts.",
        "Me duele la cabeza.",
        topic="body",
        hint="One thing → Me duele.",
        emoji="😣",
    ),
    _sentence(
        "feet",
        "My feet hurt.",
        "Me duelen los pies.",
        topic="body",
        hint="More than one → Me duelen.",
        emoji="🦶",
    ),
    _sentence("cold", "It's cold.", "Hace frío.", topic="weather", emoji="🥶"),
    _sentence(
        "winter-cold",
        "In the winter it's cold.",
        "En el invierno hace frío.",
        topic="weather",
        emoji="❄️",
    ),
    _sentence(
        "three-pencils",
        "There are three pencils.",
        "Hay tres lápices.",
        topic="classroom",
        emoji="✏️",
    ),
    _sentence(
        "monday",
        "Today is Monday.",
        "Hoy es lunes.",
        topic="calendar",
        variants=("Es lunes.",),
        emoji="📅",
    ),
    _sentence(
        "sit",
        "Sit down, please.",
        "Siéntense, por favor.",
        topic="commands",
        emoji="🪑",
    ),
    _sentence(
        "name",
        "What's your name?",
        "¿Cómo te llamas?",
        topic="greetings",
        emoji="🪪",
    ),
    _sentence(
        "like-swim",
        "I like to swim.",
        "Me gusta nadar.",
        topic="gustar",
        hint="Me gusta + infinitive.",
        emoji="🏊",
    ),
    _sentence(
        "dislike-sing",
        "I don't like to sing.",
        "No me gusta cantar.",
        topic="gustar",
        emoji="🎤",
    ),
    _sentence(
        "like-ask",
        "What do you like to do?",
        "¿Qué te gusta hacer?",
        topic="gustar",
        emoji="❓",
    ),
    _sentence(
        "like-bike",
        "I like to ride a bike.",
        "Me gusta montar en bicicleta.",
        topic="gustar",
        emoji="🚲",
    ),
    _sentence(
        "soy-atletico",
        "I am athletic.",
        "Soy atlético.",
        topic="personality",
        variants=("Yo soy atlético.",),
        hint="Soy + adjective. Boy form: atlético.",
        emoji="🏅",
    ),
    _sentence(
        "ella-seria",
        "She is serious.",
        "Ella es seria.",
        topic="personality",
        variants=("Es seria.",),
        emoji="😐",
    ),
    _sentence(
        "eres-simpatica",
        "You are nice. (talking to a girl)",
        "Eres simpática.",
        topic="personality",
        variants=("Tú eres simpática.",),
        emoji="😊",
    ),
    _sentence(
        "como-eres",
        "What are you like?",
        "¿Cómo eres?",
        topic="personality",
        emoji="🪞",
    ),
]


def _reading(
    rid: str,
    title: str,
    text: str,
    questions: list[dict[str, Any]],
    *,
    topic: str = "daily",
) -> dict[str, Any]:
    return {"id": rid, "title": title, "text": text, "questions": questions, "topic": topic}


READINGS: list[dict[str, Any]] = [
    _reading(
        "lunes-frio",
        "Un lunes frío",
        "Hoy es lunes. Hace frío. Me duele la cabeza. No me gusta correr. "
        "Me gusta leer en la sala de clases.",
        [
            {
                "question": "What day is it?",
                "options": ["Sunday", "Monday", "Friday", "Saturday"],
                "answer": 1,
                "explanation": "Hoy es lunes = Today is Monday.",
            },
            {
                "question": "How is the weather?",
                "options": ["It's hot.", "It's sunny.", "It's cold.", "It's raining."],
                "answer": 2,
                "explanation": "Hace frío = It's cold.",
            },
            {
                "question": "What does the writer like to do?",
                "options": ["Run", "Sing", "Read", "Swim"],
                "answer": 2,
                "explanation": "Me gusta leer = I like to read.",
            },
        ],
        topic="weather",
    ),
    _reading(
        "en-la-escuela",
        "En la escuela",
        "La profesora dice: «Siéntense, por favor.» Hay tres lápices y un cuaderno "
        "en el pupitre. El estudiante levanta la mano. Son las ocho de la mañana.",
        [
            {
                "question": "What does the teacher ask the class to do?",
                "options": ["Stand up", "Sit down", "Open the book", "Be quiet"],
                "answer": 1,
                "explanation": "Siéntense = Sit down.",
            },
            {
                "question": "What is on the student desk?",
                "options": [
                    "A backpack only",
                    "Three pens",
                    "Three pencils and a notebook",
                    "A folder and a book",
                ],
                "answer": 2,
                "explanation": "Hay tres lápices y un cuaderno.",
            },
            {
                "question": "What time is it?",
                "options": [
                    "It's 8:00 in the morning.",
                    "It's 8:00 at night.",
                    "It's 1:00 in the afternoon.",
                    "It's 10:00.",
                ],
                "answer": 0,
                "explanation": "Son las ocho de la mañana.",
            },
        ],
        topic="classroom",
    ),
    _reading(
        "me-gusta-nadar",
        "Me gusta nadar",
        "En el verano hace calor. Me gusta nadar y montar en bicicleta. "
        "No me gusta cantar. ¿Qué te gusta hacer?",
        [
            {
                "question": "When does this happen?",
                "options": ["In winter", "In fall", "In summer", "On Monday"],
                "answer": 2,
                "explanation": "En el verano = In the summer.",
            },
            {
                "question": "What does the writer not like?",
                "options": ["Swimming", "Riding a bike", "Singing", "Heat"],
                "answer": 2,
                "explanation": "No me gusta cantar.",
            },
            {
                "question": "¿Qué te gusta hacer? means…",
                "options": [
                    "What is your name?",
                    "What do you like to do?",
                    "How are you?",
                    "What time is it?",
                ],
                "answer": 1,
                "explanation": "This is the Capítulo 1A question.",
            },
        ],
        topic="gustar",
    ),
    _reading(
        "soy-atletico",
        "Soy atlético",
        "Me llamo Arjun. Soy atlético y estudioso. Mi hermana es simpática. "
        "Ella es seria también. ¿Cómo eres tú?",
        [
            {
                "question": "How does Arjun describe himself?",
                "options": [
                    "Funny and lazy",
                    "Athletic and studious",
                    "Serious only",
                    "Reserved and impatient",
                ],
                "answer": 1,
                "explanation": "Soy atlético y estudioso.",
            },
            {
                "question": "Who is simpática?",
                "options": ["Arjun", "The teacher", "His sister", "A friend"],
                "answer": 2,
                "explanation": "Mi hermana es simpática. Feminine -a ending.",
            },
            {
                "question": "¿Cómo eres tú? is asking…",
                "options": [
                    "What is your name?",
                    "How old are you?",
                    "What are you like?",
                    "Where are you?",
                ],
                "answer": 2,
                "explanation": "¿Cómo eres? = What are you like?",
            },
        ],
        topic="personality",
    ),
    _reading(
        "buenos-dias",
        "Buenos días",
        "— Buenos días, señor. ¿Cómo está usted?\n"
        "— Muy bien, gracias. ¿Y usted?\n"
        "— Regular. Me duelen los pies. Hasta luego.",
        [
            {
                "question": "Why do they use usted?",
                "options": [
                    "They are friends",
                    "It is informal",
                    "One speaker is being formal with an adult",
                    "It means good-bye",
                ],
                "answer": 2,
                "explanation": "Señor + usted is the formal register.",
            },
            {
                "question": "How is the second speaker feeling?",
                "options": ["Very well", "So-so; his feet hurt", "Angry", "Hungry"],
                "answer": 1,
                "explanation": "Regular. Me duelen los pies.",
            },
            {
                "question": "Hasta luego means…",
                "options": ["Good morning", "See you later", "What's up?", "Please"],
                "answer": 1,
                "explanation": "Hasta luego = See you later.",
            },
        ],
        topic="feelings",
    ),
    _reading(
        "viernes",
        "El viernes",
        "Hoy es viernes. Son las tres de la tarde. Hace sol. "
        "Me gusta patinar con mi hermano. Mañana es sábado.",
        [
            {
                "question": "What day is tomorrow?",
                "options": ["Friday", "Sunday", "Saturday", "Monday"],
                "answer": 2,
                "explanation": "Mañana es sábado.",
            },
            {
                "question": "What does the writer like to do?",
                "options": ["Skate with his brother", "Watch TV", "Draw", "Sing"],
                "answer": 0,
                "explanation": "Me gusta patinar con mi hermano.",
            },
            {
                "question": "What is the weather like?",
                "options": ["Cloudy", "Snowing", "Sunny", "Windy"],
                "answer": 2,
                "explanation": "Hace sol = It's sunny.",
            },
        ],
        topic="calendar",
    ),
]


def sentences_for_topic(topic_id: str) -> list[dict[str, Any]]:
    if topic_id in ("daily", ""):
        return list(SENTENCE_PROMPTS)
    matched = [s for s in SENTENCE_PROMPTS if s["topic"] == topic_id]
    return matched or list(SENTENCE_PROMPTS)


def readings_for_topic(topic_id: str) -> list[dict[str, Any]]:
    if topic_id in ("daily", ""):
        return list(READINGS)
    matched = [r for r in READINGS if r["topic"] == topic_id]
    return matched or list(READINGS)
