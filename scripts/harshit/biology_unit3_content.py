"""Full concept card content for Harshit Biology Unit 3 — Days 1–16 (Ch 7 How do Organisms Reproduce?)."""

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
                f"u3_d{day}_c{i:02d}",
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
    ('Why organisms reproduce', 'Organisms reproduce to create new individuals of their species so life continues generation after generation.', 'placeholder', {'label': 'Purpose of reproduction'}, 'NCERT Ch 7 opening theme.', 'Humans have children; mango trees produce seeds.', 'Reproduction is not for individual survival — it is for species continuity.', 'Reproduction is different from growth or repair.', '', ['reproduction']),
    ('DNA as genetic material', 'DNA in the nucleus carries instructions that determine body design and inherited traits of an organism.', 'placeholder', {'label': 'DNA — blueprint of life'}, 'Foundation for heredity link.', 'Eye colour and blood group information is in DNA.', 'Every cell has DNA; gametes carry half in sexual reproduction.', 'DNA copying must occur before cell division.', '', ['DNA']),
    ('Why DNA copying is needed', 'New organism must get DNA from parents so it has complete instructions to build and run its body.', 'placeholder', {'label': 'DNA passed to offspring'}, 'Links reproduction to heredity.', 'Offspring resembles parents because DNA is copied and inherited.', 'Without DNA transfer, offspring would lack design information.', 'Copying is not perfect — leads to variation.', '', []),
    ('DNA copying and cell apparatus', 'When cell divides, DNA copies and each new cell gets one copy plus existing cellular apparatus.', 'placeholder', {'label': 'DNA copy per daughter cell'}, 'NCERT cell division discussion.', 'Skin cell division replaces dead cells with same DNA.', 'Each daughter cell needs full DNA set.', 'Cell apparatus also divides — not DNA alone.', '', []),
    ('Accuracy of DNA copying', 'DNA copying is remarkably accurate but not absolutely perfect — small errors create variations.', 'placeholder', {'label': 'DNA copying accuracy'}, 'Bridge to variation day.', 'Most copies identical; rare changes alter traits.', 'High accuracy keeps species stable.', 'Errors in body cells vs gametes differ in impact.', '', []),
    ('Variations from copying errors', 'Variations are differences among individuals caused by inaccuracies in DNA copying or recombination.', 'placeholder', {'label': 'Variations arise'}, 'Survival advantage theme.', 'Some bacteria resist antibiotic due to variation.', 'Variation is raw material for evolution.', 'Not all variations are harmful or helpful.', '', ['variation']),
    ('Species-level importance', 'Reproduction at species level maintains population size and passes DNA to next generation.', 'placeholder', {'label': 'Species continuity'}, 'Big picture.', 'Endangered species decline when reproduction fails.', 'Individual dies; species continues via offspring.', '', '', []),
    ('Reproduction vs other life processes', 'Nutrition, respiration, transport support individual life; reproduction creates new individuals.', 'placeholder', {'label': 'Reproduction among life processes'}, 'Ch 5–7 connection.', 'A plant photosynthesises and also flowers to reproduce.', 'All life processes support reproduction indirectly.', '', '', []),
    ('Types of reproduction preview', 'Organisms reproduce asexually (one parent) or sexually (two parents) — different DNA mixing outcomes.', 'placeholder', {'label': 'Asexual vs sexual preview'}, 'Roadmap for unit.', 'Amoeba binary fission vs human baby from parents.', 'Sexual reproduction increases variation.', '', '', []),
    ('Chapter 7 roadmap', 'Ch 7 covers asexual modes, sexual reproduction in plants and humans, health, and Activities 7.1–7.7.', 'placeholder', {'label': 'Ch 7 roadmap — 16 days'}, 'Unit orientation.', 'Activities include yeast, hydra, bread mould, flower parts.', 'Plant and human reproduction both exam-heavy.', '', '', []),
])

DAY2 = _build_day(2, [
    ('What is variation?', 'Variation means differences in traits among individuals of the same species — height, colour, resistance, etc.', 'placeholder', {'label': 'Variation defined'}, 'Key Ch 7–8 concept.', 'Human height and fingerprint patterns vary.', 'No two individuals identical except clones.', 'Variation is not same as mutation only.', '', ['variation']),
    ('Sources of variation', 'Variations arise from DNA copying errors, sexual recombination, and environmental effects on expression.', 'placeholder', {'label': 'Sources of variation'}, 'Multi-cause understanding.', 'Sibling differences from new gene combinations.', 'Sexual reproduction shuffles genes strongly.', 'Environment affects phenotype not always genotype.', '', []),
    ('Variation in asexual reproduction', 'Asexual offspring are mostly genetically identical to parent — variation is limited unless DNA copy error occurs.', 'placeholder', {'label': 'Low variation asexual'}, 'Contrast with sexual.', 'Banana plants from suckers are clones.', 'Limited variation can be disadvantage in changing environment.', 'Sudden useful mutation rare but possible.', '', []),
    ('Variation in sexual reproduction', 'Sexual reproduction combines DNA from two parents producing new gene combinations and more variation.', 'placeholder', {'label': 'High variation sexual'}, 'NCERT emphasis.', 'Brothers look similar but not identical.', 'Meiosis and fertilisation create diversity.', 'Variation helps species adapt over time.', '', []),
    ('Advantage of variation', 'Beneficial variations may help some individuals survive environmental changes when others cannot.', 'placeholder', {'label': 'Variation and survival'}, 'Natural selection preview.', 'Bacteria variant resists new antibiotic.', 'Population with variation survives change better.', 'Harmful variation may reduce survival.', '', []),
    ('Disadvantage of too little variation', 'Population with very little variation may all die if environment changes — all lack suitable trait.', 'placeholder', {'label': 'Risk of uniformity'}, 'Clone vulnerability.', 'Monoculture crops can be wiped by one disease.', 'Asexual clones uniform — fast spread of weakness too.', '', '', []),
    ('Inherited vs acquired traits', 'Inherited traits come from DNA (eye colour); acquired traits develop in life (learned skill, scar) — usually not inherited.', 'placeholder', {'label': 'Inherited vs acquired'}, 'Ch 8 preview.', 'Cutting tail of mice does not pass to babies — NCERT example.', 'Only DNA-based traits pass to offspring.', 'Lamarck wrong; acquired not inherited.', '', []),
    ('Population variation', 'Variation exists at population level — medicine and agriculture use this (crop breeding, antibiotic resistance).', 'placeholder', {'label': 'Variation in populations'}, 'Applied biology.', 'Farmers select high-yield wheat variants.', 'Variation is practical not just theoretical.', '', '', []),
    ('Variation and evolution link', 'Accumulated variations over generations, with selection, lead to evolution — Ch 9 preview.', 'placeholder', {'label': 'Variation → evolution'}, 'Forward link.', 'Finch beak sizes varied on Galapagos.', 'Reproduction + variation + selection = evolution.', 'Class 10 needs link statement only.', '', []),
    ('Variation day summary', 'DNA copying errors and sexual recombination create variation; variation helps species adapt and survive change.', 'placeholder', {'label': 'Variation day summary'}, 'Day 2 consolidation.', 'Compare variation level asexual vs sexual.', 'Three sources: error, recombination, environment.', '', '', []),
])

