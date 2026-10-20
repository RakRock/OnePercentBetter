"""Grade 7 History Unit 1: Medieval Asian Civilizations."""

from __future__ import annotations

import copy
import random
from pathlib import Path

QUIZ_SIZE = 12
UNIT_QUIZ_SIZE = QUIZ_SIZE

UNIT = {
    "id": 1,
    "name": "Medieval Asian Civilizations",
    "emoji": "🏯",
    "color": "#b45309",
    "blurb": "Tang and Song China, then feudal Japan and the samurai",
}

TOPICS: list[dict] = [
    {"id": "china", "name": "China"},
    {"id": "japan", "name": "Japan"},
]

NOTES_DIR = Path(__file__).resolve().parent / "ArjunHistory" / "notes" / "unit_1"

LESSONS: list[dict] = [
    {
        "id": "china",
        "chapter": 1,
        "title": "The Golden Eras of China",
        "emoji": "👑",
        "file": "chapter_1_china.md",
        "topic_ids": ["china"],
    },
    {
        "id": "japan",
        "chapter": 2,
        "title": "The Land of the Samurai",
        "emoji": "⚔️",
        "file": "chapter_2_japan.md",
        "topic_ids": ["japan"],
    },
]


def _mc(question_id: int, topic: str, question: str, options: list[str], explanation: str) -> dict:
    return {
        "id": question_id,
        "topic": topic,
        "question": question,
        "options": options,
        "answer": 0,
        "explanation": explanation,
    }


