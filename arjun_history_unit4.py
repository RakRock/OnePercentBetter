"""Grade 7 History Unit 4: Medieval Europe."""

from __future__ import annotations

import copy
import random
from pathlib import Path

QUIZ_SIZE = 16
UNIT_QUIZ_SIZE = QUIZ_SIZE

UNIT = {
    "id": 4,
    "name": "Medieval Europe",
    "emoji": "🏰",
    "color": "#b45309",
    "blurb": "Feudalism, the Church, the Crusades, and the Magna Carta",
}

TOPICS: list[dict] = [
    {"id": "feudalism", "name": "Feudalism"},
    {"id": "church", "name": "The Church"},
    {"id": "crusades", "name": "The Crusades"},
    {"id": "magna", "name": "Democratic Thought"},
    {"id": "plague", "name": "Black Death"},
    {"id": "trade", "name": "Trade and Growth"},
    {"id": "conflict", "name": "Conflict"},
    {"id": "geography", "name": "Geography"},
]

NOTES_DIR = Path(__file__).resolve().parent / "ArjunHistory" / "notes" / "unit_4"

LESSONS: list[dict] = [
    {
        "id": "feudalism",
        "chapter": 1,
        "title": "The Contract System",
        "emoji": "🛡️",
        "file": "chapter_1_feudalism.md",
        "topic_ids": ["feudalism"],
    },
    {
        "id": "church",
        "chapter": 2,
        "title": "The Power of the Catholic Church",
        "emoji": "⛪",
        "file": "chapter_2_church.md",
        "topic_ids": ["church"],
    },
    {
        "id": "crusades",
        "chapter": 3,
        "title": "The Holy Wars",
        "emoji": "🏹",
        "file": "chapter_3_crusades.md",
        "topic_ids": ["crusades"],
    },
    {
        "id": "magna",
        "chapter": 4,
        "title": "Limiting the King",
        "emoji": "📜",
        "file": "chapter_4_magna_carta.md",
        "topic_ids": ["magna"],
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
    _mc(1, 'feudalism', 'What political and social system developed in Europe based on land loyalty and protection contracts?', ['Feudalism', 'Democracy', 'Imperialism', 'Socialism'], 'Feudalism arose out of a mutual need for security following the collapse of centralized Roman rule.'),
    _mc(2, 'feudalism', 'What was the name of the piece of land granted to a vassal by a lord in exchange for military loyalty?', ['A Fief', 'A Manor', 'A Guild', 'A Sacrament'], 'A fief was the land grant that provided a vassal with income and serf labor.'),
    _mc(3, 'feudalism', 'What group of peasant workers was legally bound to the land they farmed and could not leave without permission?', ['Serfs', 'Slaves', 'Knights', 'Vassals'], 'Serfs were agricultural laborers tied to the manor estate under feudal law.'),
    _mc(4, 'feudalism', 'What was the economic system of Medieval Europe centered around self-sufficient agricultural estates?', ['Manor System', 'Global Industrialization', 'Barter Token Market', 'Digital Enterprise'], 'The manor system organized economic life ensuring every estate produced its own food tools and clothing.'),
    _mc(5, 'feudalism', 'What code of conduct required medieval European knights to be brave loyal polite and protective of the weak?', ['Chivalry', 'Bushido', 'The Magna Carta', 'The Justinian Code'], 'Chivalry governed knightly behavior balancing martial prowess with Christian values and courtesy.'),
    _mc(6, 'feudalism', 'Which tier of the feudal pyramid made up the vast majority of the European population?', ['Peasants and Serfs', 'Lords and Nobles', 'Knights and Soldiers', 'Kings and Queens'], 'Over ninety percent of medieval Europeans were agricultural laborers working the fields.'),
    _mc(7, 'feudalism', "What framework determined a person's social class from birth to death under feudalism?", ['A rigid hereditary hierarchy where you stayed in the class you were born into', 'A system where you changed classes every week', 'A system based entirely on passing written exams', 'A lottery system run by the king'], 'Feudal social status was fixed by birth lines with almost zero upward social mobility.'),
    _mc(8, 'feudalism', 'What primary service did a vassal owe his lord in exchange for his fief estate?', ['Military service as a knight for a set number of days per year', "To wash the lord's clothes daily", 'To sail across the ocean to find spices', "To paint a portrait of the lord's family"], 'The core feudal contract required military defense and knightly support in exchange for land.'),
    _mc(9, 'feudalism', 'Why was a medieval manor considered self-sufficient?', ['It produced everything needed to live including food clothing and tools on site', 'It ordered all its goods from China', 'It had no citizens living on it', 'It relied entirely on imports from other countries'], 'Manors had their own fields mills workshops and pastures making outside trade unnecessary for daily survival.'),
    _mc(10, 'feudalism', 'A boy from a noble family who was training to become a knight started out at age 7 as what?', ['A Page', 'A Squire', 'A Serf', 'A Troubadour'], "A page was the first stage of training where a boy learned manners religion and basic weapon skills at a lord's castle."),
    _mc(11, 'feudalism', 'At age 14 a young boy training for knighthood advanced to become a personal servant to a knight called what?', ['A Squire', 'A Page', 'A Vassal', 'A Monk'], "Squires were teenage apprentices who cared for a knight's horses armor and accompanied them into combat."),
    _mc(12, 'feudalism', 'What was the name of the ceremonial event where a squire was officially made a full knight?', ['The Dubbing Ceremony', 'The Coronation', 'The Excommunication', 'The Investiture'], 'The dubbing ceremony involved tapping the young man on the shoulder with a sword to swear his knighthood vows.'),
    _mc(13, 'feudalism', 'What Mock battles were held in medieval Europe to allow knights to practice their combat skills and win prizes?', ['Tournaments', 'Guild Meetings', 'Parliaments', 'Inquisitions'], 'Tournaments featured events like jousting which kept knights trained and entertained during times of peace.'),
    _mc(14, 'feudalism', 'What heavy defensive armor was made of thousands of interlocking iron rings woven together?', ['Chainmail', 'Plate Armor', 'Leather Jerkins', 'Kevlar'], 'Chainmail was the primary flexible armor used by early medieval knights before full steel plates were invented.'),
    _mc(15, 'feudalism', 'What dangerous weapon did foot soldiers use that could pierce heavy armor and required less training than a longbow?', ['The Crossbow', 'The Iron Dagger', 'The Wooden Club', 'The Bronze Javelin'], 'Crossbows fired heavy bolts with massive mechanical power making regular peasants lethal against armored knights.'),
    _mc(16, 'feudalism', 'What name was given to the heavily fortified stone residences built by lords to control and defend their territories?', ['Castles', 'Monasteries', 'Manors', 'Guild Halls'], 'Castles were engineered specifically as military fortresses to withstand long enemy sieges.'),
    _mc(17, 'feudalism', 'What was the deep water-filled ditch surrounding a castle wall to prevent enemies from tunneling underneath?', ['A Moat', 'A Drawbridge', 'A Keep', 'A Portcullis'], 'Moats served as excellent obstacles against enemy battering rams and foot soldiers trying to scale the walls.'),
    _mc(18, 'feudalism', 'What was the strongest tallest tower located deep inside a medieval castle wall where the lord lived?', ['The Keep', 'The Barbican', 'The Bailey', 'The Moat'], 'The keep was the final defensive stronghold of a castle if the outer walls were breached.'),
    _mc(19, 'feudalism', 'What farming method divided field crops into segments leaving one field empty each year to rest the soil?', ['The Three-Field System', 'The Hydroponic Grid', 'The Slash-and-Burn Method', 'The Single-Crop Rotation'], 'The three-field system rotated crops like wheat and beans while leaving one field fallow to restore soil nutrients.'),
    _mc(20, 'church', 'Who was the absolute spiritual leader of the Roman Catholic Church holding massive political sway over Europe?', ['The Pope', 'The King', 'The Emperor', 'The Abbot'], 'The Pope directed the spiritual lives of Europeans and could depose kings who defied his orders.'),
    _mc(21, 'church', 'What terrifying spiritual punishment could the Pope use to banish a king and cut off his kingdom from church rituals?', ['Excommunication', 'Enlightenment', 'Taxation', 'Inquisition'], 'Excommunication cut individuals off from church sacraments which people believed led directly to damnation.'),
    _mc(22, 'church', 'What holy rituals controlled entirely by the Catholic Church were considered essential for getting into heaven?', ['Sacraments', 'Fiefs', 'Guild Laws', 'Chivalric Oaths'], 'Sacraments included sacred milestones like baptism confirmation and marriage managed by local priests.'),
    _mc(23, 'church', 'Where did medieval monks live work and preserve ancient historical texts by copying them by hand?', ['Monasteries', 'Castles', 'Manor Houses', 'Guild Halls'], 'Monasteries were isolated religious communities that acted as primary centers of literacy and healthcare.'),
    _mc(24, 'church', 'What did the Catholic Church collect from every citizen to fund its massive institutions and charities?', ['A tithe (a tax equal to ten percent of income)', 'Solid gold nuggets found in rivers', 'A basket of fresh fish every Friday', 'A share of paper currency imported from China'], 'The tithe was a mandatory religious tax that generated vast wealth for the Church.'),
    _mc(25, 'church', 'What language was used exclusively by the Catholic Church for all official prayers documents and university teaching?', ['Latin', 'English', 'French', 'German'], 'Latin served as the universal language of scholarship law and religion across fragmented Europe.'),
    _mc(26, 'church', 'What tool did monks use to create beautiful decorated manuscripts with gold leaf and bright colors?', ['Illumination techniques', 'Digital graphics software', 'Movable type presses', 'Mechanical stampers'], 'Illuminated manuscripts were painstakingly hand-decorated books reserved for holy texts.'),
    _mc(27, 'church', 'What was the name given to the local district or community managed directly by a Catholic priest?', ['A Parish', 'A Fief', 'A Manor', 'A Guild'], 'A parish was the local church district that served as the center of daily social and religious life for peasants.'),
    _mc(28, 'church', 'What special tax or payment did people make to purchase forgiveness for their sins from the medieval church?', ['Indulgences', 'Tithes', 'Fief Fees', 'Guild Dues'], "Indulgences were certificates sold by church officials promising to reduce a soul's time in purgatory."),
    _mc(29, 'church', 'What court was established by the Catholic Church to find and put on trial people accused of heresy?', ['The Inquisition', 'The Supreme Court', 'The Parliament', 'The Star Chamber'], 'The Inquisition investigated heresy (holding beliefs that went against official church teachings).'),
    _mc(30, 'church', 'What name was given to an individual who traveled to preach spread religious beliefs or perform charity work?', ['A Friar', 'A Serf', 'A Squire', 'A Vassal'], 'Friars were religious men who did not lock themselves in monasteries; instead they traveled among the public to help the poor.'),
    _mc(31, 'church', 'What major organization was the single largest landowner in all of Western Europe during the Middle Ages?', ['The Roman Catholic Church', 'The Kingdom of England', 'The Holy Roman Empire', 'The Merchant Guild of Venice'], 'Through royal donations and wills the Church accumulated ownership of vast amounts of land across Europe.'),
    _mc(32, 'church', 'What title was given to the woman who led a community of religious women called nuns?', ['An Abbess', 'A Priest', 'A Pope', 'A Friar'], 'An abbess or Mother Superior was the head leader of a medieval convent or nunnery.'),
    _mc(33, 'church', 'What architectural style featuring soaring pointed arches stained glass windows and flying buttresses dominated medieval Europe?', ['Gothic Architecture', 'Romanesque Architecture', 'Modernist Architecture', 'Classical Greek Architecture'], 'Gothic cathedrals were engineered to be incredibly tall and filled with light to inspire religious awe.'),
    _mc(34, 'church', 'What heavy external stone arches supported the tall thin walls of Gothic cathedrals allowing for massive windows?', ['Flying Buttresses', 'Iron Pillars', 'Wooden Columns', 'Drawbridges'], 'Flying buttresses redistributed the heavy weight of the roof outward away from the walls.'),
    _mc(35, 'church', 'What was the purpose of the detailed stained-glass windows inside medieval cathedrals?', ['To teach biblical stories visually to peasants who could not read', 'To keep the building completely dark', 'To protect the church from arrows', 'To show off trade maps of China'], 'Stained glass functioned as a visual storybook for an illiterate public.'),
    _mc(36, 'church', 'What primary service did early monasteries provide to travelers and the sick?', ['They ran the first basic hospitals and inns', 'They manufactured iron weapons for the king', 'They trained young boys to become knights', 'They operated commercial trading ships'], 'Monasteries were vital safety nets offering medical aid food and shelter to travelers.'),
    _mc(37, 'church', 'What name is given to the strict set of rules written to govern the daily behavior and schedule of monks?', ['The Benedictine Rule', 'The Magna Carta', 'The Code of Chivalry', 'The Bushido Code'], "Written by Saint Benedict it regulated a monk's life into balanced segments of prayer study and manual work."),
    _mc(38, 'church', 'What philosophy developed in medieval universities to blend Christian faith with classical Greek logic?', ['Scholasticism', 'Legalism', 'Daoism', 'Existentialism'], 'Scholasticism (championed by Thomas Aquinas) used human reason to defend and explain religious doctrine.'),
    _mc(39, 'church', 'Who is considered the greatest Scholastic philosopher who wrote the Summa Theologiae?', ['Thomas Aquinas', 'Pope Urban II', 'Charlemagne', 'King John'], 'Saint Thomas Aquinas argued that human reason and religious faith could harmony together beautifully.'),
    _mc(40, 'crusades', 'Which Pope gave a famous speech in 1095 CE calling on European knights to launch the first Crusade?', ['Pope Urban II', 'Pope Gregory VII', 'Pope Innocent III', 'Pope Leo X'], 'Pope Urban II rallied Western Europeans to reclaim the Holy Land from Muslim forces.'),
    _mc(41, 'crusades', 'What was the primary military objective of the European Crusaders who marched to the Middle East?', ['To capture the holy city of Jerusalem', 'To conquer the empire of China', 'To discover a sea route to America', 'To destroy the city of Rome'], 'The Crusades were launched to take control of Jerusalem and other sacred biblical locations.'),
    _mc(42, 'crusades', 'Who was the brilliant Muslim military general who recaptured Jerusalem and fought famously against Richard the Lionheart?', ['Saladin', 'Al-Khwarizmi', 'Sunni Ali', 'Ibn Battuta'], 'Saladin unified Muslim forces and was widely respected by both sides for his chivalrous behavior.'),
    _mc(43, 'crusades', 'What major economic change occurred in Europe as a direct result of the Crusades?', ['Trade exploded as Europeans demanded Eastern goods like spices and silk', 'Money was completely banned in Europe', 'Europe stopped all farming', 'Kings lost all their lands to serfs'], 'Returning crusaders introduced new products creating a massive commercial trade boom with the East.'),
    _mc(44, 'crusades', 'What mathematical system was introduced to Europe by merchants returning from the Crusades?', ['Arabic Numerals (including zero)', 'Roman Numerals', 'Binary Code', 'Fraction Blocks'], 'Western Europeans abandoned confusing Roman numerals in favor of efficient mathematical symbols from the Islamic world.'),
    _mc(45, 'crusades', 'What did Pope Urban II promise to any European knight who died while fighting on a Crusade?', ['Immediate forgiveness of all their sins and entrance to heaven', 'A massive palace built of solid gold', 'The title of Emperor of Rome', 'A free fleet of trade ships'], 'The promise of immediate salvation motivated thousands of religious warriors to volunteer.'),
    _mc(46, 'crusades', 'What empire did the Christian Crusaders shockingly sack and loot during the Fourth Crusade in 1204?', ['The Byzantine Empire at Constantinople', 'The Islamic Caliphate at Baghdad', 'The Kingdom of England', 'The Song Dynasty in China'], 'The Fourth Crusade degraded into a political assault on fellow Christians in Constantinople.'),
    _mc(47, 'crusades', 'How many major numbered Crusades were launched by Europeans to the Holy Land over two centuries?', ['Eight', 'Exactly one', 'More than fifty', 'None because they canceled them'], 'Historians track eight major military expeditions alongside various minor campaigns.'),
    _mc(48, 'crusades', 'What English king became the primary military face of Europe during the Third Crusade?', ['Richard the Lionheart', 'King John', 'William the Conqueror', 'King Henry VIII'], 'Richard I (the Lionheart) led the Third Crusade but failed to recapture Jerusalem from Saladin.'),
    _mc(49, 'crusades', 'What was a long-term political effect of the Crusades on European kings?', ['Kings grew more powerful as many feudal nobles died in battle or went bankrupt', 'Kings lost all power to the peasant class', 'Feudalism became ten times stronger', 'The Pope officially banned all European kings'], 'The deaths and bankruptcies of many nobles allowed centralized kings to seize power back from local lords.'),
    _mc(50, 'crusades', 'What luxury items did Western Europeans encounter in Middle Eastern markets during the Crusades?', ['Spices silk rugs sugar and lemons', 'Plastic beads and cotton t-shirts', 'Iron tractors and steel plows', 'Potatoes tomatoes and corn'], 'These exotic luxury items stimulated European commercial markets and maritime trade networks.'),
    _mc(51, 'crusades', 'What religious city is considered sacred to Jews Christians and Muslims alike in the Middle East?', ['Jerusalem', 'Rome', 'Baghdad', 'Timbuktu'], 'All three major monotheistic religions trace deep historical and spiritual ties to Jerusalem.'),
    _mc(52, 'crusades', 'What group of Turkish Muslims captured Jerusalem and closed it to Christian pilgrims triggering the Crusades?', ['Seljuk Turks', 'Ottoman Turks', 'Umayyads', 'Moorish Dynasties'], 'The aggressive expansion of the Seljuk Turks alarmed the Byzantine Emperor who begged the Pope for military help.'),
    _mc(53, 'crusades', 'What tragic expedition in 1212 CE involved thousands of European youths marching to the Holy Land?', ["The Children's Crusade", "The Peasant's Crusade", "The Knight's Crusade", "The Scholar's Crusade"], "The ill-fated Children's Crusade resulted in thousands of children dying of starvation or being sold into slavery."),
    _mc(54, 'crusades', 'What weapon technology did Europeans adopt and improve after seeing it used in the Middle East?', ['Gunpowder and siege tactics', 'The simple wooden spear', 'The iron broadsword', 'The leather shield'], 'Exposure to Eastern siege combat accelerated military engineering upgrades across Europe.'),
    _mc(55, 'magna', 'What famous document was King John of England forced to sign in 1215 CE limiting his royal power?', ['The Magna Carta', 'The Declaration of Independence', 'The Code of Hammurabi', 'The Treaty of Versailles'], 'The Magna Carta established that the monarch was subject to the law rather than above it.'),
    _mc(56, 'magna', 'Where did the English barons corner King John and force him to sign the Magna Carta?', ['A meadow called Runnymede', 'The Tower of London', 'The steps of the Vatican', 'The beach of Normandy'], 'The historic signing took place at Runnymede near Windsor in 1215 CE.'),
    _mc(57, 'magna', 'What revolutionary democratic principle did the Magna Carta establish regarding the King?', ['The King must follow the law of the land', 'The King can take whatever money he wants', 'The King is a living god', 'The King does not need an army'], 'The Magna Carta proved that law is supreme over personal royal dictates.'),
    _mc(58, 'magna', 'What legal right introduced by the Magna Carta prevents people from being imprisoned indefinitely without a trial?', ['Habeas Corpus (Due Process)', 'Excommunication', 'Silent Barter', 'Feudal Lordship'], 'Habeas corpus requires a valid legal reason and trial before a government can lock a citizen away.'),
    _mc(59, 'magna', 'What governing body developed out of the council of nobles created by the Magna Carta in England?', ['Parliament', 'The Senate', 'The Supreme Court', 'The Congress'], 'The Great Council evolved into the English Parliament laying the groundwork for representative government.'),
    _mc(60, 'magna', 'What tool did King John use to bully his citizens before the Magna Carta limited his powers?', ['Arbitrary taxation and illegal imprisonment', 'A fleet of advanced war canoes', 'A mass-production printing press', 'A system of civil service examinations'], 'John ruled via personal whims arresting rivals and extracting cash without legal consent.'),
    _mc(61, 'magna', "How did the Magna Carta affect the king's ability to collect new taxes?", ['He could only collect new taxes after consulting a council of nobles', 'He could take whatever he wanted at any time', 'He was banned from ever using money again', 'He had to pass a civil service exam first'], "The charter established the early democratic concept of 'no taxation without representation/consent.'"),
    _mc(62, 'magna', 'What legal body was established by the Magna Carta to ensure the king kept his promises?', ['A council of 25 barons', 'A court of foreign kings', 'A group of peasant farmers', 'A board of church monks'], "The council of barons held the legal right to seize the king's castles if he broke the treaty lines."),
    _mc(63, 'magna', 'What long-term historical impact did the Magna Carta have on global democracy?', ['It laid the foundational groundwork for modern constitutional law and individual rights', 'It proved that dictatorships are the best way to rule countries', 'It made England part of the Roman Empire again', 'It caused everyone to stop using laws entirely'], 'The concepts of limited executive power due process and legal supremacy inspired democratic frameworks worldwide.'),
    _mc(64, 'magna', 'What does the Latin phrase Magna Carta translate to in English?', ['The Great Charter', 'The Power of the King', 'The Freedom of the Serf', 'The Law of the Church'], "Magna Carta translates directly to 'The Great Charter.'"),
    _mc(65, 'magna', "Which English king established the 'Model Parliament' in 1295 to include commoners in lawmaking?", ['King Edward I', 'King John', 'King Henry II', 'King William I'], 'Edward I expanded Parliament to include representatives from towns alongside nobles and church leaders.'),
    _mc(66, 'magna', 'The development of common law in England was based on what system?', ['Past court decisions and customs rather than written royal edicts', 'The laws imported from ancient China', 'The rules written by peasant guilds', 'The strict military commands of the Shogun'], 'Common law created a unified legal system where similar cases received similar punishments across the country.'),
    _mc(67, 'magna', 'What early democratic institution allowed local English citizens to participate directly in deciding court cases?', ['The Jury System', 'The Tournament Duel', 'The Papal Council', 'The Feudal Contract'], 'Henry II popularized the use of a jury of regular citizens to investigate local crimes and disputes.'),
    _mc(68, 'plague', 'What deadly bacterial pandemic struck Europe in 1347 CE killing nearly one-third of the entire population?', ['The Black Death (Bubonic Plague)', 'Smallpox', 'The Spanish Flu', 'Malaria'], 'The Black Death devastated towns destabilized the feudal economy and altered European history.'),
    _mc(69, 'plague', 'How did the Black Death accidentally help surviving peasant workers economically?', ['Labor shortages allowed them to demand higher wages and cheaper rent', 'It made all land free for anyone', 'It turned all peasants into kings', 'It banned all taxes forever'], 'With fewer workers available serfs held greater leverage to break free from feudal ties.'),
    _mc(70, 'plague', 'What microscopic organism carried on fleas living on rats actually caused the Bubonic Plague?', ['Yersinia pestis bacteria', 'A common cold virus', 'A toxic volcanic gas', 'Muggy swamp air'], 'The bacteria was spread via flea bites when infected rodents interacted with human populations.'),
    _mc(71, 'plague', 'Where did the Black Death enter Europe through international trade routes?', ['Italian port cities like Messina', 'The mountains of northern Scotland', 'The forests of Germany', 'The castles of inland France'], 'Merchant ships traveling from the Black Sea brought infected rats directly to European harbors.'),
    _mc(72, 'plague', 'What did many medieval people mistakenly believe caused the Black Death because they lacked scientific knowledge?', ['Bad air (miasma) or punishment from God', 'Drinking clean river water', 'Reading too many hand-copied books', 'Eating too much fresh bread'], 'People blamed toxic air planets aligning or divine anger due to their ignorance of germ theory.'),
    _mc(73, 'plague', 'What religious extremist group traveled from town to town whipping themselves to try and stop the plague?', ['The Flagellants', 'The Knights Templar', 'The Scholastics', 'The Scholar-Officials'], 'Flagellants believed that punishing their own bodies would show repentance and cure the pandemic.'),
    _mc(74, 'plague', 'What long-term effect did the Black Death have on the system of feudalism?', ['It severely weakened and helped end feudalism as peasants left manors for paying jobs', 'It made feudalism permanent across Europe', 'It forced everyone to live inside castles forever', 'It caused all kings to surrender power to the Pope'], 'The labor collapse broke the traditional manor system allowing peasants to demand freedom and wages.'),
    _mc(75, 'trade', 'What business organizations were formed by medieval artisans and merchants to set prices and maintain product standards?', ['Guilds', 'Monasteries', 'Fiefs', 'Parliaments'], 'Guilds controlled manufacturing quality prices and apprentice training for specific trades.'),
    _mc(76, 'trade', 'A young person learning a craft under a master guild member without receiving wages was called what?', ['An Apprentice', 'A Journeyman', 'A Squire', 'A Page'], 'Apprentices worked for a master for several years in exchange for free food shelter and trade training.'),
    _mc(77, 'trade', 'After finishing their apprenticeship a craftsman could work for daily wages and was called what?', ['A Journeyman', 'A Master', 'A Serf', 'A Vassal'], 'Journeymen were skilled workers who traveled around earning daily pay before creating a masterpiece to become a master.'),
    _mc(78, 'trade', 'What item did a journeyman have to create to prove their skills and be accepted as a full Guild Master?', ['A Masterpiece', 'A Fief Deed', 'A Chivalry Shield', 'A Illuminated Scroll'], 'A masterpiece was an example of their finest work inspected and approved by existing guild masters.'),
    _mc(79, 'trade', 'What language did regular everyday Europeans speak at home instead of formal Latin?', ['Vernacular languages (like early English French or Italian)', 'Ancient Hieroglyphics', 'Standard Mandarin Chinese', 'Formal Arabic script'], 'Vernacular tongues were the local spoken languages of the regular public contrasting with scholarly Latin.'),
    _mc(80, 'conflict', 'What weapon completely changed medieval warfare during the Hundred Years War making knightly armor less effective?', ['The English Longbow', 'The Iron Gladius', 'The Wooden Spear', 'The Bronze Shield'], 'The longbow fired arrows fast and hard enough to penetrate traditional knightly chainmail and armor.'),
    _mc(81, 'conflict', 'Who was the teenage French peasant girl who led armies against the English before being captured during the Hundred Years War?', ['Joan of Arc', 'Queen Elizabeth', 'Eleanor of Aquitaine', 'Murasaki Shikibu'], 'Joan of Arc became a legendary French national hero and saint before her execution.'),
    _mc(82, 'conflict', 'What long series of military conflicts was fought between England and France from 1337 to 1453?', ['The Hundred Years War', 'The Crusades', 'The Peloponnesian War', 'The War of the Roses'], 'The Hundred Years War was a prolonged struggle over the rightful inheritance of the French royal throne.'),
    _mc(83, 'conflict', 'What primary weapon invention did the French use late in the Hundred Years War to blast through English castle walls?', ['Cannons (Gunpowder artillery)', 'The Catapult', 'The Battering Ram', 'The Crossbow'], 'Early cannons using gunpowder technology revolutionized siege combat rendering stone castles vulnerable.'),
    _mc(84, 'conflict', 'What political change occurred in France and England due to the Hundred Years War?', ['A surge in national pride and patriotism where people viewed themselves as citizens of a country', 'Both countries decided to combine into one kingdom', 'They both dissolved their armies forever', 'They abandoned their kings and became democracies'], 'The war transformed people from local manor subjects into proud patriotic citizens of France or England.'),
    _mc(85, 'geography', 'What major mountain range forms a natural barrier separating Italy from the rest of mainland Europe?', ['The Alps', 'The Pyrenees', 'The Urals', 'The Carpathians'], 'The steep snow-capped Alps historically isolated Italy making land invasions difficult.'),
    _mc(86, 'geography', 'What mountain range separates the Iberian Peninsula (Spain/Portugal) from France?', ['The Pyrenees', 'The Alps', 'The Himalayas', 'The Atlas Mountains'], 'The Pyrenees formed a rugged geographical border blocking easy ground transit between Spain and France.'),
    _mc(87, 'geography', 'What major river flows across central and eastern Europe emptying into the Black Sea?', ['The Danube River', 'The Nile River', 'The Thames River', 'The Seine River'], 'The Danube served as a major inland trade highway for moving goods across Central Europe.'),
    _mc(88, 'geography', 'What body of water separates the island of Great Britain from mainland Europe?', ['The English Channel', 'The Mediterranean Sea', 'The Red Sea', 'The Baltic Sea'], 'The English Channel provided Britain with a natural naval shield against quick land assaults.'),
    _mc(89, 'geography', "How did Europe's extensive network of navigable rivers affect its medieval development?", ['It encouraged long-distance trade and allowed distinct cultures to interact easily', 'It completely isolated every town preventing all contact', 'It froze completely year-round blocking all boats', 'It washed away all farming fields making life impossible'], "Europe's open river paths acted as excellent trade routes connecting coastal ports with deep inland towns."),
    _mc(90, 'conflict', 'What name was given to the centuries-long military campaign by Christian kingdoms to drive Muslim rulers out of Spain?', ['The Reconquista', 'The Crusades', 'The Inquisition', 'The Great Schism'], 'The Reconquista concluded in 1492 when King Ferdinand and Queen Isabella captured Granada.'),
    _mc(91, 'trade', 'What major annual events brought international merchants together in European towns to trade wholesale goods?', ['Trade Fairs', 'Jousting Tournaments', 'Church Councils', 'Guild Audits'], 'Fairs (like those in Champagne France) allowed seasonal mega-markets for wool spices leather and wine.'),
    _mc(92, 'trade', 'What new class of urban citizens developed in medieval towns composed of merchants and artisans?', ['The Middle Class (Burghers/Bourgeoisie)', 'The Nobility', 'The Serfdom', 'The Clergy'], 'Town growth created an independent middle class that did not fit into the traditional lord-serf feudal binary.'),
    _mc(93, 'church', 'What split occurred within the Catholic Church from 1378 to 1417 when multiple rival Popes claimed power simultaneously?', ['The Western Schism', 'The Protestant Reformation', 'The Crusades', 'The Council of Trent'], 'The Great Western Schism highly damaged the spiritual prestige and political authority of the Papacy.'),
    _mc(94, 'feudalism', 'What was the name of the main legal center of a manor estate where the lord held trials and collected taxes?', ['The Manor Court', 'The Parliament', 'The Guild Hall', 'The Monastery Library'], 'The manor court settled daily neighbor arguments punished lazy serfs and enforced local estate customs.'),
    _mc(95, 'feudalism', 'What name was given to a piece of unplanted land left to rest so it could regain nutrients naturally?', ['Fallow', 'Fief', 'Manor', 'Tithe'], 'Leaving a field fallow was a cornerstone of medieval crop science before synthetic fertilizers existed.'),
    _mc(96, 'magna', 'What English king consolidated judicial power by sending traveling royal judges across the country creating common law?', ['King Henry II', 'King John', 'King Edward I', 'King William I'], 'Henry II streamlined justice by replacing local lord trials with a centralized royal court system.'),
    _mc(97, 'magna', 'Before the jury system became common what dangerous practice used physical survival to determine legal guilt?', ['Trial by Ordeal', 'Trial by Exam', 'Trial by Silent Barter', 'Trial by Tithe'], 'Trial by ordeal forced suspects to hold hot irons or sink in water believing God would perform a miracle to save the innocent.'),
    _mc(98, 'church', 'What name was given to the beautiful hand-written letters used to open chapters in monastic books?', ['Illuminated Initials', 'Movable Typography', 'Hieroglyphic Blocks', 'Digital Icons'], 'Monks painstakingly decorated the first letter of pages with vibrant paints inks and gold leafing.'),
    _mc(99, 'church', 'What religious order was founded by Saint Francis of Assisi focusing on poverty and helping poor urban citizens?', ['The Franciscans', 'The Benedictines', 'The Almoravids', 'The Scholar-Officials'], 'The Franciscan friars abandoned wealth to model simple spiritual lives directly within crowded cities.'),
    _mc(100, 'magna', 'Which tier of English society was explicitly added to Parliament in 1295 to create the House of Commons?', ['Knights and town burgesses (commoners)', 'Only the high-ranking bishops', 'Only the bloodline relatives of the King', 'The foreign merchants from China'], 'The addition of commoners laid the foundation for modern representative bicameral legislatures.'),
]


def _check_bank() -> None:
    ids = [question["id"] for question in QUESTIONS]
    if ids != list(range(1, len(QUESTIONS) + 1)):
        raise RuntimeError("Unit 4 questions must be numbered from 1")
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