DAY3 = _build_day(3, [
    ('Asexual reproduction — definition', 'Asexual reproduction involves a single parent producing offspring genetically similar to itself without gametes.', 'placeholder', {'label': 'Asexual reproduction defined'}, 'First reproduction mode.', 'Amoeba divides into two daughter amoebae.', 'One parent; no fusion of gametes.', 'Offspring are clones unless DNA error.', '', ['asexual reproduction']),
    ('Binary fission in Amoeba', 'Amoeba reproduces by binary fission — nucleus divides then cytoplasm splits into two equal daughter cells.', 'placeholder', {'label': 'Amoeba binary fission'}, 'Classic NCERT example.', 'Pseudopodia withdraw; cell pinches in middle.', 'Unicellular simple division.', 'Not same as budding — equal halves.', '', ['binary fission']),
    ('Binary fission in Leishmania', 'Leishmania (kala-azar parasite) binary fissions oriented along whip-like flagellum axis.', 'placeholder', {'label': 'Leishmania fission'}, 'NCERT specific organism.', 'Transmitted by sandfly; affects internal organs.', 'Know organism name for exam.', 'Orientation differs from Amoeba.', '', []),
    ('Binary fission in Plasmodium', 'Plasmodium (malaria parasite) reproduces asexually in human liver and RBCs by multiple fission stages too.', 'placeholder', {'label': 'Plasmodium asexual stages'}, 'Disease link.', 'Malaria cycles include asexual multiplication in host.', 'Complex life cycle — asexual and sexual in mosquito.', 'Exam may ask organism-mode match.', '', []),
    ('Activity 7.1 — yeast budding observation', 'Activity 7.1 also compares yeast; today focus fission organisms under microscope or diagrams.', 'placeholder', {'label': 'Activity 7.1 link'}, 'Lab connection.', 'Yeast shows budding not fission.', 'Distinguish yeast from Amoeba mode.', '', '', []),
    ('Advantages of binary fission', 'Fast, energy-efficient, works well in stable environment when parent well adapted.', 'placeholder', {'label': 'Fission advantages'}, 'Why unicellular use it.', 'Amoeba doubles population quickly in pond.', 'No need to find mate.', 'Rapid colonisation of favourable habitat.', '', []),
    ('Limitations of asexual reproduction', 'Limited variation; population vulnerable to same disease or environmental shift.', 'placeholder', {'label': 'Asexual limitations'}, 'Balanced view.', 'All identical potato plants share same blight risk.', 'Trade speed for diversity.', '', '', []),
    ('Multiple fission', 'Some protozoans divide into many daughter cells at once — multiple fission (e.g. Plasmodium schizont).', 'placeholder', {'label': 'Multiple fission'}, 'Extension of asexual.', 'One cell → many daughter cells simultaneously.', 'Different from binary — many at once.', 'Still asexual — no gametes.', '', []),
    ('Asexual in unicellular vs multicellular', 'Unicellular: fission common. Multicellular: budding, fragmentation etc. — next days.', 'placeholder', {'label': 'Asexual scope'}, 'Organisation level.', 'Amoeba one cell becomes two.', 'Multicellular needs different body division.', '', '', []),
    ('Binary fission summary', 'Amoeba and Leishmania: binary fission; fast clone production; limited variation; know diagrams and steps.', 'placeholder', {'label': 'Binary fission summary'}, 'Day 3 consolidation.', 'Draw Amoeba dividing with nucleus split.', 'Name organism + mode for exam.', '', '', []),
])

DAY4 = _build_day(4, [
    ('Fragmentation', 'Fragmentation: organism breaks into pieces and each piece grows into a new individual (e.g. Spirogyra).', 'placeholder', {'label': 'Fragmentation — Spirogyra'}, 'Asexual mode.', 'Algae filaments break and each grows.', 'Needs ability of each fragment to regenerate full body.', 'Not same as regeneration after injury only.', '', ['fragmentation']),
    ('Spirogyra reproduction', 'Spirogyra alga reproduces by fragmentation when filaments break into pieces that grow into new filaments.', 'placeholder', {'label': 'Spirogyra example'}, 'NCERT named example.', 'Thread-like green alga in ponds.', 'Simple multicellular asexual.', '', '', []),
    ('Regeneration', 'Regeneration is ability to regrow lost or damaged parts; in some organisms regrown part becomes new individual.', 'placeholder', {'label': 'Regeneration defined'}, 'Planaria classic example.', 'Planaria cut into pieces — each regenerates whole worm.', 'Common in lower organisms; limited in humans.', 'Human liver regrows partly — not full body regeneration.', '', ['regeneration']),
    ('Planaria regeneration', 'Planaria (flatworm) shows high regeneration — even small body piece can form complete organism.', 'placeholder', {'label': 'Planaria example'}, 'Exam favourite.', 'Cut head or tail piece regenerates missing parts.', 'Specialised cells proliferate at cut site.', 'Regeneration used for asexual in some species.', '', []),
    ('Budding — definition', 'Budding: small outgrowth (bud) forms on parent, develops organs, detaches to live independently.', 'placeholder', {'label': 'Budding defined'}, 'Yeast and Hydra mode.', 'Yeast cell forms tiny bud that grows and separates.', 'Parent retains identity; bud becomes offspring.', 'Bud may stay attached forming colony.', '', ['budding']),
    ('Hydra budding', 'Hydra grows bud on side; bud develops tentacles and mouth then separates as new Hydra.', 'placeholder', {'label': 'Hydra budding'}, 'NCERT diagram organism.', 'Freshwater polyp on pond weeds.', 'Bud visible externally before detachment.', 'Activity 7.1 may observe Hydra buds.', '', []),
    ('Yeast budding', 'Yeast (unicellular fungus) forms bud on parent cell; nucleus divides and bud gets nucleus then pinches off.', 'placeholder', {'label': 'Yeast budding'}, 'Activity 7.1 focus.', 'Bread and beer fermentation uses yeast.', 'Asymmetric division — bud smaller than parent.', 'Yeast shows budding not binary fission.', '', []),
    ('Compare fission, fragmentation, budding', 'Fission: equal split one cell. Fragmentation: pieces of body. Budding: outgrowth from parent.', 'placeholder', {'label': 'Three asexual modes compared'}, 'Table question.', 'Amoeba fission; Spirogyra fragmentation; Hydra budding.', 'Match organism to mode.', '', '', []),
    ('Activity 7.1 review', 'Activity 7.1: yeast in sugar water — observe budding under microscope; CO₂ from respiration.', 'placeholder', {'label': 'Activity 7.1 — yeast'}, 'Practical recall.', 'Bud scar visible on yeast cells.', 'Link budding to reproduction not just fermentation.', '', '', []),
    ('Day 4 summary', 'Fragmentation (Spirogyra), regeneration (Planaria), budding (Hydra, Yeast) — three distinct asexual strategies.', 'placeholder', {'label': 'Fragmentation/budding summary'}, 'Day 4 consolidation.', 'Draw Hydra with bud labelled.', 'Regeneration ≠ fragmentation always.', '', '', []),
])

