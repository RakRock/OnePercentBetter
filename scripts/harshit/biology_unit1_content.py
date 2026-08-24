"""Full concept card content for Harshit Biology Unit 1 — Days 1–16 (Ch 5 Life Processes)."""

from __future__ import annotations


def _card(
    cid: str,
    name: str,
    simple: str,
    visual_type: str,
    visual_config: dict | None,
    why: str,
    example: str,
    remember: str,
    confusion: str = "",
    optional: str = "",
    glossary: list[str] | None = None,
) -> dict:
    return {
        "id": cid,
        "name": name,
        "simple_answer": simple,
        "visual": {"type": visual_type, **(visual_config or {})},
        "why": why,
        "example": example,
        "remember": remember,
        "common_confusion": confusion,
        "optional_detail": optional,
        "glossary_terms": glossary or [],
    }


def _build_day(day: int, cards: list[tuple]) -> list[dict]:
    out = []
    for i, row in enumerate(cards, 1):
        name, simple, vtype, vcfg, why, ex, rem, *rest = row
        confusion = rest[0] if len(rest) > 0 else ""
        optional = rest[1] if len(rest) > 1 else ""
        gloss = rest[2] if len(rest) > 2 else []
        out.append(
            _card(
                f"u1_d{day}_c{i:02d}",
                name,
                simple,
                vtype,
                vcfg if isinstance(vcfg, dict) else {},
                why,
                ex,
                rem,
                confusion,
                optional,
                gloss if isinstance(gloss, list) else [],
            )
        )
    return out


DAY1 = _build_day(1, [
    ("What are life processes?", "Life processes are the basic functions performed by living organisms to maintain life — nutrition, respiration, transport, excretion, and more.", "placeholder", {"label": "Life processes overview"}, "NCERT Ch 5 opens with maintenance of life.", "Even when not growing, your body still needs energy and repair.", "Living things must carry out life processes continuously.", "Being alive is not just about moving — plants also perform life processes.", "", ["life processes"]),
    ("Why maintenance is needed", "Living organisms need maintenance even when not growing because body cells are constantly being damaged and need repair.", "placeholder", {"label": "Maintenance of living structures"}, "Explains why life processes never stop.", "Skin cells replace themselves; muscles need ATP daily.", "Maintenance needs energy from outside or from food.", "Sleeping does not mean life processes stop.", "", []),
    ("Molecular movement and life", "All living organisms need to move molecules across their body for life processes — even plants without visible movement.", "placeholder", {"label": "Molecular movement"}, "Bridge from diffusion to transport systems.", "O₂ must reach every cell; CO₂ must leave.", "Life needs controlled movement of substances.", "Plants don't move but still transport water and food.", "", []),
    ("Diffusion — definition", "Diffusion is the movement of molecules from a region of higher concentration to lower concentration until evenly spread.", "formula_panel", {"formula": "High concentration → Low concentration", "note": "Passive movement"}, "Simplest transport mechanism in Ch 5.", "Perfume spreading in a room.", "No energy needed for simple diffusion.", "Diffusion works only over very short distances.", "", ["diffusion"]),
    ("Diffusion in unicellular organisms", "In unicellular organisms, the entire surface is in direct contact with the environment — diffusion alone is enough.", "placeholder", {"label": "Unicellular — diffusion enough"}, "Contrast with multicellular need for transport.", "Amoeba absorbs food and O₂ by diffusion through cell surface.", "Small size + large surface area → diffusion works.", "", "", []),
    ("Diffusion insufficient in multicellular organisms", "In large multicellular organisms most cells are not in direct contact with the environment — diffusion alone is too slow.", "placeholder", {"label": "Multicellular — diffusion not enough"}, "NCERT exercise Q5 theme.", "Your innermost cells cannot get O₂ by diffusion from skin.", "Special transport systems are needed in large bodies.", "Diffusion still works at cell level after delivery.", "", []),
    ("What makes something alive?", "We decide something is alive if it shows molecular movement needed for repair and maintenance — not just visible movement.", "placeholder", {"label": "Criteria for being alive"}, "NCERT criteria discussion.", "A seed is alive though it looks inactive; it respires slowly.", "Visible movement alone is not enough to prove life.", "Viruses are debated — they need a host to reproduce.", "", []),
    ("Outside raw materials", "Living organisms take in raw materials from outside: carbon-based food/CO₂, water, and inorganic salts.", "placeholder", {"label": "Outside raw materials"}, "NCERT lists three categories.", "Plants: CO₂ + water + minerals. Animals: food + water + salts.", "Carbon sources, water, and minerals from environment.", "Autotrophs build food; heterotrophs eat ready-made food.", "", []),
    ("Energy for life processes", "Outside materials are used to build body structure and to provide energy for life processes.", "placeholder", {"label": "Energy for maintenance"}, "Links nutrition to all other processes.", "Glucose from food powers muscle contraction and nerve signals.", "Food → energy + building blocks.", "Energy is stored in chemical bonds of food molecules.", "", []),
    ("Chapter 5 roadmap", "Ch 5 covers nutrition, respiration, transport, and excretion in plants and humans.", "placeholder", {"label": "Ch 5 roadmap — 16 days"}, "Orient learner to unit plan.", "Activities 5.1–5.8 support each section.", "Nutrition → respiration → transport → excretion.", "", "", []),
])

