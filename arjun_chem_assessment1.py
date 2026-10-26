"""
Chemical Reactions Assessment 1 study guide for Arjun.

Parts 4–7 of the packet become checked practice. Data tables and the two
diagrams stay on screen. The correct choice is always options[0]; build_quiz
shuffles a copy.
"""

from __future__ import annotations

import copy
import random

TITLE = "Chemical Reactions Assessment 1"
CHOICE_QUIZ_SIZE = 10

INVESTIGATION_A = {
    "title": "Investigation A · Open and closed systems",
    "intro": "Students mixed the same amounts of two substances.",
    "columns": ["System", "Mass before", "Mass after", "Change"],
    "rows": [
        ["Sealed bottle", "156.8 g", "156.8 g", "0.0 g"],
        ["Open cup", "156.8 g", "154.9 g", "-1.9 g"],
    ],
}

INVESTIGATION_B = {
    "title": "Investigation B · Bath bomb combination tests",
    "intro": "Each row is one test. Bubbles tells whether the mix fizzed.",
    "columns": ["Combination", "Observation", "Bubbles"],
    "rows": [
        ["Baking soda + water", "Powder partly dissolved", "No"],
        ["Citric acid + water", "Solid dissolved", "No"],
        ["Baking soda + citric acid dry", "Powders mixed; little visible change", "No"],
        ["Baking soda + citric acid + water", "Immediate fizzing and many bubbles", "Yes"],
        ["Baking soda + citric acid + oil", "Powders settled; little visible change", "No"],
    ],
}

CARROT = {
    "title": "Investigation C · Carrot and mystery liquids",
    "intro": "Carrot mass is 27.0 g. The water level rises from 40.0 mL to 62.5 mL.",
    "columns": ["Measurement", "Value"],
    "rows": [
        ["Mass", "27.0 g"],
        ["Water level before", "40.0 mL"],
        ["Water level with carrot", "62.5 mL"],
    ],
}

DENSITY_COLUMN = {
    "title": "Investigation D · Mystery density column",
    "intro": "The top layer is listed first. The liquids do not mix.",
    "columns": ["Place in the column", "Density"],
    "rows": [
        ["Top", "0.85 g/mL"],
        ["Second", "1.00 g/mL"],
        ["Third", "1.10 g/mL"],
        ["Bottom", "1.30 g/mL"],
    ],
}

FLOAT_DESIGN = {
    "title": "Investigation F · Ocean float design",
    "intro": "The float base is 18.3 kg. A design needs at least 3 packages, a total mass of 27.0 kg or less, and at least 7 value points.",
    "columns": ["Package", "Mass", "Value points", "What it measures"],
    "rows": [
        ["CTD", "3.3 kg", "3", "Temperature, salinity, depth"],
        ["Dissolved oxygen", "2.5 kg", "2", "Oxygen available to organisms"],
        ["Nitrate", "0.8 kg", "2", "Nutrients for phytoplankton"],
        ["Bio-optics", "2.7 kg", "3", "Chlorophyll and particles"],
    ],
}


def _q(question_id, topic, question, options, explanation, table=None, image=None):
    item = {
        "id": question_id,
        "topic": topic,
        "question": question,
        "options": options,
        "answer": 0,
        "explanation": explanation,
    }
    if table is not None:
        item["table"] = table
    if image is not None:
        item["image"] = image
    return item