DAY5 = _build_day(5, [
    ('Vegetative propagation', 'Vegetative propagation is asexual reproduction in plants using vegetative parts — root, stem, leaf — not seeds.', 'placeholder', {'label': 'Vegetative propagation'}, 'Plant asexual agriculture.', 'Potato tuber, ginger rhizome, Bryophyllum leaf.', 'Clone plants with desired traits fast.', 'Farmers use for identical crop quality.', '', ['vegetative propagation']),
    ('Potato tuber', 'Potato reproduces from tuber bearing buds (eyes) that grow into new plants genetically same as parent.', 'placeholder', {'label': 'Potato — tuber buds'}, 'Common crop example.', 'Cut tuber with eye planted in soil.', 'Tuber is modified stem not root.', '', '', []),
    ('Ginger rhizome', 'Ginger spreads underground via rhizome — horizontal stem with nodes that sprout shoots and roots.', 'placeholder', {'label': 'Ginger — rhizome'}, 'Stem modification.', 'Rhizome piece planted grows new plant.', 'Underground stem storage and reproduction.', '', '', []),
    ('Bryophyllum leaf buds', 'Bryophyllum leaf margins produce adventitious buds that fall and grow into new plants.', 'placeholder', {'label': 'Bryophyllum — leaf buds'}, 'Leaf propagation.', 'Notches on leaf edge sprout plantlets.', 'Vegetative from leaf — NCERT example.', '', '', []),
    ('Sugarcane and rose cutting', 'Stem cuttings placed in soil develop roots and shoots — artificial vegetative propagation.', 'placeholder', {'label': 'Stem cuttings'}, 'Horticulture practice.', 'Gardeners root rose cuttings in moist soil.', 'Artificial method uses same natural principle.', 'Hormone rooting powder helps cuttings.', '', []),
    ('Advantages for farmers', 'Vegetative propagation is fast, uniform quality, flowers/fruits earlier than seed-grown plants.', 'placeholder', {'label': 'Farmer advantages'}, 'Applied question.', 'Mango grafting preserves sweet variety.', 'No waiting for seed germination and long juvenile phase.', 'Disease in one clone affects all — risk too.', '', []),
    ('Spore formation', 'Some organisms reproduce by spores — tiny cells in protective coat that germinate in suitable conditions.', 'placeholder', {'label': 'Spore formation'}, 'Rhizopus and ferns.', 'Bread mould Rhizopus releases spores in air.', 'Spores lightweight, spread widely.', 'Spores are reproductive cells not seeds.', '', ['spore']),
    ('Rhizopus (bread mould)', 'Rhizopus fungus on bread produces sporangia full of spores dispersed by air.', 'placeholder', {'label': 'Rhizopus sporangia'}, 'Activity 7.2 link.', 'White thread-like hyphae with black sporangia dots.', 'Spores land on new bread start growth.', 'Activity 7.2 observes bread mould.', '', []),
    ('Spores vs seeds', 'Spores: usually single cell, no embryo food store. Seeds: multicellular embryo with stored food — flowering plants.', 'placeholder', {'label': 'Spore vs seed'}, 'Comparison.', 'Fern spores on underside of leaf.', 'Seeds are more complex reproductive structure.', '', '', []),
    ('Vegetative and spores summary', 'Plants: vegetative parts (tuber, rhizome, leaf, cutting) and spores (Rhizopus) — know examples and advantages.', 'placeholder', {'label': 'Day 5 summary'}, 'Consolidation.', 'List five plant asexual examples.', 'Match structure to plant name.', '', '', []),
])

DAY6 = _build_day(6, [
    ('Sexual reproduction — definition', 'Sexual reproduction involves fusion of male and female gametes from two parents to form a new individual.', 'placeholder', {'label': 'Sexual reproduction defined'}, 'Major mode shift in Ch 7.', 'Human baby from egg and sperm fusion.', 'Two parents; gamete formation and fusion.', 'Offspring has mixed genetic information.', '', ['sexual reproduction']),
    ('Gametes', 'Gametes are specialised reproductive cells — sperm (male) and egg/ovum (female) — usually haploid.', 'placeholder', {'label': 'Gametes — sperm and egg'}, 'Core vocabulary.', 'Pollen and egg in plants; sperm and ovum in humans.', 'Haploid: half chromosome set.', 'Gametes fuse to restore diploid zygote.', '', ['gamete']),
    ('Fertilisation', 'Fertilisation is fusion of male and female gametes to form zygote — first cell of new organism.', 'formula_panel', {'formula': 'Male gamete + Female gamete → Zygote', 'note': 'Fertilisation'}, 'Central event.', 'Zygote divides by mitosis to form embryo.', 'Internal or external fertilisation.', 'Fertilisation ≠ pollination in plants.', '', ['fertilisation']),
    ('Why sexual reproduction creates variation', 'Gametes from each parent carry different gene combinations; fusion creates unique offspring genotype.', 'placeholder', {'label': 'Sexual → variation'}, 'Link Day 2 variation.', 'Siblings share parents but differ in many traits.', 'Meiosis shuffles genes before gamete formation.', 'More variation than asexual modes.', '', []),
    ('Male and female reproductive parts', 'Flowers have stamen (male) and pistil (female); animals have separate reproductive systems.', 'placeholder', {'label': 'Reproductive parts overview'}, 'Plant and animal parallel.', 'Stamen makes pollen; ovary makes egg cell.', 'Specialised organs for gamete production.', '', '', []),
    ('Internal vs external fertilisation', 'Internal: fusion inside female body (humans, birds). External: fusion in water (many fish, frogs).', 'placeholder', {'label': 'Internal vs external fertilisation'}, 'Environment comparison.', 'Humans: sperm meets egg in oviduct.', 'External needs water medium for gametes.', 'Plants: pollination then internal fertilisation in ovule.', '', []),
    ('Embryo development preview', 'Zygote divides repeatedly forming embryo that develops into foetus/baby or seedling.', 'placeholder', {'label': 'Zygote → embryo'}, 'Development arc.', 'Human embryo implants in uterus.', 'Mitosis builds body from single zygote.', '', '', []),
    ('Asexual vs sexual summary table', 'Asexual: one parent, fast, low variation. Sexual: two parents, slower, high variation, gametes involved.', 'placeholder', {'label': 'Asexual vs sexual table'}, 'Exam comparison.', 'Fill table with at least four rows.', 'Both are reproduction modes.', '', '', []),
    ('When sexual reproduction is advantageous', 'Changing or challenging environments favour varied offspring — some may survive new conditions.', 'placeholder', {'label': 'When sexual wins'}, 'Evolutionary reasoning.', 'Pathogens evolve; variation helps host resistance.', 'Cost of finding mate offset by adaptability.', '', '', []),
    ('Sexual reproduction intro summary', 'Sexual reproduction: gametes from two parents fuse to zygote; creates variation; leads to flower and human systems.', 'placeholder', {'label': 'Day 6 summary'}, 'Consolidation.', 'Define gamete, fertilisation, zygote.', 'Preview plant flower structure next.', '', '', []),
])