DAY2 = _build_day(2, [
    ("Nutrition — definition", "Nutrition is the process of obtaining and using food for growth, repair, and energy.", "placeholder", {"label": "Nutrition defined"}, "First major life process in Ch 5.", "Eating breakfast provides glucose for the school day.", "Nutrition = taking in + using food.", "Nutrition is not the same as digestion alone.", "", ["nutrition"]),
    ("Autotrophic nutrition", "Autotrophic nutrition: organism makes its own food from simple inorganic substances like CO₂ and water.", "formula_panel", {"formula": "CO₂ + H₂O → food (glucose) + O₂", "note": "Autotrophs — self-feeders"}, "Green plants are autotrophs.", "Plants use sunlight to build starch.", "Make food from inorganic raw materials.", "Autotrophs are producers in food chains.", "", ["autotrophic nutrition"]),
    ("Heterotrophic nutrition", "Heterotrophic nutrition: organism depends on ready-made organic food from other organisms.", "placeholder", {"label": "Heterotrophs — other-feeders"}, "Animals, fungi, most bacteria.", "Humans eat plants and animals; cannot make glucose from CO₂.", "Obtain food made by others.", "All animals are heterotrophs.", "", ["heterotrophic nutrition"]),
    ("Saprotrophic nutrition", "Saprotrophic nutrition: organisms feed on dead and decaying organic matter (e.g. fungi).", "placeholder", {"label": "Saprotrophs — decomposers"}, "Subtype of heterotrophic.", "Mushrooms on rotting logs.", "Decompose dead material; recycle nutrients.", "Saprotrophs secrete enzymes outside then absorb.", "", []),
    ("Parasitic nutrition", "Parasitic nutrition: organism lives on or in a host and derives food at host's expense.", "placeholder", {"label": "Parasites"}, "Another heterotrophic mode.", "Tapeworm in intestine absorbs digested food.", "Parasite benefits; host is harmed.", "Not all parasites kill the host immediately.", "", []),
    ("Holozoic nutrition", "Holozoic nutrition: complex food is ingested and then digested inside the body.", "placeholder", {"label": "Holozoic — ingest then digest"}, "Human mode of nutrition.", "Amoeba engulfs food; humans chew and swallow.", "Ingest → digest → absorb → egest.", "", "", []),
    ("Modes of nutrition summary", "Main modes: autotrophic (plants) and heterotrophic (animals, fungi) with subtypes saprotrophic, parasitic, holozoic.", "placeholder", {"label": "Nutrition modes summary"}, "Classification for exams.", "Compare amoeba (holozoic) vs mushroom (saprotrophic).", "Know definition + one example each.", "Autotrophic vs heterotrophic is the primary split.", "", []),
    ("Enzymes in nutrition", "Enzymes are biological catalysts that speed up breakdown of complex food into absorbable simple molecules.", "placeholder", {"label": "Enzymes — biological catalysts"}, "Links to digestion section.", "Amylase breaks starch to sugar in saliva.", "Enzymes work at body temperature; are specific.", "Enzymes are not used up in the reaction.", "", ["enzyme"]),
    ("Nutrition in green plants — overview", "Green plants are autotrophs: leaves trap light; roots absorb water and minerals.", "placeholder", {"label": "Plant nutrition overview"}, "Leads to photosynthesis days.", "Leaf = food factory; root = water and mineral uptake.", "Photosynthesis in leaves; absorption by roots.", "", "", []),
    ("Nutrition in animals — overview", "Animals are heterotrophs: ingest food, digest it, absorb nutrients, and remove undigested waste.", "placeholder", {"label": "Animal nutrition overview"}, "Leads to human digestive system.", "Human alimentary canal is about 9 metres long.", "Ingestion → digestion → absorption → egestion.", "", "", []),
])

DAY3 = _build_day(3, [
    ("Photosynthesis — definition", "Photosynthesis is the process by which green plants synthesise food (glucose) using CO₂, water, and sunlight.", "formula_panel", {"formula": "6CO₂ + 6H₂O → C₆H₁₂O₆ + 6O₂", "note": "Chlorophyll + sunlight"}, "Core autotrophic process.", "Leaves produce O₂ we breathe.", "Plants make food; release oxygen.", "Photosynthesis occurs only in green parts with chlorophyll.", "", ["photosynthesis"]),
    ("Raw materials for photosynthesis", "Plants need CO₂ from air (through stomata), water from soil (through roots), and sunlight.", "placeholder", {"label": "Photosynthesis raw materials"}, "Three inputs for the equation.", "Stomata take in CO₂; xylem brings water to leaf.", "CO₂ + H₂O + light → glucose + O₂.", "Minerals from soil are needed for chlorophyll but not in the main equation.", "", []),
    ("Chlorophyll role", "Chlorophyll in chloroplasts traps solar energy needed to convert CO₂ and water into glucose.", "placeholder", {"label": "Chlorophyll traps light"}, "Why leaves are green.", "Without chlorophyll, photosynthesis cannot occur.", "Green pigment in chloroplasts absorbs light.", "Other pigments exist but chlorophyll is primary.", "", ["chlorophyll"]),
    ("Chloroplast location", "Photosynthesis occurs mainly in mesophyll cells of leaves where chloroplasts are abundant.", "placeholder", {"label": "Chloroplasts in leaf cells"}, "Anatomy link.", "Upper and lower mesophyll packed with chloroplasts.", "Leaf is the main photosynthetic organ.", "", "", []),
    ("Stomata and gas exchange", "Stomata are tiny pores on leaf surface; they allow CO₂ intake and O₂ release during photosynthesis.", "placeholder", {"label": "Stomata — gas exchange"}, "Leads to Activity 5.3.", "Guard cells control stomatal opening.", "CO₂ in for photosynthesis; O₂ out.", "Stomata also lose water vapour (transpiration).", "", ["stomata"]),
    ("Guard cells", "Two kidney-shaped guard cells surround each stoma and control its opening and closing.", "placeholder", {"label": "Guard cells control stomata"}, "Mechanism for gas/water balance.", "Stomata open in light; often close in drought.", "Guard cells swell to open stomata.", "", "", []),
    ("Products of photosynthesis", "Glucose is produced first; excess is stored as starch in leaves, stems, and roots.", "placeholder", {"label": "Glucose → starch storage"}, "Links to Activity 5.2 starch test.", "Potato stores starch in underground stem.", "Immediate product: glucose; storage form: starch.", "Starch test uses iodine — blue-black colour.", "", []),
    ("Activity 5.2 — starch test in leaf", "Boil leaf in water, then alcohol, add iodine — green leaf turns blue-black showing starch from photosynthesis.", "placeholder", {"label": "Activity 5.2 — starch test"}, "NCERT lab proof of photosynthesis.", "Variegated leaf: only green parts turn blue-black.", "Starch present where chlorophyll and light were available.", "Heat leaf in water first to kill cells and soften.", "", []),
    ("Conditions for photosynthesis", "Photosynthesis needs light, chlorophyll, CO₂, and suitable temperature.", "placeholder", {"label": "Conditions for photosynthesis"}, "Experiment design skill.", "Plant in dark fails starch test — no photosynthesis.", "Remove any one factor → rate drops or stops.", "Light-dependent and light-independent stages (detail optional).", "", []),
    ("Significance of photosynthesis", "Photosynthesis provides food for nearly all life and releases O₂ into the atmosphere.", "placeholder", {"label": "Why photosynthesis matters"}, "Big-picture importance.", "All food chains start with autotrophs.", "Ultimate source of energy for most ecosystems.", "", "", []),
])

