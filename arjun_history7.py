"""Grade 7 History for Arjun.

Unit 2 is The Rise of Islam: 100 multiple-choice questions across six topics.
The stored answer index is 0. Quiz builders shuffle the choices.
"""

from __future__ import annotations

import copy
import random
from pathlib import Path

GRADE = 7
SUBJECT = "History"
ACTIVITY_TYPE = "History"
TOPIC_QUIZ_SIZE = 8
UNIT_QUIZ_SIZE = 12

UNIT = {
    "id": 2,
    "name": "The Rise of Islam",
    "emoji": "🕌",
    "color": "#b45309",
    "blurb": "Arabia before Islam, Muhammad, the Five Pillars, the empire, and the Golden Age",
}

TOPICS: list[dict] = [
    {
        'id': 'geography',
        'name': 'Geography of the Arabian Peninsula',
        'emoji': '🏜️',
        'color': '#d97706',
        'blurb': 'Desert climate, oases, Mecca, and the trade routes that crossed Arabia',
    },
    {
        'id': 'muhammad',
        'name': 'Life of Muhammad',
        'emoji': '🕌',
        'color': '#0f766e',
        'blurb': 'Mecca, the revelations, the Hijrah, and the first Muslim community',
    },
    {
        'id': 'pillars',
        'name': 'The Five Pillars of Islam',
        'emoji': '⭐',
        'color': '#7c3aed',
        'blurb': 'Shahada, prayer, zakat, Ramadan, and the Hajj',
    },
    {
        'id': 'empire',
        'name': 'Spread of the Islamic Empire',
        'emoji': '🗺️',
        'color': '#b45309',
        'blurb': 'Caliphs, the Umayyads and Abbasids, and how trade carried the faith',
    },
    {
        'id': 'split',
        'name': "The Division Between Sunnis and Shi'as",
        'emoji': '⚖️',
        'color': '#1d4ed8',
        'blurb': 'Who should lead after Muhammad, Karbala, and what both branches share',
    },
    {
        'id': 'golden',
        'name': 'Islamic Golden Age & Achievements',
        'emoji': '📚',
        'color': '#be123c',
        'blurb': 'Algebra, medicine, the House of Wisdom, and art from Baghdad to Spain',
    },
]

