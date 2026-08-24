"""Full concept card content for Harshit Biology Unit 4 — Days 1–16 (Ch 8 Heredity)."""

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
                f"u4_d{day}_c{i:02d}",
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
    ('What is heredity?', 'Heredity is the transmission of traits from parents to offspring through genetic information in DNA.', 'placeholder', {'label': 'Heredity defined'}, 'NCERT Ch 8 opening.', 'Children resemble parents in eye colour and blood group.', 'Offspring inherit instructions from both parents in sexual reproduction.', 'Heredity is not same as growth alone.', '', ['heredity']),
    ('Inherited traits examples', 'Traits like eye colour, hair texture, earlobe attachment, and blood group pass from parents to children.', 'placeholder', {'label': 'Inherited trait examples'}, 'Relatable instances.', 'Free vs attached earlobe varies in family.', 'Observable traits have genetic basis.', 'Not all resemblance is genetic — learned behaviour differs.', '', []),
    ('Acquired vs inherited (recap)', 'Inherited traits are in DNA at birth; acquired traits develop during life and are not passed genetically.', 'placeholder', {'label': 'Inherited vs acquired recap'}, 'Ch 7–8 bridge.', 'NCERT mice tail-cutting experiment shows acquired not inherited.', 'Only germ cell DNA changes affect offspring.', 'Weight from overeating is not inherited trait.', '', []),
    ('Rules of heredity — historical question', 'For centuries people wondered if traits blend in offspring or pass as discrete units — Mendel answered with experiments.', 'placeholder', {'label': 'Historical heredity question'}, 'Mendel intro context.', 'Children are not exact average of parents.', 'Discrete traits follow patterns Mendel found.', '', '', []),
    ('Gregor Mendel', 'Gregor Mendel, Austrian monk, used pea plants in garden experiments to discover laws of inheritance.', 'placeholder', {'label': 'Gregor Mendel'}, 'Founder of genetics.', 'Pea plants easy to grow; many visible traits.', '1860s work rediscovered later.', 'Called father of genetics.', '', ['Gregor Mendel']),
    ('Why pea plants?', 'Pea plants self-pollinate, grow fast, have contrasting traits (tall/dwarf, green/yellow seeds) easy to count.', 'placeholder', {'label': 'Why Mendel chose peas'}, 'Experimental design.', 'Pure breeding lines available.', 'Short generation time.', 'Many offspring per cross.', '', []),
    ('Contrasting characters in pea', 'Mendel studied seven pairs: tall/dwarf, round/wrinkled seed, yellow/green seed, etc.', 'placeholder', {'label': 'Seven pea character pairs'}, 'Vocabulary for crosses.', 'Round yellow seeds vs wrinkled green.', 'Each trait had two clear forms.', 'Know at least four pairs for exam.', '', []),
    ('Gene and allele preview', 'Gene controls a trait; alleles are different forms of a gene (e.g. tall allele vs dwarf allele).', 'placeholder', {'label': 'Gene and allele intro'}, 'Terminology for crosses.', 'T and t represent tall and dwarf alleles.', 'Offspring gets one allele from each parent.', 'Uppercase often dominant — formal day later.', '', ['gene', 'allele']),
    ('Sexual reproduction and heredity', 'Two parents each contribute one allele per gene — offspring has new combination.', 'placeholder', {'label': 'Two parents → combination'}, 'Mechanism link Ch 7.', 'Human has 23 chromosome pairs — one set from each parent.', 'Meiosis halves chromosome number in gametes.', '', '', []),
    ('Chapter 8 roadmap', "Ch 8 covers Mendel's experiments, monohybrid and dihybrid crosses, sex determination, blood groups, and Activities 8.1–8.2.", 'placeholder', {'label': 'Ch 8 roadmap — 16 days'}, 'Unit orientation.', 'Punnett squares feature heavily.', 'Connect to variation from Ch 7.', '', '', []),
])

DAY2 = _build_day(2, [
    ('Accumulation of variations', 'Variations accumulate over generations through sexual reproduction and occasional DNA changes.', 'placeholder', {'label': 'Variation accumulation'}, 'NCERT Ch 8 theme.', 'Populations show range of heights, not one value.', 'Sexual shuffling adds new combos each generation.', 'Evolution acts on accumulated variation.', '', []),
    ('Importance for species survival', 'Species with accumulated variation has better chance some individuals survive environmental change.', 'placeholder', {'label': 'Variation aids survival'}, 'Selection logic.', 'Disease-resistant crop variant saved harvest.', 'Without variation, one stress kills all.', 'Links Ch 7 variation to Ch 8 heredity.', '', []),
    ('Sexual reproduction and new combinations', 'Each generation gets new allele combinations unlike either parent exactly — except identical twins.', 'placeholder', {'label': 'New gene combinations'}, 'Mechanism.', 'Sibling differences illustrate recombination.', 'Independent assortment increases diversity.', '', '', []),
    ('Population vs individual', 'Heredity studied at individual level (parent-offspring); variation important at population level.', 'placeholder', {'label': 'Individual heredity vs population variation'}, 'Scale distinction.', 'Breeding programmes select from population variation.', 'Both levels needed for full picture.', '', '', []),
    ('Stable vs changing environment', 'Stable environment favours current traits; changing environment favours previously rare beneficial variants.', 'placeholder', {'label': 'Environment selects variants'}, 'Evolution preview.', 'Antibiotic resistance rises when antibiotics used.', 'Variation alone insufficient — selection acts.', '', '', []),
    ('DNA copying errors in inheritance', 'Rare copying errors in gamete formation create new alleles passed to offspring if fertilisation occurs.', 'placeholder', {'label': 'Mutation in gametes'}, 'Source of new variation.', 'Most mutations neutral or harmful; few beneficial.', 'Somatic mutations not inherited.', '', '', []),
    ('Breeding and artificial selection', 'Humans select plants/animals with desired variants to breed — uses heredity and variation principles.', 'placeholder', {'label': 'Artificial selection'}, 'Applied genetics.', 'High-yield wheat from selected grains.', 'Same logic as natural selection but human directed.', '', '', []),
    ('Limitations of inherited information', 'Environment also affects expression — same genotype can differ in phenotype (nutrition affects height).', 'placeholder', {'label': 'Genotype + environment'}, 'Nature and nurture.', 'Identical twins may differ slightly in weight.', 'Heredity sets potential; environment affects outcome.', '', '', []),
    ('NCERT exercise link — variation', 'Review NCERT questions linking variation in reproduction to survival of species.', 'placeholder', {'label': 'NCERT variation questions'}, 'Textbook alignment.', 'Answer why variation is beneficial.', 'Short 3-mark style practice.', '', '', []),
    ('Variation accumulation summary', 'Sexual reproduction shuffles and accumulates variations; populations with diversity survive change better.', 'placeholder', {'label': 'Day 2 summary unit 4'}, 'Consolidation.', 'Link Ch 7 DNA copying to Ch 8 patterns.', 'Variation + heredity = evolution foundation.', '', '', []),
])

