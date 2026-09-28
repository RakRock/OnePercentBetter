"""
Grade 7 Science Corner curriculum for Arjun.

Six units, 36 lessons. The live class is the calendar. This module is the
practice companion: lesson text, IXL skill names, worksheet titles, and
quiz questions. IXL itself stays on ixl.com.
"""

from __future__ import annotations

import copy
import random

import science_content as science_bank

LESSON_QUIZ_SIZE = 8
UNIT_QUIZ_SIZE = 10
STEM_QUIZ_SIZE = 8

# Word stems for 7.E.1 and 7.E.2 (Earth's systems). Shown on Unit 1.
UNIT_WORD_STEMS: dict[int, list[dict]] = {
    1: [
        {"stem": "atmo", "meaning": "vapor", "example": "atmosphere"},
        {"stem": "cycle", "meaning": "ring, circle", "example": "water cycle"},
        {"stem": "spher", "meaning": "ball, round", "example": "atmosphere"},
        {"stem": "thermo", "meaning": "heat", "example": "thermosphere"},
        {"stem": "ex", "meaning": "out of, away from", "example": "exosphere"},
        {"stem": "meso", "meaning": "middle", "example": "mesosphere"},
        {"stem": "strat", "meaning": "layer", "example": "stratosphere"},
        {"stem": "trop", "meaning": "change, turn", "example": "troposphere"},
        {"stem": "grav", "meaning": "heavy", "example": "gravity"},
        {"stem": "baro", "meaning": "pressure", "example": "barometer"},
        {"stem": "vectus", "meaning": "to carry", "example": "convection"},
        {"stem": "alt", "meaning": "high", "example": "altitude"},
        {"stem": "densus", "meaning": "thick", "example": "density"},
        {"stem": "radi", "meaning": "ray", "example": "radiation"},
        {"stem": "tudo", "meaning": "state or condition", "example": "altitude"},
    ],
}

UNITS: list[dict] = [
    {
        "id": 1,
        "name": "Thinking Like a Scientist",
        "emoji": "🔍",
        "color": "#6366f1",
        "blurb": "Observations, fair tests, and Claim-Evidence-Reasoning",
        "lesson_ids": [1, 2, 3],
    },
    {
        "id": 2,
        "name": "Cells and Life",
        "emoji": "🧬",
        "color": "#10b981",
        "blurb": "Cells, organelles, transport, and body systems",
        "lesson_ids": [4, 5, 6, 7, 8, 9, 10],
    },
    {
        "id": 3,
        "name": "Heredity and Genetics",
        "emoji": "🧪",
        "color": "#8b5cf6",
        "blurb": "DNA, Punnett squares, and natural selection",
        "lesson_ids": [11, 12, 13, 14, 15, 16],
    },
    {
        "id": 4,
        "name": "Ecology and the Environment",
        "emoji": "🌿",
        "color": "#059669",
        "blurb": "Ecosystems, food webs, and human impact",
        "lesson_ids": [17, 18, 19, 20, 21, 22],
    },
    {
        "id": 5,
        "name": "Earth and Space",
        "emoji": "🌍",
        "color": "#ea580c",
        "blurb": "Earth's layers, weather, water, and the solar system",
        "lesson_ids": [23, 24, 25, 26, 27, 28, 29],
    },
    {
        "id": 6,
        "name": "Physical Science",
        "emoji": "⚛️",
        "color": "#2563eb",
        "blurb": "Matter, reactions, forces, energy, and waves",
        "lesson_ids": [30, 31, 32, 33, 34, 35, 36],
    },
]


def _lesson(
    lesson_id: int,
    unit_id: int,
    title: str,
    activity: str,
    ixl: list[str],
    *,
    materials: str = "",
    sheet: str = "",
    also: str = "",
) -> dict:
    return {
        "id": lesson_id,
        "unit_id": unit_id,
        "title": title,
        "activity": activity,
        "materials": materials,
        "ixl": ixl,
        "sheet": sheet,
        "also": also,
    }