QUESTIONS: list[dict] = [
    {
        'id': 1,
        'topic': 'geography',
        'question': 'What type of climate is most dominant across the Arabian Peninsula?',
        'options': ['Desert / Arid', 'Tropical Rainforest', 'Arctic Tundra', 'Mediterranean'],
        'answer': 0,
        'explanation': 'The harsh climate heavily influenced trade and nomadic travel patterns.',
    },
    {
        'id': 2,
        'topic': 'geography',
        'question': 'What are the fertile green spots in a desert where water is found called?',
        'options': ['Oases', 'Bazaars', 'Glaciers', 'Plateaus'],
        'answer': 0,
        'explanation': 'Oases allowed agriculture and towns to grow in the middle of deserts.',
    },
    {
        'id': 3,
        'topic': 'geography',
        'question': 'Which peninsula serves as a land bridge connecting Africa, Asia, and Europe?',
        'options': ['Arabian Peninsula', 'Iberian Peninsula', 'Italian Peninsula', 'Scandinavian Peninsula'],
        'answer': 0,
        'explanation': 'Its location made it a crossroads for global trade.',
    },
    {
        'id': 4,
        'topic': 'geography',
        'question': 'What lifestyle did the nomadic Bedouins live in the Arabian desert?',
        'options': ['Moving from place to place with herds', 'Farming in permanent river valleys', 'Living in large coastal cities', 'Mining in mountain regions'],
        'answer': 0,
        'explanation': 'Nomads moved continuously to find water and grazing land for their animals.',
    },
    {
        'id': 5,
        'topic': 'geography',
        'question': 'Which body of water borders the western coast of the Arabian Peninsula?',
        'options': ['Red Sea', 'Mediterranean Sea', 'Atlantic Ocean', 'Pacific Ocean'],
        'answer': 0,
        'explanation': 'The Red Sea was an important maritime route for trade ships.',
    },
    {
        'id': 6,
        'topic': 'geography',
        'question': 'Why was the city of Mecca an important town before the rise of Islam?',
        'options': ['It was a major trade and religious center', 'It was the capital of the Roman Empire', 'It was famous for its large silver mines', 'It was an isolated mountain fortress'],
        'answer': 0,
        'explanation': 'Mecca sat at the intersection of trade routes and housed the Kaaba.',
    },
    {
        'id': 7,
        'topic': 'geography',
        'question': 'What was the primary method of transportation for traders crossing the Arabian desert?',
        'options': ['Camel caravans', 'Horse-drawn chariots', 'River boats', 'Steam locomotives'],
        'answer': 0,
        'explanation': 'Camels were well-adapted to survive long desert journeys with little water.',
    },
    {
        'id': 8,
        'topic': 'geography',
        'question': 'Which sea borders the eastern side of the Arabian Peninsula?',
        'options': ['Persian Gulf', 'Baltic Sea', 'Caribbean Sea', 'Black Sea'],
        'answer': 0,
        'explanation': 'The Persian Gulf connected Arabia to the Mesopotamian and Indian trade networks.',
    },
    {
        'id': 9,
        'topic': 'geography',
        'question': 'In pre-Islamic times, what was the function of the Kaaba in Mecca?',
        'options': ['A shrine holding statues of many gods', 'A palace for the Roman emperor', 'A fortress against the Persian army', 'A grand library for scholars'],
        'answer': 0,
        'explanation': 'The Kaaba originally housed hundreds of polytheistic tribal idols.',
    },
    {
        'id': 10,
        'topic': 'geography',
        'question': 'What are the seasonal winds that bring rain to parts of southern Arabia called?',
        'options': ['Monsoons', 'Tornados', 'Blizzards', 'Hurricanes'],
        'answer': 0,
        'explanation': 'Monsoons brought rain to places like Yemen, supporting farming.',
    },
    {
        'id': 11,
        'topic': 'geography',
        'question': 'How did the harsh desert geography affect the tribes of Arabia?',
        'options': ['They competed fiercely for water and pasture', 'They formed one single united kingdom', 'They stopped all forms of trading', 'They moved away to live in Europe'],
        'answer': 0,
        'explanation': 'Scarce resources led to regular conflicts among independent tribes.',
    },
    {
        'id': 12,
        'topic': 'geography',
        'question': 'Which city north of Mecca was an important oasis town known for agriculture?',
        'options': ['Medina (Yathrib)', 'Baghdad', 'Cairo', 'Cordoba'],
        'answer': 0,
        'explanation': 'Yathrib, later named Medina, was a fertile oasis town.',
    },
    {
        'id': 13,
        'topic': 'geography',
        'question': 'Why did towns develop primarily along the coastal edges of the Arabian Peninsula?',
        'options': ['The coasts had more rainfall and ports for trade', 'The interior deserts were rich in gold', 'The coasts were protected from all wind', 'The interior deserts were too cold to live in'],
        'answer': 0,
        'explanation': 'Coastal areas provided access to shipping routes and better farming conditions.',
    },
    {
        'id': 14,
        'topic': 'geography',
        'question': 'What do we call traders who travel together in large groups for safety across deserts?',
        'options': ['Caravans', 'Guilds', 'Fleets', 'Armadas'],
        'answer': 0,
        'explanation': 'Caravans protected merchants from bandits and harsh conditions.',
    },
    {
        'id': 15,
        'topic': 'geography',
        'question': 'What term describes people who settle down in towns and permanent structures?',
        'options': ['Sedentary', 'Nomadic', 'Migratory', 'Barbaric'],
        'answer': 0,
        'explanation': 'Sedentary Arabs lived in trading towns and farming oases.',
    },
    {
        'id': 16,
        'topic': 'muhammad',
        'question': 'In which year was the prophet Muhammad born in Mecca?',
        'options': ['570 CE', '476 CE', '632 CE', '800 CE'],
        'answer': 0,
        'explanation': 'Muhammad was born into the prominent Quraysh tribe in 570 CE.',
    },
    {
        'id': 17,
        'topic': 'muhammad',
        'question': 'What profession did Muhammad practice during his early adult life?',
        'options': ['Merchant / Trader', 'Blacksmith', 'Ship Captain', 'Gladiator'],
        'answer': 0,
        'explanation': 'He worked in the caravan trade and earned a reputation for honesty.',
    },
    {
        'id': 18,
        'topic': 'muhammad',
        'question': "Who was Muhammad's wife, a wealthy and respected businesswoman in Mecca?",
        'options': ['Khadijah', 'Fatima', 'Aisha', 'Mary'],
        'answer': 0,
        'explanation': 'Khadijah was his first wife and the first person to accept his teachings.',
    },
    {
        'id': 19,
        'topic': 'muhammad',
        'question': 'Where did Muhammad receive his first religious revelation in 610 CE?',
        'options': ['In a cave on Mount Hira', 'In the center of the Roman Colosseum', 'On top of the Egyptian pyramids', 'Inside the palace of the Persian king'],
        'answer': 0,
        'explanation': 'He was meditating in a cave when Muslims believe the angel Gabriel appeared to him.',
    },
    {
        'id': 20,
        'topic': 'muhammad',
        'question': "According to Islamic belief, which angel delivered God's revelations to Muhammad?",
        'options': ['Gabriel', 'Michael', 'Raphael', 'Uriel'],
        'answer': 0,
        'explanation': 'The angel Gabriel (Jibril) is believed to have delivered the messages over 23 years.',
    },
    {
        'id': 21,
        'topic': 'muhammad',
        'question': "Why did the wealthy merchants of Mecca initially reject Muhammad's message?",
        'options': ['They feared losing trade and religious pilgrims', 'They wanted to follow a leader from Europe', 'They disagreed with his stance on farming', 'They wanted him to declare himself an emperor'],
        'answer': 0,
        'explanation': 'Monotheism threatened their polytheistic shrines and profitable trade.',
    },
    {
        'id': 22,
        'topic': 'muhammad',
        'question': 'What is the Arabic word for the one supreme God in Islam?',
        'options': ['Allah', 'Yahweh', 'Brahma', 'Zeus'],
        'answer': 0,
        'explanation': 'Allah is the Arabic term for the single God worshipped in Abrahamic faiths.',
    },
    {
        'id': 23,
        'topic': 'muhammad',
        'question': 'What name was given to the city of Yathrib after it welcomed Muhammad and his followers?',
        'options': ['Medina', 'Mecca', 'Baghdad', 'Damascus'],
        'answer': 0,
        'explanation': "Medina translates to 'City of the Prophet'.",
    },
    {
        'id': 24,
        'topic': 'muhammad',
        'question': 'The migration from Mecca to Medina in 622 CE is known as the:',
        'options': ['Hijrah', 'Hajj', 'Jihad', 'Sharia'],
        'answer': 0,
        'explanation': 'The Hijrah marks the foundational moment and the start of the Islamic calendar.',
    },
    {
        'id': 25,
        'topic': 'muhammad',
        'question': 'Why is the year 622 CE chosen as Year 1 on the Islamic calendar?',
        'options': ['It marks the year of the Hijrah', 'It is the year Muhammad was born', 'It is the year Muhammad died', 'It marks the building of the Kaaba'],
        'answer': 0,
        'explanation': 'The migration established the first independent Muslim community (Ummah).',
    },
    {
        'id': 26,
        'topic': 'muhammad',
        'question': 'What is the name of the holy book that contains the revelations received by Muhammad?',
        'options': ['Quran', 'Torah', 'Vedas', 'Gita'],
        'answer': 0,
        'explanation': 'The Quran is considered the literal word of God by Muslims.',
    },
    {
        'id': 27,
        'topic': 'muhammad',
        'question': 'What are the recorded habits, actions, and sayings of Muhammad used as a guide called?',
        'options': ['Sunnah', 'Caliphate', 'Monotheism', 'Ramadan'],
        'answer': 0,
        'explanation': 'The Sunnah provides practical examples of how to follow Islamic laws.',
    },
    {
        'id': 28,
        'topic': 'muhammad',
        'question': 'When Muhammad and his followers returned to Mecca in 630 CE, what did they do to the Kaaba?',
        'options': ['They removed all polytheistic idols', 'They tore it down completely', 'They turned it into a Roman palace', 'They filled it with gold coins'],
        'answer': 0,
        'explanation': 'They dedicated it solely to the worship of one God.',
    },
    {
        'id': 29,
        'topic': 'muhammad',
        'question': 'In which year did the prophet Muhammad pass away in Medina?',
        'options': ['632 CE', '610 CE', '650 CE', '750 CE'],
        'answer': 0,
        'explanation': 'His death led to questions about who would succeed him as leader of the community.',
    },
    {
        'id': 30,
        'topic': 'muhammad',
        'question': "What term describes the belief in only one God, which is central to Muhammad's message?",
        'options': ['Monotheism', 'Polytheism', 'Animism', 'Atheism'],
        'answer': 0,
        'explanation': 'Islam is strictly a monotheistic religion, sharing roots with Judaism and Christianity.',
    },
    {
        'id': 31,
        'topic': 'pillars',
        'question': 'How many baseline duties form the framework of worship and daily life in Islam?',
        'options': ['Five', 'Ten', 'Seven', 'Three'],
        'answer': 0,
        'explanation': 'These are known globally as the Five Pillars of Islam.',
    },
    {
        'id': 32,
        'topic': 'pillars',
        'question': 'What is the first pillar, Shahada, which represents the profession of faith?',
        'options': ['Declaring belief in one God and Muhammad as His prophet', 'Praying five times a day', 'Giving money to the poor', 'Fasting during a holy month'],
        'answer': 0,
        'explanation': 'It is the essential creed required to enter the Islamic faith.',
    },
    {
        'id': 33,
        'topic': 'pillars',
        'question': 'How many times a day are Muslims traditionally expected to perform ritual prayers?',
        'options': ['Five times', 'One time', 'Three times', 'Seven times'],
        'answer': 0,
        'explanation': 'The daily prayers (Salat) are performed at fixed times throughout the day.',
    },
    {
        'id': 34,
        'topic': 'pillars',
        'question': 'In which direction must all Muslims face when performing their daily prayers?',
        'options': ['Toward the Kaaba in Mecca', 'Toward the rising sun in the east', 'Toward the city of Jerusalem', 'Toward the capital city of Baghdad'],
        'answer': 0,
        'explanation': 'The Kaaba serves as the unified focal point for global prayers.',
    },
    {
        'id': 35,
        'topic': 'pillars',
        'question': 'What is the purpose of the third pillar, Zakat (almsgiving)?',
        'options': ['To give a portion of wealth to help the poor and needy', 'To pay taxes for military expansion', 'To buy luxury items for mosques', 'To fund exploration voyages'],
        'answer': 0,
        'explanation': 'Zakat is a compulsory act of charity meant to ease economic inequality.',
    },
    {
        'id': 36,
        'topic': 'pillars',
        'question': 'During which holy month do Muslims fast from dawn until sunset?',
        'options': ['Ramadan', 'Dhul-Hijjah', 'Muharram', 'Safara'],
        'answer': 0,
        'explanation': 'Ramadan is the ninth month of the Islamic lunar calendar.',
    },
    {
        'id': 37,
        'topic': 'pillars',
        'question': 'What is the Arabic word for the religious obligation to fast during Ramadan?',
        'options': ['Sawm', 'Salat', 'Shahada', 'Hajj'],
        'answer': 0,
        'explanation': 'Sawm requires abstaining from food, drink, and negative behaviors during daylight hours.',
    },
    {
        'id': 38,
        'topic': 'pillars',
        'question': 'What is the fifth pillar of Islam, known as the Hajj?',
        'options': ['A pilgrimage to Mecca', 'A journey to Jerusalem', 'A declaration of holy war', 'A daily charity donation'],
        'answer': 0,
        'explanation': 'Every Muslim who is physically and financially able must perform Hajj once in their lifetime.',
    },
    {
        'id': 39,
        'topic': 'pillars',
        'question': 'What special white clothing do pilgrims wear during the Hajj to show equality?',
        'options': ['Ihram', 'Turban', 'Tunic', 'Toga'],
        'answer': 0,
        'explanation': 'The simple white garments eliminate visible distinctions of wealth or social status.',
    },
    {
        'id': 40,
        'topic': 'pillars',
        'question': 'What is a Muslim house of worship called?',
        'options': ['Mosque', 'Synagogue', 'Cathedral', 'Temple'],
        'answer': 0,
        'explanation': 'Mosques serve as community hubs, schools, and places for prayer.',
    },
    {
        'id': 41,
        'topic': 'pillars',
        'question': 'What is the term for the call to prayer chanted by a muezzin?',
        'options': ['Adhan', 'Khutbah', 'Hajj', 'Zakat'],
        'answer': 0,
        'explanation': 'The Adhan signals to believers that it is time for ritual prayer.',
    },
    {
        'id': 42,
        'topic': 'pillars',
        'question': 'What is the name of the tower on a mosque from which the call to prayer is made?',
        'options': ['Minaret', 'Dome', 'Obelisk', 'Spire'],
        'answer': 0,
        'explanation': 'Minarets are prominent architectural features of traditional mosques.',
    },
    {
        'id': 43,
        'topic': 'pillars',
        'question': 'Who traditionally leads the community in prayers inside a mosque?',
        'options': ['Imam', 'Caliph', 'Sultan', 'Emperor'],
        'answer': 0,
        'explanation': 'An Imam is a spiritual leader who guides congregational prayers.',
    },
    {
        'id': 44,
        'topic': 'pillars',
        'question': 'On which day of the week do Muslims gather for congregational Friday prayers?',
        'options': ['Friday', 'Sunday', 'Saturday', 'Wednesday'],
        'answer': 0,
        'explanation': 'Friday afternoon prayers (Jummah) include a sermon alongside ritual worship.',
    },
    {
        'id': 45,
        'topic': 'pillars',
        'question': 'What is the sermon delivered during Friday congregational prayers called?',
        'options': ['Khutbah', 'Sunnah', 'Sharia', 'Hadith'],
        'answer': 0,
        'explanation': 'The Khutbah offers moral, spiritual, or community guidance.',
    },
    {
        'id': 46,
        'topic': 'pillars',
        'question': 'What ritual washing must Muslims perform before they begin their prayers?',
        'options': ['Wudu', 'Zakat', 'Sawm', 'Hijrah'],
        'answer': 0,
        'explanation': 'Wudu involves cleaning hands, face, arms, and feet to ensure physical cleanliness.',
    },
    {
        'id': 47,
        'topic': 'pillars',
        'question': 'What lifecycle event does a Muslim celebrate at the conclusion of Ramadan?',
        'options': ['Eid al-Fitr', 'Eid al-Adha', 'The Hijrah', 'Mawlid'],
        'answer': 0,
        'explanation': 'Eid al-Fitr is the festival of breaking the fast, celebrated with feasts and charity.',
    },
    {
        'id': 48,
        'topic': 'pillars',
        'question': 'What festival marks the conclusion of the annual Hajj pilgrimage?',
        'options': ['Eid al-Adha', 'Eid al-Fitr', 'Ramadan', 'The Hijrah'],
        'answer': 0,
        'explanation': 'Eid al-Adha is the Festival of Sacrifice, honoring the obedience of Abraham.',
    },
    {
        'id': 49,
        'topic': 'pillars',
        'question': 'What percentage of surplus wealth is traditionally given for Zakat?',
        'options': ['2.5%', '10%', '5%', '1%'],
        'answer': 0,
        'explanation': 'Muslims typically give 2.5% of their accumulated savings annually.',
    },
    {
        'id': 50,
        'topic': 'pillars',
        'question': 'Why do Muslims practice fasting during the month of Ramadan?',
        'options': ['To practice self-discipline and remember the less fortunate', 'To prepare for military training', 'To protest against the government', 'To save money on groceries'],
        'answer': 0,
        'explanation': 'Fasting builds empathy for the hungry and fosters spiritual focus.',
    },
    {
        'id': 51,
        'topic': 'empire',
        'question': "What title, meaning 'successor', was given to the political and religious leaders after Muhammad?",
        'options': ['Caliph', 'Pharaoh', 'Tsar', 'Sultan'],
        'answer': 0,
        'explanation': 'The caliphs led the unified Muslim community (Caliphate).',
    },
    {
        'id': 52,
        'topic': 'empire',
        'question': "What are the first four caliphs who ruled after Muhammad's death collectively called?",
        'options': ['The Rightly Guided Caliphs', 'The Umayyad Dynasty', 'The Abbasid Dynasty', 'The Ottoman Emperors'],
        'answer': 0,
        'explanation': 'They knew Muhammad personally and followed his example closely.',
    },
    {
        'id': 53,
        'topic': 'empire',
        'question': 'Which dynasty took power in 661 CE and moved the capital of the empire to Damascus?',
        'options': ['Umayyad Dynasty', 'Abbasid Dynasty', 'Fatimid Dynasty', 'Mughal Dynasty'],
        'answer': 0,
        'explanation': 'The Umayyads oversaw major territorial expansion into North Africa and Spain.',
    },
    {
        'id': 54,
        'topic': 'empire',
        'question': 'To which Syrian city did the Umayyad Dynasty move the capital of the Islamic Empire?',
        'options': ['Damascus', 'Baghdad', 'Cairo', 'Mecca'],
        'answer': 0,
        'explanation': 'Damascus provided a more central location to govern the expanding Mediterranean lands.',
    },
    {
        'id': 55,
        'topic': 'empire',
        'question': 'Which dynasty overthrew the Umayyads in 750 CE and moved the capital to Baghdad?',
        'options': ['Abbasid Dynasty', 'Ottoman Dynasty', 'Safavid Dynasty', 'Byzantine Dynasty'],
        'answer': 0,
        'explanation': 'The Abbasids focused more on trade, culture, and science than conquests.',
    },
    {
        'id': 56,
        'topic': 'empire',
        'question': 'What famous capital city was built by the Abbasids along the Tigris River?',
        'options': ['Baghdad', 'Constantinople', 'Rome', 'Alexandria'],
        'answer': 0,
        'explanation': 'Baghdad became the center of the Islamic Golden Age.',
    },
    {
        'id': 57,
        'topic': 'empire',
        'question': 'Which European country was known as Al-Andalus under Muslim rule for centuries?',
        'options': ['Spain', 'France', 'Germany', 'Italy'],
        'answer': 0,
        'explanation': 'Muslim forces crossed from North Africa into the Iberian Peninsula in 711 CE.',
    },
    {
        'id': 58,
        'topic': 'empire',
        'question': 'Which famous battle in 732 CE halted the advance of Muslim armies into Western Europe?',
        'options': ['Battle of Tours', 'Battle of Hastings', 'Battle of Waterloo', 'Battle of Marathon'],
        'answer': 0,
        'explanation': 'Charles Martel led the Frankish forces to victory against an Umayyad army in France.',
    },
    {
        'id': 59,
        'topic': 'empire',
        'question': 'What language became the official language of government, trade, and religion across the empire?',
        'options': ['Arabic', 'Latin', 'Greek', 'Sanskrit'],
        'answer': 0,
        'explanation': 'A shared language helped unify diverse cultures and accelerated trade.',
    },
    {
        'id': 60,
        'topic': 'empire',
        'question': 'What was the special tax paid by non-Muslims who wished to retain their own religions?',
        'options': ['Jizya', 'Zakat', 'Tribute', 'Tariff'],
        'answer': 0,
        'explanation': 'The jizya allowed religious minorities protection and freedom of worship.',
    },
    {
        'id': 61,
        'topic': 'empire',
        'question': "What status, meaning 'protected people', was given to Jews and Christians under Islamic rule?",
        'options': ['Dhimmi', 'Bedouin', 'Caliph', 'Janissary'],
        'answer': 0,
        'explanation': 'Dhimmis had legal rights and protection in exchange for paying the jizya.',
    },
    {
        'id': 62,
        'topic': 'empire',
        'question': "Why did the Quran refer to Jews and Christians as 'People of the Book'?",
        'options': ['Because they also followed monotheistic scriptures', 'Because they invented the first printing press', 'Because they worked primarily as librarians', 'Because they only read books instead of trading'],
        'answer': 0,
        'explanation': 'Islam respects previous Abrahamic revelations found in the Torah and Bible.',
    },
    {
        'id': 63,
        'topic': 'empire',
        'question': 'Which two long-standing empires were weak and exhausted, allowing the early Caliphate to expand?',
        'options': ['Byzantine and Persian Empires', 'Roman and Carthaginian Empires', 'Spanish and British Empires', 'Mongol and Chinese Empires'],
        'answer': 0,
        'explanation': 'Decades of fighting each other left these two empires vulnerable to Arab forces.',
    },
    {
        'id': 64,
        'topic': 'empire',
        'question': 'How did trade networks help spread the religion of Islam beyond imperial borders?',
        'options': ['Merchants shared their faith while doing business in distant lands', 'Governments banned all non-Muslim goods', 'Traders forced customers to convert to buy items', 'Ships refused to sail to non-Muslim ports'],
        'answer': 0,
        'explanation': 'Trade routes carried ideas, culture, and faith to places like West Africa and Southeast Asia.',
    },
    {
        'id': 65,
        'topic': 'empire',
        'question': 'What major administrative reform helped the Umayyad Caliphate manage its vast lands?',
        'options': ['Creating a unified currency and language for government', 'Allowing every city to make its own laws', 'Banning all forms of communication between cities', 'Giving up control of all territories outside Arabia'],
        'answer': 0,
        'explanation': 'Coinage and Arabic records streamlined trade and taxation across provinces.',
    },
    {
        'id': 66,
        'topic': 'empire',
        'question': 'Which North African nomadic people converted to Islam and formed the main army that entered Spain?',
        'options': ['Berbers', 'Vikings', 'Mongols', 'Franks'],
        'answer': 0,
        'explanation': 'The Berbers became key actors in the culture and history of Islamic Spain.',
    },
    {
        'id': 67,
        'topic': 'empire',
        'question': 'What Spanish city became a brilliant center of culture, literacy, and tolerance in Al-Andalus?',
        'options': ['Cordoba', 'Madrid', 'Paris', 'London'],
        'answer': 0,
        'explanation': 'Cordoba featured paved streets, streetlights, and a massive library while Europe was in the Dark Ages.',
    },
    {
        'id': 68,
        'topic': 'empire',
        'question': 'What term describes the system of law based on the Quran and Sunnah that developed in the empire?',
        'options': ['Sharia', 'Code of Hammurabi', 'Twelve Tables', 'Magna Carta'],
        'answer': 0,
        'explanation': 'Sharia outlines moral duties, legal codes, and daily behaviors for Muslims.',
    },
    {
        'id': 69,
        'topic': 'empire',
        'question': 'How did the expansion of the empire impact global commerce?',
        'options': ['It connected trade routes from China to Europe under a single network', 'It stopped all maritime trading completely', 'It caused a worldwide shortage of paper', 'It outlawed the use of gold and silver coins'],
        'answer': 0,
        'explanation': 'The Pax Islamica allowed merchants to travel safely across safe, continuous trade routes.',
    },
    {
        'id': 70,
        'topic': 'empire',
        'question': 'What happened to local cultures in places conquered by the Islamic Empire?',
        'options': ['They blended with Arabic culture, leading to cultural synthesis', 'They were completely erased overnight', 'They were forced to migrate to northern Europe', 'They stopped speaking languages entirely'],
        'answer': 0,
        'explanation': 'Conquered regions retained local elements while adopting aspects of Arabic culture and language.',
    },
    {
        'id': 71,
        'topic': 'split',
        'question': "What was the root cause of the split between Sunni and Shi'a Muslims?",
        'options': ['A dispute over who should lead the Muslim community after Muhammad', 'A disagreement over the direction of prayer', 'A conflict regarding the language of the Quran', 'An economic dispute over camel trading'],
        'answer': 0,
        'explanation': "The debate over rightful leadership began immediately following the Prophet's death.",
    },
    {
        'id': 72,
        'topic': 'split',
        'question': "Who did the Shi'a believe was the rightful first successor to Muhammad?",
        'options': ['Ali ibn Abi Talib', 'Abu Bakr', 'Umar ibn al-Khattab', 'Uthman ibn Affan'],
        'answer': 0,
        'explanation': "Shi'as believed leadership belonged to Muhammad's family line, starting with his son-in-law and cousin, Ali.",
    },
    {
        'id': 73,
        'topic': 'split',
        'question': 'Who was chosen as the very first caliph by a consensus of early Muslim leaders?',
        'options': ['Abu Bakr', 'Ali', 'Umar', 'Muawiyah'],
        'answer': 0,
        'explanation': 'Abu Bakr was a close friend and father-in-law of Muhammad, supported by the majority (Sunnis).',
    },
    {
        'id': 74,
        'topic': 'split',
        'question': 'Which branch of Islam makes up the vast majority (about 85-90%) of Muslims worldwide today?',
        'options': ['Sunni', "Shi'a", 'Sufi', 'Kharijite'],
        'answer': 0,
        'explanation': 'The Sunnis follow the tradition of selecting leaders by community consensus.',
    },
    {
        'id': 75,
        'topic': 'split',
        'question': "The word 'Shi'a' comes from an Arabic phrase that translates to what?",
        'options': ['Party or Faction of Ali', 'Followers of the Sunnah', 'People of the Desert', 'Scholars of the Book'],
        'answer': 0,
        'explanation': "Shi'at Ali means the supporters or faction of Ali.",
    },
    {
        'id': 76,
        'topic': 'split',
        'question': "The word 'Sunni' is derived from a term meaning what?",
        'options': ["Followers of the Prophet's tradition", 'Descendants of the family', 'Rulers of the city', 'Fighters of the desert'],
        'answer': 0,
        'explanation': 'Sunnis emphasize following the Sunnah (customs/traditions) of Muhammad.',
    },
    {
        'id': 77,
        'topic': 'split',
        'question': "Which tragic battle in 680 CE sealed the emotional and permanent divide between Sunnis and Shi'as?",
        'options': ['Battle of Karbala', 'Battle of Tours', 'Battle of the Trench', 'Battle of Yarmouk'],
        'answer': 0,
        'explanation': "The martyrdom of Muhammad's grandson, Hussein, at Karbala is a defining moment for Shi'as.",
    },
    {
        'id': 78,
        'topic': 'split',
        'question': "Who was the grandson of Muhammad whose death at Karbala is mourned annually by Shi'a Muslims?",
        'options': ['Hussein ibn Ali', 'Abu Bakr', 'Muawiyah', 'Harun al-Rashid'],
        'answer': 0,
        'explanation': 'Hussein refused to pledge allegiance to the Umayyad caliph, leading to his death.',
    },
    {
        'id': 79,
        'topic': 'split',
        'question': "What is the name of the annual day of mourning observed by Shi'a Muslims to remember Hussein?",
        'options': ['Ashura', 'Ramadan', 'Eid', 'Hijrah'],
        'answer': 0,
        'explanation': 'Ashura features solemn processions and historical reenactments of the battle.',
    },
    {
        'id': 80,
        'topic': 'split',
        'question': "How did the Umayyad Caliphate handle the supporters of Ali's family line?",
        'options': ['They persecuted them to maintain political control', 'They gave them complete control of the empire', "They converted to Shi'a Islam themselves", 'They moved the capital to Medina to please them'],
        'answer': 0,
        'explanation': "The Umayyads suppressed Shi'a uprisings to protect their dynastic power.",
    },
    {
        'id': 81,
        'topic': 'split',
        'question': "What title did Shi'as historically use for their infallible spiritual leaders?",
        'options': ['Imam', 'Emperor', 'Pope', 'King'],
        'answer': 0,
        'explanation': "To Shi'as, the Imam represents an divinely guided leader from the Prophet's bloodline.",
    },
    {
        'id': 82,
        'topic': 'split',
        'question': 'What do Sunnis believe regarding the personal qualities of their political caliphs?',
        'options': ['They are human leaders who can make mistakes', 'They are divine beings with magical powers', 'They must always be direct descendants of Ali', 'They are directly appointed by angels'],
        'answer': 0,
        'explanation': 'Sunnis view caliphs as political protectors of the law, not infallible religious figures.',
    },
    {
        'id': 83,
        'topic': 'split',
        'question': "Which country in modern times has the largest Shi'a-majority population?",
        'options': ['Iran', 'Saudi Arabia', 'Egypt', 'Indonesia'],
        'answer': 0,
        'explanation': "Iran has been the center of Shi'a political and religious thought for centuries.",
    },
    {
        'id': 84,
        'topic': 'split',
        'question': "Despite their split over leadership, what core book do both Sunnis and Shi'as read?",
        'options': ['The Quran', 'The Torah', 'The Code of Justinian', 'The Analects'],
        'answer': 0,
        'explanation': 'Both branches share the same foundational holy scripture and pillars.',
    },
    {
        'id': 85,
        'topic': 'split',
        'question': 'Which mystical movement in Islam focused on personal, direct spiritual experience rather than politics?',
        'options': ['Sufism', 'Sunni', "Shi'a", 'Wahhabism'],
        'answer': 0,
        'explanation': 'Sufis use meditation, poetry, and chanting to grow closer to God.',
    },
    {
        'id': 86,
        'topic': 'golden',
        'question': 'What mathematical system was pioneered by scholar al-Khwarizmi during the Golden Age?',
        'options': ['Algebra', 'Calculus', 'Geometry', 'Statistics'],
        'answer': 0,
        'explanation': "Al-Khwarizmi wrote a textbook on solving equations, giving us the word 'algebra'.",
    },
    {
        'id': 87,
        'topic': 'golden',
        'question': 'What numerical system did Muslim scholars adopt from India and introduce to Europe?',
        'options': ['Arabic numerals (0-9)', 'Roman numerals (I, V, X)', 'Hieroglyphics', 'Binary code'],
        'answer': 0,
        'explanation': 'This system included the crucial concept of zero, making math much simpler.',
    },
    {
        'id': 88,
        'topic': 'golden',
        'question': 'What was the name of the famous library and research academy established in Baghdad?',
        'options': ['House of Wisdom', 'Library of Alexandria', 'Academy of Athens', 'British Museum'],
        'answer': 0,
        'explanation': 'The House of Wisdom hosted scholars who translated global knowledge into Arabic.',
    },
    {
        'id': 89,
        'topic': 'golden',
        'question': 'Which navigation instrument was perfected by Muslim scientists to measure the positions of stars?',
        'options': ['Astrolabe', 'Compass', 'Barometer', 'Telescope'],
        'answer': 0,
        'explanation': 'The astrolabe helped sailors navigate open seas and find the direction of Mecca.',
    },
    {
        'id': 90,
        'topic': 'golden',
        'question': "Which famous Muslim doctor wrote 'The Canon of Medicine', a standard textbook for centuries?",
        'options': ['Ibn Sina (Avicenna)', 'Al-Khwarizmi', 'Ibn Battuta', 'Omar Khayyam'],
        'answer': 0,
        'explanation': 'Ibn Sina diagnosed diseases like tuberculosis and advanced pharmaceutical sciences.',
    },
    {
        'id': 91,
        'topic': 'golden',
        'question': 'Why did Islamic artists avoid painting human or animal figures in religious art?',
        'options': ['To avoid idolatry and honor the unseen nature of God', 'Because they did not know how to draw people', 'Because paints were too expensive to make', 'Because the government banned all colorful art'],
        'answer': 0,
        'explanation': 'Artists developed geometric and floral patterns instead of realistic figures.',
    },
    {
        'id': 92,
        'topic': 'golden',
        'question': 'What style of beautiful, decorative handwriting was perfected during the Golden Age?',
        'options': ['Calligraphy', 'Hieroglyphic', 'Cuneiform', 'Graffiti'],
        'answer': 0,
        'explanation': 'Calligraphy was widely used to copy the Quran and decorate mosque walls.',
    },
    {
        'id': 93,
        'topic': 'golden',
        'question': 'What art form features complex, repeating geometric designs resembling plant leaves and stems?',
        'options': ['Arabesque', 'Mosaic', 'Fresco', 'Sculpture'],
        'answer': 0,
        'explanation': 'Arabesque art reflects the infinite nature of God through symmetric patterns.',
    },
    {
        'id': 94,
        'topic': 'golden',
        'question': 'What practical technology did Muslims adopt from China that revolutionized libraries and books?',
        'options': ['Paper making', 'Woodblock printing', 'The printing press', 'Digital typing'],
        'answer': 0,
        'explanation': 'Paper mills in Baghdad made books cheap, plentiful, and widely accessible.',
    },
    {
        'id': 95,
        'topic': 'golden',
        'question': 'Which famous Muslim traveler spent 30 years exploring Africa, Asia, and Europe?',
        'options': ['Ibn Battuta', 'Marco Polo', 'Christopher Columbus', 'Zheng He'],
        'answer': 0,
        'explanation': 'He logged over 73,000 miles, documenting medieval Islamic societies.',
    },
    {
        'id': 96,
        'topic': 'golden',
        'question': 'In what field of science did Ibn al-Haytham make breakthroughs by studying lenses and light?',
        'options': ['Optics', 'Geology', 'Botany', 'Zoology'],
        'answer': 0,
        'explanation': 'He is considered a pioneer of the scientific method and camera mechanics.',
    },
    {
        'id': 97,
        'topic': 'golden',
        'question': 'What was a major architectural hallmark of medieval Islamic palaces and mosques?',
        'options': ['Grand domes and pointed arches', 'Pyramids with steps', 'Skyscrapers made of iron', 'Log cabins with chimneys'],
        'answer': 0,
        'explanation': 'Domes and arches distributed weight effectively, allowing for vast open indoor spaces.',
    },
    {
        'id': 98,
        'topic': 'golden',
        'question': 'How did Golden Age scholars help save ancient Greek and Roman philosophy?',
        'options': ['They translated texts into Arabic, protecting them from destruction', 'They buried all original scrolls in desert caves', 'They sold the books to kings in northern Europe', 'They memorized them without ever writing them down'],
        'answer': 0,
        'explanation': 'When European libraries fell, these Arabic translations preserved crucial classical knowledge.',
    },
    {
        'id': 99,
        'topic': 'golden',
        'question': 'What were the bustling, open-air marketplaces in Islamic cities called?',
        'options': ['Bazaars (or Souks)', 'Guilds', 'Forums', 'Manors'],
        'answer': 0,
        'explanation': 'Bazaars were international economic hubs filled with silks, spices, and paper.',
    },
    {
        'id': 100,
        'topic': 'golden',
        'question': 'Which collection of folk tales and stories includes characters like Aladdin and Sinbad?',
        'options': ['One Thousand and One Nights', 'The Odyssey', 'The Epic of Gilgamesh', "Aesop's Fables"],
        'answer': 0,
        'explanation': 'This compilation reflected the diverse, cosmopolitan cultures of the Abbasid Empire.',
    },
]