DAY3 = _build_day(3, [
    ("Mendel's monohybrid experiment", 'Mendel crossed pea plants differing in one trait (e.g. tall × dwarf) and tracked offspring traits.', 'placeholder', {'label': 'Monohybrid cross experiment'}, 'Experimental method.', 'P generation pure lines; F1 all tall in classic cross.', 'Counted thousands of plants for ratios.', 'One trait at a time — monohybrid.', '', ['monohybrid cross']),
    ('P generation', 'P (parental) generation uses pure breeding homozygous plants — tall × tall always tall before cross.', 'placeholder', {'label': 'P generation pure lines'}, 'Starting lines.', 'True-breeding tall and dwarf peas.', 'Homozygous: same alleles for trait.', '', '', []),
    ('F1 generation result', 'F1 offspring of tall × dwarf cross were all tall — dwarf seemed to disappear.', 'placeholder', {'label': 'F1 all tall'}, 'First surprise result.', 'F1 uniformly showed dominant trait.', 'Dwarf trait not lost — hidden.', 'Cross between contrasting P parents.', '', ['F1 generation']),
    ('F2 generation result', 'F1 self-pollinated → F2 showed both tall and dwarf in approximately 3:1 ratio.', 'formula_panel', {'formula': 'F2 ratio ≈ 3 tall : 1 dwarf', 'note': 'Monohybrid F2'}, "Mendel's key numerical finding.", 'Counted 787 tall : 277 dwarf ≈ 3:1.', 'Hidden dwarf reappeared in F2.', 'Large sample gave statistical ratio.', '', ['F2 generation']),
    ('Law of Dominance', 'When two contrasting alleles combine, one (dominant) expresses in F1; other (recessive) hidden but can return in F2.', 'placeholder', {'label': 'Law of Dominance'}, 'First Mendel law.', 'Tall allele T dominant over t.', "Dominant not 'stronger' — expression pattern.", 'Recessive needs two copies to show.', '', ['dominant', 'recessive']),
    ('Law of Segregation', 'Alleles separate during gamete formation so each gamete carries only one allele per gene.', 'placeholder', {'label': 'Law of Segregation'}, 'Second Mendel law.', 'Tt plant makes T and t gametes in equal proportion.', 'Also called purity of gametes.', 'Segregation happens in meiosis.', '', ['segregation']),
    ('Activity 8.1 — monohybrid cross simulation', 'Activity 8.1 uses beads/cards to simulate allele combinations showing 3:1 F2 ratio.', 'placeholder', {'label': 'Activity 8.1 — monohybrid sim'}, 'Hands-on ratio proof.', 'Random pick two alleles mimics fertilisation.', 'Repeat many trials — ratio approaches 3:1.', '', '', []),
    ("Mendel's method strength", 'Large sample size, one variable at a time, mathematical counting, pure lines — scientific rigour.', 'placeholder', {'label': "Mendel's scientific method"}, 'Why his work succeeded.', 'Statistics revealed patterns others missed.', 'Controlled crosses in monastery garden.', '', '', []),
    ('Terminology checkpoint', 'Define: allele, dominant, recessive, homozygous, heterozygous, genotype, phenotype — formal day next.', 'placeholder', {'label': 'Terminology preview'}, 'Prep for Day 5.', 'Tt is heterozygous tall phenotype.', 'TT and Tt both tall phenotype.', '', '', []),
    ('Mendel rules summary', 'Dominance explains F1 uniformity; segregation explains F2 3:1 ratio; gametes carry one allele each.', 'placeholder', {'label': 'Day 3 summary unit 4'}, 'Consolidation.', 'State both laws with pea example.', 'Activity 8.1 reinforces ratios.', '', '', []),
])

DAY4 = _build_day(4, [
    ('Punnett square — purpose', 'Punnett square diagram predicts offspring genotypes and phenotypes from parent gametes.', 'placeholder', {'label': 'Punnett square tool'}, 'Problem-solving skill.', '2×2 grid for monohybrid cross.', 'Combine gametes systematically.', 'Named after Reginald Punnett.', '', ['Punnett square']),
    ('Gamete formation for Tt', 'Heterozygous Tt produces 50% T gametes and 50% t gametes — segregation.', 'placeholder', {'label': 'Gametes from Tt'}, 'Half-half rule.', 'Write T and t on one parent side of square.', 'Each gamete one allele only.', '', '', []),
    ('Cross Tt × Tt', 'Both parents heterozygous tall: gametes T and t each; offspring TT, Tt, tT, tt.', 'formula_panel', {'formula': 'Tt × Tt → TT : Tt : tt = 1 : 2 : 1', 'note': 'Genotype ratio'}, 'Standard cross.', 'Phenotype 3 tall : 1 dwarf.', 'Genotype ratio differs from phenotype ratio.', '', []),
    ('Genotype vs phenotype', 'Genotype is genetic makeup (TT, Tt, tt); phenotype is observable trait (tall or dwarf).', 'placeholder', {'label': 'Genotype vs phenotype'}, 'Essential distinction.', 'Tt and TT both tall phenotype.', 'Same phenotype can differ genotype.', 'Blood group phenotype from genotype.', '', ['genotype', 'phenotype']),
    ('Homozygous vs heterozygous', 'Homozygous: same alleles (TT or tt). Heterozygous: different alleles (Tt).', 'placeholder', {'label': 'Homozygous vs heterozygous'}, 'Genotype classes.', 'TT homozygous dominant; tt homozygous recessive.', 'Tt heterozygous carries recessive hidden.', '', '', []),
    ('Test cross (brief)', 'Cross unknown dominant with homozygous recessive — if any recessive offspring, unknown was heterozygous.', 'placeholder', {'label': 'Test cross idea'}, 'Breeding diagnostic.', 'T? × tt — dwarf offspring means Tt parent.', 'Used to find hidden genotype.', '', '', []),
    ('Probability interpretation', '3:1 ratio is probabilistic — small families may not match exactly; large numbers approach ratio.', 'placeholder', {'label': 'Ratio as probability'}, 'Statistics concept.', 'Coin toss analogy — fair expectation.', 'Each offspring independent event.', '', '', []),
    ('Monohybrid cross problems', 'Practice: cross TT×tt, Tt×tt, tt×tt — write genotype and phenotype ratios each.', 'placeholder', {'label': 'Monohybrid problem drill'}, 'Exam skill.', 'Show Punnett square in answer.', 'Label parent genotypes and gametes.', '', '', []),
    ('Human monohybrid examples', "Some traits simplified as monohybrid for teaching — earlobe attachment, widow's peak (simplified models).", 'placeholder', {'label': 'Human trait examples'}, 'Application note.', 'Real human genetics often more complex.', 'Use for Punnett practice only.', '', '', []),
    ('Monohybrid summary', 'Draw Punnett square; gametes on axes; read off 1:2:1 genotype and 3:1 phenotype for Tt×Tt.', 'placeholder', {'label': 'Day 4 summary unit 4'}, 'Consolidation.', 'Ten practice crosses without notes.', 'Dominant allele capital letter convention.', '', '', []),
])