LESSONS: list[dict] = [
    _lesson(1, 1, "What is Science?", "Observe a hidden household object and write clues from evidence only.", ["A.1 The process of scientific inquiry", "C.1 Identify parts of the engineering-design process"]),
    _lesson(2, 1, "Scientific Method and Experimental Design", "Paper-towel absorbency test: change one thing and keep the rest the same.", ["B.1 Identify control and experimental groups", "B.2 Identify independent and dependent variables"], materials="Paper towels, water, coin, cup"),
    _lesson(3, 1, "Analyzing Data and Scientific Explanations", "Graph sample experiment data and write a claim, evidence, and reasoning.", ["B.4 Identify questions that can be investigated with a set of materials", "B.5 Understand an experimental protocol about plant growth"]),
    _lesson(4, 2, "Introduction to Cells", "Is it alive? Sort objects using evidence that living things are made of cells.", ["R.1 Understanding cells", "P. Are bacteria and viruses alive?"]),
    _lesson(5, 2, "Prokaryotic vs. Eukaryotic Cells", "Make a Venn diagram of simple cells and cells with a nucleus.", ["R.6 Compare cells and cell parts"], sheet="Cell Organelles"),
    _lesson(6, 2, "Cell Organelles and Function", "Design a cell model using the cell-as-a-city idea.", ["R.3 Identify functions of animal cell parts", "R.5 Animal cell diagrams: label parts"], sheet="Label the Animal Cell: Level 1"),
    _lesson(7, 2, "Plant vs. Animal Cells", "Compare the structures only plant cells have with the structures both kinds share.", ["R.2 Identify functions of plant cell parts", "R.4 Plant cell diagrams: label parts"], sheet="Label the Plant Cell: Level 1; Animal Cells vs. Plant Cells"),
    _lesson(8, 2, "Osmosis and Diffusion", "Gummy-bear osmosis test in plain water and salt water.", ["O.2 Diffusion across membranes", "B.6 Understand an experimental protocol about diffusion"], materials="Gummy bears, cups, water, salt"),
    _lesson(9, 2, "From Cells to Systems", "Map how cells form tissues, organs, and organ systems.", ["S.1 Organization in the human body"], sheet="The Respiratory System"),
    _lesson(10, 2, "Body Systems and Homeostasis", "Measure pulse before and after movement to see the body stay in balance.", ["S.2 Science literacy: how does the nervous system produce phantom pain?"], sheet="The Nervous System: Part 1"),
    _lesson(11, 3, "DNA and Genetic Information", "Build a paper model of DNA.", ["T.8 Genes, proteins, and traits"], materials="Paper and colored pencils"),
    _lesson(12, 3, "Chromosomes and Cell Division", "Order mitosis pictures, then act out the stages.", ["R.7 Mitosis and the cell cycle", "T.2 Genetic variation in sexual reproduction"]),
    _lesson(13, 3, "Punnett Squares and Probability", "Flip a coin to simulate inherited traits and predict offspring.", ["T.3 Genetics vocabulary: genotype and phenotype", "T.4 Genetics vocabulary: dominant and recessive", "T.5 Complete and interpret Punnett squares"], materials="Coin", also="Also T.6 ratios and T.7 probabilities of offspring types."),
    _lesson(14, 3, "Types of Traits and Variation", "Survey family traits and separate inherited traits from acquired ones.", ["T.1 Inherited and acquired traits", "T.10 How do genes and the environment affect plant growth?"], also="Optional: T.9 Describe the effects of gene mutations."),
    _lesson(15, 3, "Natural Selection and Adaptation", "Simulate bird beaks competing for food.", ["U.2 Introduction to natural selection", "U.5 Construct explanations of natural selection"]),
    _lesson(16, 3, "Environmental Change and Survival of Traits", "Hunt colored objects to see how camouflage changes survival.", ["U.3 Calculate the percentages of traits in a population", "U.4 Calculate the averages of traits in a population"], materials="Paper squares or small candies", also="Also U.1 How animal behaviors affect reproductive success."),
    _lesson(17, 4, "Ecosystems and Biomes", "Draw and label a biome with living and nonliving parts.", ["Y.1 Describe populations, communities, and ecosystems", "Y.2 Identify ecosystems", "Y.3 Describe ecosystems"], sheet="Research an Ecosystem"),
    _lesson(18, 4, "Food Webs and Energy Flow", "Build a food-web puzzle showing how energy moves.", ["Z.1 How does matter move in food chains?", "Z.2 Interpret food webs I", "Z.4 Trophic levels and energy pyramids"], sheet="Food Webs: Cycling of Matter and Flow of Energy", also="Also Z.3 Interpret food webs II."),
    _lesson(19, 4, "Populations and Carrying Capacity", "Use small objects to show a population running out of resources.", ["Z.5 Use food chains to predict changes in populations"], materials="10–20 beans, beads, or cereal pieces"),
    _lesson(20, 4, "Symbiosis and Species Interactions", "Sort real organism pairs into mutualism, commensalism, parasitism, and competition.", ["Z.6 Classify ecological relationships", "Z.7 Classify symbiotic relationships"]),
    _lesson(21, 4, "Human Impact and Environmental Solutions", "Photo-hunt human impacts nearby and brainstorm one solution.", ["AA.1 Coral reef biodiversity and human uses: explore a problem", "AA.2 Coral reef biodiversity and human uses: evaluate solutions", "BB.2 Renewable and nonrenewable energy resources"], also="Also BB.3 groundwater claims and BB.4 fossil-fuel claims."),
    _lesson(22, 4, "Matter and Energy Cycling", "Act as a molecule traveling through the water, carbon, or nitrogen cycle.", ["FF.4 The carbon cycle", "X.1 How do plants use and change energy?", "X.2 Identify the photosynthetic organism"], sheet="Photosynthesis: Cycling of Matter and Flow of Energy", also="Q.1 carbohydrates, lipids, proteins, and nucleic acids only after photosynthesis practice is solid."),
    _lesson(23, 5, "Earth's Structure", "Build a model of Earth's layers.", ["DD.1 Label Earth layers", "FF.1 Describe the geosphere, biosphere, hydrosphere, and atmosphere"], also="Topo maps (EE.1) have no lesson. Practice EE.1 once during this lesson or the rock cycle."),
    _lesson(24, 5, "Plate Tectonics", "Use crackers and frosting, or paper and glue, to show plates moving.", ["DD.2 Evidence of continental drift and plate tectonics", "DD.3 Label Earth features at tectonic plate boundaries", "DD.4 Describe tectonic plate boundaries around the world"], materials="Crackers and frosting, or paper and glue", also="Also II.1 Analyze natural hazard maps."),
    _lesson(25, 5, "Rock Cycle and Geologic Processes", "Melt and reshape crayons or candy to model how rocks change.", ["CC.1 Identify rocks and minerals", "CC.2 Introduction to the rock cycle", "V.1 Compare fossils to modern organisms"], materials="Crayons, warm water, or Starbursts", sheet="The Rock Cycle: Vocabulary", also="Also CC.3–CC.6 and V.2 Compare ages of fossils in a rock sequence."),
    _lesson(26, 5, "Weather vs. Climate", "Present a short forecast and compare it with a climate description.", ["HH.1 Use data to describe climates", "GG.4 The greenhouse effect"], also="Also HH.2–HH.5 climate factors, atmospheric layers, and GG.1–GG.3 air masses. Severe weather names (hurricane, tornado) are IXL-only if climate skills are already solid."),
    _lesson(27, 5, "Water Cycle and Earth Systems", "Build a mini water cycle in a sealed bag and watch evaporation and condensation.", ["FF.2 Label parts of water cycle diagrams", "FF.3 Select parts of water cycle diagrams", "B.7 Understand an experimental protocol about evaporation"], materials="Ziplock bag, water, permanent marker"),
    _lesson(28, 5, "Solar System and Gravity", "Swing an object on a string to model an orbit.", ["JJ.6 Identify objects in the solar system", "JJ.7 Analyze data to compare properties of planets", "JJ.10 Gravity and its role in the universe"], materials="String and a small ball", sheet="Earth's Rotation and Revolution", also="Also the new skill: how mass affects gravitational force."),
    _lesson(29, 5, "Life Cycle of Stars and Our Place in the Universe", "Follow a star's life path from nebula to its ending.", ["JJ.9 Structure of the universe", "JJ.8 Identify constellations"], sheet="Earth-Sun-Moon System: Phases of the Moon", also="Also practice Moon phases, eclipses, seasons, and tides: JJ.1–JJ.5 and JJ.11. Those ideas are on the Grade 7 list and are not a separate live lesson."),
    _lesson(30, 6, "Matter and Its Properties", "Build particle models of solids, liquids, and gases, then identify mystery matter.", ["E.1 What are atoms and chemical elements?", "L.1 How does particle motion affect temperature?", "D.1 Compare the densities of substances"], materials="Household objects such as rice or beads", sheet="Classifying Matter Using Particle Models 1; Periodic Table", also="Also metals and nonmetals, D.2 density calculations, L.2–L.4, and F.1–F.5 formulas if atoms are already comfortable. KK unit abbreviations can sit here."),
    _lesson(31, 6, "Chemical Reactions", "Mix safe kitchen materials and separate physical changes from chemical reactions.", ["G.1 Identify reactants and products", "G.5 Compare physical and chemical changes", "G.2 Count atoms and molecules in chemical reactions"], materials="Baking soda, water, salt, sugar", also="G.3 amount calculations only after counting atoms is comfortable. Optional project: Self-Inflating Balloons."),
    _lesson(32, 6, "Forces and Motion Basics", "Launch a balloon rocket and connect the motion to Newton's laws.", ["I.5 Balanced and unbalanced forces", "I.6 Newton's laws of motion", "H.1 Calculate velocity from time and distance"], materials="Balloon, straw, string, tape", sheet="Newton's First Law of Motion; Newton's Second Law: Mass, Force, and Motion", also="Also H.6 Create a distance-time graph."),
    _lesson(33, 6, "Gravity, Friction, and Momentum", "Design a crash pad that protects a toy on impact.", ["I.2 How does mass affect force and acceleration?", "I.4 Predict forces using Newton's third law", "I.7 Collisions and car safety features"], materials="Toy, paper, cloth, tape", also="Also I.3 calculate acceleration, and H.2–H.5 and H.7 if velocity is already comfortable."),
    _lesson(34, 6, "Energy Transfer", "Build a short Rube Goldberg chain where one motion starts the next.", ["J.1 Identify changes in gravitational potential energy", "J.3 Explore energy transformations: roller coaster ride", "M. Conduction, convection, and radiation"], materials="Books, cups, pencils, toys, or domino-like objects", sheet="Changes in Potential Energy; Design Challenge: Design a Roller Coaster", also="Electricity and magnetism (K.1–K.4) are IXL-only. This course has no live electricity lesson. Also J.2, J.4, M.1, and M.2."),
    _lesson(35, 6, "Waves, Sound, and Light", "Make rice jump with sound, then test how light reflects and bends.", ["N.1 Transverse waves", "N.2 Longitudinal waves", "N.3 Sound waves", "N.4 Compare amplitudes, wavelengths, and frequencies of waves"], materials="Bowl, plastic wrap, rice, flashlight", also="Also N.6 transmission, reflection, and absorption. N.5 and N.7–N.9 after those are comfortable."),
    _lesson(36, 6, "Final STEM Project and Year Review", "Design and present a solution to a real problem using science from this year.", ["C.2 Evaluate tests of engineering-design solutions", "C.3 Use data from tests to compare engineering-design solutions", "C.4 Explore the engineering-design process: going to the Moon!"]),
]