_TOPIC_BY_ID = {topic["id"]: topic for topic in TOPICS}
_QUESTIONS_BY_TOPIC: dict[str, list[dict]] = {topic["id"]: [] for topic in TOPICS}
for _question in QUESTIONS:
    _QUESTIONS_BY_TOPIC[_question["topic"]].append(_question)


def _check_bank() -> None:
    ids = [question["id"] for question in QUESTIONS]
    if ids != list(range(1, 101)):
        raise RuntimeError("History Unit 2 questions must be numbered 1 through 100")
    if set(_QUESTIONS_BY_TOPIC) != set(_TOPIC_BY_ID):
        raise RuntimeError("Every topic needs a question list")
    for question in QUESTIONS:
        options = question["options"]
        if len(options) != 4 or len(set(options)) != 4:
            raise RuntimeError(f"Question {question['id']} needs four different choices")
        if question["answer"] != 0:
            raise RuntimeError(f"Question {question['id']} must store the correct choice first")
        if not question["question"].strip() or not question["explanation"].strip():
            raise RuntimeError(f"Question {question['id']} needs a question and an explanation")
        if question["topic"] not in _TOPIC_BY_ID:
            raise RuntimeError(f"Question {question['id']} has an unknown topic")


_check_bank()


def topic_by_id(topic_id: str) -> dict:
    return _TOPIC_BY_ID[str(topic_id)]