DAY7 = _build_day(7, [
    ('Flower — reproductive organ', 'Flower is the reproductive organ of angiosperms (flowering plants) producing male and female gametes.', 'placeholder', {'label': 'Flower — plant reproduction'}, 'Plant sexual reproduction start.', 'Mustard or hibiscus flower dissection in lab.', 'Modified shoot for reproduction.', 'Not all plants have flowers — ferns use spores.', '', ['flower']),
    ('Stamen — male part', 'Stamen consists of anther (pollen grains) and filament; produces male gametes in pollen.', 'placeholder', {'label': 'Stamen — anther and filament'}, 'Male flower part.', 'Yellow anthers dust pollen on finger.', 'Pollen carries male gamete to egg.', 'Filament holds anther up.', '', ['stamen']),
    ('Pistil (carpel) — female part', 'Pistil has stigma, style, and ovary; ovule inside ovary contains female gamete (egg cell).', 'placeholder', {'label': 'Pistil — stigma, style, ovary'}, 'Female flower part.', 'Ovary becomes fruit after fertilisation.', 'Stigma receives pollen; style is tube path.', 'Egg is inside ovule not directly in ovary wall.', '', ['pistil']),
    ('Pollen grain', 'Pollen grain is male gametophyte containing male gamete; formed in anther.', 'placeholder', {'label': 'Pollen grain'}, 'Male gamete carrier.', 'Pollen allergy from inhaling pollen.', 'Light pollen wind-dispersed; sticky for insects.', '', '', []),
    ('Pollination — definition', 'Pollination is transfer of pollen from anther to stigma of same or another flower.', 'placeholder', {'label': 'Pollination defined'}, 'Must occur before fertilisation.', 'Bees carry pollen flower to flower.', 'Pollination ≠ fertilisation.', 'Can be self or cross pollination.', '', ['pollination']),
    ('Self-pollination', 'Pollen transferred to stigma of same flower or another flower on same plant.', 'placeholder', {'label': 'Self-pollination'}, 'Less variation than cross.', 'Peas often self-pollinate.', 'Faster but less genetic mixing.', '', '', []),
    ('Cross-pollination', 'Pollen transferred to stigma of flower on different plant of same species — more variation.', 'placeholder', {'label': 'Cross-pollination'}, 'Agents needed.', 'Mango often cross-pollinated by insects.', 'Wind, water, insects, animals as agents.', 'Preferred in breeding for new combinations.', '', []),
    ('Pollinating agents', 'Wind (grasses), water (hydrilla), insects (bees, butterflies), birds, bats carry pollen.', 'placeholder', {'label': 'Pollination agents'}, 'Adaptation match.', 'Wind pollination: light dry pollen, feathery stigma.', 'Flower colour and nectar attract insects.', '', '', []),
    ('Activity 7.3 — flower parts', 'Activity 7.3: dissect flower, identify sepals, petals, stamen, pistil; locate anther and ovary.', 'placeholder', {'label': 'Activity 7.3 — flower dissection'}, 'Hands-on NCERT.', 'Draw labelled diagram from dissection.', 'Sepals protect bud; petals attract pollinators.', '', '', []),
    ('Pollination day summary', 'Know flower parts; pollen to stigma = pollination; agents include wind and insects; then fertilisation in ovule.', 'placeholder', {'label': 'Day 7 summary'}, 'Consolidation.', 'Draw longitudinal flower section.', 'Pollination before fertilisation always.', '', '', []),
])

DAY8 = _build_day(8, [
    ('Pollen tube growth', 'After pollen lands on stigma, pollen tube grows down style carrying male gametes to ovule.', 'placeholder', {'label': 'Pollen tube in style'}, 'Path to egg.', 'Chemotropism guides pollen tube to ovule.', 'Tube nucleus leads path through style tissues.', '', '', []),
    ('Fertilisation in plants', 'Male gamete fuses with egg cell in ovule forming zygote; second male gamete may fuse with polar nuclei (triple fusion).', 'placeholder', {'label': 'Fertilisation in ovule'}, 'Double fertilisation in angiosperms.', 'Zygote becomes embryo; endosperm food tissue forms.', 'Unique to flowering plants — detail as NCERT.', 'Fertilisation occurs inside ovule.', '', []),
    ('Ovule to seed', 'After fertilisation ovule develops into seed containing embryo and stored food (cotyledons/endosperm).', 'placeholder', {'label': 'Ovule → seed'}, 'Seed formation.', 'Bean seed has two cotyledons with stored food.', 'Seed protects embryo in dormant state.', 'Ovule wall becomes seed coat.', '', []),
    ('Ovary to fruit', 'Ovary wall develops into fruit after fertilisation; protects seeds and aids dispersal.', 'placeholder', {'label': 'Ovary → fruit'}, 'Fruit role.', 'Apple flesh is swollen ovary tissue.', 'Fruit formation signals successful reproduction.', 'Fruit not always sweet — dry fruits too.', '', []),
    ('Seed dispersal', 'Seeds spread by wind, water, animals, explosion — reduces competition with parent plant.', 'placeholder', {'label': 'Seed dispersal methods'}, 'Population spread.', 'Maple winged seeds float on wind.', 'Dispersal increases survival chance.', '', '', []),
    ('Germination', 'Seed absorbs water, embryo resumes growth, radicle emerges as root, plumule as shoot.', 'placeholder', {'label': 'Seed germination'}, 'New plant start.', 'Bean seed splits; root goes down first.', 'Needs water, air, suitable temperature.', 'Germination is not fertilisation.', '', ['germination']),
    ('Activity 7.4 — germination conditions', 'Activity 7.4 tests seeds with/without water, air, warmth — identify conditions needed for germination.', 'placeholder', {'label': 'Activity 7.4 — germination'}, 'Experimental design.', "Boiled seed control — dead embryo won't grow.", 'Oxygen needed for respiration in germination.', '', '', []),
    ('Reproduction in plants summary diagram', 'Pollination → pollen tube → fertilisation in ovule → seed + fruit → dispersal → germination.', 'formula_panel', {'formula': 'Pollination → Fertilisation → Seed → Fruit → Germination', 'note': 'Plant sexual cycle'}, 'Flow chart for exams.', 'Draw linear sequence with labels.', 'Include agents at pollination step.', '', '', []),
    ('Hybridisation (brief)', 'Farmers cross pollinate selected plants to combine desirable traits — uses cross-pollination principle.', 'placeholder', {'label': 'Hybridisation in agriculture'}, 'Application.', 'High-yield hybrid maize.', 'Human use of plant reproduction biology.', '', '', []),
    ('Plant fertilisation summary', 'Fertilisation in ovule forms embryo; ovule→seed, ovary→fruit; germination needs water, air, warmth.', 'placeholder', {'label': 'Day 8 summary'}, 'Consolidation.', 'Contrast pollination vs fertilisation.', 'Double fertilisation keyword for angiosperms.', '', '', []),
])