DAY5 = _build_day(5, [
    ('Dominant allele expression', 'Dominant allele expresses its trait in phenotype when at least one copy present (TT or Tt).', 'placeholder', {'label': 'Dominant expression rule'}, 'Formal dominance.', 'Tall T dominates dwarf t.', 'Capital letter denotes dominant convention.', 'Dominant does not mean more common in population.', '', ['dominant']),
    ('Recessive allele expression', 'Recessive allele shows phenotype only when two copies present (homozygous recessive tt).', 'placeholder', {'label': 'Recessive needs two copies'}, 'Hidden in heterozygote.', 'Dwarf pea needs tt genotype.', 'Carrier heterozygote Tt looks tall.', 'Recessive traits can skip generations.', '', ['recessive']),
    ('F1 uniform phenotype explained', 'F1 all tall because T from one parent dominates t from other — every F1 is Tt.', 'placeholder', {'label': 'Why F1 all same'}, 'Dominance application.', 'TT × tt → all Tt tall.', 'Recessive phenotype absent in F1.', '', '', []),
    ('F2 separation explained', 'F1 Tt self-cross: gametes combine giving TT, Tt, tt in 1:2:1 — tt shows dwarf again.', 'placeholder', {'label': 'Why F2 shows 3:1'}, 'Segregation application.', 'Recessive reappears when two t gametes meet.', 'Mathematical Mendel discovery.', '', '', []),
    ('Carrier concept', 'Heterozygous individual carries recessive allele without showing trait — called carrier.', 'placeholder', {'label': 'Carrier heterozygote'}, 'Human genetics relevance.', 'Carrier of recessive disease allele healthy but can pass allele.', 'Important in genetic counselling.', '', '', []),
    ('Pure vs hybrid (Mendel terms)', 'Pure breeding = homozygous; hybrid = heterozygous F1 from contrasting parents.', 'placeholder', {'label': 'Pure vs hybrid'}, 'Historical terms.', 'Hybrid vigour different concept — optional.', "Mendel's 'hybrid' means heterozygous.", '', '', []),
    ('Pedigree preview', 'Family tree diagrams track traits across generations — recessive can appear from carrier parents.', 'placeholder', {'label': 'Pedigree intro'}, 'Visual tool.', 'Squares male, circles female in standard pedigree.', 'Filled symbol means affected phenotype.', '', '', []),
    ('Why ratios matter', 'Predicting ratios helps plant breeding and understanding genetic disease inheritance patterns.', 'placeholder', {'label': 'Practical ratio use'}, 'Application.', 'Expect 25% homozygous recessive from carrier × carrier.', 'Medical genetics uses same logic.', '', '', []),
    ('Common dominance misconceptions', 'Dominant ≠ better or more common; recessive ≠ absent from population; one allele from each parent always.', 'placeholder', {'label': 'Fix dominance myths'}, 'Error prevention.', 'Recessive traits persist in carriers.', 'Two dominant alleles possible (TT).', '', '', []),
    ('F1 F2 summary', 'F1 heterozygous shows dominant; F2 self-cross restores recessive in 1/4 — dominance + segregation together.', 'placeholder', {'label': 'Day 5 summary unit 4'}, 'Consolidation.', 'Explain F1 and F2 without memorising only ratio.', 'Write paragraph answer for board.', '', '', []),
])

DAY6 = _build_day(6, [
    ('Dihybrid cross — definition', 'Dihybrid cross tracks inheritance of two traits simultaneously (e.g. seed shape and colour).', 'placeholder', {'label': 'Dihybrid cross defined'}, 'Two genes at once.', 'Round yellow × wrinkled green peas.', 'Each trait has own allele pair.', '', ['dihybrid cross']),
    ('Mendel dihybrid experiment', 'Mendel crossed round yellow (RRYY) with wrinkled green (rryy); F1 all round yellow.', 'placeholder', {'label': 'Mendel dihybrid P and F1'}, 'Classic starting cross.', 'F1 RrYy heterozygous both traits.', 'Both dominant traits in F1.', '', '', []),
    ('F2 dihybrid ratio', 'F2 showed 9:3:3:1 phenotype ratio — round-yellow, round-green, wrinkled-yellow, wrinkled-green.', 'formula_panel', {'formula': 'F2 phenotypes = 9 : 3 : 3 : 1', 'note': 'Dihybrid classic ratio'}, 'Second Mendel numerical law.', '9/16 round yellow dominant both.', 'New combinations 3+3 in middle terms.', '', []),
    ('Law of Independent Assortment', 'Genes for different traits assort independently during gamete formation if on different chromosome pairs.', 'placeholder', {'label': 'Independent Assortment'}, 'Third Mendel law.', 'R/r assortment independent of Y/y.', 'Produces new trait combinations in F2.', 'Exception: linked genes on same chromosome — beyond basic.', '', ['independent assortment']),
    ('Dihybrid Punnett square', '16-box Punnett square for RrYy × RrYy — track both allele pairs together.', 'placeholder', {'label': '4×4 Punnett square'}, 'Exam skill advanced.', 'Gametes: RY, Ry, rY, ry from each parent.', 'Systematic filling avoids errors.', '', '', []),
    ('Gamete types from RrYy', 'Heterozygous dihybrid produces four gamete types in equal proportion: RY, Ry, rY, ry.', 'placeholder', {'label': 'Four gamete types'}, 'Independent assortment result.', 'Each gamete one allele per gene.', '2^n gamete types for n heterozygous gene pairs.', '', '', []),
    ('Why 9:3:3:1', '9 = both dominant; 3 = one dominant one recessive each way; 1 = both recessive.', 'placeholder', {'label': 'Ratio breakdown'}, 'Interpretation skill.', '(3:1) × (3:1) = 9:3:3:1 mathematically.', 'Product of two monohybrid ratios.', '', '', []),
    ('Activity 8.2 — dihybrid simulation', 'Activity 8.2 simulates dihybrid cross with beads showing approach to 9:3:3:1.', 'placeholder', {'label': 'Activity 8.2 — dihybrid sim'}, 'NCERT activity.', 'More trials → closer to expected ratio.', 'Pair with Activity 8.1 monohybrid.', '', '', []),
    ('Dihybrid problem strategy', 'Step 1: identify parent genotypes. Step 2: list gametes. Step 3: Punnett square. Step 4: count phenotypes.', 'placeholder', {'label': 'Dihybrid problem steps'}, 'Exam method.', 'Show work for partial credit.', 'Check arithmetic twice.', '', '', []),
    ('Dihybrid summary', 'Independent assortment gives F2 9:3:3:1; four gamete types from RrYy; practice 16-box square.', 'placeholder', {'label': 'Day 6 summary unit 4'}, 'Consolidation.', 'One full dihybrid problem timed.', 'Three Mendel laws complete set.', '', '', []),
])