# Question ids from science_content.QUESTION_BANK, placed on a Grade 7 lesson.
ASSIGNED: dict[int, list[int]] = {
    4: [1, 4, 27],
    6: [2, 3, 6, 13, 20, 23, 198, 206, 207],
    7: [8, 15],
    9: [5, 7, 9, 11, 12, 14, 17, 18, 19, 21, 22, 24, 26, 29, 30, 200, 201, 208, 209],
    10: [10, 16, 25, 28],
    11: [31, 32, 37, 52, 210, 218],
    12: [33, 34, 43, 44, 53, 54, 214, 219],
    13: [38, 39, 42, 211, 212, 213, 220, 221],
    14: [35, 40, 45, 51, 55, 217],
    15: [41, 49],
    16: [215],
    17: [56, 72, 74, 75, 76, 222, 223, 228],
    18: [57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 73, 79, 80, 81, 87, 225, 226, 231, 233],
    19: [229, 230],
    20: [83, 84, 227],
    21: [71, 77, 82, 86, 172, 173, 224, 256],
    22: [69, 70, 78, 232],
    23: [131, 132, 133, 134, 252],
    24: [135, 136, 137, 138, 139, 140, 141, 142, 175, 247],
    25: [143, 144, 145, 146, 147, 148, 149, 150, 174, 251, 257],
    26: [85, 151, 152, 153, 154, 155, 156, 157, 158, 246, 253],
    27: [68, 126, 127],
    28: [102, 159, 160, 161, 168, 170, 171, 254],
    29: [162, 163, 164, 165, 166, 167, 169, 248, 249, 250, 255, 258, 259],
    30: [89, 90, 91, 92, 93, 94, 97, 98, 99, 100, 101, 103, 112, 113, 114, 115, 116, 117, 120, 234, 235, 236, 243, 244],
    31: [95, 96, 121, 125],
    32: [111, 119, 124, 238],
    33: [104, 105, 130, 237],
    34: [106, 107, 108, 109, 110, 118, 122, 123, 129, 239, 241, 245],
    35: list(range(176, 198)) + [242] + list(range(260, 273)),
}