CHOICE_QUESTIONS: list[dict] = [
    _q("mc-1", "Part 4", "Which statement best explains why air is matter?", [
        "Air has mass and takes up space",
        "Air is usually invisible",
        "Air always moves upward",
        "Air has no particles",
    ], "Matter has mass and takes up space. Invisible gases still count."),
    _q("mc-2", "Part 4", "Which description is a physical property?", [
        "A liquid has a density of 0.90 g/mL",
        "A substance can burn",
        "A metal reacts with acid",
        "Wood forms ash when heated",
    ], "Density can be measured without turning the liquid into a new substance."),
    _q("mc-3", "Part 4", "Which description is a chemical property?", [
        "Flammability",
        "Color",
        "Boiling point",
        "Volume",
    ], "Flammability describes how a substance can burn and form new substances."),
    _q("mc-4", "Part 4", "Which event is a physical change?", [
        "Ice melting",
        "Iron rusting",
        "Wood burning",
        "An egg rotting",
    ], "Melting changes the state. The substance is still water."),
    _q("mc-5", "Part 4", "Which event is the strongest evidence that a new substance may have formed?", [
        "An unexpected gas formed after substances were mixed",
        "A solid was cut into pieces",
        "A liquid was poured into a new cup",
        "Water froze into ice",
    ], "A new gas from mixing is evidence of a chemical change. Cutting, pouring, and freezing do not make a new substance."),
    _q("mc-6", "Part 4", "A powder seems to disappear when stirred into water. What is the best explanation?", [
        "The powder dissolved and its particles spread through the water",
        "The matter was destroyed",
        "The powder became weightless",
        "The water removed all particles",
    ], "Dissolving spreads particles through the liquid. The matter is still there."),
    _q("mc-7", "Part 4", "Which statement is an inference?", [
        "The reaction released energy",
        "The liquid temperature is 31°C",
        "Bubbles are rising through the liquid",
        "A white solid is at the bottom",
    ], "Temperature, bubbles, and a white solid are observations. Saying the reaction released energy is an interpretation."),
    _q("mc-8", "Part 4", "A sealed bottle has a mass of 212.4 g before mixing and 212.4 g after bubbling stops. What is supported?", [
        "Mass was conserved in the closed system",
        "The gas has no mass",
        "All particles disappeared",
        "The balance ignored the products",
    ], "Nothing entered or left the sealed bottle, and the mass stayed 212.4 g."),
    _q("mc-9", "Part 4", "An uncovered cup loses 2.1 g during a bubbling reaction. Which explanation is most reasonable?", [
        "Some matter may have left the system as gas",
        "Matter was destroyed",
        "The products have no particles",
        "The cup became less dense, so mass vanished",
    ], "An open cup lets gas cross the boundary, so the measured mass can fall."),
    _q("mc-10", "Part 4", "Which particle explanation agrees with conservation of matter?", [
        "Atoms rearrange into new molecules while the total matter remains",
        "Atoms vanish when a gas forms",
        "Heat creates new atoms from nothing",
        "Gas particles do not count as matter",
    ], "Atoms are rearranged. They are not created or destroyed."),
    _q("mc-11", "Part 4", "Which combination should produce the strongest bath-bomb bubbling?", [
        "Baking soda, citric acid, and water",
        "Baking soda and water",
        "Citric acid and water",
        "Baking soda and citric acid kept dry",
    ], "Strong bubbling needs both powders and water so they can interact."),
    _q("mc-12", "Part 4", "Which test best checks whether bath-bomb gas was already trapped in the dry solid?", [
        "Test ingredients separately and in controlled combinations with and without water",
        "Compare the colors of two bath bombs",
        "Measure the diameter only",
        "Place two identical bath bombs in the same cup",
    ], "Dry powders show little change. Bubbles appear when water lets the ingredients react, so the gas is not just stored in the dry solid."),
    _q("mc-13", "Part 4", "What does flammability describe?", [
        "Whether a substance can burn under suitable conditions",
        "How easily a substance dissolves",
        "How much space a substance takes up",
        "Whether a liquid floats",
    ], "Flammability is a chemical property."),
    _q("mc-14", "Part 4", "A gas puts out a flame and moves downward through air. Which conclusion is best?", [
        "Its properties are consistent with carbon dioxide, but more evidence may be needed",
        "It is definitely helium",
        "It is definitely oxygen",
        "It is not matter",
    ], "One or two properties can match a gas. Identifying it confidently needs several properties."),
    _q("mc-15", "Part 4", "Which sentence is evidence in a CER?", [
        "The flame went out when placed in the collected gas",
        "The gas is not flammable",
        "A nonflammable gas does not continue burning, so the result supports the claim",
        "I think the gas is interesting",
    ], "Evidence is the observation. The claim and the science connection are the other CER parts."),
    _q("mc-16", "Part 4", "Which equation calculates density?", [
        "mass ÷ volume",
        "mass × volume",
        "volume ÷ mass",
        "mass + volume",
    ], "Density = mass ÷ volume. Common units are g/mL or g/cm³."),
    _q("mc-17", "Part 4", "A sample has a mass of 42 g and a volume of 35 mL. What is its density?", [
        "1.20 g/mL",
        "0.83 g/mL",
        "1.00 g/mL",
        "7.0 g/mL",
    ], "42 ÷ 35 = 1.20. Include g/mL."),
    _q("mc-18", "Part 4", "An object with a density of 1.08 g/mL is placed in a liquid with a density of 1.20 g/mL. What should happen?", [
        "It should generally float",
        "It should generally sink",
        "Its mass becomes zero",
        "It changes into a gas",
    ], "1.08 is less than 1.20, so the object is less dense than the liquid and floats."),
    _q("mc-19", "Part 4", "Why is saltwater often denser than freshwater?", [
        "Dissolved salt adds mass with little change in volume",
        "Salt removes particles from the water",
        "Saltwater has no volume",
        "Salt makes every object less dense",
    ], "Extra mass in about the same volume raises the density."),
    _q("mc-20", "Part 4", "Three nonmixing liquids have densities of 0.80, 1.00, and 1.25 g/mL. What is their order from top to bottom?", [
        "0.80, 1.00, 1.25",
        "1.25, 1.00, 0.80",
        "1.00, 0.80, 1.25",
        "0.80, 1.25, 1.00",
    ], "The least dense liquid stays on top. The most dense liquid settles at the bottom."),
    _q("mc-21", "Part 4", "Which method gives a density column the best chance to form stable layers?", [
        "Pour slowly and avoid stirring",
        "Shake after each liquid is added",
        "Use new liquids in every trial",
        "Judge only by color",
    ], "Stirring mixes the layers. A slow pour lets density stack them."),
    _q("mc-22", "Part 4", "Which starting substance is used in Elephant Toothpaste?", [
        "Hydrogen peroxide",
        "Saltwater",
        "Citric acid only",
        "Carbon dioxide",
    ], "The reaction starts with hydrogen peroxide."),
    _q("mc-23", "Part 4", "What is the main role of dish soap in Elephant Toothpaste?", [
        "It traps gas in bubbles and makes foam visible",
        "It creates oxygen atoms",
        "It stops the reaction",
        "It changes oxygen into carbon dioxide",
    ], "The soap does not make the gas. It catches the gas so you can see foam."),
    _q("mc-24", "Part 4", "What is the role of the catalyst in yeast?", [
        "It speeds up the reaction",
        "It adds all the matter to the products",
        "It creates soap",
        "It lowers the mass of the system",
    ], "A catalyst speeds the reaction. It is not the source of the new matter."),
    _q("mc-25", "Part 4", "The Elephant Toothpaste bottle becomes warmer. What does this support?", [
        "Energy was transferred to the surroundings",
        "All heat was destroyed",
        "The foam has no energy",
        "The gas became massless",
    ], "A warmer bottle means energy left the reaction and warmed the surroundings."),
    _q("mc-26", "Part 4", "Two reactions both make bubbles. What can you conclude?", [
        "Both may produce gas, but more evidence is needed to identify each gas",
        "They must produce the same gas",
        "They must use the same reactants",
        "All bubbles contain oxygen",
    ], "Bubbles show a gas. They do not name which gas."),
    _q("mc-27", "Part 4", "What is the main purpose of an ocean science float?", [
        "Collect ocean measurements over time",
        "Carry passengers",
        "Remove salt from seawater",
        "Heat deep water",
    ], "The float's mission is to collect measurements, not to carry people."),
    _q("mc-28", "Part 4", "Which set of measurements comes from a CTD?", [
        "Temperature, salinity, and pressure/depth",
        "Wind, rainfall, and cloud cover",
        "Fish count, waves, and sunlight",
        "Nitrate, chlorophyll, and GPS only",
    ], "CTD means conductivity/salinity, temperature, and depth from pressure."),
    _q("mc-29", "Part 4", "A float has a base mass of 18.3 kg and instruments of 3.3 kg, 2.5 kg, and 0.8 kg. What is the total?", [
        "24.9 kg",
        "21.6 kg",
        "25.7 kg",
        "27.0 kg",
    ], "18.3 + 3.3 + 2.5 + 0.8 = 24.9 kg."),
    _q("mc-30", "Part 4", "A design must have at least 3 instruments, a mass of 27 kg or less, and at least 7 value points. Which design meets all constraints?", [
        "3 instruments, 26 kg, 7 points",
        "2 instruments, 24 kg, 8 points",
        "3 instruments, 28 kg, 9 points",
        "4 instruments, 25 kg, 6 points",
    ], "Two instruments is too few, 28 kg is over the limit, and 6 points is under 7."),
]