DAY9 = _build_day(9, [
    ('Human male system overview', 'Male reproductive system produces sperm in testes and delivers them through penis.', 'placeholder', {'label': 'Male system overview'}, 'Human reproduction block.', 'Testes in scrotum outside body cavity.', 'Produces sperm and testosterone.', 'Know main organs and functions.', '', []),
    ('Testes — sperm and hormone', 'Testes produce male gametes (sperm) and male sex hormone testosterone.', 'placeholder', {'label': 'Testes — sperm + testosterone'}, 'Primary male gonads.', 'Sperm formed in seminiferous tubules.', 'Lower temperature in scrotum aids sperm formation.', 'Testosterone controls secondary sexual characters.', '', ['testes']),
    ('Scrotum location', 'Testes lie in scrotum outside abdomen — cooler than body core for viable sperm production.', 'placeholder', {'label': 'Scrotum — temperature'}, 'Adaptation reason.', 'Tight clothing excess heat may reduce sperm count temporarily.', 'Sperm production needs ~2–3°C below body.', '', '', []),
    ('Vas deferens and path', 'Sperm pass from testes through vas deferens to urethra; seminal vesicles and prostate add fluid.', 'placeholder', {'label': 'Sperm delivery pathway'}, 'Anatomy sequence.', 'Semen = sperm + gland secretions.', 'Vas deferens stores and transports sperm.', 'Urethra carries urine and semen (not together).', '', []),
    ('Semen composition', 'Semen nourishes and transports sperm; fluid from seminal vesicles, prostate, and other glands.', 'placeholder', {'label': 'Semen — fluid + sperm'}, 'Function not just transport.', 'Provides alkaline medium neutralising vaginal acidity.', 'Sperm are minority volume of semen.', '', '', []),
    ('Penis — delivery', 'Penis delivers semen into female reproductive tract during mating (copulation).', 'placeholder', {'label': 'Penis — copulation'}, 'External organ role.', 'Urethra runs through penis.', 'Delivery organ not gamete producer.', '', '', []),
    ('Puberty in males', 'Puberty: voice deepens, facial hair, broader shoulders — driven by testosterone from testes.', 'placeholder', {'label': 'Male puberty changes'}, 'Secondary sexual characters.', "Adam's apple growth from larynx enlargement.", 'Puberty marks reproductive maturity.', '', '', []),
    ('Sperm structure (basic)', 'Sperm has head (nucleus), middle piece (energy), tail (motility) — adapted for reaching egg.', 'placeholder', {'label': 'Sperm structure'}, 'Cell specialisation.', 'Millions in one ejaculation; one fertilises egg.', 'Haploid nucleus in head.', '', '', []),
    ('Male hygiene and health', 'Keep reproductive organs clean; seek medical help for pain, swelling, or irregular discharge.', 'placeholder', {'label': 'Male reproductive health'}, 'Health awareness.', 'Regular check-ups if problems.', 'Early treatment prevents complications.', '', '', []),
    ('Male system summary', 'Testes → sperm + testosterone; vas deferens, glands, urethra, penis — label diagram and state functions.', 'placeholder', {'label': 'Day 9 summary'}, 'Consolidation.', 'Draw and label male system.', 'Scrotum temperature point is exam favourite.', '', '', []),
])

DAY10 = _build_day(10, [
    ('Female system overview', 'Female system produces eggs in ovaries, nurtures embryo in uterus, and has birth canal (vagina).', 'placeholder', {'label': 'Female system overview'}, 'Parallel to male day.', 'Ovaries alternate egg release roughly monthly.', 'Also produces estrogen and progesterone.', '', '', []),
    ('Ovaries — egg production', 'Ovaries produce female gametes (ova/eggs) and hormones estrogen and progesterone.', 'placeholder', {'label': 'Ovaries — eggs + hormones'}, 'Female gonads.', 'One mature egg released per cycle typically.', 'Girl born with all egg precursors — maturation later.', '', ['ovary']),
    ('Oviduct (Fallopian tube)', 'Oviduct carries egg from ovary to uterus; usual site of fertilisation.', 'placeholder', {'label': 'Oviduct — fertilisation site'}, 'Critical location.', 'Cilia line tube moving egg toward uterus.', 'Blockage can cause infertility.', 'Also called fallopian tube.', '', ['oviduct']),
    ('Uterus — womb', 'Uterus is muscular chamber where embryo implants and grows during pregnancy.', 'placeholder', {'label': 'Uterus — embryo development'}, 'Pregnancy organ.', 'Thick lining (endometrium) each cycle.', 'Strong muscle wall for labour contractions.', '', ['uterus']),
    ('Vagina — birth canal', 'Vagina receives sperm during copulation and serves as birth canal during delivery.', 'placeholder', {'label': 'Vagina — copulation and birth'}, 'External connection.', 'Elastic muscular tube.', 'Part of female external/internal anatomy set.', '', '', []),
    ('Menstrual cycle overview', 'Roughly 28-day cycle: egg matures, uterus lining thickens, if no fertilisation lining breaks down — menstruation.', 'placeholder', {'label': 'Menstrual cycle'}, 'NCERT core process.', 'Period bleeding is lining shedding not egg loss mainly.', 'Cycle regulated by hormones.', 'Menarche starts cycle; menopause ends.', '', ['menstruation']),
    ('Menstruation', 'Menstruation is monthly shedding of uterine lining through vagina when fertilisation does not occur.', 'placeholder', {'label': 'Menstruation defined'}, 'Normal healthy process.', 'Typically 3–7 days bleeding.', 'Not a disease — sign of reproductive maturity.', 'Hygiene and rest during period important.', '', []),
    ('Puberty in females', 'Breast development, wider hips, menstruation begins — estrogen and progesterone driven.', 'placeholder', {'label': 'Female puberty'}, 'Secondary characters.', 'Menarche marks start of menstrual cycles.', 'Timing varies individually — normal range wide.', '', '', []),
    ('Female system diagram', 'Label ovary, oviduct, uterus, cervix, vagina on NCERT diagram; state one function each.', 'placeholder', {'label': 'Female diagram practice'}, 'Exam figure.', 'Side view cut-section common in papers.', 'Cervix is uterus opening to vagina.', '', '', []),
    ('Female system summary', 'Ovaries release egg; fertilisation in oviduct; uterus nurtures embryo; menstruation if no pregnancy.', 'placeholder', {'label': 'Day 10 summary'}, 'Consolidation.', 'Draw cycle timeline with hormone roles brief.', 'Fertilisation site ≠ uterus initially.', '', '', []),
])