QUESTIONS: list[dict] = [
    _mc(1, 'china', 'Which dynasty is famous for stabilizing the Silk Road and expanding the Grand Canal?', ['Tang Dynasty', 'Qin Dynasty', 'Han Dynasty', 'Zhou Dynasty'], "The Tang Dynasty expanded China's infrastructure and re-secured international trade routes."),
    _mc(2, 'china', 'What did a Chinese citizen have to pass to earn a coveted job as a government scholar-official?', ['The Civil Service Exam', 'A horse-riding duel', 'A physical endurance test', 'An art tournament'], "The civil service exams tested a candidate's knowledge of Confucian texts and classic literature."),
    _mc(3, 'china', 'The civil service exams in Tang and Song China were based primarily on the teachings of which philosopher?', ['Confucius', 'Laozi', 'Buddha', 'Aristotle'], 'Confucianism emphasized social duty hierarchy respect and moral integrity in government.'),
    _mc(4, 'china', 'What unique economic tool was invented during the Song Dynasty to replace heavy metal coins?', ['Paper Money', 'Credit Cards', 'Wooden Tokens', 'Silver Bars'], "Song China issued the world's first government-backed paper cash system to aid merchants."),
    _mc(5, 'china', 'What military invention was created by accident by Chinese alchemists looking for an elixir of life?', ['Gunpowder', 'The Longbow', 'Iron Armor', 'The Catapult'], 'Gunpowder was discovered during the Tang era and eventually adapted for warfare.'),
    _mc(6, 'china', 'Which navigational tool was perfected during the Song Dynasty allowing sailors to navigate open oceans?', ['The Magnetic Compass', 'The Astrolabe', 'The Telescope', 'The Sundial'], 'The magnetic compass revolutionized sea travel by indicating true north independently of the stars.'),
    _mc(7, 'china', 'What printing technology allowed the Song Dynasty to mass-produce books and increase literacy?', ['Movable Type Printing', 'Clay Tablet Stamping', 'Digital Typeface', 'Papyrus Scroll Rolling'], 'Movable type allowed characters to be rearranged quickly dramatically accelerating book production.'),
    _mc(8, 'china', 'What staple crop experienced a massive production boom in southern China during the Song Dynasty?', ['Champa Rice', 'Wheat', 'Barley', 'Potatoes'], 'Fast-ripening Champa rice allowed farmers to harvest two crops a year doubling the population.'),
    _mc(9, 'china', 'How did the development of Champa rice directly affect the population of China?', ['It caused the population to double', 'It caused widespread famine', 'It made everyone leave the cities', 'It decreased the population significantly'], "A steady food surplus from double-harvest rice caused China's population to surge over 100 million."),
    _mc(10, 'china', 'What was the main purpose of expanding the Grand Canal system?', ['To transport northern armies and southern rice easily', 'To provide a scenic path for the emperor', 'To create a barrier against ocean pirates', 'To drain water away from crop fields'], 'The Grand Canal linked major river networks connecting agricultural south China with political north China.'),
    _mc(11, 'china', "What name was given to the highly educated ruling class selected via China's strict exam system?", ['Scholar-Officials', 'Samurai Lords', 'Pharaohs', 'Feudal Vassals'], 'Scholar-officials ran the daily bureaucracy of China based on intellectual merit rather than family wealth.'),
    _mc(12, 'china', 'Which industry became a massive state-run manufacturing success producing fine pottery for export?', ['Porcelain', 'Glassblowing', 'Weaving Wool', 'Papyrus Manufacturing'], "Thin delicate porcelain (often called 'china') became a highly prized global luxury trade good."),
    _mc(13, 'china', "What trade path connected China's capital city directly to marketplaces in Europe and the Middle East?", ['The Silk Road', 'The Appian Way', 'The Amber Route', 'The Northwest Passage'], 'The Silk Road was an overland network of trade routes protected by successive Chinese dynasties.'),
    _mc(14, 'china', 'What major religious and philosophical system spread from India into China along trade paths?', ['Buddhism', 'Hinduism', 'Judaism', 'Shintoism'], 'Buddhism gained widespread popularity in China during times of instability offering spiritual comfort.'),
    _mc(15, 'china', 'What architectural structure did the Tang and Song dynasties fortify to protect northern borders?', ['The Great Wall', 'The Colosseum', 'The Taj Mahal', 'The Parthenon'], 'China constantly repaired and extended the Great Wall to guard against nomadic steppe invaders.'),
    _mc(16, 'china', 'The Song Dynasty split into Northern and Southern eras because of invasions by which group?', ['The Jurchen (Jin Dynasty)', 'The Roman Legions', 'The British Navy', 'The Egyptian Caliphate'], 'Northern nomadic groups captured the capital forcing the Song court to relocate south.'),
    _mc(17, 'china', 'What luxury fabric material was kept a closely guarded secret in China for centuries?', ['Silk', 'Cotton', 'Wool', 'Linen'], 'Silk manufacturing from silkworm cocoons was a highly guarded industrial state secret.'),
    _mc(18, 'china', 'What social practice involving restructuring feet became common among wealthy women during the Song era?', ['Foot-binding', 'Toe-stretching', 'Heel-clipping', 'Ankle-braiding'], 'Foot-binding was a painful restrictive custom that reflected upper-class standards of beauty and status.'),
    _mc(19, 'china', 'What primary philosophy focused on creating harmony through poetry painting and landscapes in China?', ['Daoism', 'Legalism', 'Stoicism', 'Scholasticism'], 'Daoism encouraged artists to focus on nature balance and the flow of the universe.'),
    _mc(20, 'china', 'Which dynasty emerged directly after the fall of the Tang Dynasty before the Song stabilized things?', ['The Five Dynasties and Ten Kingdoms period', 'The Ming Dynasty', 'The Qing Dynasty', 'The Yuan Dynasty'], 'A brief period of political fragmentation occurred between the fall of Tang and the rise of Song.'),
    _mc(21, 'china', 'What did Chinese scholar-officials use to record government accounts on a massive scale?', ['Paper made from mulberry bark', 'Parchment made from sheepskin', 'Clay bricks', 'Wax tablets'], 'The invention of lightweight paper allowed Chinese bureaucracy to keep extensive written files.'),
    _mc(22, 'china', 'What core value did Confucianism say was the most important within a family unit?', ['Filial Piety (respecting parents)', 'Individual Independence', 'Military Glory', 'Wealth Accumulation'], 'Filial piety demanded children show absolute respect obedience and care toward parents and ancestors.'),
    _mc(23, 'china', "What urban feature characterized capitals like Tang Chang'an and Southern Song Hangzhou?", ['Massive populations grids and bustling night markets', 'Complete lack of safety walls', 'No trade businesses allowed', 'Total abandonment of houses'], 'Chinese capitals were highly organized crowded centers of global trade and entertainment.'),
    _mc(24, 'china', 'What did China use to clear the Grand Canal of mud and keep it navigable?', ['Advanced engineering dredges and locks', 'Manual labor with spoons', 'Nothing it filled with sand', 'Foreign magic tricks'], 'Chinese engineers developed sophisticated water gates locks and maintenance systems to keep canals open.'),
    _mc(25, 'china', 'What did the invention of movable type do to the cost of purchasing books?', ['It made books much cheaper and accessible', 'It made books completely illegal to own', 'It multiplied the price by ten', 'It had no effect on book costs'], 'Mass production lowered printing costs allowing more regular citizens to buy books and learn.'),
    _mc(26, 'china', 'What did the Song Dynasty use to protect their coastline and shipping routes from naval pirates?', ['A permanent standing state navy', 'A wall built across the ocean', 'A fleet of hot air balloons', 'Nothing they abandoned the coast'], "Song China established the world's first permanent professional navy to guard maritime commerce."),
    _mc(27, 'china', 'What lightweight white ceramic did Chinese craftspeople create using kaolin clay?', ['Porcelain', 'Terracotta', 'Pewter', 'Lead Glass'], 'Porcelain was fired at incredibly high temperatures to create highly durable elegant luxury vessels.'),
    _mc(28, 'china', 'What moral philosophy experienced a revival during the Song era adding spiritual ideas to traditional family rules?', ['Neo-Confucianism', 'Legalism', 'Zen Buddhism', 'Stoicism'], 'Neo-Confucianism blended traditional social ethics with Buddhist and Daoist spiritual concepts.'),
    _mc(29, 'china', 'What system did the Grand Canal use to lift boats safely up and down sloped landscapes?', ['Pound Locks', 'Water Wheels', 'Rope Cranes', 'Steam Elevators'], 'Pound locks allowed water levels to be raised or lowered within a chamber to shift boats over hills.'),
    _mc(30, 'china', 'What happened to the layout of Chinese cities as trade boomed during the Song era?', ['They abandoned strict curfew rules and opened bustling 24-hour shops', 'They became completely empty ghost towns', 'They banned all merchants from entering city walls', 'They tore down all houses to grow more rice'], 'Cities transformed from rigid closed administrative zones into vibrant open commercial landscapes.'),
    _mc(31, 'japan', 'Who held the supreme military and political power in Feudal Japan?', ['The Shogun', 'The Emperor', 'The Pharaoh', 'The Sultan'], 'The Shogun was the military dictator who ran the country while the emperor acted as a figurehead.'),
    _mc(32, 'japan', 'What was the role of the Emperor in Feudal Japan?', ['He was a religious figurehead with little real political power', 'He commanded all the battlefield armies directly', 'He made all the daily laws and taxes', 'He was elected by the peasants every four years'], 'The Emperor was respected as a spiritual symbol but held virtually no actual governing authority.'),
    _mc(33, 'japan', 'What was the name of the wealthy land-owning warlords who controlled private regional estates?', ['Daimyo', 'Samurai', 'Griots', 'Vassals'], 'Daimyo were powerful nobles who answered to the Shogun and controlled vast lands.'),
    _mc(34, 'japan', 'What was the name of the elite hereditary class of warriors who protected the Daimyo?', ['Samurai', 'Knights', 'Gladiators', 'Janissaries'], 'Samurai were skilled swordsmen who served as the private military forces of the Daimyo.'),
    _mc(35, 'japan', "What strict code of conduct guided every aspect of a Samurai's life and honor?", ['Bushido', 'Chivalry', 'Sharia', 'The Magna Carta'], "Bushido or 'Way of the Warrior' demanded total loyalty bravery discipline and honor."),
    _mc(36, 'japan', 'What does the word Bushido translate to in English?', ['The Way of the Warrior', 'The Power of the Sword', 'The Peace of the Mind', 'The Law of the Land'], "Bushido translates directly to 'The Way of the Warrior' defining samurai conduct."),
    _mc(37, 'japan', 'What traditional native religion of Japan focuses on worshipping nature spirits called kami?', ['Shintoism', 'Buddhism', 'Daoism', 'Confucianism'], 'Shinto is the indigenous spirituality of Japan centered on purity nature and ancestral spirits.'),
    _mc(38, 'japan', 'Which branch of Buddhism became highly popular among Samurai due to its focus on meditation and mental control?', ['Zen Buddhism', 'Theravada Buddhism', 'Tibetan Buddhism', 'Pure Land Buddhism'], 'Zen Buddhism emphasized mental discipline and focus which helped warriors stay calm on the battlefield.'),
    _mc(39, 'japan', 'What basic geographic feature made unifying Japan difficult for ancient rulers?', ['It is an archipelago composed of thousands of mountainous islands', 'It is a flat landlocked desert plain', 'It is a single massive river delta', 'It is connected directly to mainland Europe by land'], "Japan's mountainous island geography naturally isolated regions leading to local warlord control."),
    _mc(40, 'japan', 'At the bottom of the feudal Japanese social pyramid which group was surprisingly ranked below peasants?', ['Merchants', 'Farmers', 'Samurai', 'Artisans'], "Merchants were ranked lowest because they did not produce anything themselves; they only sold other people's goods."),
    _mc(41, 'japan', 'What weapon was considered the literal soul of a Samurai warrior?', ['The Katana sword', 'The Crossbow', 'The Iron Mace', 'The Halberd'], "The katana was a finely crafted curved steel sword that symbolized a samurai's rank and honor."),
    _mc(42, 'japan', 'What style of theater featuring slow stylized movements and masks developed in medieval Japan?', ['Noh Theater', 'Broadway Theater', 'Opera Theater', 'Kabuki Pop Theater'], 'Noh theater was a classical musical drama favored by the samurai elite and nobility.'),
    _mc(43, 'japan', "What famous female author wrote The Tale of Genji considered the world's first novel?", ['Murasaki Shikibu', 'Empress Wu', 'Ban Zhao', 'Sei Shonagon'], 'Lady Murasaki wrote this classic masterpiece detailing court life during the Heian period.'),
    _mc(44, 'japan', 'What twice-occurring natural disaster destroyed invading Mongol fleets and was named Kamikaze?', ['Typhoons', 'Earthquakes', 'Volcanic Eruptions', 'Blizzards'], "Massive storms wrecked Mongol ships saving Japan; the grateful people named them 'Kamikaze' or divine winds."),
    _mc(45, 'japan', 'What did a Samurai risk losing if they showed cowardice or failed their Daimyo?', ['Their honor and their life', 'Their horses only', 'Their collection of books', 'Their right to farm rice'], 'A samurai valued honor above all else; losing it meant facing complete social disgrace or ritual suicide.'),
    _mc(46, 'japan', 'What was a major difference between European knights and Japanese samurai?', ['Samurai studied poetry and calligraphy alongside fighting', 'Knights never used iron armor', 'Samurai fought exclusively on foot', 'Knights did not serve a specific lord'], 'Samurai culture blended intense martial skill with refined arts Zen meditation and literature.'),
    _mc(47, 'japan', 'What type of structure did Daimyo build to defend their territories from rival warlords?', ['Muted wood and stone castles', 'Brick pyramids', 'Underground trenches', 'Glass skyscrapers'], 'Daimyo built massive hillside fortresses and castles surrounded by moats for military defense.'),
    _mc(48, 'japan', 'What was the core duty of a peasant farmer within the Japanese feudal system?', ['To grow rice to feed the entire samurai and noble class', 'To travel abroad as a merchant', 'To manufacture iron swords for the shogun', 'To build ocean warships for the emperor'], 'Peasants worked the land providing the rice tax that sustained the non-working warrior class.'),
    _mc(49, 'japan', 'What period of Japanese history featured a complete breakdown of central power and constant civil war?', ['The Sengoku Period (Warring States)', 'The Edo Period', 'The Meiji Period', 'The Jomon Period'], 'The Sengoku period was an era of near-constant warfare among rival Daimyo for control of Japan.'),
    _mc(50, 'japan', 'What happened to merchants if they tried to act higher than their assigned social rank in Japan?', ['They faced severe punishments from the samurai class', "They were automatically elected to the Shogun's council", 'They were given free islands', 'Nothing because there were no social laws'], 'Sumptuary laws strictly regulated what clothes house types and items lower classes could use.'),
    _mc(51, 'japan', 'What short three-line poetic form focused on nature developed out of Japanese literary culture?', ['Haiku', 'Sonnet', 'Epic Stanza', 'Ballad'], 'Haiku emerged as a concise poetic expression tracking themes of nature and passing seasons.'),
    _mc(52, 'japan', 'What internal value did Zen Buddhism teach that made it useful during stressful military combat?', ['Self-discipline mental focus and overcoming the fear of death', 'The accumulation of gold coins', 'The art of building long stone walls', 'How to manufacture gunpowder explosives'], "Zen's rigorous meditation trains the mind to remain detached calm and focused during mortal danger."),
    _mc(53, 'japan', 'Who was the first official Shogun of Japan establishing the Kamakura Shogunate in 1192?', ['Minamoto no Yoritomo', 'Oda Nobunaga', 'Tokugawa Ieyasu', 'Toyotomi Hideyoshi'], 'Yoritomo seized military dominance and established the tradition of warrior-led governance.'),
    _mc(54, 'japan', 'What is the name of the sacred gate that marks the entrance to a Shinto shrine?', ['Torii Gate', 'Obelisk', 'Triumphal Arch', 'Ziggurat'], 'A Torii gate separates the secular regular world from the sacred space of nature spirits.'),
    _mc(55, 'japan', 'Why did Japanese feudalism last for hundreds of years without major changes?', ['The strict warrior class enforced stability and social boundaries', 'There were no weapons available', 'The Emperor banned all changes to laws', 'Peasants loved paying high rice taxes'], 'The rigid military power of the shogunate suppressed rebellions and strictly locked people into social roles.'),
    _mc(56, 'japan', 'What natural barriers kept Japan protected from foreign land invasions for centuries?', ['The rough seas and straits surrounding the islands', 'A giant stone wall built across the ocean', 'A ring of year-round active glaciers', 'A deep trench carved by hand'], "Japan's geographic isolation as an island archipelago made launching amphibious invasions extremely difficult."),
    _mc(57, 'japan', 'What classic text is considered a primary primary source detailing Heian court styles fashion and etiquette?', ['The Pillow Book', 'The Quran', 'The Magna Carta', 'The Prince'], "Sei Shonagon's 'The Pillow Book' offers a brilliant direct window into medieval court life."),
    _mc(58, 'japan', 'What role did women play in the literary culture of medieval Japan?', ['They wrote some of the greatest masterpiece novels and diaries using a simplified script', 'They were banned from learning how to speak', 'They were forced to become samurai generals', 'They ran all the government exam centers'], 'While men wrote in formal imported Chinese women utilized kana script to invent classic Japanese literature.'),
    _mc(59, 'japan', 'What occurred during the Ashikaga Shogunate regarding the power of regional warlords?', ['The central Shogun lost power and regional Daimyo became completely independent', 'The Shogun eliminated all weapons', 'The Emperor took total military control', 'Japan was successfully conquered by China'], 'The Ashikaga era was marked by high political decentralization and regional warfare.'),
    _mc(60, 'japan', 'What unique feature did Samurai armor have to protect them while keeping them mobile?', ['It was made of overlapping lacquered iron plates tied with silk cords', 'It was built from solid heavy blocks of concrete', 'It was made of light transparent glass', 'It was a simple tunic made of soft cotton'], 'Japanese armor was engineered for flexibility speed and deflecting arrows or sword cuts.'),
]