DAY4 = _build_day(4, [
    ("Site of photosynthesis", "Photosynthesis occurs in the green parts of plants, especially leaves.", "placeholder", {"label": "Site — green parts of plant"}, "Exam favourite.", "Non-green stems with chlorophyll also photosynthesise.", "Leaves are primary site.", "Roots do not photosynthesise — no chlorophyll, no light.", "", []),
    ("Light reaction (overview)", "Light energy splits water; O₂ is released; energy stored temporarily in molecules.", "placeholder", {"label": "Light-dependent stage"}, "Simplified NCERT level.", "O₂ bubbles from aquatic plants in bright light.", "Needs light; happens in grana of chloroplast.", "Detailed biochemistry beyond Class 10 scope.", "", []),
    ("Dark reaction (overview)", "CO₂ is fixed into glucose using energy from light reaction — does not require light directly.", "placeholder", {"label": "Light-independent stage"}, "Completes photosynthesis picture.", "Calvin cycle idea at textbook level.", "Can proceed in dark if products of light stage available.", "Called 'dark' because it doesn't need light directly.", "", []),
    ("Factors affecting photosynthesis", "Rate depends on light intensity, CO₂ concentration, temperature, and chlorophyll amount.", "placeholder", {"label": "Factors affecting rate"}, "Graph interpretation skill.", "Greenhouse farmers enrich CO₂ to boost yield.", "Limiting factor: the factor in shortest supply caps rate.", "", "", []),
    ("Nutrition in non-green plants", "Some plants lack chlorophyll (e.g. Cuscuta) and are parasitic — heterotrophic nutrition.", "placeholder", {"label": "Parasitic plants — Cuscuta"}, "Exception to autotrophic rule.", "Amarbel (Cuscuta) wraps around host plant.", "Not all plants are autotrophs.", "", "", []),
    ("Insectivorous plants", "Plants like pitcher plant supplement minerals by trapping insects — still autotrophic for energy.", "placeholder", {"label": "Insectivorous plants"}, "NCERT example.", "Pitcher plant digests insect for nitrogen.", "Photosynthesise but catch insects for soil-poor habitats.", "", "", []),
    ("Activity 5.3 — stomata observation", "Peel lower epidermis of leaf, stain with safranin, observe stomata under microscope.", "placeholder", {"label": "Activity 5.3 — stomata peel"}, "Microscopy skill.", "See guard cells and stomatal pore.", "Lower epidermis peel shows stomata clearly.", "Safranin stains nuclei pink.", "", []),
    ("Gas exchange day and night", "Day: photosynthesis dominates — CO₂ in, O₂ out. Night: only respiration — O₂ in, CO₂ out.", "placeholder", {"label": "Day vs night gas exchange"}, "Common exam comparison.", "Net O₂ release only when photosynthesis > respiration.", "Both processes occur in plants; balance shifts.", "Do not say plants don't respire.", "", ""),
    ("Replenish atmosphere O₂", "Photosynthesis by green plants continuously replenishes atmospheric oxygen.", "placeholder", {"label": "O₂ replenishment"}, "Environmental significance.", "Amazon and all forests contribute O₂ globally.", "Photosynthesis counterbalances respiration and combustion.", "", "", []),
    ("Photosynthesis vs nutrition", "Photosynthesis is the specific autotrophic process; nutrition is the broader obtaining and use of food.", "placeholder", {"label": "Photosynthesis within nutrition"}, "Terminology precision.", "Photosynthesis makes food; nutrition includes using it.", "Photosynthesis ⊂ autotrophic nutrition.", "", "", []),
])

DAY5 = _build_day(5, [
    ("Heterotrophic nutrition — recap", "Organisms that cannot make their own food ingest complex organic matter and break it down.", "placeholder", {"label": "Heterotrophic recap"}, "Start animal nutrition section.", "Cow (herbivore), lion (carnivore), human (omnivore).", "All depend on autotrophs directly or indirectly.", "", "", []),
    ("Steps in holozoic nutrition", "Ingestion → digestion → absorption → assimilation → egestion.", "placeholder", {"label": "Five steps — holozoic"}, "Process sequence for exams.", "Undigested food leaves as faeces (egestion).", "Memorise order of five steps.", "Absorption is into blood; assimilation is use by cells.", "", []),
    ("Ingestion", "Ingestion is taking food into the body through the mouth.", "placeholder", {"label": "Ingestion — taking food in"}, "First step in humans.", "Biting and chewing apple pieces.", "Mouth is start of alimentary canal.", "", "", []),
    ("Digestion — definition", "Digestion breaks complex insoluble food into simple soluble molecules using enzymes.", "placeholder", {"label": "Digestion defined"}, "Core process before absorption.", "Starch → maltose → glucose.", "Large molecules → small absorbable units.", "Physical digestion (chewing) + chemical (enzymes).", "", ["digestion"]),
    ("Absorption", "Absorption is uptake of digested food from intestine into blood.", "placeholder", {"label": "Absorption into blood"}, "After digestion in gut.", "Glucose and amino acids enter blood capillaries.", "Mainly in small intestine.", "Villi increase surface area for absorption.", "", []),
    ("Assimilation", "Assimilation is using absorbed nutrients for energy, growth, and repair.", "placeholder", {"label": "Assimilation — using food"}, "After absorption.", "Glucose oxidised in cells for ATP.", "Food becomes part of body or fuel.", "", "", []),
    ("Egestion", "Egestion removes undigested food as faeces — not the same as excretion.", "placeholder", {"label": "Egestion vs excretion"}, "Important distinction.", "Fibre leaves body via anus.", "Egestion = undigested food out; excretion = metabolic waste.", "Faeces are not metabolic wastes.", "", []),
    ("Single-chambered vs multi-chambered stomach", "Ruminants (cow) have four-chambered stomach; humans have one stomach.", "placeholder", {"label": "Ruminant digestion"}, "NCERT comparison.", "Cow regurgitates cud for re-chewing.", "Cellulose digestion needs symbiotic bacteria in ruminants.", "", "", []),
    ("Amoeba nutrition", "Amoeba extends pseudopodia around food, forms food vacuole, digests with enzymes.", "placeholder", {"label": "Amoeba — holozoic in water"}, "Unicellular heterotroph example.", "Food vacuole fuses with lysosomes.", "No alimentary canal — intracellular digestion.", "", "", []),
    ("Paramoecium nutrition", "Paramoecium has oral groove and gullet leading to food vacuole for digestion.", "placeholder", {"label": "Paramoecium feeding"}, "Second unicellular example.", "Cilia sweep food into oral groove.", "Specialised structures for feeding in one cell.", "", "", []),
])

DAY6 = _build_day(6, [
    ("Human digestive system overview", "Alimentary canal plus associated glands form the human digestive system.", "placeholder", {"label": "Alimentary canal overview"}, "Map for Days 6–7.", "Mouth → oesophagus → stomach → intestine → anus.", "Also: salivary glands, liver, pancreas.", "", "", []),
    ("Mouth and buccal cavity", "Teeth mechanically break food; tongue mixes and tastes; saliva begins chemical digestion.", "placeholder", {"label": "Mouth — mechanical + chemical start"}, "First organ.", "Chewing increases surface area for enzymes.", "Incisors cut, canines tear, molars grind.", "", "", []),
    ("Saliva and salivary amylase", "Saliva moistens food and contains amylase (ptyalin) that starts starch digestion to maltose.", "formula_panel", {"formula": "Starch → Maltose", "note": "Salivary amylase — pH ~ neutral"}, "Enzyme in mouth.", "Bread tastes sweet if chewed long — maltose forms.", "Starch digestion begins in mouth.", "Amylase inactive in strong acid of stomach.", "", []),
    ("Oesophagus (food pipe)", "Peristaltic movements push food from mouth to stomach through the oesophagus.", "placeholder", {"label": "Oesophagus — peristalsis"}, "No digestion in oesophagus.", "You can swallow upside down — peristalsis works.", "Muscular wave moves bolus downward.", "Peristalsis is involuntary muscle contraction.", "", ["peristalsis"]),
    ("Stomach structure", "Stomach is a muscular bag; gastric glands secrete HCl, mucus, and pepsin.", "placeholder", {"label": "Stomach — gastric juices"}, "Protein digestion starts here.", "HCl kills bacteria and gives acid pH for pepsin.", "Churning mixes food with gastric juice.", "", "", []),
    ("Pepsin action", "Pepsin breaks proteins into peptides in acidic medium of stomach.", "formula_panel", {"formula": "Proteins → Peptides", "note": "Pepsin — acidic pH"}, "First protein-digesting enzyme.", "Inactive pepsinogen activated by HCl.", "Protein digestion begins in stomach.", "Pepsin works only in acid — not in mouth.", "", []),
    ("Mucus in stomach", "Mucus protects stomach lining from being digested by its own acid and pepsin.", "placeholder", {"label": "Mucus protects stomach wall"}, "Why stomach doesn't self-digest.", "Ulcers may occur if mucus layer damaged.", "Self-protection is essential.", "", "", []),
    ("Small intestine — main digestion site", "Complete digestion of carbohydrates, proteins, and fats occurs in small intestine.", "placeholder", {"label": "Small intestine — main digestion"}, "Longest part of canal (~7.5 m).", "Receives bile and pancreatic juice.", "Most absorption also happens here.", "", "", []),
    ("Liver and bile", "Liver makes bile stored in gall bladder; bile emulsifies fats (no enzyme).", "placeholder", {"label": "Bile emulsifies fats"}, "Fat digestion aid.", "Bile breaks large fat globules into smaller droplets.", "Emulsification increases lipase efficiency.", "Bile is alkaline — neutralises stomach acid.", "", []),
    ("Pancreatic juice", "Pancreas secretes trypsin (proteins), lipase (fats), and pancreatic amylase (starch).", "formula_panel", {"formula": "Trypsin | Lipase | Amylase", "note": "Pancreatic enzymes"}, "Major enzyme source.", "Juice released into duodenum.", "Completes digestion started elsewhere.", "", "", []),
])