DAY7 = _build_day(7, [
    ('Sex determination — need', 'Mechanism decides whether offspring develops as male or female — species-specific.', 'placeholder', {'label': 'Sex determination defined'}, 'NCERT human focus.', 'Humans XY system.', 'Not same in all organisms.', 'Separate from general body traits inheritance.', '', ['sex determination']),
    ('Human chromosomes', 'Humans have 23 pairs chromosomes — 22 autosome pairs + 1 sex chromosome pair.', 'placeholder', {'label': '23 pairs chromosomes'}, 'Chromosome set fact.', 'Karyotype shows 46 chromosomes.', 'Sex chromosomes are pair 23.', '', '', []),
    ('XX female, XY male', 'Females have XX sex chromosomes; males have XY — male determines sex of child via gamete.', 'formula_panel', {'formula': 'Female XX | Male XY', 'note': 'Human sex chromosomes'}, 'Core human pattern.', 'Mother always contributes X.', 'Father contributes X or Y.', "Sex of baby depends on father's sperm.", '', []),
    ('Gametes and sex chromosomes', 'All egg cells have X chromosome; sperm half carry X and half carry Y.', 'placeholder', {'label': 'Eggs X; sperm X or Y'}, '50-50 mechanism.', 'XX egg + X sperm → girl; XX egg + Y sperm → boy.', 'Roughly 50:50 sex ratio in population.', '', '', []),
    ("Sex determination is not 'blame'", 'Biology shows sex determined at fertilisation by chromosome combination — avoid social misconceptions.', 'placeholder', {'label': 'Scientific view sex determination'}, 'NCERT social note.', 'Only one parent contributes Y for male offspring.', 'Educational campaigns use chromosome facts.', '', '', []),
    ('Other species examples', 'Birds often ZW female ZZ male; some reptiles temperature-dependent — contrast with humans.', 'placeholder', {'label': 'Other sex systems brief'}, 'Breadth note.', 'Human XY is one system among many.', 'Exam usually human XY only.', '', '', []),
    ('Sex linked preview', 'Genes on X chromosome (e.g. colour blindness) show different inheritance patterns — related topic.', 'placeholder', {'label': 'Sex-linked preview'}, 'Extension.', 'Males XY have one X — express X recessive more.', 'Colour blindness more common males.', '', '', []),
    ('Punnett for sex determination', 'Cross XX × XY on Punnett square gives 50% XX and 50% XY offspring.', 'placeholder', {'label': 'Sex Punnett square'}, 'Simple grid.', 'Not using T/t — use X and Y symbols.', 'No YY viable human — not standard cross.', '', '', []),
    ('Misconceptions', "Mother does not 'decide' baby sex in XY system; Y chromosome from father makes male development pathway.", 'placeholder', {'label': 'Sex determination myths'}, 'Myth busting.', 'Equal probability each pregnancy.', 'Old folk beliefs lack chromosome basis.', '', '', []),
    ('Sex determination summary', 'Human female XX, male XY; sperm X or Y decides; Punnett shows 1:1; know chromosome pair count.', 'placeholder', {'label': 'Day 7 summary unit 4'}, 'Consolidation.', 'Draw karyotype sketch XX and XY.', 'Autosomes vs sex chromosomes.', '', '', []),
])

DAY8 = _build_day(8, [
    ('ABO blood groups', 'Human ABO blood group controlled by gene with alleles Iᴬ, Iᴮ, and i — inherited trait.', 'placeholder', {'label': 'ABO blood groups'}, 'Applied heredity.', 'Type A, B, AB, O phenotypes.', 'Multiple alleles for one gene.', 'Not simple single dominant only.', '', ['blood group']),
    ('Multiple alleles', 'More than two alleles exist for a gene in population though individual has only two.', 'placeholder', {'label': 'Multiple alleles'}, 'ABO illustration.', 'Iᴬ and Iᴮ codominant; i recessive.', 'You inherit one allele from each parent.', '', '', []),
    ('Codominance in AB', 'Blood group AB shows both A and B antigens — codominance of Iᴬ and Iᴮ.', 'placeholder', {'label': 'Codominance AB group'}, 'Not same as blending.', 'AB has neither A nor B dominant over other.', 'Both expressed on RBC surface.', '', ['codominance']),
    ('Genotype to phenotype ABO', 'IᴬIᴬ or Iᴬi → type A; IᴮIᴮ or Iᴮi → type B; IᴬIᴮ → AB; ii → type O.', 'formula_panel', {'formula': 'Iᴬ, Iᴮ dominant over i', 'note': 'ABO genotypes'}, 'Table to memorise.', 'Type O is universal donor (RBC) simplified teaching.', 'Know parent cross predicts child possibilities.', '', []),
    ('Blood transfusion compatibility', 'Transfusion needs compatible blood groups to avoid clumping — ABO antigen-antibody reaction.', 'placeholder', {'label': 'Transfusion compatibility'}, 'Health application.', 'Wrong group transfusion dangerous.', 'O donors often universal; AB receivers often universal.', 'Rh factor adds another layer.', '', []),
    ('Rh factor (brief)', 'Rh protein on RBC — Rh+ or Rh− inherited separately from ABO.', 'placeholder', {'label': 'Rh factor intro'}, 'Second blood system.', 'Rh incompatibility in pregnancy managed medically.', 'Positive has Rh protein; negative lacks.', '', '', []),
    ('Blood group inheritance problems', 'Practice cross: Iᴬi × Iᴮi — possible offspring genotypes and phenotypes with Punnett square.', 'placeholder', {'label': 'ABO Punnett practice'}, 'Exam application.', 'Child type O from two type A possible if both Iᴬi.', 'Show working for medical genetics style Q.', '', '', []),
    ('Ethical note — blood donation', 'Voluntary blood donation saves lives; know your group; science enables safe matching.', 'placeholder', {'label': 'Blood donation awareness'}, 'Civic science.', 'Blood camps in schools and communities.', 'Inherited trait has social use.', '', '', []),
    ('Blood group vs Mendel pea', 'ABO shows codominance and multiple alleles — extends basic dominant/recessive pea model.', 'placeholder', {'label': 'Beyond simple dominance'}, 'Conceptual stretch.', 'Not all traits follow single T/t pattern.', 'Peas teach foundation; blood groups add complexity.', '', '', []),
    ('Blood groups summary', 'ABO: Iᴬ, Iᴮ, i alleles; codominance AB; practice inheritance problems; transfusion compatibility.', 'placeholder', {'label': 'Day 8 summary unit 4'}, 'Consolidation.', 'Fill ABO genotype-phenotype table.', 'Rh mentioned for completeness.', '', '', []),
])