DAY11 = _build_day(11, [
    ('Fertilisation in humans', 'Sperm fuses with egg in oviduct forming zygote which begins dividing while moving to uterus.', 'placeholder', {'label': 'Human fertilisation'}, 'Start of pregnancy path.', 'Millions sperm; one reaches egg.', 'Zygote is diploid — 46 chromosomes human.', '', '', []),
    ('Implantation', 'Blastocyst embeds in thickened uterine lining (endometrium) — implantation.', 'placeholder', {'label': 'Implantation in uterus'}, 'Pregnancy establishment.', 'Occurs about week after fertilisation.', 'Without implantation pregnancy cannot continue.', '', '', []),
    ('Embryo and foetus', 'Embryo term early development; foetus after major organs formed — grows in uterus until birth.', 'placeholder', {'label': 'Embryo → foetus'}, 'Development stages.', 'Heartbeat detectable early in pregnancy.', 'Placenta connects mother and embryo.', '', '', []),
    ('Placenta function', 'Placenta provides oxygen, nutrients from mother to embryo and removes wastes; barrier to some not all substances.', 'placeholder', {'label': 'Placenta — exchange organ'}, 'Critical structure.', 'Umbilical cord links embryo to placenta.', 'No direct blood mixing — exchange across membranes.', 'Alcohol and drugs can cross — harm baby.', '', ['placenta']),
    ('Umbilical cord', 'Umbilical cord connects foetus to placenta carrying blood vessels for nutrient and gas exchange.', 'placeholder', {'label': 'Umbilical cord'}, 'Physical link.', 'Cut at birth; scar becomes navel.', 'Two arteries one vein in cord typically.', '', '', []),
    ('Gestation period', 'Human gestation about 9 months (280 days) — full development before birth.', 'placeholder', {'label': 'Gestation ~9 months'}, 'Timeline fact.', 'Trimesters divide pregnancy care stages.', 'Varies slightly individual to individual.', '', '', []),
    ('Birth (parturition)', 'Strong uterine contractions and cervical dilation expel baby; followed by placenta delivery.', 'placeholder', {'label': 'Birth process'}, 'Basic overview.', 'Labour contractions rhythmically increase.', 'Medical assistance reduces risk.', '', '', []),
    ("Mother's health during pregnancy", 'Balanced diet, folic acid, iron, check-ups, avoid alcohol/tobacco/drugs — essential for healthy baby.', 'placeholder', {'label': 'Pregnancy health'}, 'NCERT health emphasis.', "Mother's nutrition affects foetal development.", 'Rubella vaccination before pregnancy ideal.', '', '', []),
    ('Lactation (brief)', 'After birth, mammary glands produce milk — nutrition and immunity for newborn.', 'placeholder', {'label': 'Breastfeeding benefits'}, 'Post-birth care.', 'Colostrum rich in antibodies.', 'Breastfeeding supports infant health.', '', '', []),
    ('Pregnancy summary', 'Fertilisation in oviduct → implantation → placenta exchange → birth; maternal health critical throughout.', 'placeholder', {'label': 'Day 11 summary'}, 'Consolidation.', 'Draw placenta exchange diagram.', 'Placenta is temporary organ.', '', '', []),
])

DAY12 = _build_day(12, [
    ('Reproductive health — definition', 'Reproductive health means physical, emotional, and social well-being in all matters related to reproductive system.', 'placeholder', {'label': 'Reproductive health defined'}, 'WHO-aligned NCERT theme.', 'Access to safe care and information.', 'Not merely absence of disease.', 'Includes informed choice and hygiene.', '', ['reproductive health']),
    ('Adolescence and puberty care', 'Adolescents need balanced diet, exercise, hygiene, and accurate information during puberty changes.', 'placeholder', {'label': 'Adolescent care'}, 'Age-appropriate guidance.', 'Myths about puberty cause anxiety.', 'Talk to trusted adults or doctors.', '', '', []),
    ('Population and family planning', 'Responsible parenthood and family planning help healthy spacing of children and resource planning.', 'placeholder', {'label': 'Family planning'}, 'Social biology angle.', 'Government awareness programmes.', 'Voluntary informed decisions.', '', '', []),
    ('Contraception — purpose', 'Contraception prevents unwanted pregnancy; some methods also reduce STD risk.', 'placeholder', {'label': 'Contraception purpose'}, 'Methods overview day.', 'Couples choose method with medical advice.', 'Does not replace reproductive health education.', '', ['contraception']),
    ('Barrier methods', 'Condoms (male/female) block sperm entry and reduce STD transmission.', 'placeholder', {'label': 'Barrier — condoms'}, 'Dual protection.', 'Only method that greatly reduces many STDs.', 'Must be used correctly each time.', '', '', []),
    ('Chemical methods', 'Oral pills change hormone levels preventing ovulation — prescription and monitoring needed.', 'placeholder', {'label': 'Oral contraceptive pills'}, 'Hormonal method.', 'Doctor advises suitable pill.', 'Does not protect against STDs alone.', '', '', []),
    ('Intrauterine devices (IUD)', 'Copper-T placed in uterus prevents implantation — long-term reversible method with medical insertion.', 'placeholder', {'label': 'Copper-T IUD'}, 'NCERT named device.', 'Inserted by trained health worker.', 'Check-ups ensure proper placement.', '', '', []),
    ('Surgical methods', 'Vasectomy (male) and tubectomy (female) block gamete transport — permanent sterilisation option.', 'placeholder', {'label': 'Surgical contraception'}, 'Permanent choice.', 'Should be voluntary informed adult decision.', 'Difficult to reverse — consider carefully.', '', '', []),
    ('Emergency and myths', 'Avoid unscientific methods; emergency contraception exists but is not regular method; myths cause harm.', 'placeholder', {'label': 'Avoid myths'}, 'Critical thinking.', 'Safe abortion only at licensed medical facilities where legal.', 'Peer misinformation common — verify medically.', '', '', []),
    ('Contraception summary', 'Know barrier, hormonal, IUD, surgical methods; condoms also reduce STD risk; choose with medical guidance.', 'placeholder', {'label': 'Day 12 summary'}, 'Consolidation.', 'Table: method, mechanism, STD protection.', 'No single method suits everyone.', '', '', []),
])