DAY7 = _build_day(7, [
    ("Intestinal juice (succus entericus)", "Intestinal glands secrete enzymes completing digestion of all major food types.", "placeholder", {"label": "Intestinal juice"}, "Final chemical digestion.", "Maltase converts maltose to glucose.", "Carbohydrates → glucose; proteins → amino acids; fats → fatty acids + glycerol.", "", "", []),
    ("Villi and microvilli", "Inner wall of small intestine has finger-like villi with microvilli to absorb digested food.", "placeholder", {"label": "Villi increase surface area"}, "Adaptation for absorption.", "Each villus has blood capillaries and lacteal.", "Huge surface area in folded wall.", "Lacteal absorbs fatty acids and glycerol.", "", ["villi"]),
    ("Absorption in small intestine", "Glucose and amino acids enter blood; fatty acids enter lacteals of lymph system.", "placeholder", {"label": "Absorption routes"}, "Transport after digestion.", "Blood carries sugars and amino acids to liver.", "Villi → capillaries → hepatic portal vein.", "", "", []),
    ("Large intestine role", "Large intestine absorbs water and minerals; forms and stores faeces.", "placeholder", {"label": "Large intestine — water absorption"}, "Last part of canal.", "Diarrhoea if water not reabsorbed properly.", "Colon hosts helpful bacteria.", "No significant digestion in large intestine.", "", []),
    ("Rectum and anus", "Faeces stored in rectum and eliminated through anus — egestion.", "placeholder", {"label": "Egestion pathway"}, "End of alimentary canal.", "Defecation is egestion, not excretion.", "Anus is exit for undigested residue.", "", "", []),
    ("Digestive enzymes summary", "Amylase (starch), pepsin/trypsin (proteins), lipase (fats) — know source and product.", "formula_panel", {"formula": "Amylase | Pepsin | Trypsin | Lipase", "note": "Match enzyme to substrate"}, "Exam table question.", "Draw table: enzyme, source, substrate, product.", "Memorise four key enzymes.", "One enzyme generally acts on one substrate type.", "", []),
    ("pH and enzyme action", "Salivary amylase needs neutral pH; pepsin needs acid; intestinal enzymes need alkaline pH.", "placeholder", {"label": "pH matches enzyme site"}, "Why digestion is sequential.", "Bicarbonate in pancreatic juice neutralises acid.", "Each enzyme works best at specific pH.", "", "", []),
    ("Dental hygiene", "Brushing removes food particles; prevents acid from bacteria decaying teeth.", "placeholder", {"label": "Dental care"}, "Health link in NCERT.", "Saliva washes teeth; bacteria cause cavities.", "Prevention is part of nutrition health.", "", "", []),
    ("Disorders — indigestion", "Indigestion from inadequate enzyme action or overeating; antacids neutralise excess acid.", "placeholder", {"label": "Indigestion and antacids"}, "Everyday application.", "Antacids raise pH in stomach.", "Lifestyle affects digestion efficiency.", "", "", []),
    ("Human digestion summary", "Mouth (starch start) → stomach (protein start) → small intestine (complete digestion + absorption).", "placeholder", {"label": "Digestion pathway summary"}, "Day 6–7 consolidation.", "Trace one bite of bread to glucose in blood.", "Know organ order and main function each.", "", "", []),
])

DAY8 = _build_day(8, [
    ("Respiration — definition", "Respiration is the process of releasing energy from food (glucose) inside cells.", "formula_panel", {"formula": "Food + O₂ → Energy + CO₂ + H₂O", "note": "Cellular respiration"}, "Second major life process.", "ATP powers muscle contraction.", "Not the same as breathing — breathing is ventilation.", "Breathing ≠ respiration.", "", ["respiration"]),
    ("Why respiration is essential", "Energy from respiration drives synthesis, transport, movement, and maintenance.", "placeholder", {"label": "Energy for all life processes"}, "Links to Day 1 maintenance.", "Nerve impulses need ATP constantly.", "Without respiration, cells cannot function.", "", "", []),
    ("Breathing vs respiration", "Breathing ( ventilation) is inhaling/exhaling air; respiration is biochemical breakdown of glucose in cells.", "placeholder", {"label": "Breathing vs respiration"}, "Critical distinction.", "Lungs move air; mitochondria release energy.", "Breathing provides O₂ for cellular respiration.", "Students often conflate the two terms.", "", []),
    ("Glucose as fuel", "Glucose (C₆H₁₂O₆) is the common substrate broken down in respiration to release energy.", "formula_panel", {"formula": "C₆H₁₂O₆ + 6O₂ → 6CO₂ + 6H₂O + ATP", "note": "Aerobic summary"}, "Central molecule.", "From digested carbohydrates.", "Fats and proteins can also be respired.", "", []),
    ("ATP — energy currency", "ATP (adenosine triphosphate) stores and transfers energy for cellular work.", "placeholder", {"label": "ATP — energy currency"}, "Product used by cell.", "Muscle uses ATP for contraction.", "Energy released when ATP → ADP + Pi.", "", "", ["ATP"]),
    ("Aerobic respiration — definition", "Aerobic respiration uses oxygen and completely breaks glucose into CO₂, water, and much ATP.", "placeholder", {"label": "Aerobic — with oxygen"}, "Most efficient pathway.", "Occurs in mitochondria of cells.", "Maximum energy from one glucose molecule.", "Needs continuous O₂ supply.", "", ["aerobic respiration"]),
    ("Anaerobic respiration — definition", "Anaerobic respiration breaks glucose without oxygen, producing less energy and different products.", "placeholder", {"label": "Anaerobic — without oxygen"}, "Used when O₂ limited.", "Yeast: ethanol + CO₂. Muscles: lactic acid.", "Less ATP than aerobic pathway.", "Also called fermentation in yeast.", "", ["anaerobic respiration"]),
    ("Respiration in plants", "Plant cells respire all the time in mitochondria — roots, stems, leaves, flowers.", "placeholder", {"label": "Plants respire too"}, "Correct plant misconception.", "Germinating seeds respire vigorously.", "Photosynthesis and respiration both occur in plants.", "Plants do not 'only photosynthesise'.", "", []),
    ("Gas exchange in plants", "Plants exchange O₂ and CO₂ through stomata and lenticels; roots also need O₂ in soil air spaces.", "placeholder", {"label": "Plant gas exchange"}, "Transport link preview.", "Waterlogged soil kills roots — no O₂ for respiration.", "Stomata for leaves; lenticels for woody stems.", "", "", []),
    ("Respiration chapter map", "Aerobic in mitochondria; anaerobic in cytoplasm (and yeast); compare energy yield next days.", "placeholder", {"label": "Respiration roadmap"}, "Days 8–10 structure.", "Activity 5.1 demonstrates yeast anaerobic respiration.", "Cytoplasm → partial breakdown; mitochondria → complete.", "", "", []),
])