def questions_for_topic(topic_id: str) -> list[dict]:
    return list(_QUESTIONS_BY_TOPIC[str(topic_id)])


def question_counts() -> dict[str, int]:
    return {topic_id: len(items) for topic_id, items in _QUESTIONS_BY_TOPIC.items()}


def _shuffle_question(question: dict, rng: random.Random) -> dict:
    item = copy.deepcopy(question)
    correct = item["options"][item["answer"]]
    options = list(item["options"])
    rng.shuffle(options)
    item["options"] = options
    item["answer"] = options.index(correct)
    return item


def build_quiz(
    *,
    topic_id: str | None = None,
    full_topic: bool = False,
    unit_mix: bool = False,
    rng: random.Random | None = None,
) -> list[dict]:
    """Return a shuffled quiz. Does not change the stored question bank."""
    picker = rng or random.Random()
    if topic_id is not None:
        pool = questions_for_topic(topic_id)
        if not pool:
            return []
        if full_topic:
            picked = list(pool)
            picker.shuffle(picked)
        else:
            picked = picker.sample(pool, min(TOPIC_QUIZ_SIZE, len(pool)))
    elif unit_mix:
        picked = []
        per_topic = UNIT_QUIZ_SIZE // len(TOPICS)
        for topic in TOPICS:
            pool = questions_for_topic(topic["id"])
            picked.extend(picker.sample(pool, min(per_topic, len(pool))))
        picker.shuffle(picked)
    else:
        return []
    return [_shuffle_question(question, picker) for question in picked]


