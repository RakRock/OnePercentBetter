"""
Knowledge-graph quiz for Arjun's Spectrum Science Chapter 1 notes.

Each idea is one link from the packet: a concept, how it connects, and a
question that checks that link. The quiz samples the links. It does not
replace the 36-lesson practice bank.
"""

from __future__ import annotations

import copy
import random

QUIZ_SIZE = 8

SECTIONS: list[dict] = [
    {"id": "1.1", "title": "Science as Inquiry"},
    {"id": "1.2", "title": "The Human Hobbits"},
    {"id": "1.3", "title": "Searching for Our Ancestors"},
    {"id": "1.4", "title": "Vanishing Nature"},
    {"id": "1.5", "title": "Freezing-point lab"},
    {"id": "1.6", "title": "Squeaky Clean"},
    {"id": "1.7", "title": "Older Than Time"},
    {"id": "1.8", "title": "Measuring the Stars"},
    {"id": "1.9", "title": "Changing with the Times"},
]


def _idea(
    idea_id: str,
    section: str,
    link: str,
    question: str,
    options: list[str],
    explanation: str,
) -> dict:
    return {
        "id": idea_id,
        "section": section,
        "topic": f"Chapter 1 · {section}",
        "link": link,
        "question": question,
        "options": options,
        "answer": 0,
        "explanation": explanation,
    }