DAY9 = _build_day(9, [
    ("Aerobic respiration steps (overview)", "Glycolysis in cytoplasm → pyruvate enters mitochondria → complete oxidation to CO₂ and H₂O.", "placeholder", {"label": "Aerobic pathway overview"}, "Simplified NCERT pathway.", "Pyruvate breakdown needs O₂ in mitochondria.", "Two stages: cytoplasm then mitochondria.", "Krebs cycle detail optional for Class 10.", "", []),
    ("Glycolysis", "One glucose molecule splits into two pyruvate molecules in cytoplasm, releasing small amount of ATP.", "formula_panel", {"formula": "Glucose → 2 Pyruvate + ATP", "note": "Glycolysis in cytoplasm"}, "First step all respiration types.", "Does not require oxygen directly.", "Common to aerobic and anaerobic paths.", "", []),
    ("Mitochondria — powerhouse", "Mitochondria are organelles where pyruvate is fully oxidised in presence of O₂ to release maximum ATP.", "placeholder", {"label": "Mitochondria — aerobic site"}, "NCERT exercise Q4 answer.", "Muscle cells have many mitochondria.", "Pyruvate + O₂ → CO₂ + H₂O + ATP in mitochondria.", "More mitochondria = more aerobic capacity.", "", ["mitochondria"]),
    ("Products of aerobic respiration", "CO₂, water, and about 38 ATP molecules (theoretical max) per glucose.", "formula_panel", {"formula": "C₆H₁₂O₆ + 6O₂ → 6CO₂ + 6H₂O + ATP", "note": "Complete oxidation"}, "Compare with anaerobic later.", "CO₂ leaves body via lungs.", "Most efficient energy release.", "", []),
    ("Respiration in humans — overview", "O₂ inhaled → diffuses into blood → carried to cells → used in mitochondria; CO₂ reverse path.", "placeholder", {"label": "Human respiration gas route"}, "Links breathing to cellular level.", "Haemoglobin carries O₂ in RBCs.", "Lungs exchange gases; cells respire.", "", "", []),
    ("Alveoli structure", "Alveoli are tiny air sacs in lungs with thin moist walls and rich blood capillaries for gas exchange.", "placeholder", {"label": "Alveoli — gas exchange"}, "NCERT exercise Q11 theme.", "Millions of alveoli = huge surface area.", "Thin wall + moisture + capillaries = efficient diffusion.", "Do not confuse alveoli with nephron.", "", ["alveoli"]),
    ("Diffusion in alveoli", "O₂ diffuses from alveolar air into blood; CO₂ diffuses from blood into alveoli to be exhaled.", "placeholder", {"label": "O₂ in, CO₂ out at alveoli"}, "Gas exchange mechanism.", "Steep concentration gradient maintained by blood flow.", "Passive diffusion across thin epithelium.", "", "", []),
    ("Haemoglobin and O₂ transport", "Haemoglobin in red blood cells binds O₂ in lungs and releases it in tissues.", "placeholder", {"label": "Haemoglobin carries O₂"}, "Blood transport role.", "Oxyhaemoglobin forms in lungs.", "Iron in haemoglobin binds O₂ reversibly.", "", "", []),
    ("Activity 5.1 — yeast and sugar", "Yeast in sugar solution produces CO₂ bubbles — anaerobic respiration (fermentation).", "placeholder", {"label": "Activity 5.1 — yeast fermentation"}, "Lab evidence for anaerobic path.", "Balloon on flask inflates with CO₂.", "Yeast: glucose → ethanol + CO₂ + energy.", "Same activity shows gas evolution sign of life.", "", []),
    ("Comparing energy yield", "Aerobic respiration releases far more ATP per glucose than anaerobic fermentation.", "placeholder", {"label": "Aerobic vs anaerobic energy"}, "Why O₂ is vital for active animals.", "Sprinters feel burn — temporary anaerobic in muscles.", "Aerobic is preferred when O₂ available.", "", "", []),
])

DAY10 = _build_day(10, [
    ("Anaerobic in yeast", "Yeast ferments glucose to ethanol, CO₂, and limited ATP — used in bread and brewing.", "formula_panel", {"formula": "Glucose → Ethanol + CO₂ + ATP", "note": "Alcoholic fermentation"}, "Activity 5.1 equation.", "Bread rises from CO₂ bubbles in dough.", "Anaerobic in yeast — industry application.", "", "", []),
    ("Anaerobic in muscle cells", "During intense exercise, muscles respire anaerobically producing lactic acid and less ATP.", "formula_panel", {"formula": "Glucose → Lactic acid + ATP", "note": "Muscle fatigue"}, "Sports physiology link.", "Cramp and fatigue from lactic acid accumulation.", "Temporary when O₂ delivery lags demand.", "Oxygen debt repaid after exercise.", "", []),
    ("Oxygen debt", "After vigorous exercise, extra O₂ needed to oxidise accumulated lactic acid — breathing stays heavy.", "placeholder", {"label": "Oxygen debt / recovery"}, "Post-exercise panting explained.", "Deep breathing clears lactic acid.", "Repaying oxygen debt restores pH.", "", "", []),
    ("Aerobic vs anaerobic — table", "Aerobic: needs O₂, CO₂ + H₂O products, more ATP, in mitochondria. Anaerobic: no O₂, partial products, less ATP, cytoplasm.", "placeholder", {"label": "Aerobic vs anaerobic table"}, "NCERT exercise Q10 style.", "Fill table for location, O₂, products, ATP.", "Know at least two differences each.", "Photosynthesis is not respiration reversed in location.", "", []),
    ("When anaerobic is used", "Anaerobic pathways when O₂ supply insufficient — yeast in sealed flask, sprinting muscles.", "placeholder", {"label": "When anaerobic occurs"}, "Context for each example.", "Root cells in waterlogged soil may switch.", "Survival pathway, not primary for humans.", "", "", []),
    ("Respiration vs photosynthesis", "Respiration breaks glucose for energy in all living cells; photosynthesis makes glucose in green plants using light.", "placeholder", {"label": "Respiration vs photosynthesis"}, "Major swap misconception.", "Both involve gas exchange but opposite roles overall in plants.", "Respiration: all cells. Photosynthesis: chloroplasts only.", "Do not swap equations or locations.", "", []),
    ("Balancing photosynthesis and respiration", "Plants produce O₂ by photosynthesis and use O₂ in respiration — net gas exchange varies.", "placeholder", {"label": "Net gas exchange in plants"}, "Day vs night balance.", "Young plant in light releases net O₂.", "Both processes run in green plants.", "", "", []),
    ("Respiration in germinating seeds", "Seeds respire actively during germination even before green shoots appear.", "placeholder", {"label": "Germinating seeds respire"}, "Proof seeds are alive.", "Warm flask with seeds — heat from respiration.", "No photosynthesis until chlorophyll forms.", "", "", []),
    ("Commercial fermentation", "Anaerobic yeast respiration used for bread, beer, wine, and bioethanol production.", "placeholder", {"label": "Fermentation industry"}, "Application section.", "CO₂ raises dough; ethanol in beverages.", "Biotechnology uses controlled fermentation.", "", "", []),
    ("Respiration summary", "All living cells respire; aerobic in mitochondria is main path; anaerobic when O₂ limited.", "placeholder", {"label": "Respiration unit summary"}, "End of respiration block.", "Link breathing → blood → cell → mitochondria.", "Draw full pathway for exam revision.", "", "", []),
])