# Grade 6 items that are not part of this Grade 7 course.
DROPPED = {
    36, 46, 47, 48, 50, 88, 128, 199, 202, 203, 204, 205, 216, 240,
}


def _mc(question_id: int, lesson_id: int, question: str, options: list[str], answer: int, explanation: str) -> dict:
    return {
        "id": question_id,
        "lesson": lesson_id,
        "category": f"lesson_{lesson_id}",
        "question": question,
        "options": options,
        "answer": answer,
        "explanation": explanation,
    }


# New questions for units the weekly plan fills first: 1, 2, and 5.
EXTRA_QUESTIONS: list[dict] = [
    _mc(1001, 1, "Which statement is an observation?", ["The rock feels rough and has green specks", "The rock is beautiful", "The rock is boring", "The rock wants to be a fossil"], 0, "An observation uses senses or measurements. Calling it beautiful is an opinion."),
    _mc(1002, 1, "A scientific fact is best described as…", ["A claim backed by evidence that can be checked", "Whatever most people feel is true", "A guess with no test", "A story that cannot be changed"], 0, "Science trusts claims that evidence can support or challenge."),
    _mc(1003, 1, "You can see a closed box. Which clue is evidence about what is inside?", ["It rattles when you tilt it", "You hope it is candy", "It looks mysterious", "Your friend likes boxes"], 0, "The rattle is something you observed. A hope is not evidence."),
    _mc(1004, 1, "An inference is…", ["An idea you conclude from observations", "A measurement you write down", "The same thing as an opinion", "A tool in the lab"], 0, "You observe the rattle, then infer that something loose is inside."),
    _mc(1005, 1, "Why do scientists change an explanation?", ["New evidence disagrees with the old explanation", "They get bored of the old one", "Explanations must change every day", "Opinions are better than evidence"], 0, "A strong explanation survives tests. A weak one gets replaced when evidence says so."),
    _mc(1006, 1, "The first step in an engineering-design process is to…", ["Define the problem or need", "Buy the most expensive materials", "Skip testing", "Copy a design without looking at the goal"], 0, "Design starts by naming what the solution must do."),
    _mc(1007, 1, "Which of these is an opinion?", ["This leaf is the prettiest", "This leaf is 8 cm long", "This leaf has five points", "This leaf is green"], 0, "Pretty depends on the person. Length, shape, and color can be checked."),
    _mc(1008, 1, "A good science clue about a hidden object should…", ["Describe only what you can observe", "Name the object without looking", "Use the word 'obviously'", "Ignore what your senses tell you"], 0, "Mystery-scientist clues stay with the evidence."),
    _mc(1009, 2, "A hypothesis is…", ["A testable prediction", "The final answer", "A list of materials", "An opinion about the scientist"], 0, "A hypothesis says what you expect and can be checked with a test."),
    _mc(1010, 2, "In a paper-towel test, the kind of towel is the…", ["Independent variable", "Dependent variable", "Control variable that you keep the same", "The conclusion"], 0, "You choose the towel type. That is the independent variable."),
    _mc(1011, 2, "In that same test, how much water the towel absorbs is the…", ["Dependent variable", "Independent variable", "Hypothesis", "Constant"], 0, "The result you measure depends on the towel you chose."),
    _mc(1012, 2, "A fair test changes…", ["Only one variable at a time", "Every variable at once", "The hypothesis after each drop", "Nothing, including the towels"], 0, "If two things change, you cannot tell which one caused the result."),
    _mc(1013, 2, "The control group in an experiment is the group that…", ["Is kept in the usual condition for comparison", "Gets every new treatment", "Is left out of the data", "Proves the hypothesis before the test"], 0, "The control gives you a baseline."),
    _mc(1014, 2, "Which variable should stay the same when you compare two towels?", ["The amount of water you start with", "The brand of towel", "The thickness of the towel", "The material of the towel"], 0, "Water amount is a constant. Towel type is what you are comparing."),
    _mc(1015, 2, "The experimental group is the group that…", ["Receives the change you are testing", "Is never measured", "Is the same as your opinion", "Writes the lab report"], 0, "That group gets the treatment you want to study."),
    _mc(1016, 2, "Why write the steps of a test before you start?", ["So someone else can repeat the same test", "So you can change the data later", "So the hypothesis cannot be wrong", "So you do not need measurements"], 0, "A clear procedure makes the test repeatable."),
    _mc(1017, 3, "In Claim-Evidence-Reasoning, the claim is…", ["The answer you are arguing for", "The graph paper", "A feeling about the lab", "The list of materials"], 0, "The claim is the statement. Evidence and reasoning support it."),
    _mc(1018, 3, "Which sentence is evidence?", ["Plant A grew 4 cm and Plant B grew 1 cm", "I think plants are cool", "The experiment was fun", "Plants always do what I want"], 0, "Evidence is the measurement, not the feeling."),
    _mc(1019, 3, "Reasoning in a CER explanation…", ["Connects the evidence to the claim with a science idea", "Repeats the claim in the same words", "Replaces the data", "Is optional if you have a strong opinion"], 0, "Reasoning says why the evidence supports the claim."),
    _mc(1020, 3, "A line graph of plant height over days is useful because it…", ["Shows how the measurement changed over time", "Hides the numbers", "Replaces the need for a claim", "Proves every hypothesis"], 0, "The graph makes the pattern easier to see."),
    _mc(1021, 3, "You have seeds, cups, soil, and a ruler. Which question can you investigate?", ["Does the amount of water change how tall the seedlings grow?", "What do plants dream about?", "Which plant is the nicest?", "Will this seed be famous?"], 0, "You can measure water and height with those materials."),
    _mc(1022, 3, "In a plant-growth test, a good protocol includes…", ["What you will change, what you will measure, and what you will keep the same", "Only the conclusion", "A new hypothesis every hour", "No measurements"], 0, "The protocol is the plan for a fair test."),
    _mc(1023, 3, "Two plants got different amounts of light and different amounts of water. What is the problem?", ["You cannot tell which change caused the growth difference", "Graphs are not allowed", "Plants cannot be measured", "Claims do not need evidence"], 0, "Two changes at once make the result unclear."),
    _mc(1024, 3, "After you graph the data, the next science step is to…", ["Write a claim that the graph actually supports", "Pick the claim you liked before the test", "Erase points that do not match your guess", "Skip the reasoning"], 0, "The claim has to fit the evidence you collected."),
    _mc(1025, 4, "Cell theory says that…", ["All living things are made of one or more cells", "Only animals are made of cells", "Rocks are made of cells", "Cells are optional in plants"], 0, "If it is alive, it is made of cells."),
    _mc(1026, 4, "New cells come from…", ["Existing cells dividing", "Rocks breaking apart", "Sunlight by itself", "Empty space"], 0, "Cells arise from other cells."),
    _mc(1027, 4, "Most cells are…", ["Too small to see without a microscope", "As big as a soccer ball", "Visible across the room", "Larger than your hand"], 0, "A microscope lets you see the cells that make up living things."),
    _mc(1028, 4, "Bacteria are…", ["Living things made of cells", "Nonliving rocks", "Always viruses", "Too big to be cells"], 0, "A bacterium is a cell. A virus is not."),
    _mc(1029, 4, "Why is a virus not considered a cell?", ["It is not made of a cell and cannot carry out life functions on its own", "It has a nucleus and mitochondria", "It is a plant", "It is an animal organ"], 0, "Viruses need a host cell. They are not cells themselves."),
    _mc(1030, 5, "A prokaryotic cell…", ["Has no nucleus", "Always has chloroplasts", "Is only found in animals", "Is larger than every eukaryotic cell"], 0, "Prokaryotes keep their DNA in the cytoplasm, not in a nucleus."),
    _mc(1031, 5, "A eukaryotic cell…", ["Has a nucleus", "Never has DNA", "Is always a bacterium", "Has no cell membrane"], 0, "Plants, animals, fungi, and protists are eukaryotes."),
    _mc(1032, 5, "Which organism is prokaryotic?", ["A bacterium", "A maple tree", "A dog", "A mushroom"], 0, "Bacteria are the familiar prokaryotes in this course."),
    _mc(1033, 5, "Which structure do both prokaryotic and eukaryotic cells have?", ["A cell membrane", "A nucleus", "Chloroplasts", "A large central vacuole"], 0, "Both kinds of cells have a membrane around them."),
    _mc(1034, 5, "Where is the DNA in a prokaryotic cell?", ["In the cytoplasm", "Inside a nucleus", "Inside a chloroplast only", "Outside the cell"], 0, "No nucleus means the DNA sits in the cytoplasm."),
    _mc(1035, 5, "Compared with eukaryotic cells, prokaryotic cells are usually…", ["Smaller and simpler", "Always multicellular", "Filled with many organelles like mitochondria", "Unable to have DNA"], 0, "Prokaryotes are simpler cells."),
    _mc(1036, 5, "A plant cell is eukaryotic because it…", ["Has a nucleus", "Has no membrane", "Is a virus", "Has no DNA"], 0, "A nucleus is the marker used in this comparison."),
    _mc(1037, 5, "On a Venn diagram of the two cell types, the overlap should include…", ["Cell membrane and DNA", "Nucleus only", "Chloroplast only", "Bone and muscle"], 0, "Shared parts go in the middle. Nucleus goes only on the eukaryotic side."),
    _mc(1038, 7, "Which structure is found in plant cells but not animal cells?", ["A cell wall", "A cell membrane", "Cytoplasm", "A nucleus"], 0, "The cell wall sits outside the membrane and supports the plant cell."),
    _mc(1039, 7, "Chloroplasts are found in…", ["Plant cells", "Animal cells only", "Every prokaryote", "Viruses"], 0, "Chloroplasts capture light for photosynthesis."),
    _mc(1040, 7, "Which organelle is in both plant and animal cells?", ["Mitochondria", "Chloroplast", "Cell wall", "A large central vacuole that fills most of the cell"], 0, "Both kinds of cells need mitochondria to release energy."),
    _mc(1041, 7, "A large central vacuole is typical of…", ["Plant cells", "Animal cells", "Viruses", "Rocks"], 0, "It stores water and helps the plant cell keep its shape."),
    _mc(1042, 7, "Animal cells do not have…", ["A cell wall", "A nucleus", "A cell membrane", "Cytoplasm"], 0, "Animals are supported by skeletons and tissues, not cell walls."),
    _mc(1043, 7, "Both plant and animal cells have a nucleus, so both are…", ["Eukaryotic", "Prokaryotic", "Viruses", "Nonliving"], 0, "The nucleus puts them in the eukaryotic group."),
    _mc(1044, 8, "Diffusion is the movement of particles from…", ["Higher concentration to lower concentration", "Lower concentration to higher concentration, always", "Cold places to magnets", "The nucleus to the cell wall only"], 0, "Particles spread out until they are more even."),
    _mc(1045, 8, "Osmosis is…", ["The diffusion of water across a membrane", "The cell making food", "A type of mitosis", "Water boiling"], 0, "Osmosis is a special case of diffusion: water moving through a membrane."),
    _mc(1046, 8, "A gummy bear left in plain water usually…", ["Swells as water moves in", "Turns into salt", "Loses all of its sugar and disappears instantly", "Becomes a prokaryote"], 0, "Water enters the bear because the water concentration is higher outside."),
    _mc(1047, 8, "A gummy bear in very salty water often…", ["Shrinks as water moves out", "Grows a cell wall", "Freezes", "Starts photosynthesis"], 0, "Water leaves the bear toward the saltier side."),
    _mc(1048, 8, "The cell structure that controls what enters and leaves is the…", ["Cell membrane", "Nucleus", "Chloroplast", "Ribosome"], 0, "The membrane is the gate for diffusion and osmosis."),
    _mc(1049, 8, "Simple diffusion does not require the cell to…", ["Use energy", "Have a membrane", "Be made of matter", "Contain water"], 0, "The particles move on their own from high to low concentration."),
    _mc(1050, 8, "Equilibrium in diffusion means…", ["Concentrations have become more balanced", "All water has left the cell forever", "The cell has stopped being alive", "Salt has turned into sugar"], 0, "Net movement slows when both sides are similar."),
    _mc(1051, 8, "In an osmosis test, the independent variable is often…", ["Whether the water is plain or salty", "The color of the cup", "The day of the week", "The scientist's favorite candy"], 0, "You change the liquid and watch what the gummy bear does."),
    _mc(1052, 10, "After you sprint, your pulse usually rises so that…", ["Muscles get oxygen faster", "Your bones can grow instantly", "You stop needing water", "Your cells leave your body"], 0, "A faster heart moves oxygen and food to working muscles."),
    _mc(1053, 10, "Sweating helps homeostasis by…", ["Cooling the body when it is too warm", "Adding salt to your bones", "Stopping your heart", "Turning sweat into food"], 0, "Evaporating sweat carries heat away."),
    _mc(1054, 10, "Shivering is a response that…", ["Warms the body when it is cold", "Digests lunch", "Replaces the nucleus", "Stops diffusion"], 0, "Muscle activity releases heat."),
    _mc(1055, 10, "Homeostasis in the body means…", ["Organs work together to keep internal conditions steady", "The body never changes", "Only the heart is involved", "Cells stop using oxygen"], 0, "Pulse, breathing, and temperature shift, then move back toward balance."),
    _mc(1056, 23, "Earth's geosphere is…", ["The solid rock of the crust and deeper layers", "Only the air", "Only the oceans", "Only living things"], 0, "Geo means earth. The geosphere is the rocky part."),
    _mc(1057, 23, "The hydrosphere includes…", ["Oceans, rivers, ice, and other water", "Only the inner core", "Only the clouds of Jupiter", "Only living cells"], 0, "Hydro means water."),
    _mc(1058, 23, "The biosphere is…", ["All the places where life exists", "The liquid outer core only", "A kind of igneous rock", "The Moon's craters"], 0, "Bio means life. Living things sit within the other spheres."),
    _mc(1059, 23, "The atmosphere is…", ["The layer of gases around Earth", "The solid inner core", "The tectonic plates only", "A fossil"], 0, "We live at the bottom of that blanket of air."),
    _mc(1060, 27, "Precipitation in the water cycle is…", ["Water falling as rain, snow, sleet, or hail", "Water soaking into magma", "Rock melting", "Wind changing direction"], 0, "After clouds form, water can fall back to the surface."),
    _mc(1061, 27, "What mainly powers the water cycle?", ["Energy from the Sun", "The Moon's craters", "Fossils", "A bar magnet"], 0, "Sunlight heats water so it can evaporate."),
    _mc(1062, 27, "Droplets on the inside of a sealed water-cycle bag are evidence of…", ["Condensation", "The rock cycle", "Mitosis", "A solar eclipse"], 0, "Water vapor cooled on the plastic and turned back into liquid."),
    _mc(1063, 27, "Water vapor is…", ["Water in the gas state", "Solid ice only", "A kind of rock", "Liquid water in a lake"], 0, "Evaporation turns liquid water into vapor."),
    _mc(1064, 27, "After rain hits the ground, water may…", ["Run off to rivers or soak into the soil", "Turn into iron in the core", "Leave Earth immediately", "Become a star"], 0, "Collection and infiltration return water to the cycle."),
]