DAY13 = _build_day(13, [
    ('STDs — definition', 'Sexually transmitted diseases spread mainly through sexual contact — bacterial or viral infections.', 'placeholder', {'label': 'STDs defined'}, 'Health education section.', 'HIV/AIDS most discussed in NCERT.', 'Prevention better than cure.', '', ['STD']),
    ('Common STD examples', 'Examples: gonorrhoea, syphilis (bacterial); warts, HIV (viral) — NCERT list.', 'placeholder', {'label': 'STD examples'}, 'Name recognition.', 'Symptoms vary; some silent initially.', 'Early medical treatment essential.', '', '', []),
    ('HIV and AIDS', 'HIV attacks immune system; AIDS is advanced stage with opportunistic infections; no complete cure yet.', 'placeholder', {'label': 'HIV → AIDS'}, 'Major public health topic.', 'Antiretroviral therapy controls HIV.', 'HIV is virus; AIDS is syndrome.', 'Not spread by casual touch or sharing meals.', '', ['HIV', 'AIDS']),
    ('Modes of HIV transmission', 'HIV spreads through infected blood, sexual contact, and mother-to-child (birth/breastfeeding) — not casual contact.', 'placeholder', {'label': 'HIV transmission modes'}, 'Myth busting.', 'Shared needles high risk.', 'Know factual modes for exam.', 'Shaking hands does not transmit HIV.', '', []),
    ('Prevention of STDs', 'Use condoms, limit partners, avoid shared needles, screening, and timely treatment of infections.', 'placeholder', {'label': 'STD prevention'}, 'Action list.', 'Abstinence or safe practices.', 'Vaccination available for some (e.g. HPV) — beyond core NCERT.', '', '', []),
    ('Stigma and testing', 'STD/HIV stigma prevents testing; confidential counselling and testing save lives.', 'placeholder', {'label': 'Reduce stigma'}, 'Social awareness.', 'Support affected individuals.', 'Medical confidentiality important.', '', '', []),
    ('Mother-to-child prevention', 'Medical interventions during pregnancy and delivery reduce HIV transmission from mother to child.', 'placeholder', {'label': 'Prevent vertical transmission'}, 'Applied health.', 'Antiretroviral drugs to mother and baby.', 'Public health programmes exist.', '', '', []),
    ('Adolescent responsibility', 'Delay sexual activity, seek scientific information, respect consent, and protect self and partner health.', 'placeholder', {'label': 'Responsible behaviour'}, 'Values-linked science.', 'Peer pressure vs informed choice.', 'School health programmes help.', '', '', []),
    ('Government programmes', 'Awareness campaigns, free condoms, HIV testing centres, and adolescent health clinics.', 'placeholder', {'label': 'Public health programmes'}, 'Civic link.', 'NACO and related initiatives in India.', 'Know prevention is collective effort.', '', '', []),
    ('STD day summary', 'STDs preventable; HIV factual modes; condoms help; no stigma; seek medical help early.', 'placeholder', {'label': 'Day 13 summary'}, 'Consolidation.', 'List prevention methods without myths.', 'HIV vs AIDS distinction required.', '', '', []),
])

DAY14 = _build_day(14, [
    ('Activity 7.1 — yeast budding recap', 'Observe yeast budding; sugar provides energy; reproduction via bud formation.', 'placeholder', {'label': 'Activity 7.1 recap'}, 'Asexual lab.', 'Write aim, material, observation, conclusion.', 'Distinguish budding from fission.', '', '', []),
    ('Activity 7.2 — Rhizopus spores recap', 'Bread mould shows hyphae and sporangia; spores airborne; asexual reproduction.', 'placeholder', {'label': 'Activity 7.2 recap'}, 'Fungal spores.', 'Black dots are sporangia on hyphae.', 'Keep bread moist covered for growth.', '', '', []),
    ('Activity 7.3 — flower dissection recap', 'Identify stamen, pistil, anther, ovary; relate to pollination and fertilisation.', 'placeholder', {'label': 'Activity 7.3 recap'}, 'Plant structure lab.', 'Longitudinal section diagram from dissection.', 'Link parts to gamete location.', '', '', []),
    ('Activity 7.4 — germination recap', 'Seeds need water, oxygen, suitable temperature; boiled seed control fails to germinate.', 'placeholder', {'label': 'Activity 7.4 recap'}, 'Conditions experiment.', 'Variable one factor at a time.', 'Germination vs growth later in soil.', '', '', []),
    ('Match organism to reproduction mode', 'Drill: Amoeba-fission, Hydra-budding, Spirogyra-fragmentation, Rhizopus-spores, Yeast-budding.', 'placeholder', {'label': 'Organism-mode matching'}, 'Exam drill.', 'Flashcards both directions.', 'NCERT named organisms only.', '', '', []),
    ('Pollination vs fertilisation written', 'Practice distinguishing: pollen to stigma vs gamete fusion in ovule.', 'placeholder', {'label': 'Pollination vs fertilisation'}, 'Common confusion fix.', 'Two sentences each with example.', 'Order: pollination first.', '', '', []),
    ('Human reproductive pathway', 'Trace sperm path and egg path; mark fertilisation site and implantation site.', 'placeholder', {'label': 'Human pathway trace'}, 'Integration exercise.', 'Label diagram without textbook.', 'Urethra vs oviduct — different systems.', '', '', []),
    ('NCERT intext Ch 7 review', 'Answer intext questions on DNA copying, modes of reproduction, placenta, contraception.', 'placeholder', {'label': 'NCERT intext Ch 7'}, 'Textbook checkpoint.', 'Self-test closed book.', 'Intext mirrors board style.', '', '', []),
    ('Comparison table practice', 'Asexual vs sexual; self vs cross pollination; internal vs external fertilisation.', 'placeholder', {'label': 'Comparison tables Ch 7'}, 'Written prep.', 'Three tables from memory.', 'At least three differences each.', '', '', []),
    ('Activities 7.1–7.4 summary', 'Four activities cover asexual observation, spores, flower anatomy, germination — know conclusions.', 'placeholder', {'label': 'Activities block summary'}, 'Day 14 consolidation.', 'One paragraph per activity.', 'Activities support diagram questions.', '', '', []),
])