DAY9 = _build_day(9, [
    ('Family resemblance', 'Children inherit combination of traits from both parents — explains resemblance and differences among siblings.', 'placeholder', {'label': 'Family resemblance'}, 'Everyday heredity.', 'Nose shape may resemble one parent; hair another.', 'Unique combo except identical twins.', '', '', []),
    ('Single gene traits (teaching examples)', "Earlobe attachment, rolling tongue, widow's peak taught as simplified inherited examples.", 'placeholder', {'label': 'Teaching trait examples'}, 'School lab surveys.', 'Class phenotype tally shows variation.', 'Real genetics may involve multiple genes.', '', '', []),
    ('Hidden recessive traits', 'Recessive traits skip generations when carriers marry carriers — appears in quarter of children on average.', 'placeholder', {'label': 'Recessive skips generations'}, 'Pedigree logic.', 'Rare genetic conditions often recessive.', 'Carrier frequency matters in population.', '', '', []),
    ('Dominant traits in pedigree', 'Dominant traits appear every generation if allele present — unless new mutation.', 'placeholder', {'label': 'Dominant in pedigree'}, 'Pattern recognition.', 'Affected child usually has affected parent for dominant.', 'Exceptions: new mutation or non-paternity rare.', '', '', []),
    ('Identical vs fraternal twins', 'Identical (monozygotic) same genotype; fraternal (dizygotic) like siblings born together.', 'placeholder', {'label': 'Twin types'}, 'Variation illustration.', 'Identical twin nature-nurture studies famous.', 'Fraternal twins can be opposite sex.', '', '', []),
    ('Sex-linked colour blindness', 'Red-green colour blindness often X-linked recessive — more common in males with one X.', 'placeholder', {'label': 'Colour blindness inheritance'}, 'Sex-linked example.', 'Carrier mother can pass to son.', 'Males XY express X recessive directly.', '', '', []),
    ('Genetic counselling (brief)', 'Couples with family history of genetic disorder may seek counselling to understand risks.', 'placeholder', {'label': 'Genetic counselling'}, 'Health application.', 'Informed family planning.', 'Science supports medical advice not stigma.', '', '', []),
    ('Heredity not determinism', 'Genes influence traits but environment, nutrition, and choice also matter especially for complex traits.', 'placeholder', {'label': 'Genes not sole fate'}, 'Balanced view.', 'Height potential from genes; nutrition affects achieved height.', 'Avoid genetic determinism socially.', '', '', []),
    ('Class survey activity idea', 'Tally inherited traits in class (attached earlobe etc.) — discuss ratios not exact Mendelian in small sample.', 'placeholder', {'label': 'Class trait survey'}, 'Active learning.', "Small N won't match 3:1 exactly.", 'Introduces population variation.', '', '', []),
    ('Inherited traits summary', 'Human traits follow Mendelian principles often simplified; pedigrees, carriers, sex-linked examples extend basics.', 'placeholder', {'label': 'Day 9 summary unit 4'}, 'Consolidation.', 'Draw sample pedigree with legend.', 'Link to blood groups day before.', '', '', []),
])

DAY10 = _build_day(10, [
    ('Mendel experiment timeline', 'P pure lines → F1 cross → F1 self → F2 count — repeat for seven traits and dihybrid.', 'placeholder', {'label': 'Experiment sequence'}, 'Review structure.', 'Monohybrid first then dihybrid.', 'Same methodical approach each trait.', '', '', []),
    ('Seven traits list recall', 'Recall pea pairs: stem length, flower colour, pod shape, pod colour, seed shape, seed colour, flower position.', 'placeholder', {'label': 'Seven trait pairs recall'}, 'Memory drill.', 'At least four enough for short answers.', 'Round/wrinkled and yellow/green seeds common in questions.', '', '', []),
    ('Three laws restated', 'Dominance; Segregation; Independent Assortment — each with one-sentence meaning and pea evidence.', 'placeholder', {'label': 'Three laws restated'}, 'Exam long answer core.', 'F2 ratios support laws 2 and 3.', "Write laws in Mendel's terms.", '', '', []),
    ('Why Mendel succeeded — review', 'Math, large samples, pure lines, one/two traits isolated, careful record keeping.', 'placeholder', {'label': 'Mendel success factors'}, 'Science history question.', 'Contrast with earlier blending theories.', 'Rediscovery 1900 with chromosomes.', '', '', []),
    ('Monohybrid ratio recap', 'F2 3:1 phenotype; 1:2:1 genotype for single trait heterozygous cross.', 'formula_panel', {'formula': 'Phenotype 3:1 | Genotype 1:2:1', 'note': 'Monohybrid F2'}, 'Numbers memorised with meaning.', 'Derive from Punnett not rote only.', '', '', []),
    ('Dihybrid ratio recap', 'F2 9:3:3:1 phenotypes from independently assorting two genes.', 'formula_panel', {'formula': 'Dihybrid F2 = 9 : 3 : 3 : 1', 'note': 'Phenotype ratio'}, 'Second ratio set.', 'Product rule (3:1)².', '', '', []),
    ('Compare monohybrid vs dihybrid', 'Monohybrid: one trait, 4 Punnett boxes. Dihybrid: two traits, 16 boxes, independent assortment.', 'placeholder', {'label': 'Mono vs dihybrid compare'}, 'Table revision.', 'F1 all dominant for both in standard dihybrid start.', '', '', []),
    ('NCERT in-text Mendel questions', "Review NCERT questions on Mendel's conclusions and ratio explanations.", 'placeholder', {'label': 'NCERT Mendel intext'}, 'Textbook checkpoint.', 'Explain why F2 has 3:1 without just stating.', '', '', []),
    ('Historical context', 'Mendel presented 1865; work ignored then rediscovered — foundation of modern genetics.', 'placeholder', {'label': 'Mendel historical note'}, 'Appreciation.', 'Chromosomes and meiosis later explained mechanism.', '', '', []),
    ('Mendel review summary', 'Pea experiments → three laws → monohybrid 3:1 → dihybrid 9:3:3:1 — full story for board exam.', 'placeholder', {'label': 'Day 10 summary unit 4'}, 'Consolidation.', "10-minute essay outline Mendel's work.", 'Activities 8.1–8.2 simulate ratios.', '', '', []),
])