WORD_QUESTIONS: list[dict] = [
    _q("w-1", "Part 5", "Anything that has mass and takes up space is…", [
        "matter", "density", "foam", "an inference",
    ], "That is the definition of matter."),
    _q("w-2", "Part 5", "Mass divided by volume is…", [
        "density", "matter", "a catalyst", "flammability",
    ], "Density = mass ÷ volume."),
    _q("w-3", "Part 5", "Bubbles can be evidence that a __________ has formed.", [
        "gas", "CTD", "closed system", "physical change only",
    ], "Bubbles are a visible sign that a gas formed."),
    _q("w-4", "Part 5", "In a sealed reaction, total mass should be…", [
        "conserved", "lower", "destroyed", "doubled",
    ], "A closed system keeps the matter inside, so the mass stays the same."),
    _q("w-5", "Part 5", "Dish soap traps gas and produces visible…", [
        "foam", "CTD readings", "rust", "a closed system",
    ], "The soap catches the gas and makes foam you can see."),
    _q("w-6", "Part 5", "A __________ measures ocean temperature, salinity, and pressure/depth.", [
        "CTD", "catalyst", "density column", "flame test",
    ], "Those three measurements are the CTD package."),
    _q("w-7", "Part 5", "An object generally floats when its density is __________ than the liquid’s density.", [
        "lower", "higher", "equal to zero", "unknown",
    ], "Lower density than the liquid means the object floats."),
    _q("w-8", "Part 5", "“The temperature increased by 5°C” is a direct…", [
        "observation", "inference", "chemical property", "constraint",
    ], "A tool measurement is an observation."),
    _q("w-9", "Part 5", "“The reaction released energy” is an __________ based on temperature evidence.", [
        "inference", "observation", "equation", "open system",
    ], "The temperature rise is observed. The energy explanation is the inference."),
    _q("w-10", "Part 5", "The ability of a substance to burn is called…", [
        "flammability", "solubility", "buoyancy", "volume",
    ], "Flammability is the chemical property of being able to burn."),
    _q("w-11", "Part 5", "A substance that speeds up a reaction without being used up the same way is a…", [
        "catalyst", "closed system", "CTD", "physical change",
    ], "Yeast acts as a catalyst in Elephant Toothpaste by speeding the reaction."),
    _q("w-12", "Part 5", "Burning wood is a __________ because new substances form.", [
        "chemical change", "physical change", "density", "observation",
    ], "Ash, smoke, and other new substances mean the wood itself changed."),
    _q("s-ice", "Part 5", "Sort this example: melting ice.", [
        "Physical change", "Physical property", "Chemical property", "Chemical change",
    ], "Ice becomes liquid water. The substance is still water."),
    _q("s-oil", "Part 5", "Sort this example: the density of oil is 0.90 g/mL.", [
        "Physical property", "Physical change", "Chemical property", "Chemical change",
    ], "Density is measured without changing what the oil is."),
    _q("s-burn", "Part 5", "Sort this example: wood can burn.", [
        "Chemical property", "Physical property", "Physical change", "Chemical change",
    ], "“Can burn” describes flammability, a chemical property. The burning itself would be the change."),
    _q("s-rust", "Part 5", "Sort this example: iron forms rust.", [
        "Chemical change", "Physical change", "Physical property", "Chemical property",
    ], "Rust is a new substance, so forming it is a chemical change."),
    _q("s-boil", "Part 5", "Sort this example: water boils.", [
        "Physical change", "Chemical change", "Chemical property", "Physical property",
    ], "Boiling changes liquid water to water vapor. It is still water."),
    _q("s-dissolve", "Part 5", "Sort this example: citric acid dissolves in water.", [
        "Physical change", "Chemical change", "Chemical property", "Physical property",
    ], "Dissolving spreads the citric acid particles. It does not by itself make a new substance."),
]