DAY15 = _build_day(15, [
    ('Activity 7.5 — reproduction health discussion', 'Discuss adolescent changes, hygiene, and myths; link to NCERT reproductive health section.', 'placeholder', {'label': 'Activity 7.5 recap'}, 'Discussion activity.', 'Scientific attitude toward puberty.', 'Counselor or teacher guided.', '', '', []),
    ('Activity 7.6 — contraceptive awareness', 'Collect information on contraceptive methods from reliable health sources — compare mechanisms.', 'placeholder', {'label': 'Activity 7.6 recap'}, 'Research activity.', 'Poster or table presentation.', 'Emphasise medical reliability of sources.', '', '', []),
    ('Activity 7.7 — STD awareness', 'Prepare awareness material on STD/HIV prevention — factual modes of transmission.', 'placeholder', {'label': 'Activity 7.7 recap'}, 'Health campaign style.', 'Correct myths in community.', 'Confidential testing information.', '', '', []),
    ('5-mark: Asexual modes with examples', 'Describe fission, budding, fragmentation, regeneration, spore formation with NCERT organism each.', 'placeholder', {'label': '5-mark asexual modes'}, 'Long answer practice.', 'Intro + five modes + examples + conclusion.', 'Diagram optional per mode.', '', '', []),
    ('5-mark: Human female system', 'Draw diagram; explain menstruation cycle; role of ovary and uterus.', 'placeholder', {'label': '5-mark female system'}, 'Long answer.', 'Hormone names add credit.', 'Menstruation not shameful — health view.', '', '', []),
    ('5-mark: Plant reproduction sequence', 'Explain pollination, fertilisation, seed and fruit formation with diagram.', 'placeholder', {'label': '5-mark plant reproduction'}, 'Plant long Q.', 'Label anther, stigma, ovule.', 'Agents of pollination included.', '', '', []),
    ('Diagram: flower L.S. and germination', 'Practice flower longitudinal section and seed germination sequence diagrams.', 'placeholder', {'label': 'Diagram drill Ch 7'}, 'Visual exam prep.', 'Timed 10 minutes both.', 'Neat labels with leader lines.', '', '', []),
    ('Previous year Ch 7 themes', 'Recurring: reproduction modes table, placenta function, contraceptive methods, HIV prevention.', 'placeholder', {'label': 'Board themes Ch 7'}, 'Strategic review.', 'Solve 5 PYQs timed.', 'Health questions increasing in boards.', '', '', []),
    ('Ethical and social dimensions', 'Write short notes on responsible parenthood, gender respect, and access to health services.', 'placeholder', {'label': 'Social-ethical notes'}, 'Holistic NCERT.', 'Science plus social responsibility.', 'Value-based questions use this.', '', '', []),
    ('Extended review summary', 'Activities 7.5–7.7 plus long answers and diagrams — complete Ch 7 written preparation.', 'placeholder', {'label': 'Day 15 summary'}, 'Consolidation.', 'Checklist tick all activities.', 'Ready for exam complete day.', '', '', []),
])

DAY16 = _build_day(16, [
    ('Ch 7 key terms set 1', 'Reproduction, DNA copying, variation, gamete, zygote, fertilisation, embryo, asexual, sexual.', 'placeholder', {'label': 'Key terms Ch 7 set 1'}, 'Flashcard drill.', 'Define in one line each.', 'Cover and recall.', '', '', []),
    ('Ch 7 key terms set 2', 'Binary fission, budding, fragmentation, regeneration, spore, pollination, stigma, anther, ovule, seed.', 'placeholder', {'label': 'Key terms set 2'}, 'Continued drill.', 'Match term to example organism/structure.', 'Second set of ten.', '', '', []),
    ('Ch 7 key terms set 3', 'Testes, ovary, oviduct, uterus, placenta, menstruation, contraception, STD, HIV, vasectomy.', 'placeholder', {'label': 'Key terms set 3'}, 'Human health terms.', 'Spelling matters in boards.', 'Third set completes unit vocabulary.', '', '', []),
    ('Top comparisons Ch 7', 'Asexual vs sexual; self vs cross pollination; pollination vs fertilisation; embryo vs foetus; HIV vs AIDS.', 'placeholder', {'label': 'Top comparisons unit 3'}, 'Revision tables.', 'One table per pair.', 'High-frequency compare questions.', '', '', []),
    ('Must-draw diagrams Ch 7', 'Flower L.S., human male, human female, Rhizopus, yeast budding, germination stages.', 'placeholder', {'label': 'Must-draw six diagrams'}, 'Final visual check.', 'Redraw without notes.', 'Allocate practice time per figure.', '', '', []),
    ('Must-know activities 7.1–7.7', 'List aim and conclusion for all seven activities — NCERT box questions often activity-based.', 'placeholder', {'label': 'All activities recall'}, 'Activity master list.', '7.1 yeast; 7.2 mould; 7.3 flower; 7.4 germination; 7.5–7.7 health.', 'Conclusion one sentence each.', '', '', []),
    ('Common mistakes Ch 7', 'Calling pollination fertilisation; saying HIV spreads by touch; forgetting placenta exchange role.', 'placeholder', {'label': 'Avoid mistakes Ch 7'}, 'Error correction.', 'Review your wrong MCQs.', 'Fix before practice stage.', '', '', []),
    ('15-minute mixed quiz Ch 7', 'Mix modes, flower parts, human organs, health methods — timed recall.', 'placeholder', {'label': 'Mixed quiz unit 3'}, 'Pre-MCQ stage.', 'Use before Stage 2 days.', 'Identify weak day topic.', '', '', []),
    ('NCERT Ch 7 summary review', 'Re-read chapter summary; verify every bullet has corresponding concept card.', 'placeholder', {'label': 'NCERT summary Ch 7'}, 'Textbook closure.', 'Summary bullets = exam blueprint.', 'Tick 160/160 cards covered.', '', '', []),
    ('Unit 3 complete', 'Unit 3 How do Organisms Reproduce complete — 160 concept cards; proceed to Practice when unlocked.', 'placeholder', {'label': 'Unit 3 complete — 160 cards'}, 'Completion card.', 'Next unit: Heredity Ch 8.', 'Concepts done → practice → NCERT MCQs.', '', '', []),
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
    16: lambda: DAY16
}

DAY_TITLES = {
    1: "Why Reproduce and DNA Copying",
    2: "Variation and Its Significance",
    3: "Asexual Reproduction — Binary Fission",
    4: "Fragmentation, Regeneration and Budding",
    5: "Vegetative Propagation and Spores",
    6: "Sexual Reproduction — Introduction",
    7: "Flower Structure and Pollination",
    8: "Fertilisation and Seed Formation in Plants",
    9: "Male Reproductive System",
    10: "Female Reproductive System and Menstruation",
    11: "Pregnancy and Development",
    12: "Reproductive Health and Contraception",
    13: "Sexually Transmitted Diseases (STDs)",
    14: "Activities 7.1–7.4 Review",
    15: "Activities 7.5–7.7 and Extended Review",
    16: "Exam Complete — Unit 3"
}