DAY11 = _build_day(11, [
    ('Activity 8.1 — detailed recap', 'Monohybrid simulation with beads/cards: parent alleles in bags, random draw pairs, tally F2 phenotypes over 20+ trials.', 'placeholder', {'label': 'Activity 8.1 full recap'}, 'Procedure recall.', 'Aim: demonstrate 3:1 ratio experimentally.', 'Conclusion: random fusion produces Mendelian ratio approximately.', '', '', []),
    ('Activity 8.2 — detailed recap', 'Dihybrid simulation: two gene bead sets; combine draws; tally four phenotype classes approaching 9:3:3:1.', 'placeholder', {'label': 'Activity 8.2 full recap'}, 'Procedure recall.', 'More classes than monohybrid — need more trials.', 'Independent assortment demonstrated.', '', '', []),
    ('Writing activity conclusions', 'Format: Aim, Materials, Procedure, Observation table, Conclusion linking to Mendel laws.', 'placeholder', {'label': 'Activity write-up format'}, 'Lab exam skill.', 'Conclusion must mention ratio and law.', 'Observation table with totals and percentages.', '', '', []),
    ('Simulation to Punnett link', 'Bead draw equals random fertilisation; Punnett square lists all equally likely outcomes theoretically.', 'placeholder', {'label': 'Simulation ↔ Punnett link'}, 'Conceptual bridge.', 'Both predict 3:1 for monohybrid.', 'Simulation adds experimental flavour.', '', '', []),
    ('Sources of experimental error', 'Small trial number deviates from ratio; recording errors; unequal gamete representation if bags wrong.', 'placeholder', {'label': 'Experimental error sources'}, 'Critical analysis.', 'Increase trials improves match.', 'Good science discusses error.', '', '', []),
    ('Class data pooling', 'Combine whole class F2 counts — pooled data closer to expected ratio — law of large numbers.', 'placeholder', {'label': 'Pool class data'}, 'Statistics insight.', "One group's 8:4 may differ; 200 pairs stabilise.", 'Collaborative data strengthens conclusion.', '', '', []),
    ('Viva questions for activities', 'Prepare: Why 3:1? What is segregation? Why repeat trials? What represents gamete?', 'placeholder', {'label': 'Activity viva prep'}, 'Oral exam readiness.', 'Bead colour = allele version.', 'Teacher may ask predict before trial.', '', '', []),
    ('Diagram for activity setup', 'Sketch bead bags, parent labels Tt, drawing grid for recording offspring genotypes.', 'placeholder', {'label': 'Activity setup diagram'}, 'Visual record.', 'Neat labelled figure in notebook.', '', '', []),
    ('Extend activity thinking', 'Ask: What if parents TT × tt? Predict F2 if F1 selfed — connect to different starting crosses.', 'placeholder', {'label': 'Extend activity questions'}, 'Higher order.', 'Not all crosses start Tt × Tt.', 'Predict then simulate verify.', '', '', []),
    ('Activities 8.1–8.2 summary', 'Simulations validate Mendel ratios; write full report; link to laws; pool data for accuracy.', 'placeholder', {'label': 'Day 11 summary unit 4'}, 'Consolidation.', 'Redo simulation at home with coins.', 'Activities support ratio long answers.', '', '', []),
])

DAY12 = _build_day(12, [
    ('Genotype notation practice', 'Write genotypes for homozygous dominant, heterozygous, homozygous recessive using gene symbols T/t, R/r.', 'placeholder', {'label': 'Genotype notation drill'}, 'Symbol discipline.', 'Consistent letters per gene.', 'Same letter upper/lower for alleles.', '', '', []),
    ('Phenotype from genotype rule', 'Read phenotype from genotype using dominance rules — TT Tt tall; tt dwarf.', 'placeholder', {'label': 'Genotype → phenotype'}, 'Forward problem.', 'ABO uses special I notation.', 'Write phenotype words not just letters.', '', '', []),
    ('Reverse problem — infer genotype', 'Given phenotype and parent info infer possible genotypes (carrier detection).', 'placeholder', {'label': 'Infer genotype'}, 'Reverse skill.', 'Tall plant could TT or Tt — test cross distinguishes.', 'Multiple genotypes same phenotype possible.', '', '', []),
    ('Monohybrid mixed problems set', 'Solve five crosses: state gametes, Punnett, genotype and phenotype ratios each.', 'placeholder', {'label': 'Five monohybrid problems'}, 'Timed drill.', '10 minutes total.', 'Check ratios sum to 4 or 16.', '', '', []),
    ('Dihybrid mixed problems set', 'Solve two dihybrid crosses fully — 16-box squares.', 'placeholder', {'label': 'Two dihybrid problems'}, 'Advanced drill.', '20 minutes.', 'Label gametes RY Ry rY ry.', '', '', []),
    ('ABO inheritance problem', 'Cross type A (Iᴬi) × type B (Iᴮi) — list all child blood groups possible with probabilities.', 'placeholder', {'label': 'ABO problem practice'}, 'Applied genetics.', 'Four phenotypes possible: A, B, AB, O.', 'Each 25% in this cross.', '', '', []),
    ('Sex determination problem', 'Cross XX × XY — fraction male vs female; explain chromosome contribution.', 'placeholder', {'label': 'Sex cross problem'}, 'Simple probability.', '50% each.', "Father's sperm determines.", '', '', []),
    ('Word problems', 'Parents both heterozygous for unattached earlobe dominant E — fraction homozygous recessive children?', 'placeholder', {'label': 'Word problem Ee × Ee'}, 'Story to square.', 'Answer 25% ee if simple dominance.', 'Translate words to genotypes first.', '', '', []),
    ('Error checking checklist', 'Gametes one allele each; square size correct; ratios count all boxes; phenotype matches dominance.', 'placeholder', {'label': 'Problem checklist'}, 'Avoid lost marks.', 'Underline final ratios in answer.', '', '', []),
    ('Genotype/phenotype day summary', 'Fluent in Punnett squares mono and dihybrid, ABO, sex crosses — timed practice builds exam speed.', 'placeholder', {'label': 'Day 12 summary unit 4'}, 'Consolidation.', 'Redo wrong problems next day.', 'Genotype/phenotype language automatic.', '', '', []),
])