DATA_QUESTIONS: list[dict] = [
    _q("a-closed", "Investigation A", "Which system is closed? Use the mass data as evidence.", [
        "The sealed bottle, because its mass stayed 156.8 g",
        "The open cup, because its mass fell by 1.9 g",
        "Both, because they started at the same mass",
        "Neither, because both held a mixture",
    ], "A closed system does not let matter in or out. The sealed bottle's change is 0.0 g.", table=INVESTIGATION_A),
    _q("a-open-loss", "Investigation A", "Why might the open cup have a lower final mass?", [
        "A gas made by the reaction left the open cup",
        "The scale removed 1.9 g on its own",
        "The sealed bottle took mass from the cup",
        "The matter in the cup was destroyed",
    ], "The open cup went from 156.8 g to 154.9 g. The sealed bottle lost nothing, so the missing mass left the open system.", table=INVESTIGATION_A),
    _q("a-not-destroyed", "Investigation A", "Why do these results not show that matter was destroyed?", [
        "The sealed bottle kept all 156.8 g, so the matter was still there",
        "The open cup ended heavier than it started",
        "Both systems lost 1.9 g",
        "The change column shows new matter was created",
    ], "If matter had been destroyed, the sealed bottle would lose mass too. Its change is 0.0 g.", table=INVESTIGATION_A),
    _q("b-claim", "Investigation B", "Which materials are needed for strong bubbling?", [
        "Baking soda, citric acid, and water",
        "Baking soda and water only",
        "Citric acid and water only",
        "Baking soda, citric acid, and oil",
    ], "Only baking soda + citric acid + water has Bubbles = Yes.", table=INVESTIGATION_B),
    _q("b-evidence", "Investigation B", "Which two rows best support that claim?", [
        "Baking soda + citric acid + water (Yes) and baking soda + citric acid dry (No)",
        "Baking soda + water (No) and citric acid + water (No)",
        "Baking soda + citric acid + oil (No) and citric acid + water (No)",
        "Baking soda + water (No) and baking soda + citric acid + oil (No)",
    ], "The water row shows the strong reaction. The dry row shows the same powders do not bubble without water.", table=INVESTIGATION_B),
    _q("b-water", "Investigation B", "What role does water appear to play?", [
        "Water lets the baking soda and citric acid interact and form gas",
        "Water is the gas that was stored in the dry powders",
        "Water stops the powders from touching",
        "Water has the same effect as oil",
    ], "The dry mix and the oil mix show little change. Bubbles appear when water is the liquid.", table=INVESTIGATION_B),
    _q("c-volume", "Investigation C", "What is the carrot’s volume?", [
        "22.5 mL",
        "27.0 mL",
        "62.5 mL",
        "102.5 mL",
    ], "Volume = 62.5 mL − 40.0 mL = 22.5 mL.", table=CARROT),
    _q("c-density", "Investigation C", "What is the carrot’s density?", [
        "1.20 g/mL",
        "0.43 g/mL",
        "27.0 g/mL",
        "22.5 g/mL",
    ], "Density = 27.0 g ÷ 22.5 mL = 1.20 g/mL.", table=CARROT),
    _q("c-liquids", "Investigation C", "The carrot sinks in Mystery Liquid A and floats in Mystery Liquid B. What does that say about the densities?", [
        "Liquid A is less dense than 1.20 g/mL, and Liquid B is more dense than 1.20 g/mL",
        "Both liquids are less dense than the carrot",
        "Both liquids are more dense than the carrot",
        "The carrot’s density changes in each liquid",
    ], "It sinks when it is denser than the liquid and floats when it is less dense than the liquid.", table=CARROT),
    _q("c-salt", "Investigation C", "Could these results alone prove that Liquid B contains salt?", [
        "No. Another dissolved substance could also raise the density",
        "Yes. Only salt can make a carrot float",
        "Yes. Floating always means the liquid is freshwater",
        "No. Density has nothing to do with floating",
    ], "Salt is one way to add mass. The float test shows Liquid B is denser than the carrot, not what is dissolved in it.", table=CARROT),
    _q("d-ends", "Investigation D", "Which layer is the least dense, and which is the most dense?", [
        "0.85 g/mL is least dense and on top; 1.30 g/mL is most dense and on the bottom",
        "1.30 g/mL is least dense because it is on the bottom",
        "1.00 g/mL is both the least and the most dense",
        "0.85 g/mL is the most dense because it is orange",
    ], "In a column of liquids that do not mix, density increases from top to bottom.", table=DENSITY_COLUMN, image="chem_density_column"),
    _q("d-115", "Investigation D", "Where would a nonmixing liquid with a density of 1.15 g/mL settle?", [
        "Between the 1.10 g/mL layer and the 1.30 g/mL layer",
        "Above the 0.85 g/mL layer",
        "Between the 0.85 g/mL layer and the 1.00 g/mL layer",
        "Mixed evenly through every layer",
    ], "1.15 is greater than 1.10 and less than 1.30, so it sits between those two layers.", table=DENSITY_COLUMN, image="chem_density_column"),
    _q("d-pattern", "Investigation D", "What pattern explains the column?", [
        "The least dense liquid stays on top, and each denser liquid settles below it",
        "The liquids stack by color, from orange to brown",
        "The densest liquid rises to the top",
        "Equal densities always form four layers",
    ], "Each layer is denser than the one above it: 0.85, then 1.00, then 1.10, then 1.30.", table=DENSITY_COLUMN, image="chem_density_column"),
    _q("e-change", "Investigation E", "What change does the model show after the bath bomb is added to water?", [
        "The particles mix in the liquid, and new gas particles appear above it",
        "The water particles disappear",
        "The bath-bomb particles stay in their own box",
        "New gas particles replace every water particle",
    ], "Before mixing, water and bath-bomb particles are separate. After mixing, they share the liquid and new gas particles are above it.", image="chem_particle_model"),
    _q("e-evidence", "Investigation E", "Which two details from the model are the best evidence?", [
        "Separate particle boxes become one mixture, and open circles labeled new gas particles appear",
        "The water box stays full and the bath-bomb box stays separate",
        "The gas particles are the same color as the water particles",
        "The boxes get larger but the particles do not move",
    ], "The model shows rearrangement into a mixture and new gas particles. Particles are not erased.", image="chem_particle_model"),
    _q("f-a", "Investigation F", "CTD + dissolved oxygen + nitrate: what are the total mass and value points, and does the design meet every constraint?", [
        "24.9 kg and 7 points. Yes, it meets all three constraints",
        "24.9 kg and 7 points. No, because the mass is over 27.0 kg",
        "26.8 kg and 8 points. Yes",
        "18.3 kg and 3 points. Yes",
    ], "18.3 + 3.3 + 2.5 + 0.8 = 24.9 kg. Points are 3 + 2 + 2 = 7. That is 3 packages, under 27.0 kg, and at least 7 points.", table=FLOAT_DESIGN),
    _q("f-b", "Investigation F", "CTD + dissolved oxygen + bio-optics: what are the total mass and value points, and does the design meet every constraint?", [
        "26.8 kg and 8 points. Yes, it meets all three constraints",
        "26.8 kg and 8 points. No, because 26.8 kg is over 27.0 kg",
        "24.9 kg and 7 points. Yes",
        "27.3 kg and 8 points. No",
    ], "18.3 + 3.3 + 2.5 + 2.7 = 26.8 kg. Points are 3 + 2 + 3 = 8. The mass is still under 27.0 kg.", table=FLOAT_DESIGN),
    _q("f-choice", "Investigation F", "Which design is stronger for studying conditions that affect phytoplankton, and what is one limitation?", [
        "Design A, because nitrate measures nutrients. A limitation is that it does not measure chlorophyll",
        "Design B, because it is over the mass limit and that makes it stronger",
        "Design A, because 7 points is below the requirement",
        "Neither, because a float cannot carry a CTD",
    ], "Nitrate tells about nutrients phytoplankton use. Design A misses chlorophyll, which bio-optics would measure.", table=FLOAT_DESIGN),
]