def _coverage() -> None:
    source_ids = {q["id"] for q in science_bank.QUESTION_BANK}
    assigned: dict[int, int] = {}
    for lesson_id, question_ids in ASSIGNED.items():
        for question_id in question_ids:
            if question_id in assigned:
                raise RuntimeError(f"Question {question_id} is on lessons {assigned[question_id]} and {lesson_id}")
            assigned[question_id] = lesson_id
    overlap = set(assigned) & DROPPED
    if overlap:
        raise RuntimeError(f"Questions both kept and dropped: {sorted(overlap)}")
    missing = source_ids - set(assigned) - DROPPED
    unknown = (set(assigned) | DROPPED) - source_ids
    if missing or unknown:
        raise RuntimeError(f"Unplaced questions {sorted(missing)}; unknown ids {sorted(unknown)}")


_coverage()

_LESSON_BY_ID = {lesson["id"]: lesson for lesson in LESSONS}
_UNIT_BY_ID = {unit["id"]: unit for unit in UNITS}
_SOURCE_BY_ID = {q["id"]: q for q in science_bank.QUESTION_BANK}


def _with_lesson(question: dict, lesson_id: int) -> dict:
    item = copy.deepcopy(question)
    item["lesson"] = lesson_id
    item["category"] = f"lesson_{lesson_id}"
    return item