DAY13 = _build_day(13, [
    ('Pea plant trait diagram', 'Sketch tall vs dwarf pea, round vs wrinkled seed — label for Mendel experiment context.', 'placeholder', {'label': 'Pea trait sketches'}, 'Visual Mendel context.', 'Simple side-by-side drawings.', 'Used in long answer introductions.', '', '', []),
    ('Punnett square neat drawing', 'Draw 2×2 and 4×4 squares with labelled parent genotypes and gametes on axes.', 'placeholder', {'label': 'Punnett square exam standard'}, 'Must-have figure skill.', 'Use ruler for clarity.', 'Shade or circle genotype classes for counting.', '', '', []),
    ('Monohybrid cross figure', 'Show P → F1 → F2 generations with genotypes and phenotypes labelled in diagram flow.', 'placeholder', {'label': 'P-F1-F2 flow diagram'}, 'Generation diagram.', 'Arrows between generations.', 'Include ratios on F2.', '', '', []),
    ('Dihybrid cross figure', 'Four seed types in F2 grid picture: round-yellow, round-green, wrinkled-yellow, wrinkled-green.', 'placeholder', {'label': 'F2 seed types diagram'}, 'Classic illustration.', '9:3:3:1 under each class count.', 'NCERT textbook figure style.', '', '', []),
    ('Human sex chromosome diagram', 'Draw XX female and XY male karyotype sketch; show egg X and sperm X or Y.', 'placeholder', {'label': 'Sex chromosome diagram'}, 'Sex determination figure.', '23rd pair enlarged.', 'Autosomes shown as grouped.', '', '', []),
    ('Pedigree chart symbols', 'Square male, circle female, filled affected, horizontal mating line, vertical offspring line.', 'placeholder', {'label': 'Pedigree symbols'}, 'Standard notation.', 'Draw three-generation sample.', 'Legend box on diagram.', '', '', []),
    ('ABO table diagram', 'Table: genotype IᴬIᴬ, Iᴬi, etc. mapped to phenotype A, B, AB, O.', 'placeholder', {'label': 'ABO table figure'}, 'Quick reference chart.', 'Neat table in exam answer.', 'Include in long blood group answer.', '', '', []),
    ('Diagram timing practice', 'Complete Punnett + sex chromosome + pedigree in 15 minutes total.', 'placeholder', {'label': 'Timed diagram set'}, 'Exam simulation.', 'Practice weekly.', 'Neatness counts.', '', '', []),
    ('Label spelling genetics', 'Homozygous, heterozygous, phenotype, genotype, allele, gamete — spell correctly.', 'placeholder', {'label': 'Genetics spelling list'}, 'Language accuracy.', 'Lose marks on repeated misspellings.', 'Write glossary card.', '', '', []),
    ('Diagram day summary unit 4', 'Master Punnett squares, P-F1-F2 flow, sex chromosomes, pedigree — draw without textbook.', 'placeholder', {'label': 'Day 13 summary unit 4'}, 'Consolidation.', 'Peer exchange and mark diagrams.', 'Diagrams carry 3–5 marks each.', '', '', []),
])

DAY14 = _build_day(14, [
    ("3-mark: Mendel's contribution", 'Mendel used pea plants, counted offspring, proposed laws of dominance and segregation explaining F2 3:1 ratio.', 'placeholder', {'label': '3-mark Mendel contribution'}, 'Short answer template.', 'Experiment + ratio + law.', 'Under 100 words.', '', '', []),
    ('3-mark: Dominant vs recessive', 'Define with example; dominant expresses in heterozygote; recessive needs homozygous; pea tall/dwarf.', 'placeholder', {'label': '3-mark dominance definitions'}, 'Definition pair.', 'Example mandatory.', 'Carrier mention adds value.', '', '', []),
    ('5-mark: Monohybrid cross explanation', 'Describe Mendel monohybrid experiment P F1 F2 with diagram Punnett and 3:1 ratio explanation via segregation.', 'placeholder', {'label': '5-mark monohybrid essay'}, 'Long answer structure.', 'Intro experiment → results → law → diagram.', 'Allocate marks: diagram 2, text 3.', '', '', []),
    ('5-mark: Dihybrid and independent assortment', 'Explain dihybrid cross, F2 9:3:3:1, state law of independent assortment with gamete types.', 'placeholder', {'label': '5-mark dihybrid essay'}, 'Second long answer type.', '16-box square in answer.', 'Link to Activity 8.2.', '', '', []),
    ('5-mark: Sex determination humans', 'Explain XX XY system, role of father sperm, Punnett square, dispel myths.', 'placeholder', {'label': '5-mark sex determination'}, 'Human genetics long Q.', 'Include chromosome diagram.', 'Social awareness sentence acceptable.', '', '', []),
    ('5-mark: Blood group inheritance', 'Explain multiple alleles, codominance AB, sample cross predicting offspring groups.', 'placeholder', {'label': '5-mark ABO inheritance'}, 'Applied long answer.', 'Table genotypes to phenotypes.', 'Transfusion one line application.', '', '', []),
    ('NCERT exercise long questions', 'Practice textbook end questions on Mendel laws, variation accumulation, and sex determination.', 'placeholder', {'label': 'NCERT exercise Ch 8'}, 'Textbook aligned.', 'Answer without notes first.', 'Compare with marking points after.', '', '', []),
    ('Assertion-reason heredity', 'Practice AR: e.g. assertion F1 all dominant phenotype — reason segregation of alleles in gametes.', 'placeholder', {'label': 'AR practice Ch 8'}, 'Objective written style.', 'Both statements may be true independently.', 'Reason must explain assertion.', '', '', []),
    ('Previous year themes Ch 8', "Recurring: 3:1 and 9:3:3:1 ratios, sex determination, ABO cross, Mendel's laws list.", 'placeholder', {'label': 'Board themes unit 4'}, 'Strategic revision.', 'Solve 5 PYQs.', 'Ratio questions almost certain.', '', '', []),
    ('Written prep summary unit 4', 'Prepare 3 short + 4 long templates covering Mendel, crosses, sex, blood groups.', 'placeholder', {'label': 'Day 14 summary unit 4'}, 'Consolidation.', 'Timed writing under exam conditions.', 'Self-mark with NCERT key points.', '', '', []),
])