CER_QUESTIONS: list[dict] = [
    _q("cer-1", "Part 7", "A bath bomb bubbles in water. Which CER fits a sealed bottle?", [
        "The bubbles show a new gas formed. In the sealed bottle, the total mass stays the same because the gas cannot leave",
        "The bubbles show the powder vanished. In the sealed bottle, the mass falls because gas has no mass",
        "The bubbles show a physical change only. The sealed bottle gains mass from new atoms",
        "The bubbles show light. The sealed bottle’s mass changes because the bottle is open",
    ], "Gas formation is evidence of a chemical reaction. Conservation of matter keeps the sealed mass the same."),
    _q("cer-2", "Part 7", "A flame went out when it was lowered into collected bath-bomb gas. Which CER fits?", [
        "The gas is not flammable. The evidence is that the flame went out. A flammable gas would have kept the flame burning",
        "The gas is oxygen. The evidence is that the flame went out. Oxygen always puts flames out",
        "The gas is flammable. The evidence is that the flame went out. Going out means it burned",
        "The gas is not matter. The evidence is the color of the flame",
    ], "Claim: not flammable. Evidence: the flame went out. Reasoning: a flammable gas would support the flame."),
    _q("cer-3", "Part 7", "Why is burning wood a chemical change?", [
        "New substances form. Wood’s flammability is a chemical property. Evidence includes ash and smoke or light",
        "Only the shape changes. Wood’s color is a chemical property. Evidence includes the log getting shorter",
        "The wood melts. Density is the chemical property. Evidence includes a cooler flame",
        "No new substance forms. Boiling point is the property. Evidence includes liquid water",
    ], "Flammability lets wood burn. Ash and smoke are new substances, so the change is chemical."),
    _q("cer-4", "Part 7", "A carrot sinks in freshwater but floats in saltwater. Which explanation fits?", [
        "The carrot is denser than freshwater, so it sinks. Dissolved salt adds mass and makes saltwater denser, so the carrot floats",
        "The carrot is less dense than freshwater, so it sinks. Salt removes mass from the water",
        "The carrot changes into salt. Freshwater and saltwater have the same density",
        "The carrot floats in freshwater because salt particles are in the carrot",
    ], "Sinking means the carrot is denser than that liquid. Salt adds mass to the water and raises its density."),
    _q("cer-6", "Part 7", "Which ocean-float explanation includes a sensor, its scientific value, and a limitation?", [
        "I selected the CTD because it measures temperature, salinity, and depth. A limitation is its 3.3 kg mass, so I would check the total before adding another sensor",
        "I selected every sensor because more is always better. There is no mass limit",
        "I selected dish soap because it measures chlorophyll. A limitation is that soap has no mass",
        "I selected the float base only. It measures nitrate, and it has no cost",
    ], "A strong answer names the measurement, how it serves the mission, and a constraint such as mass."),
]


def _shuffle_choices(question: dict) -> dict:
    item = copy.deepcopy(question)
    correct = item["options"][item["answer"]]
    options = list(item["options"])
    random.shuffle(options)
    item["options"] = options
    item["answer"] = options.index(correct)
    return item


def questions_for(section: str) -> list[dict]:
    if section == "choice":
        return CHOICE_QUESTIONS
    if section == "words":
        return WORD_QUESTIONS
    if section == "data":
        return DATA_QUESTIONS
    if section == "cer":
        return CER_QUESTIONS
    return []


def build_quiz(section: str) -> list[dict]:
    """Return a practice set. Multiple choice is a 10-question sample. The other parts keep packet order."""
    bank = questions_for(section)
    if not bank:
        return []
    if section == "choice":
        picked = random.sample(bank, min(CHOICE_QUIZ_SIZE, len(bank)))
    else:
        picked = list(bank)
    return [_shuffle_choices(question) for question in picked]