DAY11 = _build_day(11, [
    ("Transport in plants — why needed", "Plants need transport to move water, minerals, and food between roots, stem, and leaves.", "placeholder", {"label": "Why plants need transport"}, "Third life process block.", "Tall trees move water 50+ metres up.", "Roots absorb; leaves photosynthesise — connection needed.", "", "", []),
    ("Xylem — definition", "Xylem transports water and dissolved minerals from roots upward to all plant parts.", "placeholder", {"label": "Xylem — water and minerals"}, "NCERT exercise Q2 theme.", "Dead hollow cells form continuous tubes.", "One-way upward flow mainly.", "Xylem carries water — not food.", "", ["xylem"]),
    ("Phloem — definition", "Phloem transports food (sucrose) from leaves to storage organs and growing parts.", "placeholder", {"label": "Phloem — food transport"}, "Pair with xylem.", "Bark contains phloem; peeling ring kills tree.", "Bidirectional food movement.", "Do not swap xylem and phloem functions.", "", ["phloem"]),
    ("Root hair cells", "Root hairs increase surface area to absorb water and minerals from soil by osmosis and active uptake.", "placeholder", {"label": "Root hairs — absorption"}, "Start of xylem pathway.", "Millions of root hairs near tip.", "Large surface area in small zone.", "", "", []),
    ("Path of water in plant", "Soil water → root hair → xylem → stem → leaves → evaporates from stomata.", "placeholder", {"label": "Water pathway in plant"}, "Continuous column idea.", "Activity 5.4 shows coloured water in xylem.", "Transpiration pull draws water up.", "", "", []),
    ("Transpiration", "Transpiration is loss of water vapour from aerial parts of plant, mainly through stomata.", "placeholder", {"label": "Transpiration — water loss"}, "Drives xylem flow.", "Wilting on hot dry day.", "Creates suction pulling water upward.", "Transpiration cools leaf surface.", "", ["transpiration"]),
    ("Transpiration pull", "Evaporation from leaves creates tension that pulls water column up through xylem.", "placeholder", {"label": "Transpiration pull mechanism"}, "Cohesion-tension at NCERT level.", "Like sucking drink through straw.", "No energy spent by plant to lift water — passive pull.", "", "", []),
    ("Activity 5.4 — xylem dye experiment", "Place plant stem in eosin/coloured water; cut sections show dye in xylem vessels.", "placeholder", {"label": "Activity 5.4 — xylem staining"}, "Visual proof of xylem path.", "Red streaks in stem cross-section.", "Dye follows water pathway in xylem.", "", "", []),
    ("Activity 5.5 — transpiration bag", "Plastic bag on leaf shows water droplets inside — proof of transpiration.", "placeholder", {"label": "Activity 5.5 — transpiration proof"}, "Simple school experiment.", "Bag mists up over hours in sun.", "Water vapour from leaf condenses.", "", "", []),
    ("Xylem tissue structure", "Xylem has vessels and tracheids — thick lignified walls, no cytoplasm in mature cells.", "placeholder", {"label": "Xylem vessel structure"}, "Adaptation for water pipe.", "Lignin strengthens against suction.", "Dead cells form hollow tubes.", "", "", []),
])

DAY12 = _build_day(12, [
    ("Phloem tissue structure", "Phloem has sieve tubes and companion cells; living cells transport dissolved sugars.", "placeholder", {"label": "Phloem sieve tubes"}, "Contrast dead xylem.", "Companion cells help load sugar.", "Sieve plates allow flow between cells.", "", "", []),
    ("Translocation", "Translocation is movement of food (sucrose) through phloem from source to sink.", "placeholder", {"label": "Translocation in phloem"}, "Official term for food transport.", "Leaves (source) → roots/t fruits (sink).", "Uses ATP at source loading.", "Bidirectional — up or down as needed.", "", ["translocation"]),
    ("Source and sink", "Source is where food is made/stored for export; sink is where food is used or stored.", "placeholder", {"label": "Source → sink"}, "Phloem direction logic.", "Leaf in summer = source; growing root = sink.", "Direction reverses seasonally in some plants.", "", "", []),
    ("Ringing experiment", "Removing phloem ring around trunk causes swelling above cut — food cannot pass down.", "placeholder", {"label": "Ringing experiment"}, "Classic phloem proof.", "Tree may die if bark ring removed completely.", "Proves phloem is in bark.", "", "", []),
    ("Xylem vs phloem summary", "Xylem: water + minerals, upward, dead cells. Phloem: food, bidirectional, living sieve tubes.", "placeholder", {"label": "Xylem vs phloem table"}, "High-frequency exam table.", "Never swap contents or direction.", "Both are vascular tissues in plants.", "Xylem/phloem swap is top misconception.", "", []),
    ("Transport in aquatic plants", "Some aquatic plants have reduced xylem support; still need gas and nutrient transport.", "placeholder", {"label": "Aquatic plant transport"}, "Variation note.", "Hydrilla releases O₂ bubbles in water.", "Adaptations match habitat.", "", "", []),
    ("Mineral uptake", "Minerals enter root hairs by active transport against concentration gradient — needs energy.", "placeholder", {"label": "Active mineral uptake"}, "Not passive like some water entry.", "Nitrates for proteins; magnesium for chlorophyll.", "Active transport uses ATP from respiration.", "", "", []),
    ("Wilting and recovery", "Excess transpiration without water uptake causes wilting; watering restores turgor.", "placeholder", {"label": "Wilting explained"}, "Everyday plant observation.", "Hot afternoon wilting; evening recovery.", "Turgor pressure supports herbaceous plants.", "", "", []),
    ("Guard cells and transpiration", "Open stomata allow CO₂ for photosynthesis but increase transpiration water loss.", "placeholder", {"label": "Stomata trade-off"}, "Balance gas gain vs water loss.", "Desert plants have sunken stomata.", "Plants regulate stomatal opening.", "", "", []),
    ("Plant transport summary", "Xylem + transpiration pull for water up; phloem + translocation for food to all parts.", "placeholder", {"label": "Plant transport summary"}, "Days 11–12 consolidation.", "Draw whole plant with both pathways labelled.", "Activities 5.4 and 5.5 support xylem/transpiration.", "", "", []),
])

