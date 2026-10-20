"""Grade 7 History Unit 3: Gold and Salt Kingdoms of West Africa."""

from __future__ import annotations

import copy
import random
from pathlib import Path

QUIZ_SIZE = 12
UNIT_QUIZ_SIZE = QUIZ_SIZE

UNIT = {
    "id": 3,
    "name": "The Gold and Salt Kingdoms of West Africa",
    "emoji": "🦁",
    "color": "#b45309",
    "blurb": "Sahara trade, Ghana, Mali, Songhai, and the griots who remembered it all",
}

TOPICS: list[dict] = [
    {'id': 'geography', 'name': 'Geography'},
    {'id': 'trade', 'name': 'Trade'},
    {'id': 'ghana', 'name': 'Ghana'},
    {'id': 'mali', 'name': 'Mali'},
    {'id': 'songhai', 'name': 'Songhai'},
    {'id': 'culture', 'name': 'Culture'},
]

NOTES_DIR = Path(__file__).resolve().parent / "ArjunHistory" / "notes" / "unit_3"

LESSONS: list[dict] = [
    {
        "id": "geography",
        "chapter": 1,
        "title": "The Ultimate Sandbox Trade",
        "emoji": "🐪",
        "file": "chapter_1_geography.md",
        "topic_ids": ["geography"],
    },
    {
        "id": "ghana",
        "chapter": 2,
        "title": "Ghana, the Middlemen",
        "emoji": "👑",
        "file": "chapter_2_ghana.md",
        "topic_ids": ["ghana"],
    },
    {
        "id": "mali",
        "chapter": 3,
        "title": "Mali and the Lion King",
        "emoji": "🦁",
        "file": "chapter_3_mali.md",
        "topic_ids": ["mali"],
    },
    {
        "id": "songhai",
        "chapter": 4,
        "title": "Songhai and the War Canoes",
        "emoji": "🛶",
        "file": "chapter_4_songhai.md",
        "topic_ids": ["songhai"],
    },
    {
        "id": "culture",
        "chapter": 5,
        "title": "Griots, the Living Libraries",
        "emoji": "🪕",
        "file": "chapter_5_griots.md",
        "topic_ids": ["culture"],
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
    _mc(1, 'geography', 'Which massive desert covers most of North and West Africa and is rich in rock salt mines?', ['Sahara Desert', 'Kalahari Desert', 'Gobi Desert', 'Mojave Desert'], 'The Sahara Desert spans North and West Africa and was a major source of salt.'),
    _mc(2, 'geography', 'Which river was the main trade highway and water source for Ghana Mali and Songhai?', ['Niger River', 'Nile River', 'Congo River', 'Zambezi River'], 'The Niger River was the economic lifeline for travel and farming in West Africa.'),
    _mc(3, 'geography', 'What animal revolutionized trans-Saharan trade because it can travel for days without water?', ['Arabian Camel', 'Water Buffalo', 'Donkey', 'Clydesdale Horse'], 'Camels have special adaptations that allow them to traverse harsh deserts easily.'),
    _mc(4, 'geography', 'Which vegetation zone consists of flat semi-arid grasslands just south of the desert?', ['The Sahel', 'The Rain Forest', 'The Tundra', 'The Alpine Peaks'], 'The Sahel and Savanna are flat grasslands between the dry desert and wet forests.'),
    _mc(5, 'trade', 'What secret method allowed traders to exchange gold and salt safely without speaking?', ['Silent Barter', 'Open Auction', 'Digital Exchange', 'Barter Token System'], 'Silent barter used drums and designated drop spots to negotiate trade safely.'),
    _mc(6, 'ghana', 'The Ghana Empire became incredibly wealthy primarily by doing what?', ['Taxing traders passing through', 'Mining all the salt themselves', 'Invading European nations', 'Manufacturing silk garments'], 'Ghana acted as a middleman and charged taxes on all gold and salt caravans.'),
    _mc(7, 'ghana', 'The King of Ghana decreed that regular citizens could only buy and trade what?', ['Gold dust', 'Solid gold nuggets', 'Silver coins', 'Iron bars'], 'The king claimed solid gold nuggets for himself to prevent gold from losing value.'),
    _mc(8, 'ghana', 'What metals did Ghana use to make powerful weapons that easily defeated neighbors?', ['Iron', 'Bronze', 'Copper', 'Aluminium'], 'Ghana used iron weapons which were much stronger than the stone or wood tools of neighbors.'),
    _mc(9, 'ghana', 'What was the name of the famous capital city of the Ghana Empire?', ['Koumbi Saleh', 'Timbuktu', 'Gao', 'Taghaza'], 'Koumbi Saleh was the bustling dual-capital city of ancient Ghana.'),
    _mc(10, 'ghana', "Why was Ghana's capital city split into two separate halves?", ['To keep Muslim merchants separate from the king', 'To divide the rich from the poor', 'To keep the army away from citizens', 'To separate the gold from the salt'], 'One half was for the African king and the other was a town for Muslim traders.'),
    _mc(11, 'ghana', 'What valuable resource did merchants from North Africa bring south across the desert?', ['Salt', 'Silk', 'Porcelain', 'Potatoes'], 'North African traders brought large slabs of rock salt mined in the desert.'),
    _mc(12, 'ghana', 'Where did the gold that was traded in Ghana come from?', ['The southern forest mines of Wangara', 'The northern desert mines of Taghaza', 'The banks of the Nile River', 'The mountains of Europe'], 'Gold was mined secretly in the southern forest regions of Wangara.'),
    _mc(13, 'ghana', 'Why was salt considered just as valuable as gold in ancient West Africa?', ['It preserved food and kept people hydrated', 'It was used to make shiny royal jewelry', 'It was used to build strong fortress walls', 'It was used as fuel for cooking fires'], 'Salt was vital for preserving meat and replacing sweat lost in hot climates.'),
    _mc(14, 'ghana', 'What group of Muslim invaders from North Africa attacked Ghana in the 1000s CE?', ['Almoravids', 'Romans', 'Mongols', 'Vikings'], 'The Almoravids launched a holy war against Ghana which weakened the empire.'),
    _mc(15, 'ghana', 'What led to the final collapse and decline of the Ghana Empire?', ['Overgrazing herds and enemy invasions', 'A massive ice age', 'The sudden discovery of electricity', 'A giant volcanic eruption'], "Overgrazing ruined farmland and foreign invasions weakened Ghana's power."),
    _mc(16, 'mali', 'According to West African oral history who was the legendary founder of Mali?', ['Sundiata Keita', 'Mansa Musa', 'Sunni Ali', 'Askia Muhammad'], 'Sundiata Keita overcame physical disabilities to unite his people and form Mali.'),
    _mc(17, 'mali', 'What nickname was given to the legendary emperor Sundiata Keita?', ['The Lion King', 'The Desert Fox', 'The Iron Emperor', 'The Great Navigator'], 'Sundiata was called the Lion King due to his strength and leadership.'),
    _mc(18, 'mali', 'At which historic battle did Sundiata defeat the cruel king of the Sosso people?', ['Battle of Kirina', 'Battle of Tours', 'Battle of Hastings', 'Battle of Marathon'], 'Sundiata won the Battle of Kirina in 1235 CE to establish the Mali Empire.'),
    _mc(19, 'mali', 'What does the title Mansa translate to in the language of ancient Mali?', ['Emperor or King', 'Priest', 'General', 'Chief Merchant'], 'Mansa was the supreme title used by the rulers of the Mali Empire.'),
    _mc(20, 'mali', 'Which famous ruler of Mali is considered the wealthiest individual in world history?', ['Mansa Musa', 'Sundiata Keita', 'Sunni Ali', 'Askia Muhammad'], 'Mansa Musa accumulated unmatched wealth by controlling West African gold trade.'),
    _mc(21, 'mali', 'In what year did Mansa Musa make his famous religious pilgrimage to Mecca?', ['1324 CE', '1066 CE', '1492 CE', '1776 CE'], 'Mansa Musa made his legendary journey across Africa to Mecca in 1324 CE.'),
    _mc(22, 'mali', 'What religion did Mansa Musa practice and help spread throughout West Africa?', ['Islam', 'Christianity', 'Buddhism', 'Hinduism'], 'Mansa Musa was a devout Muslim who built mosques and universities.'),
    _mc(23, 'mali', 'What city did Mansa Musa transform into a global center of Islamic learning?', ['Timbuktu', 'Koumbi Saleh', 'Gao', 'Taghaza'], 'Mansa Musa turned Timbuktu into an intellectual hub famous for its books.'),
    _mc(24, 'mali', "What happened to the economy of Cairo because of Mansa Musa's visit?", ['Gold lost its value causing inflation', 'The city completely ran out of food', 'Silver became the new currency', 'The city built a massive wall'], 'Mansa Musa gave away so much free gold that its value crashed for over ten years.'),
    _mc(25, 'mali', 'What was the name of the famous university built in Timbuktu?', ['University of Sankore', 'Oxford University', 'Harvard Academy', 'House of Wisdom'], 'The University of Sankore attracted scholars from all over the world.'),
    _mc(26, 'mali', 'How many camels did Mansa Musa bring on his famous trip to Mecca?', ['Between 80 and 100 loaded with gold', 'Exactly five', 'More than ten thousand', 'None because he walked'], 'Mansa Musa traveled with a caravan that included about 80 to 100 gold-carrying camels.'),
    _mc(27, 'mali', 'What did Mansa Musa bring back to Mali from his trip to Mecca?', ['Arab architects and scholars', 'A massive army of knights', 'Sacks of rare desert diamonds', 'A fleet of war ships'], 'Mansa Musa brought back scholars and architects to build new mosques and schools.'),
    _mc(28, 'mali', 'What major trade goods allowed Mali to become even richer than Ghana?', ['Gold salt and agricultural crops', 'Silk tea and fine porcelain', 'Iron spices and cedar wood', 'Glass beads and woolen blankets'], 'Mali controlled both the gold-salt trade and rich farming along the Niger River.'),
    _mc(29, 'mali', 'What language became the main language of government and education in Mali?', ['Arabic', 'Latin', 'English', 'Spanish'], 'Arabic became the dominant language for writing and schooling due to Islamic influence.'),
    _mc(30, 'mali', 'What caused the Mali Empire to eventually weaken and lose power?', ['Weak leadership and attacks by raiders', 'The invention of steam engines', 'A massive global drought', 'An attack by Roman gladiators'], 'Later kings could not protect the borders and nomadic raiders captured key cities.'),
    _mc(31, 'songhai', 'Which empire rose to power as the third great kingdom of West Africa?', ['Songhai', 'Ghana', 'Axum', 'Kush'], 'The Songhai Empire broke away from Mali and became the largest of the three kingdoms.'),
    _mc(32, 'songhai', 'Who was the fierce military general who founded the Songhai Empire?', ['Sunni Ali', 'Mansa Musa', 'Sundiata Keita', 'Askia the Great'], 'Sunni Ali conquered neighboring lands to build the foundation of Songhai.'),
    _mc(33, 'songhai', 'What was the primary capital city of the Songhai Empire?', ['Gao', 'Timbuktu', 'Koumbi Saleh', 'Taghaza'], 'The city of Gao served as the central capital of the Songhai Empire.'),
    _mc(34, 'songhai', 'What special military force did Sunni Ali use to control the Niger River?', ['A navy of armored war canoes', 'A fleet of hot air balloons', 'A pack of trained crocodiles', 'A row of stone bridges'], 'Sunni Ali built a powerful fleet of war canoes to secure river trade routes.'),
    _mc(35, 'songhai', 'Which important city did Sunni Ali capture from Tuareg invaders in 1468?', ['Timbuktu', 'Cairo', 'Mecca', 'Marrakesh'], 'Sunni Ali recaptured Timbuktu and restored its status as a trading hub.'),
    _mc(36, 'songhai', "Who overthrew Sunni Ali's son to become the greatest peaceful ruler of Songhai?", ['Askia Muhammad', 'Sundiata Keita', 'Mansa Musa', 'King Ezana'], 'Askia Muhammad took control and focused on laws education and government.'),
    _mc(37, 'songhai', 'What title did Askia Muhammad take to show his political and religious leadership?', ['Askia', 'Mansa', 'Pharaoh', 'Caliph'], 'He took the title Askia to establish his new ruling dynasty.'),
    _mc(38, 'songhai', 'How did Askia Muhammad make trading fairer across the Songhai Empire?', ['He standardized weights and measures', 'He banned the use of gold dust', 'He made all items free on Fridays', 'He only allowed trading at night'], 'He made sure all marketplaces used the same scales so buyers were not cheated.'),
    _mc(39, 'songhai', 'How did Askia Muhammad organize his massive empire to run smoothly?', ['He divided it into provinces with loyal governors', 'He made everyone live in the capital', 'He let every town make its own laws', 'He banned all government jobs'], 'He used a system of local provinces and governors to manage the large territory.'),
    _mc(40, 'songhai', 'What country sent an army across the desert to attack Songhai in 1591?', ['Morocco', 'Egypt', 'Spain', 'Italy'], 'Morocco invaded Songhai to capture its valuable gold mines.'),
    _mc(41, 'songhai', 'What new weapon allowed the Moroccan army to easily defeat Songhai?', ['Gunpowder muskets and cannons', 'Iron broadswords', 'Crossbows', 'Chariots'], "Morocco brought early firearms which completely overwhelmed Songhai's traditional weapons."),
    _mc(42, 'songhai', 'At what historic battle was the Songhai Empire finally defeated?', ['Battle of Tondibi', 'Battle of Kirina', 'Battle of Tours', 'Battle of Waterloo'], 'The Moroccan army crushed Songhai forces at the Battle of Tondibi in 1591.'),
    _mc(43, 'songhai', 'What happened to Timbuktu after the Moroccan invasion?', ['Its scholars were captured and libraries ruined', 'It became the new capital of Spain', 'It disappeared into a sinkhole', 'It was turned into a massive farm'], 'The golden age of learning ended as scholars were arrested and books scattered.'),
    _mc(44, 'songhai', 'What geographic feature did the Songhai Empire use to transport its armies?', ['The Niger River', 'The Mediterranean Sea', 'The Atlantic Ocean', 'The Nile River'], "The Niger River was the main highway for Songhai's trade and war canoes."),
    _mc(45, 'songhai', 'What was the main religion of the ruling class in the Songhai Empire?', ['Islam', 'Christianity', 'Judaism', 'Buddhism'], 'Like Mali the emperors of Songhai were devout followers of Islam.'),
    _mc(46, 'culture', 'What is a Griot in traditional West African culture?', ['A storyteller and oral historian', 'A high-ranking military general', 'A person who mines rock salt', 'A type of river war canoe'], 'Griots were the keepers of history who memorized events and family trees.'),
    _mc(47, 'culture', 'Why were Griots so important to ancient West African societies?', ['They kept history alive without written books', 'They knew how to turn iron into weapons', 'They were the only ones who could find gold', 'They predicted the weather using the stars'], 'Since there was no written language Griots were the living history books.'),
    _mc(48, 'culture', 'What musical instrument is traditionally played by a Griot during a performance?', ['Kora', 'Sitar', 'Bagpipes', 'Piano'], 'The Kora is a 21-stringed instrument made from a large gourd.'),
    _mc(49, 'culture', 'How did someone become a Griot in West African traditions?', ['The job was passed down from parent to child', 'They were elected by a town vote', 'They had to find a solid gold nugget', 'They won a musical tournament'], 'Being a Griot was a hereditary profession passed down through families.'),
    _mc(50, 'culture', 'Which bright geometric cloth was traditionally woven strictly for West African royalty?', ['Kente cloth', 'Silk fabric', 'Tweed fabric', 'Burlap fabric'], 'Kente cloth features vibrant hand-woven patterns made for kings and leaders.'),
    _mc(51, 'geography', 'What is the name of the wet vegetation zone located south of the West African savannas?', ['The Rain Forest', 'The Sahara Desert', 'The Tundra', 'The Steppe'], 'The rain forest is dense and wet contrasting sharply with the dry northern desert.'),
    _mc(52, 'geography', 'Which major geographical zone is an area of tall grasses and scattered trees?', ['Savanna', 'Desert', 'Glacier', 'Swamp'], 'The savanna is the grassy plain where livestock and farming thrived in West Africa.'),
    _mc(53, 'trade', 'Why was the introduction of camels a game-changer for West Africa?', ['It connected West Africa to global trade networks', 'It allowed people to travel up rivers', 'It replaced the use of iron plows', 'It provided wool for making royal clothes'], 'Camels allowed merchants to cross the Sahara and trade with the Mediterranean world.'),
    _mc(54, 'trade', 'What did North African traders want to buy from West Africans more than anything else?', ['Gold', 'Salt', 'Ice', 'Wheat'], 'North African merchants traveled south specifically to obtain precious gold.'),
    _mc(55, 'trade', 'What did the southern forest dwellers need to buy from the northern traders?', ['Salt', 'Gold', 'Sand', 'Bananas'], 'Forest dwellers had plenty of gold but desperately needed salt to stay healthy.'),
    _mc(56, 'ghana', 'What was the main weapon material that gave Ghana an advantage over its neighbors?', ['Iron', 'Wood', 'Stone', 'Copper'], 'Iron spears and swords easily shattered the wooden weapons of rival tribes.'),
    _mc(57, 'ghana', 'What did the King of Ghana do with all the taxes he collected?', ['He maintained a large army and a grand court', 'He gave it all back to North Africans', 'He built a giant pyramid', 'He buried it in a secret desert cave'], 'Taxes paid for a massive military force that kept trade routes safe from bandits.'),
    _mc(58, 'ghana', 'How did the spread of Islam change the way government worked in Ghana?', ['Kings began using written Arabic for records', 'Kings stopped collecting trade taxes', 'Kings moved their capitals to Mecca', 'Kings banned the use of iron weapons'], 'Muslim scholars taught the government how to keep written books and records in Arabic.'),
    _mc(59, 'ghana', 'What did regular citizens of Ghana use as a form of money in the marketplace?', ['Gold dust', 'Solid gold bricks', 'Paper dollars', 'Plastic cards'], 'While the king kept gold nuggets regular people used measured gold dust to buy goods.'),
    _mc(60, 'ghana', 'What resource was mined at the desert settlement of Taghaza?', ['Salt', 'Gold', 'Diamonds', 'Coal'], 'Taghaza was a miserable desert town where slaves mined giant slabs of salt.'),
    _mc(61, 'mali', 'What happened to the size of the empire when Mali took over from Ghana?', ['Mali grew much larger than Ghana ever was', 'Mali shrank to the size of a single village', 'Mali stayed the exact same size', 'Mali moved completely to North Africa'], 'Mali conquered Ghana and expanded to control nearly all of West Africa.'),
    _mc(62, 'mali', 'What was the original homeland and ethnic group of the founders of Mali?', ['The Malinke people', 'The Egyptian people', 'The Roman people', 'The Berber people'], 'The Malinke or Mandinka people formed the core of the Mali Empire.'),
    _mc(63, 'mali', 'What does the word Mali mean in its native language?', ['Where the king lives', 'The mountain of gold', 'The land of salt', 'The river highway'], 'Mali translates roughly to the place where the king or master resides.'),
    _mc(64, 'mali', 'How did Mansa Musa support education throughout his empire?', ['He built schools libraries and universities', 'He banned books and closed local markets', 'He made school free only for soldiers', 'He forced everyone to study algebra'], 'Mansa Musa turned cities like Timbuktu into famous learning centers full of books.'),
    _mc(65, 'mali', 'What architectural feature did Mansa Musa introduce to West African mosques?', ['Earthen domes and towering minarets', 'Glass windows and marble columns', 'Wooden log cabins', 'Stone pyramids'], 'Mansa Musa hired architects to design grand mosques with unique clay towers.'),
    _mc(66, 'mali', 'Who was the famous Muslim traveler who wrote a book about his visit to Mali?', ['Ibn Battuta', 'Marco Polo', 'Christopher Columbus', 'Zheng He'], 'Ibn Battuta traveled across Mali and wrote about its safe roads and justice system.'),
    _mc(67, 'mali', 'What did Ibn Battuta admire most about the people of Mali?', ['Their dedication to justice and safe roads', 'Their skills at building wooden castles', 'Their ability to speak fluent Latin', 'Their large fleet of ocean ships'], 'Ibn Battuta praised Mali because travelers had no fear of being robbed by bandits.'),
    _mc(68, 'mali', 'What valuable crop did farmers grow in abundance along the fertile Niger River?', ['Cotton', 'Sugar cane', 'Potatoes', 'Corn'], 'Cotton became a major crop used to weave clothing for the empire.'),
    _mc(69, 'mali', 'What did the people of Mali use to build their homes and mosques?', ['Mud and wooden beams', 'Solid gold blocks', 'Ice blocks', 'Imported marble'], 'They developed a unique style using sun-dried mud bricks reinforced with wooden poles.'),
    _mc(70, 'mali', "What external group began capturing Mali's border towns as the empire grew weak?", ['Tuareg raiders', 'Roman legions', 'Spanish conquistadors', 'British explorers'], 'Tuareg nomads from the Sahara desert took advantage of weak kings and seized cities.'),
    _mc(71, 'songhai', 'Before becoming a massive empire Songhai was originally a province of which kingdom?', ['Mali', 'Ghana', 'Egypt', 'Rome'], 'Songhai was once a smaller territory controlled by the rulers of Mali.'),
    _mc(72, 'songhai', 'What city did Sunni Ali conquer in 1473 that was known for its wealthy markets?', ['Jenne', 'Cairo', 'Rome', 'London'], 'Sunni Ali captured Jenne securing total control over regional trade networks.'),
    _mc(73, 'songhai', 'Why did Sunni Ali spend his entire reign fighting battles on horseback?', ["To expand and defend his new empire's borders", 'To find a magical fountain of youth', 'To escape from his capital city', 'To compete in international races'], 'Sunni Ali was a constantly moving warrior king who never lost a battle.'),
    _mc(74, 'songhai', "What did Askia Muhammad do to guarantee his empire's religious standing?", ['He completed a grand pilgrimage to Mecca', 'He forced everyone to become a monk', 'He moved the capital to Jerusalem', 'He banned all religious holidays'], 'Askia Muhammad went to Mecca to gain support from global Islamic leaders.'),
    _mc(75, 'songhai', "What group of people held high positions in Askia Muhammad's government?", ['Scholars and judges', 'Foreign gladiators', 'Roman senators', 'Nomadic bandits'], 'Askia filled his courts with educated lawyers judges and religious scholars.'),
    _mc(76, 'songhai', 'What major flaw made the Songhai army vulnerable to the Moroccans?', ['They lacked modern gunpowder weapons', 'They did not know how to ride horses', 'They used wooden weapons instead of iron', 'They had no soldiers in their army'], 'Songhai had brave soldiers but their spears and bows could not match Moroccan cannons.'),
    _mc(77, 'songhai', 'What did Morocco want to control by invading Songhai?', ['The West African gold and salt mines', 'The Atlantic slave ships', 'The European silk routes', 'The Egyptian spice markets'], 'Morocco wanted to take over the highly profitable trans-Saharan trade networks.'),
    _mc(78, 'songhai', 'What river did the Moroccan army use to navigate through Songhai territory?', ['Niger River', 'Nile River', 'Congo River', 'Rhine River'], 'The Moroccans moved along the Niger River to attack key cities like Gao and Timbuktu.'),
    _mc(79, 'songhai', 'What happened to the trade routes across the Sahara after Songhai collapsed?', ['They became chaotic and dangerous for merchants', 'They were replaced by high-speed trains', 'They were completely forgotten forever', 'They were taken over by the Roman Empire'], 'Without a strong empire to protect the roads trade became dangerous and declined.'),
    _mc(80, 'songhai', 'How did Songhai merchants transport goods across the grasslands?', ['Using donkey caravans and human porters', 'Using heavy iron steam trains', 'Using wooden horse-drawn chariots', 'Using large ocean-going sailboats'], 'Donkeys and porters carried goods across areas where camels could not travel easily.'),
    _mc(81, 'culture', 'What did a Griot do when a king needed advice on a new law?', ['They recited historical stories about past kings', 'They played a game of chess with the king', 'They painted a portrait of the king', 'They wrote a message on a paper scroll'], 'Griots used their knowledge of the past to help kings make fair decisions.'),
    _mc(82, 'culture', 'What type of art was commonly used in West African religious ceremonies?', ['Wooden masks representing ancestors', 'Oil paintings on canvas', 'Large stone sculptures of emperors', 'Stained glass windows'], 'Carved wooden masks were worn during dances to honor spirits and ancestors.'),
    _mc(83, 'culture', 'How did West African artists pass down their crafting skills?', ['Through specialized family craft guilds', 'By posting instructions on stone walls', 'By attending European art schools', 'By reading printed instruction manuals'], 'Skills like blacksmithing and weaving were kept secret within specific family guilds.'),
    _mc(84, 'culture', 'What did the patterns on a piece of Kente cloth usually represent?', ["The wearer's social status and family history", 'A hidden map to the secret gold mines', 'A list of marketplace rules and taxes', 'A recipe for preserving meat with salt'], "The specific colors and shapes told stories about a person's clan or achievements."),
    _mc(85, 'culture', 'What name is given to the traditional West African oral history epics?', ['Sundiata Epic', 'The Odyssey', 'The Iliad', 'The Epic of Gilgamesh'], 'The story of the Lion King Sundiata is the most famous oral epic of the region.'),
    _mc(86, 'trade', 'What is the name of the geographic transition zone between the desert and the savanna?', ['Sahel', 'Oasis', 'Jungle', 'Tundra'], 'The Sahel is a shoreline of land bordering the dry sands of the Sahara.'),
    _mc(87, 'trade', "Why didn't gold miners reveal the exact locations of their forest mines?", ['To keep the value of gold high and prevent theft', 'Because they forgot where they dug them', 'Because the king banned people from visiting', 'Because the mines were guarded by dragons'], 'Miners kept the locations a secret to protect their resources from foreign invaders.'),
    _mc(88, 'trade', 'What did North African traders bring to exchange besides physical goods?', ['The religion of Islam and written Arabic', 'The invention of the wheel', 'The Christian Bible', 'Fine silk clothing from China'], 'Traders brought their Islamic faith and literacy which transformed West African culture.'),
    _mc(89, 'ghana', 'What unique crown material did the King of Ghana wear to show his power?', ['A cap decorated with gold and regular robes', 'A helmet made of solid iron', 'A crown of imported sea shells', 'A wreath of green laurel leaves'], 'The king wore fine fabrics adorned with woven gold thread and jewelry.'),
    _mc(90, 'ghana', "What happened to Ghana's trade routes when the empire grew unsafe?", ['Merchants stopped visiting and trade declined', 'Merchants started using airplanes', 'Merchants moved the routes to Europe', 'Merchants traded using paper money'], 'When Ghana could no longer protect traders from bandits caravans found other paths.'),
    _mc(91, 'mali', 'How did the introduction of Islam affect architecture in Mali?', ['Buildings became blocky with distinct minarets', 'People stopped building permanent homes', 'All buildings were made of solid gold', 'People only built stone pyramids'], 'Architects blended local mud-brick styles with Islamic towers and arches.'),
    _mc(92, 'mali', 'What was the primary resource used to make books in Timbuktu?', ['Hand-copied paper scrolls', 'Printed woodblocks', 'Stamped iron plates', 'Dried palm leaves'], 'Books were luxury items hand-copied by scribes onto imported paper sheets.'),
    _mc(93, 'mali', 'What did Mansa Musa do to show his devotion to Islam while traveling?', ['He built a new mosque every Friday along his path', 'He forced his entire army to walk barefoot', 'He gave up all his royal wealth to become a monk', 'He changed his name to Muhammad'], 'Tradition says Mansa Musa ordered a mosque to be constructed wherever his caravan stopped on a Friday.'),
    _mc(94, 'mali', 'What did the University of Sankore teach besides religious studies?', ['Astronomy medicine and mathematics', 'How to build gunpowder weapons', 'European languages and history', 'Ocean navigation and mapmaking'], 'Sankore was a fully rounded university teaching advanced science and math.'),
    _mc(95, 'mali', "Why did Mansa Musa's fame spread all the way to medieval Europe?", ['European mapmakers added him holding a gold coin', 'He launched a military invasion of Italy', 'He bought all his clothes from French merchants', 'He visited England on his way to Mecca'], 'News of his massive gold caravan reached Europe where he was drawn on famous world maps.'),
    _mc(96, 'songhai', 'What did Askia Muhammad do to improve safety for international merchants?', ['He created a professional transit police force', 'He built stone walls along every trade road', 'He banned local citizens from entering markets', 'He made all merchants travel in total silence'], 'He used a centralized army to keep roads clear of bandits and thieves.'),
    _mc(97, 'songhai', 'What happened to the gold-salt trade after the fall of Songhai?', ['Sea routes around Africa began replacing desert routes', 'The trade completely stopped forever', 'Gold became worthless worldwide', 'Salt was replaced by sugar trade'], 'European ships began trading along the West African coast rendering desert paths less vital.'),
    _mc(98, 'songhai', 'Which language did Askia Muhammad enforce for all official legal documents?', ['Arabic', 'Songhai', 'Spanish', 'Greek'], 'Arabic was utilized as the standard written language for laws and court records.'),
    _mc(99, 'culture', 'What did a Griot use to help them remember complex historical timelines?', ['Rhythmic songs and specific string melodies', 'Written notches on wooden sticks', 'A system of colored stone beads', 'A printed pocket dictionary'], 'Rhythm and music acted as memory triggers to help Griots recall massive amounts of history.'),
    _mc(100, 'culture', 'Why are the historical accounts told by Griots still studied by modern historians?', ['They provide valuable insights into African history and culture', 'They are the only written records available', 'They contain magical spells from ancient times', 'They list the exact dates of every solar eclipse'], 'Griots offer an irreplaceable record of the cultural perspectives laws and events of ancient West Africa.'),
]


def _check_bank() -> None:
    ids = [question["id"] for question in QUESTIONS]
    if ids != list(range(1, len(QUESTIONS) + 1)):
        raise RuntimeError("Unit 3 questions must be numbered from 1")
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