QUESTIONS: list[dict] = []
for _lesson_id, _ids in ASSIGNED.items():
    for _qid in _ids:
        QUESTIONS.append(_with_lesson(_SOURCE_BY_ID[_qid], _lesson_id))
QUESTIONS.extend(copy.deepcopy(EXTRA_QUESTIONS))

_QUESTIONS_BY_LESSON: dict[int, list[dict]] = {lesson["id"]: [] for lesson in LESSONS}
for _question in QUESTIONS:
    _QUESTIONS_BY_LESSON[_question["lesson"]].append(_question)


def lesson_by_id(lesson_id: int) -> dict:
    return _LESSON_BY_ID[int(lesson_id)]


def unit_by_id(unit_id: int) -> dict:
    return _UNIT_BY_ID[int(unit_id)]


def unit_for_lesson(lesson_id: int) -> dict:
    return unit_by_id(lesson_by_id(lesson_id)["unit_id"])


def questions_for_lesson(lesson_id: int) -> list[dict]:
    return list(_QUESTIONS_BY_LESSON.get(int(lesson_id), []))


def questions_for_unit(unit_id: int) -> list[dict]:
    unit = unit_by_id(unit_id)
    pool: list[dict] = []
    for lesson_id in unit["lesson_ids"]:
        pool.extend(_QUESTIONS_BY_LESSON.get(lesson_id, []))
    return pool