DAY13 = _build_day(13, [
    ("Transport in animals — need", "Animals need circulatory system to deliver O₂, food, hormones and remove wastes from all cells.", "placeholder", {"label": "Why animals need blood"}, "Fourth process subsection.", "Human has ~5 litres blood circulating.", "Diffusion alone fails beyond tiny thickness.", "", "", []),
    ("Blood — components", "Blood has plasma (liquid) and formed elements: RBCs, WBCs, and platelets.", "placeholder", {"label": "Blood components"}, "Composition question.", "Plasma is straw-coloured, mostly water.", "RBCs carry O₂; WBCs fight infection; platelets clot.", "", "", []),
    ("Plasma function", "Plasma transports digested food, CO₂, hormones, and waste products dissolved in water.", "placeholder", {"label": "Plasma — transport medium"}, "Liquid part of blood.", "Urea carried in plasma to kidney.", "About 55% of blood volume.", "", "", []),
    ("Red blood cells", "RBCs contain haemoglobin; biconcave shape increases surface area; no nucleus in mature human RBC.", "placeholder", {"label": "RBC — oxygen carriers"}, "Adaptation for O₂.", "Millions per drop of blood.", "Haemoglobin binds O₂ in lungs.", "", "", []),
    ("White blood cells", "WBCs defend against pathogens; larger, have nucleus, can leave blood vessels.", "placeholder", {"label": "WBC — immunity"}, "Defence role.", "Phagocytes engulf bacteria.", "Part of immune system.", "", "", []),
    ("Platelets", "Platelets are cell fragments that help blood clot at injury sites.", "placeholder", {"label": "Platelets — clotting"}, "Prevent blood loss.", "Cut finger stops bleeding from clot.", "Too few platelets → bleeding risk.", "", "", []),
    ("Blood vessels — three types", "Arteries carry blood away from heart; veins return blood to heart; capillaries exchange with tissues.", "placeholder", {"label": "Artery | Vein | Capillary"}, "Structural comparison.", "Arteries thick-walled; veins have valves.", "Capillaries are one cell thick.", "", "", []),
    ("Arteries vs veins", "Arteries: thick elastic walls, high pressure, no valves. Veins: thinner walls, valves prevent backflow.", "placeholder", {"label": "Artery vs vein"}, "Exam diagram labels.", "Aorta is largest artery.", "Pulmonary artery carries deoxygenated blood — exception.", "", "", []),
    ("Capillaries", "Capillaries connect arteries to veins; thin walls allow exchange of gases, nutrients, and wastes.", "placeholder", {"label": "Capillaries — exchange"}, "Site of tissue exchange.", "Blood slows in capillary beds.", "Single-cell thick endothelium.", "", "", []),
    ("Double circulation preview", "Human heart drives double circulation — pulmonary and systemic circuits.", "placeholder", {"label": "Double circulation intro"}, "Leads to Day 14 heart.", "Blood passes heart twice per full body circuit.", "Separates low-pressure lung circuit from high-pressure body.", "", "", []),
])

DAY14 = _build_day(14, [
    ("Human heart — chambers", "Heart has four chambers: two atria (receive blood) and two ventricles (pump blood out).", "placeholder", {"label": "Four-chambered heart"}, "Core heart anatomy.", "Left side pumps to body; right to lungs.", "Atria on top; ventricles below.", "", "", []),
    ("Pulmonary circulation", "Right ventricle pumps deoxygenated blood to lungs; returns oxygenated to left atrium.", "placeholder", {"label": "Pulmonary circuit"}, "Lung loop.", "Pulmonary artery → lungs → pulmonary vein.", "Gas exchange in alveoli.", "", "", []),
    ("Systemic circulation", "Left ventricle pumps oxygenated blood to entire body; returns deoxygenated to right atrium.", "placeholder", {"label": "Systemic circuit"}, "Body loop.", "Aorta branches to all organs.", "Left ventricle wall is thickest — high pressure.", "", "", []),
    ("Heart valves", "Valves prevent backflow — tricuspid, bicuspid (mitral), pulmonary and aortic semilunar valves.", "placeholder", {"label": "Heart valves — one-way flow"}, "Lub-dub sounds from valves.", "Valves snap shut after ventricle contraction.", "Faulty valves cause murmurs.", "", "", []),
    ("Heartbeat mechanism", "SA node triggers rhythmic contraction — atria contract then ventricles ( lub-dub ).", "placeholder", {"label": "Cardiac cycle overview"}, "Pacemaker concept.", "Activity 5.6 — stethoscope on chest.", "Electrical signal coordinates chambers.", "", "", []),
    ("Activity 5.6 — heartbeat sound", "Stethoscope on chest hears lub-dub of valves closing during cardiac cycle.", "placeholder", {"label": "Activity 5.6 — stethoscope"}, "NCERT practical.", "Lub = AV valves close; dub = semilunar close.", "Count beats per minute at rest.", "", "", []),
    ("Pulse rate", "Pulse is wave of arterial expansion felt at wrist; equals heart rate at rest.", "placeholder", {"label": "Pulse measurement"}, "Links to Activity 5.7.", "Normal resting pulse ~70–80 bpm in adults.", "Pulse points: wrist, neck.", "", "", []),
    ("Activity 5.7 — pulse after exercise", "Pulse rate increases after exercise because muscles need more O₂ and glucose faster.", "placeholder", {"label": "Activity 5.7 — exercise pulse"}, "Physiology experiment.", "Compare resting vs after running.", "Heart pumps faster to meet demand.", "", "", []),
    ("Lymphatic system (brief)", "Lymph carries absorbed fats from intestine and returns tissue fluid to blood.", "placeholder", {"label": "Lymph — fat transport"}, "Links villi lacteals.", "Lymph nodes filter pathogens.", "Complements blood circulation.", "", "", []),
    ("Circulation summary", "Heart → arteries → capillaries → veins → heart; O₂ and food delivered, CO₂ and wastes collected.", "placeholder", {"label": "Circulation summary"}, "Day 13–14 consolidation.", "Trace one red blood cell through full circuit.", "Double circulation in humans and birds.", "", "", []),
])