# Correct choice is always options[0]. build_quiz shuffles a copy.
IDEAS: list[dict] = [
    _idea(
        "c1-observation",
        "1.1",
        "Careful observation → reliable results",
        "Which skill does this chapter say every scientist needs?",
        [
            "Careful observation",
            "Typing on a keyboard",
            "Guessing the answer before looking",
            "Keeping results secret",
        ],
        "Observation, math, and communication are the shared skills. Typing is not one of them.",
    ),
    _idea(
        "c1-missed-note",
        "1.1",
        "A missed observation → incomplete results",
        "Why does a missed observation matter?",
        [
            "The results can be incomplete and unreliable",
            "The hypothesis automatically becomes a law",
            "The lab tools stop working",
            "Journals refuse any math",
        ],
        "If you never notice or record an event, you cannot use it later. The research is incomplete.",
    ),
    _idea(
        "c1-velocity",
        "1.1",
        "Velocity → distance divided by time",
        "In this chapter, velocity is…",
        [
            "Distance divided by time",
            "Time divided by distance",
            "Mass times volume",
            "The brightness of a star",
        ],
        "The chapter's simple formula is v = d/t.",
    ),
    _idea(
        "c1-journals",
        "1.1",
        "New research → scientific journals",
        "Where does this chapter say the newest research usually appears first?",
        [
            "Scientific journals",
            "Only in a classroom textbook",
            "In a novel at a bookstore",
            "In notes that are never shared",
        ],
        "Journals let other scientists review the methods and decide how reliable the results are.",
    ),
    _idea(
        "c1-interdisciplinary",
        "1.1",
        "Interdisciplinary → more than one field",
        "Interdisciplinary means…",
        [
            "Using more than one field of study",
            "Working in only one laboratory",
            "Publishing without evidence",
            "Measuring with a single tool",
        ],
        "A good scientist draws on more than one kind of knowledge.",
    ),
    _idea(
        "c1-flores",
        "1.2",
        "Homo floresiensis → Flores, Indonesia",
        "Homo floresiensis was found…",
        [
            "In a cave on the island of Flores in Indonesia",
            "In Olduvai Gorge in Tanzania",
            "In the Great Lakes",
            "In northern Maine",
        ],
        "Researchers found the small remains in a cave on Flores in 2004.",
    ),
    _idea(
        "c1-teeth",
        "1.2",
        "Worn teeth → adult, not a child",
        "Scientists first thought the small skull belonged to a child. They changed that idea because…",
        [
            "The teeth were too worn for a child",
            "The cave had no tools",
            "The skull was larger than a modern adult skull",
            "The bones were 20 million years old",
        ],
        "The body was child-sized, but the tooth wear fit an adult about 30 years old.",
    ),
    _idea(
        "c1-age-surprise",
        "1.2",
        "18,000-year-old bones → other early humans were thought to be gone",
        "The hobbit remains were surprising because they were…",
        [
            "Only about 18,000 years old, from a time when other early human species were thought to be gone",
            "Older than Earth",
            "Found on every continent",
            "Identical to modern humans in every way",
        ],
        "Scientists had thought every early human species was extinct before Homo sapiens. These bones were much younger.",
    ),
    _idea(
        "c1-microcephaly",
        "1.2",
        "Several small individuals → not one case of microcephaly",
        "Some scientists said the hobbit had microcephaly. The chapter says that idea is weaker because…",
        [
            "Several other individuals from Flores were the same small size, and later skull casts did not match the condition",
            "The skull was found in Africa",
            "Mary Leakey dated it to 1.75 million years ago",
            "The teeth showed it was a child",
        ],
        "One person with microcephaly would be possible. A group of the same size, plus the 2007 skull comparison, points to a separate species.",
    ),
    _idea(
        "c1-asia",
        "1.3",
        "Louis Leakey → earliest humans in Africa, not Asia",
        "Before Louis Leakey's work, many scientists thought the earliest humans lived in…",
        [
            "Asia",
            "South America",
            "Australia",
            "Antarctica",
        ],
        "Leakey argued from African fossils that the earliest human ancestors were in Africa. He called Africa the cradle of humanity.",
    ),
    _idea(
        "c1-habilis",
        "1.3",
        "Homo habilis → handy man, the toolmaker",
        "Homo habilis means…",
        [
            "Handy man, because stone tools were found nearby",
            "Upright walker, because of the footprints",
            "Small person, because of the Flores skull",
            "Fire maker, because of a hospital lamp",
        ],
        "The Leakeys concluded that this ancestor was the first toolmaker.",
    ),
    _idea(
        "c1-footprints",
        "1.3",
        "Volcanic-ash footprints → Australopithecus walked upright",
        "Mary Leakey's footprints in volcanic ash showed that Australopithecus afarensis…",
        [
            "Could walk upright",
            "Could not walk upright",
            "Lived only in Asia",
            "Became extinct in the year 1600",
        ],
        "The footprints were 2.9 to 3.5 million years old and matched fossils from the same area.",
    ),
    _idea(
        "c1-extinct",
        "1.4",
        "No recent evidence → extinct",
        "A species is considered extinct when…",
        [
            "No recent evidence of it is found over a period of time",
            "Fewer than 10 individuals are left",
            "No fossils of it have ever been found",
            "It lives on only one island",
        ],
        "Extinct means the species is gone, not merely rare. Fossils can still exist from when it was alive.",
    ),
    _idea(
        "c1-rate",
        "1.4",
        "Last 500 years → much faster extinctions",
        "Compared with the long average, extinction rates in the last 500 years may be…",
        [
            "50 to 100 times higher",
            "About the same",
            "Half as high",
            "Zero, because fossils stopped forming",
        ],
        "The chapter says recent extinctions are far faster than the usual rate through Earth's history.",
    ),
    _idea(
        "c1-permian",
        "1.4",
        "End of the Permian → most marine and land animals gone",
        "The end-Permian extinction, about 250 million years ago, wiped out about…",
        [
            "96 percent of marine animals and 77 percent of land animals",
            "Only the round goby",
            "12 percent of surgical patients",
            "Half of the stars",
        ],
        "The chapter links that mass extinction to changes in sea level and ocean salinity.",
    ),
    _idea(
        "c1-invasive",
        "1.4",
        "Greatest recent threat → invasive species",
        "The chapter calls the greatest recent threat to living species…",
        [
            "Invasive species brought into a new place",
            "A new ice age every year",
            "The loss of scientific journals",
            "Counting tree rings",
        ],
        "An invasive species can be introduced on purpose, as a crop, or by accident, as a traveler in cargo.",
    ),
    _idea(
        "c1-goby",
        "1.4",
        "Round goby → ship ballast water → Great Lakes",
        "The round goby reached the Great Lakes…",
        [
            "In the ballast water of ships",
            "By walking across dry land",
            "Inside an increment borer",
            "On the Leakey expeditions",
        ],
        "The goby is native to the Black and Caspian seas. Ballast water carried it into the Great Lakes.",
    ),
    _idea(
        "c1-variable",
        "1.5",
        "Changed variable → what was mixed into the water",
        "In the freezing-point lab, the variable that was changed was…",
        [
            "What was mixed into the water",
            "The brand of thermometer",
            "The day of the week",
            "The size of the room",
        ],
        "The beakers held pure water, salt water, sugar water, or alcohol mixed with water.",
    ),
    _idea(
        "c1-alcohol",
        "1.5",
        "40% alcohol → lowest freezing point",
        "Which solution froze at the lowest temperature?",
        [
            "The 40 percent isopropyl alcohol",
            "Pure water",
            "Salt water",
            "Sugar water",
        ],
        "Pure water froze at 0°C. Salt water and sugar water both froze at −4.5°C. The alcohol mixture froze at −17.5°C.",
    ),
    _idea(
        "c1-hypothesis",
        "1.5",
        "Incorrect hypothesis → result is still useful",
        "The student predicted that salt water would freeze at the lowest temperature. The result means…",
        [
            "The hypothesis was incorrect, and the result is still worth reporting",
            "The hypothesis was incorrect, so the data should be thrown away",
            "The hypothesis was correct because salt and sugar matched",
            "Alcohol froze at 0°C",
        ],
        "An incorrect hypothesis still teaches something. The alcohol mixture froze lowest.",
    ),
    _idea(
        "c1-unfair",
        "1.5",
        "Unequal amounts → unreliable conclusion",
        "Why were the lab results unreliable?",
        [
            "The salt and sugar were one tablespoon each, while the alcohol mixture was already 40 percent, so the amounts did not match",
            "The student used four different beakers",
            "Pure water was included",
            "A thermometer is not a scientific tool",
        ],
        "One tablespoon is 6.25 percent of a cup. The alcohol beaker was much more concentrated, so two variables changed at once.",
    ),
    _idea(
        "c1-sepsis",
        "1.6",
        "Sepsis → microorganisms, not bad air",
        "Lister decided sepsis was caused by…",
        [
            "Microorganisms, not bad air",
            "Carbolic acid",
            "Cold hospital windows",
            "Worn teeth",
        ],
        "Sepsis is an infection in the blood. Covering wounds to keep out bad air gave bacteria a dark, moist place to grow.",
    ),
    _idea(
        "c1-carbolic",
        "1.6",
        "Carbolic acid → hands, tools, and wounds",
        "Lister used carbolic acid to…",
        [
            "Wash hands, clean tools, and treat wounds",
            "Date fossils",
            "Measure the distance to a star",
            "Thicken mussel shells",
        ],
        "Carbolic acid was his antiseptic. It had already been used to deodorize sewage.",
    ),
    _idea(
        "c1-mortality",
        "1.6",
        "Antiseptic use → deaths fell from about 50% to about 12%",
        "Lister knew the antiseptic was working because…",
        [
            "Deaths in that surgical ward fell from about 50 percent to about 12 percent",
            "Every surgeon agreed on the first day",
            "Carbolic acid made bacteria grow faster",
            "Patients stopped needing surgery",
        ],
        "The drop happened by 1869, about four years after he started. Other surgeons did not accept the idea immediately.",
    ),
    _idea(
        "c1-ring",
        "1.7",
        "One growth ring → one year",
        "One tree ring usually stands for…",
        [
            "One year of growth",
            "One ice age",
            "One invasive species",
            "One light-year",
        ],
        "A burst of spring growth and slower later growth make one ring each year.",
    ),
    _idea(
        "c1-borer",
        "1.7",
        "Increment borer → a sample without cutting the tree down",
        "An increment borer lets scientists…",
        [
            "Take a thin sample of a living tree without cutting it down",
            "Cut down every tree they study",
            "Measure the distance to Sirius",
            "Kill microorganisms on surgical tools",
        ],
        "The sample is only a few millimeters across, and it still shows the rings.",
    ),
    _idea(
        "c1-overlap",
        "1.7",
        "Matching rings → when a dead tree was alive",
        "Matching rings from a living bristlecone pine and a dead one tells scientists…",
        [
            "When the dead tree was alive",
            "The name of the person who planted it",
            "Which crabs ate the mussels",
            "The freezing point of alcohol",
        ],
        "The same pattern of wide and narrow rings marks the years the two trees shared. Methuselah, a living bristlecone, is nearly 5,000 years old.",
    ),
    _idea(
        "c1-switch",
        "1.8",
        "Light switch in the example → the star",
        "In the parallax example, the light switch stands for…",
        [
            "The star being measured",
            "The scientist's thumb",
            "Earth's orbit",
            "A spectroscope",
        ],
        "Your two eyes are the two viewpoints. The switch seems to jump, just as a nearer star seems to shift against farther stars.",
    ),
    _idea(
        "c1-six-months",
        "1.8",
        "Two viewpoints → opposite sides of Earth's orbit",
        "To measure a star's distance by parallax, astronomers observe it…",
        [
            "From opposite sides of Earth's orbit, about six months apart",
            "Only at noon from one spot",
            "By cutting a tree sample",
            "Through a hospital microscope",
        ],
        "The base of their triangle is Earth's move from one side of the sun to the other. Geometry then gives the distance.",
    ),
    _idea(
        "c1-spectroscopy",
        "1.8",
        "A star's colors → the elements inside it",
        "Spectroscopy tells scientists which elements a star contains because…",
        [
            "Each element gives off its own colors of light",
            "Brighter stars are always closer",
            "Every star is made of only iron",
            "A prism stops the star from moving",
        ],
        "A spectroscope spreads starlight into a spectrum, the way a prism spreads sunlight.",
    ),
    _idea(
        "c1-invasive-crab",
        "1.9",
        "Asian shore crab → invasive species carried by ships",
        "The Asian shore crab is called an invasive species in the United States because…",
        [
            "It arrived in ships and was not already living there",
            "It is a kind of blue mussel",
            "It thickens its own shell as a mating ritual",
            "The Leakeys brought it from Africa",
        ],
        "The crab first entered U.S. waters in the late 1980s and began eating blue mussels.",
    ),
    _idea(
        "c1-shell",
        "1.9",
        "Crab chemical → mussel thickens its shell",
        "Blue mussels thicken their shells when…",
        [
            "They detect chemicals from a crab they recognize as a predator",
            "They are ready to mate",
            "A scientist cuts a growth ring",
            "The water starts to freeze",
        ],
        "A thicker shell is a defense. It makes the mussel harder for the crab to eat.",
    ),
    _idea(
        "c1-maine",
        "1.9",
        "No past contact → no defense against that crab",
        "Maine mussels did not thicken their shells for Asian shore crabs because…",
        [
            "Those crabs had never lived near them, so the mussels did not recognize the chemical",
            "Maine mussels cannot grow shells",
            "Green crabs were unknown in Maine",
            "The experiment used carbolic acid",
        ],
        "Both groups thickened their shells for green crabs, which they already lived with. Only the mussels that had lived near Asian shore crabs responded to that crab.",
    ),
    _idea(
        "c1-fifteen",
        "1.9",
        "About 15 years → a new shell defense",
        "Freeman and Byers's hypothesis was that blue mussels…",
        [
            "Evolved a thicker-shell defense against the Asian shore crab in about 15 years",
            "Became extinct in the last 500 years",
            "Walked upright 3 million years ago",
            "Froze at a lower temperature than salt water",
        ],
        "The experiment supported that hypothesis. For most species, a new trait does not appear in less than ten years, so this change was fast.",
    ),
]


def ideas_for_section(section_id: str) -> list[dict]:
    return [idea for idea in IDEAS if idea["section"] == section_id]


def build_quiz(size: int = QUIZ_SIZE) -> list[dict]:
    """Return a shuffled quiz. Does not change the stored ideas."""
    if not IDEAS:
        return []
    picked = random.sample(IDEAS, min(size, len(IDEAS)))
    quiz = []
    for idea in picked:
        item = copy.deepcopy(idea)
        correct = item["options"][item["answer"]]
        options = list(item["options"])
        random.shuffle(options)
        item["options"] = options
        item["answer"] = options.index(correct)
        quiz.append(item)
    return quiz