NOTES_DIR = Path(__file__).resolve().parent / "ArjunHistory" / "notes" / "unit_2"

LESSONS: list[dict] = [
    {
        "id": "geography",
        "chapter": 1,
        "title": "The Giant Sandbox",
        "subtitle": "The geography of the Arabian Peninsula",
        "emoji": "🐪",
        "file": "chapter_1_geography.md",
        "topic_ids": ["geography"],
    },
    {
        "id": "muhammad",
        "chapter": 2,
        "title": "The Honest Merchant",
        "subtitle": "The Prophet Muhammad",
        "emoji": "📜",
        "file": "chapter_2_muhammad.md",
        "topic_ids": ["muhammad"],
    },
    {
        "id": "pillars",
        "chapter": 3,
        "title": "The 5 Rules of the Game",
        "subtitle": "The Five Pillars of Islam",
        "emoji": "🖐️",
        "file": "chapter_3_pillars.md",
        "topic_ids": ["pillars"],
    },
    {
        "id": "empire",
        "chapter": 4,
        "title": "The Expanding Empire and the Big Disagreement",
        "subtitle": "Caliphs, trade, and Sunni and Shi'a",
        "emoji": "👑",
        "file": "chapter_4_empire.md",
        "topic_ids": ["empire", "split"],
    },
    {
        "id": "golden",
        "chapter": 5,
        "title": "Unlocking Achievements",
        "subtitle": "The Islamic Golden Age",
        "emoji": "🔬",
        "file": "chapter_5_golden_age.md",
        "topic_ids": ["golden"],
    },
]