DAY15 = _build_day(15, [
    ('Ch 8 key terms set 1', 'Heredity, variation, gene, allele, dominant, recessive, genotype, phenotype, homozygous, heterozygous.', 'placeholder', {'label': 'Key terms set 1 unit 4'}, 'Flashcard drill.', 'One-line definition each.', 'Cover and recall.', '', '', []),
    ('Ch 8 key terms set 2', 'Monohybrid, dihybrid, F1, F2, segregation, independent assortment, Punnett square, gamete, zygote, carrier.', 'placeholder', {'label': 'Key terms set 2 unit 4'}, 'Second flashcard set.', 'Link term to pea example.', '', '', []),
    ('Ch 8 key terms set 3', 'Sex chromosome, autosome, XX, XY, codominance, multiple alleles, blood group, pedigree, Mendel, inheritance.', 'placeholder', {'label': 'Key terms set 3 unit 4'}, 'Third flashcard set.', 'Spell homozygous correctly.', '', '', []),
    ('Ratio memory with meaning', "3:1 phenotype mono F2; 1:2:1 genotype mono; 9:3:3:1 dihybrid — derive don't rote.", 'placeholder', {'label': 'Ratios with meaning'}, 'Number drill.', 'Explain from Punnett each time.', 'Product rule for dihybrid.', '', '', []),
    ('Three laws one sentence each', 'Dominance, Segregation, Independent Assortment — write from memory.', 'placeholder', {'label': 'Three laws recall'}, 'Core Mendel output.', 'Pea evidence each.', 'Activities simulate laws 2 and 3.', '', '', []),
    ('Top comparisons unit 4', 'Genotype vs phenotype; dominant vs recessive; monohybrid vs dihybrid; XX vs XY; codominance vs dominance.', 'placeholder', {'label': 'Comparison tables unit 4'}, 'Revision tables.', 'Five tables from memory.', '', '', []),
    ('Must-do problems checklist', 'Ten monohybrid, three dihybrid, two ABO, one sex cross — all correct before exam.', 'placeholder', {'label': 'Problem checklist'}, 'Skills gate.', 'Tick when 100% right.', '', '', []),
    ('Common mistakes unit 4', 'Confusing genotype/phenotype ratios; forgetting gamete one allele; mother blamed for baby sex.', 'placeholder', {'label': 'Avoid mistakes unit 4'}, 'Error list.', 'Review wrong answers.', '', '', []),
    ('NCERT Ch 8 summary review', 'Re-read summary; every point mapped to a concept card.', 'placeholder', {'label': 'NCERT summary Ch 8'}, 'Textbook closure.', 'Summary = exam blueprint.', '', '', []),
    ('Revision day summary', 'Terms, laws, ratios, problems, diagrams — full Ch 8 revision before unit completion.', 'placeholder', {'label': 'Day 15 summary unit 4'}, 'Consolidation.', 'Identify weakest day topic; redo cards.', '', '', []),
])

DAY16 = _build_day(16, [
    ('Cross-unit link Ch 7–8', 'Reproduction creates variation; heredity transmits DNA; together they explain similarity and difference in families.', 'placeholder', {'label': 'Ch 7–8 synthesis'}, 'Big picture.', 'DNA copying errors + sexual shuffle + Mendelian patterns.', 'Variation raw material; heredity rules.', '', '', []),
    ('Evolution preview Ch 9', 'Accumulated variation + selection leads to evolution — heredity chapter sets foundation.', 'placeholder', {'label': 'Link to evolution Ch 9'}, 'Forward connection.', 'Mendel + Darwin ideas combine in modern biology.', 'Not exam depth now — awareness.', '', '', []),
    ('15-minute mixed quiz unit 4', 'Mix laws, ratios, Punnett, sex chromosomes, ABO — timed.', 'placeholder', {'label': 'Mixed quiz unit 4'}, 'Final skills check.', 'Score and review errors.', '', '', []),
    ('Full Mendel essay timed', 'Write complete Mendel monohybrid account in 8 minutes from memory.', 'placeholder', {'label': 'Timed Mendel essay'}, 'Exam simulation.', 'Include ratio and law.', '', '', []),
    ('Full dihybrid problem timed', 'One RrYy × RrYy square in 5 minutes with ratios.', 'placeholder', {'label': 'Timed dihybrid problem'}, 'Speed drill.', 'No notes.', '', '', []),
    ('Concept map Ch 8', 'Draw map: Mendel → laws → mono/dihybrid → sex → blood groups → human traits.', 'placeholder', {'label': 'Ch 8 concept map'}, 'Visual synthesis.', 'One page revision poster.', '', '', []),
    ('Peer teaching test', 'Explain F2 3:1 to classmate without notes — teaching tests understanding.', 'placeholder', {'label': 'Peer teach heredity'}, 'Active recall.', 'Fix gaps where explanation breaks.', '', '', []),
    ('Board exam readiness checklist', 'Laws ✓ Ratios ✓ Punnett ✓ Sex ✓ ABO ✓ Activities ✓ Diagrams ✓', 'placeholder', {'label': 'Exam readiness checklist'}, 'Self audit.', 'All ticked before MCQ stage.', '', '', []),
    ('Congratulations message', '160 concept cards master NCERT Class 10 Heredity — strong foundation for boards and Ch 9.', 'placeholder', {'label': 'Completion encouragement'}, 'Motivation card.', 'Consistency beats cramming.', '', '', []),
    ('Unit 4 complete', 'Unit 4 Heredity complete — 160 concept cards; proceed to Practice when unlocked.', 'placeholder', {'label': 'Unit 4 complete — 160 cards'}, 'Completion card.', 'Biology Units 2–4 concept stage done.', 'Concepts done → practice → NCERT MCQs.', '', '', []),
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
    1: "Heredity — Introduction",
    2: "Variation Accumulation",
    3: "Mendel's Rules of Inheritance",
    4: "Monohybrid Cross and Punnett Square",
    5: "Dominant, Recessive, F1 and F2",
    6: "Dihybrid Cross",
    7: "Sex Determination",
    8: "Blood Groups — Inherited Traits",
    9: "Inherited Traits in Humans",
    10: "Mendel Experiments Review",
    11: "Activities 8.1–8.2 Review",
    12: "Genotype and Phenotype Practice",
    13: "Exam Diagrams — Heredity",
    14: "Written Questions — Heredity",
    15: "Revision — Unit 4",
    16: "Unit 4 Complete"
}