def question_counts() -> dict[int, int]:
    return {lesson_id: len(items) for lesson_id, items in _QUESTIONS_BY_LESSON.items()}


def clamp_lesson(lesson_number: int) -> int:
    return max(1, min(36, int(lesson_number)))


def _shuffle_question(question: dict) -> dict:
    item = copy.deepcopy(question)
    correct = item["options"][item["answer"]]
    options = list(item["options"])
    random.shuffle(options)
    item["options"] = options
    item["answer"] = options.index(correct)
    return item


def word_stems_for_unit(unit_id: int) -> list[dict]:
    return list(UNIT_WORD_STEMS.get(int(unit_id), []))


def _stem_questions() -> list[dict]:
    """One question per Unit 1 stem, kept out of the lesson banks."""
    stems = {row["stem"]: row for row in UNIT_WORD_STEMS[1]}

    def ask(question_id: int, stem: str, prompt: str, options: list[str], answer: int, explanation: str) -> dict:
        row = stems[stem]
        return _mc(question_id, 1, prompt, options, answer, explanation + f" Stem {row['stem']} means {row['meaning']}. Example: {row['example']}.")

    return [
        ask(1101, "atmo", "The stem atmo means…", ["vapor", "heat", "middle", "heavy"], 0, "Atmosphere is the vapor layer around Earth."),
        ask(1102, "cycle", "The stem cycle means…", ["ring or circle", "a straight line", "heavy", "a ray"], 0, "The water cycle is water moving in a circle."),
        ask(1103, "spher", "The stem spher means…", ["ball or round", "layer", "high", "thick"], 0, "Atmosphere uses spher, the round blanket of air around Earth."),
        ask(1104, "thermo", "Which layer's name uses the stem for heat?", ["Thermosphere", "Mesosphere", "Exosphere", "Troposphere"], 0, "Thermo means heat."),
        ask(1105, "ex", "The stem ex means…", ["out of or away from", "middle", "heavy", "a circle"], 0, "The exosphere is the outer layer, away from Earth's surface."),
        ask(1106, "meso", "The stem meso means…", ["middle", "heat", "pressure", "vapor"], 0, "The mesosphere is the middle layer of the atmosphere."),
        ask(1107, "strat", "The stem strat means…", ["layer", "ray", "thick", "to carry"], 0, "The stratosphere is a layer of the atmosphere."),
        ask(1108, "trop", "The stem trop means…", ["change or turn", "high", "vapor", "ball"], 0, "Weather turns and changes in the troposphere."),
        ask(1109, "grav", "The stem grav means…", ["heavy", "light", "middle", "out of"], 0, "Gravity is the pull that makes things feel heavy."),
        ask(1110, "baro", "A barometer measures pressure. The stem baro means…", ["pressure", "heat", "ray", "circle"], 0, "Baro means pressure."),
        ask(1111, "vectus", "The stem vectus means…", ["to carry", "to melt", "to measure", "to freeze"], 0, "Convection carries heat as warm air or water moves."),
        ask(1112, "alt", "The stem alt means…", ["high", "low", "thick", "round"], 0, "Altitude is how high something is."),
        ask(1113, "densus", "The stem densus means…", ["thick", "thin", "high", "a ray"], 0, "Density describes how thickly matter is packed."),
        ask(1114, "radi", "The stem radi means…", ["ray", "layer", "circle", "heavy"], 0, "Radiation travels in rays, including heat from the Sun."),
        ask(1115, "tudo", "The stem tudo means…", ["state or condition", "middle layer", "to carry", "vapor"], 0, "The ending -tude names a state or condition, as in altitude."),
    ]


STEM_QUESTIONS: list[dict] = _stem_questions()


def build_stem_quiz(unit_id: int) -> list[dict]:
    if int(unit_id) != 1:
        return []
    pool = STEM_QUESTIONS
    picked = random.sample(pool, min(STEM_QUIZ_SIZE, len(pool)))
    return [_shuffle_question(q) for q in picked]


def build_quiz(*, lesson_id: int | None = None, unit_id: int | None = None) -> list[dict]:
    """Return a shuffled quiz. Does not change the stored question bank."""
    if lesson_id is not None:
        pool = questions_for_lesson(lesson_id)
        limit = LESSON_QUIZ_SIZE
    elif unit_id is not None:
        pool = questions_for_unit(unit_id)
        limit = UNIT_QUIZ_SIZE
    else:
        return []
    if not pool:
        return []
    picked = random.sample(pool, min(limit, len(pool)))
    return [_shuffle_question(q) for q in picked]