_LESSON_BY_ID = {lesson["id"]: lesson for lesson in LESSONS}
_LESSON_BY_TOPIC = {
    topic_id: lesson["id"]
    for lesson in LESSONS
    for topic_id in lesson["topic_ids"]
}


def lesson_by_id(lesson_id: str) -> dict:
    return _LESSON_BY_ID[str(lesson_id)]


def lesson_for_topic(topic_id: str) -> dict:
    return lesson_by_id(_LESSON_BY_TOPIC[str(topic_id)])


def load_lesson_notes(lesson_id: str) -> str:
    lesson = lesson_by_id(lesson_id)
    return (NOTES_DIR / lesson["file"]).read_text(encoding="utf-8")


def load_review_notes() -> str:
    return (NOTES_DIR / "review.md").read_text(encoding="utf-8")


def list_units() -> list[dict]:
    import arjun_history_unit3 as unit3

    cards = []
    for content in (_self(), unit3):
        unit = content.UNIT
        cards.append(
            {
                "id": unit["id"],
                "name": unit["name"],
                "emoji": unit["emoji"],
                "color": unit["color"],
                "blurb": unit["blurb"],
                "questions": len(content.QUESTIONS),
            }
        )
    return cards


def content_for(unit_id: int):
    import arjun_history_unit3 as unit3

    if int(unit_id) == 3:
        return unit3
    if int(unit_id) == 2:
        return _self()
    raise KeyError(unit_id)


def _self():
    import sys

    return sys.modules[__name__]