def _check_bank() -> None:
    ids = [question["id"] for question in QUESTIONS]
    if ids != list(range(1, len(QUESTIONS) + 1)):
        raise RuntimeError("Unit 1 questions must be numbered from 1")
    topic_ids = {topic["id"] for topic in TOPICS}
    for question in QUESTIONS:
        options = question["options"]
        if len(options) != 4 or len(set(options)) != 4:
            raise RuntimeError(f"Question {question['id']} needs four different choices")
        if question["answer"] != 0:
            raise RuntimeError(f"Question {question['id']} must store the correct choice first")
        if question["topic"] not in topic_ids:
            raise RuntimeError(f"Question {question['id']} has an unknown topic")


_check_bank()

_QUESTIONS_BY_TOPIC: dict[str, list[dict]] = {topic["id"]: [] for topic in TOPICS}
for _question in QUESTIONS:
    _QUESTIONS_BY_TOPIC[_question["topic"]].append(_question)

_LESSON_BY_ID = {lesson["id"]: lesson for lesson in LESSONS}


def lesson_by_id(lesson_id: str) -> dict:
    return _LESSON_BY_ID[str(lesson_id)]


def questions_for_topic(topic_id: str) -> list[dict]:
    return list(_QUESTIONS_BY_TOPIC[str(topic_id)])


def load_lesson_notes(lesson_id: str) -> str:
    lesson = lesson_by_id(lesson_id)
    return (NOTES_DIR / lesson["file"]).read_text(encoding="utf-8")


def load_review_notes() -> str:
    return (NOTES_DIR / "review.md").read_text(encoding="utf-8")


def _shuffle_question(question: dict, rng: random.Random) -> dict:
    item = copy.deepcopy(question)
    correct = item["options"][item["answer"]]
    options = list(item["options"])
    rng.shuffle(options)
    item["options"] = options
    item["answer"] = options.index(correct)
    return item


def build_quiz(*, unit_mix: bool = False, rng: random.Random | None = None, **_ignored) -> list[dict]:
    """Return a shuffled unit quiz. Does not change the stored bank."""
    if not unit_mix:
        return []
    picker = rng or random.Random()
    per_topic = max(1, QUIZ_SIZE // len(TOPICS))
    picked: list[dict] = []
    for topic in TOPICS:
        pool = questions_for_topic(topic["id"])
        picked.extend(picker.sample(pool, min(per_topic, len(pool))))
    picker.shuffle(picked)
    return [_shuffle_question(question, picker) for question in picked[:QUIZ_SIZE]]