DAY15 = _build_day(15, [
    ("Excretion — definition", "Excretion is removal of harmful metabolic wastes produced in the body.", "placeholder", {"label": "Excretion defined"}, "Fourth life process.", "Urea from protein metabolism.", "Not the same as egestion or sweating alone.", "Excretion removes metabolic wastes.", "", ["excretion"]),
    ("Egestion vs excretion vs secretion", "Egestion: undigested food out. Excretion: metabolic waste out. Secretion: useful substances released.", "placeholder", {"label": "Three terms compared"}, "Terminology precision.", "Faeces = egestion; urine = excretion.", "Do not call urination egestion.", "", "", []),
    ("Excretion in plants", "Plants excrete O₂ (photosynthesis), CO₂ (respiration), water vapour, and store or drop wastes.", "placeholder", {"label": "Plant excretion"}, "NCERT exercise Q13 theme.", "Plants store waste in vacuoles or bark.", "Resins and gums are waste products.", "Plants don't have kidneys.", "", []),
    ("Plant waste removal methods", "Plants lose gaseous wastes through stomata; shed leaves; store wastes in cellular vacuoles and old xylem.", "placeholder", {"label": "How plants remove wastes"}, "List for exam.", "Tamarind stores tartaric acid in fruits.", "Guttation exudes liquid water with salts.", "", "", []),
    ("Excretion in humans — organs", "Main excretory organs: kidneys (urine), lungs (CO₂), skin (sweat — some urea/salts).", "placeholder", {"label": "Human excretory organs"}, "Multi-organ excretion.", "Kidneys primary for nitrogenous waste.", "Lungs excrete CO₂ every breath.", "", "", []),
    ("Kidney location and role", "Pair of kidneys filter blood to remove urea, excess water, and salts as urine.", "placeholder", {"label": "Kidneys filter blood"}, "NCERT exercise Q1 theme.", "Kidneys maintain water-salt balance (osmoregulation).", "Bean-shaped organs in abdomen.", "Kidneys → excretion, not digestion.", "", ["kidney"]),
    ("Urine pathway", "Kidney → ureter → urinary bladder → urethra.", "placeholder", {"label": "Urinary pathway"}, "Anatomy sequence.", "Bladder stores urine temporarily.", "Ureter connects kidney to bladder.", "", "", []),
    ("Structure of kidney (overview)", "Kidney has outer cortex and inner medulla containing millions of nephrons.", "placeholder", {"label": "Kidney structure overview"}, "Leads to nephron Day 16.", "Renal artery brings blood; renal vein takes filtered blood.", "Each nephron is filtering unit.", "", "", []),
    ("Why excretion matters", "Accumulated wastes poison cells — urea must be removed to maintain homeostasis.", "placeholder", {"label": "Homeostasis and excretion"}, "Health importance.", "Kidney failure raises blood urea dangerously.", "Excretion maintains internal environment.", "", "", []),
    ("Excretion block preview", "Day 16 covers nephron structure, filtration, and Activity 5.8 dialysis model.", "placeholder", {"label": "Excretion roadmap"}, "Bridge to final day.", "Do not confuse alveoli (gas) with nephron (filter).", "Nephron is functional unit of kidney.", "", "", []),
])

DAY16 = _build_day(16, [
    ("Nephron — functional unit", "Nephron is the structural and functional unit of kidney — filters blood and forms urine.", "placeholder", {"label": "Nephron — kidney unit"}, "NCERT exercise Q12 core.", "Each kidney has about 1 million nephrons.", "Damage to nephrons impairs filtration.", "Alveoli vs nephron is common confusion.", "", ["nephron"]),
    ("Nephron parts", "Nephron: Bowman's capsule + glomerulus, proximal tubule, loop of Henle, distal tubule, collecting duct.", "placeholder", {"label": "Nephron labelled diagram"}, "Diagram question.", "Glomerulus is capillary knot for filtration.", "Know at least four parts for exam.", "", "", []),
    ("Ultrafiltration in glomerulus", "Blood pressure forces water, urea, glucose, salts into Bowman's capsule; large proteins stay in blood.", "placeholder", {"label": "Filtration in glomerulus"}, "First nephron step.", "Filterate enters tubule.", "Proteins and RBCs not filtered.", "", "", []),
    ("Reabsorption in tubule", "Useful substances (glucose, most water, salts) reabsorbed into blood; waste stays in tubule.", "placeholder", {"label": "Selective reabsorption"}, "Second nephron step.", "All glucose normally reabsorbed.", "Saves body resources.", "", "", []),
    ("Urine formation", "Remaining fluid in collecting duct is urine — concentrated urea, excess water and salts.", "placeholder", {"label": "Urine composition"}, "Final product.", "Urine ~95% water.", "Volume varies with hydration.", "", "", []),
    ("Activity 5.8 — dialysis model", "Visking tubing in water bath models selective permeability like dialysis in kidney failure treatment.", "placeholder", {"label": "Activity 5.8 — dialysis tubing"}, "NCERT activity.", "Small molecules pass through membrane; starch/protein retained.", "Real dialysis filters blood artificially.", "", "", []),
    ("Kidney failure and dialysis", "When kidneys fail, dialysis machine removes urea from blood using semi-permeable membrane.", "placeholder", {"label": "Clinical dialysis"}, "Application of excretion concept.", "Regular dialysis replaces kidney function.", "Transplant is long-term alternative.", "", "", []),
    ("NCERT summary — life processes", "Nutrition, respiration, transport, and excretion maintain life in plants and animals.", "placeholder", {"label": "Ch 5 summary — four processes"}, "Unit completion.", "Match process to organ system.", "All four needed continuously.", "", "", []),
    ("Must-know comparisons", "Autotroph vs heterotroph; aerobic vs anaerobic; xylem vs phloem; breathing vs respiration; egestion vs excretion.", "placeholder", {"label": "Exam comparison checklist"}, "Revision list.", "One table each for top five pairs.", "Comparison questions are common.", "", "", []),
    ("Unit 1 complete", "Unit 1 Life Processes complete — 160 concept cards; proceed to Practice when unlocked.", "placeholder", {"label": "Unit 1 complete — 160 cards"}, "Completion card.", "200 MCQs in bank; Stage 2 days 17–20 follow.", "Concepts done → practice → NCERT MCQs.", "", "", []),
])

DAY_BUILDERS = {
    1: lambda: DAY1,
    2: lambda: DAY2,
    3: lambda: DAY3,
    4: lambda: DAY4,
    5: lambda: DAY5,
    6: lambda: DAY6,
    7: lambda: DAY7,
    8: lambda: DAY8,
    9: lambda: DAY9,
    10: lambda: DAY10,
    11: lambda: DAY11,
    12: lambda: DAY12,
    13: lambda: DAY13,
    14: lambda: DAY14,
    15: lambda: DAY15,
    16: lambda: DAY16,
}

DAY_TITLES = {
    1: "Life Processes — Introduction",
    2: "Nutrition — Modes and Overview",
    3: "Autotrophic Nutrition and Photosynthesis",
    4: "Photosynthesis — Details and Stomata",
    5: "Heterotrophic Nutrition",
    6: "Human Digestion — Upper Tract",
    7: "Human Digestion — Absorption",
    8: "Respiration — Introduction",
    9: "Aerobic Respiration and Gas Exchange",
    10: "Anaerobic Respiration",
    11: "Transport in Plants — Xylem",
    12: "Transport in Plants — Phloem",
    13: "Transport in Animals — Blood",
    14: "Heart and Circulation",
    15: "Excretion — Plants and Kidneys",
    16: "Nephron, Dialysis and Exam Prep",
}
