"""Full concept card content for Harshit Chemistry Unit 1 — Days 1–16 (Ch 1 Chemical Reactions)."""

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
    ("What is a chemical reaction?", "A chemical reaction is a process in which one or more substances change into new substances with different properties.", "placeholder", {"label": "Reactants → Products"}, "Foundation of Ch 1 — everything else builds on this.", "Burning magnesium ribbon gives white ash (magnesium oxide).", "New substances form in a chemical reaction.", "", "", ["chemical reaction"]),
    ("Reactants and products", "Substances that take part in a reaction are reactants; new substances formed are products.", "formula_panel", {"formula": "Reactants → Products", "note": "Arrow shows direction of change"}, "Standard vocabulary for all equations.", "In Mg + O₂ → MgO, Mg and O₂ are reactants; MgO is product.", "Left side = reactants; right side = products.", "Products are not always fewer in number than reactants.", "", ["reactant", "product"]),
    ("Chemical reactions everywhere", "Cooking, rusting, digestion, respiration, and burning are everyday chemical reactions.", "placeholder", {"label": "Everyday chemical change"}, "NCERT opens with familiar examples.", "Curd forms from milk; iron gate rusts in rain.", "Chemistry is not only in the lab.", "", "", []),
    ("Physical vs chemical change", "Physical change: same substance, altered form (melting ice). Chemical change: new substance with new properties.", "placeholder", {"label": "Physical vs chemical change"}, "Students must distinguish before writing equations.", "Breaking a chalk is physical; burning it is chemical.", "New substance + new properties → chemical change.", "Dissolving salt in water is physical, not chemical.", "", []),
    ("Activity 1.1 — magnesium ribbon", "Clean Mg ribbon burns with dazzling white flame; white powdery ash (MgO) forms.", "placeholder", {"label": "Activity 1.1 — Mg burning"}, "First NCERT lab activity in Ch 1.", "Hold ribbon with tongs; flame is very bright.", "Mg + O₂ → MgO (combination reaction).", "", "", []),
    ("Magnesium oxide ash", "White ash from burning magnesium is magnesium oxide (MgO) — a new compound, not leftover Mg.", "formula_panel", {"formula": "2Mg + O₂ → 2MgO", "note": "Combination reaction"}, "Links Activity 1.1 to products.", "Ash is basic oxide; dissolves in water to form Mg(OH)₂.", "Burning Mg gives magnesium oxide.", "Ash is not 'burnt metal dust' — it is a compound.", "", []),
    ("Why clean the Mg ribbon?", "Magnesium ribbon is cleaned with sandpaper to remove oxide layer so it burns readily.", "placeholder", {"label": "Clean ribbon before burning"}, "Practical step in Activity 1.1.", "Oxide coating slows reaction with air.", "Remove surface oxide before heating.", "", "", []),
    ("Observation skills in lab", "Record what you see: flame colour, smoke, residue colour, temperature change.", "placeholder", {"label": "Observe and record"}, "Scientific method in school activities.", "Dazzling white flame + white ash + heat released.", "Good notes mention colour, state, and heat.", "", "", []),
    ("Energy in chemical reactions", "Many reactions release heat (exothermic); some absorb heat (endothermic).", "formula_panel", {"formula": "Exothermic: releases heat", "note": "Endothermic: absorbs heat"}, "Temperature change is one sign of reaction.", "Burning Mg feels hot — exothermic.", "Heat change often accompanies chemical reactions.", "Not all reactions feel hot to touch immediately.", "", []),
    ("Chapter 1 roadmap", "Ch 1 covers signs of reactions, equations, balancing, reaction types, and redox in daily life.", "placeholder", {"label": "Ch 1 roadmap"}, "Orient learner to 16-day plan.", "Activities 1.1–1.3 introduce signs; later sections classify reactions.", "Signs → equations → types → redox → corrosion/rancidity.", "", "", []),
])

DAY2 = _build_day(2, [
    ("Signs of a chemical reaction", "A chemical reaction may show change in state, colour, gas evolution, or temperature change.", "placeholder", {"label": "Four signs of reaction"}, "NCERT lists four observable clues.", "Any one sign may appear — not all four every time.", "Four signs: state, colour, gas, temperature.", "", "", []),
    ("Change in state", "Reactants and products may differ in physical state — solid, liquid, or gas.", "placeholder", {"label": "Change in state"}, "First sign in NCERT list.", "Zn (solid) + HCl (liquid) → H₂ (gas) + solution.", "Watch for new solid, liquid, or gas forming.", "State change alone does not prove chemical change (melting).", "", []),
    ("Change in colour", "A visible colour change often indicates a new substance has formed.", "placeholder", {"label": "Change in colour"}, "Second sign; Activity 1.2 is classic.", "Colourless solutions → bright yellow precipitate.", "New colour usually means new substance.", "", "", []),
    ("Evolution of a gas", "Bubbles or gas given off (often with sound or smell) suggest a chemical reaction.", "placeholder", {"label": "Gas evolution"}, "Third sign; Activity 1.3.", "Zn + dil HCl → hydrogen bubbles at surface.", "Bubbles in acid + metal often mean H₂.", "Carbonated drink fizz is physical release of dissolved CO₂.", "", []),
    ("Change in temperature", "Reaction vessel feels hotter (exothermic) or colder (endothermic) than before.", "placeholder", {"label": "Temperature change"}, "Fourth sign.", "Hand near test tube of burning Mg feels warmth.", "Hot or cold test tube → likely chemical change.", "", "", []),
    ("Activity 1.2 — lead nitrate + KI", "Mix Pb(NO₃)₂ and KI solutions → yellow precipitate of lead iodide (PbI₂).", "formula_panel", {"formula": "Pb(NO₃)₂ + 2KI → PbI₂ ↓ + 2KNO₃", "note": "Yellow precipitate"}, "Double displacement producing insoluble salt.", "Instant yellow solid in colourless mix.", "Two solutions → yellow solid = PbI₂.", "", "", []),
    ("Precipitate meaning", "Precipitate is an insoluble solid that separates from a solution during a reaction.", "placeholder", {"label": "Precipitate (insoluble solid)"}, "Key term for Activity 1.2 and BaSO₄ reactions.", "Yellow PbI₂ settles in test tube.", "Solid forming from solution = precipitate.", "Precipitate is not always coloured.", "", "", ["precipitate"]),
    ("Activity 1.3 — zinc and HCl", "Zn granules in dilute HCl produce hydrogen gas bubbles; zinc dissolves.", "formula_panel", {"formula": "Zn + 2HCl → ZnCl₂ + H₂ ↑", "note": "Gas evolution sign"}, "Displacement reaction + gas evolution.", "Pop sound when lighted splint brought near mouth of tube.", "Metal + acid → salt + hydrogen gas.", "", "", []),
    ("Testing hydrogen gas", "Hydrogen burns with a pop sound when a burning splint is held at the tube mouth.", "placeholder", {"label": "H₂ — pop test"}, "Standard school test for H₂.", "Activity 1.3 confirmation step.", "Pop sound → likely hydrogen.", "Do not confuse with oxygen (relights splint).", "", "", []),
    ("Signs are clues not proof alone", "One sign suggests a reaction; combine observations and equation writing for certainty.", "placeholder", {"label": "Signs are clues"}, "Avoid over-claiming from single observation.", "Dissolving sugar looks like change but is physical.", "Use signs together with new substance evidence.", "Boiling water shows bubbles but is physical change.", "", "", []),
])

DAY3 = _build_day(3, [
    ("Why write chemical equations?", "Equations summarise a reaction briefly using symbols — easier than long sentences.", "placeholder", {"label": "Equations summarise reactions"}, "Motivation before word/symbol forms.", "One line replaces a paragraph of description.", "Equations are shorthand for reactions.", "", "", []),
    ("Word equation", "A word equation names reactants and products in words, separated by plus and arrow.", "formula_panel", {"formula": "Magnesium + Oxygen → Magnesium oxide", "note": "Word equation"}, "First step before symbols.", "From Activity 1.1: magnesium + oxygen → magnesium oxide.", "Words + arrow; no symbols yet.", "", "", ["word equation"]),
    ("Arrow meaning in equations", "Arrow (→) means 'yields' or 'forms' — separates reactants (left) from products (right).", "formula_panel", {"formula": "Reactants → Products", "note": "Arrow = yields"}, "Never use equals sign for chemical equations.", "Plus (+) separates multiple reactants or products.", "→ means produces; not the same as =.", "Equals sign wrongly suggests reversible balance.", "", []),
    ("Symbol equation intro", "Symbol equation uses chemical formulae and state symbols instead of names.", "formula_panel", {"formula": "Mg + O₂ → MgO", "note": "Symbol equation (unbalanced)"}, "Bridge from words to formulae.", "Same reaction as word form, more compact.", "Use correct chemical formulae.", "", "", ["symbol equation"]),
    ("Chemical formula reminder", "Formula shows elements and their ratio in a compound — e.g. H₂O, CO₂, NaCl.", "placeholder", {"label": "Chemical formulae"}, "Prerequisite for symbol equations.", "O₂ is diatomic oxygen; never write O alone for gas.", "Subscripts count atoms; coefficients count molecules.", "Coefficient vs subscript is a common exam trap.", "", []),
    ("State symbols — (s)", "(s) means solid — e.g. Zn(s), CaCO₃(s).", "formula_panel", {"formula": "(s) = solid", "note": "State symbol"}, "NCERT uses (s), (l), (g), (aq).", "Mg ribbon before burning: Mg(s).", "(s) after formula = solid state.", "", "", []),
    ("State symbols — (l), (g), (aq)", "(l) = liquid, (g) = gas, (aq) = aqueous (dissolved in water).", "formula_panel", {"formula": "(l) (g) (aq)", "note": "Liquid, gas, aqueous"}, "Complete set of state symbols.", "H₂O(l) water; H₂(g) hydrogen; NaCl(aq) salt solution.", "Four states: s, l, g, aq.", "(l) is pure liquid; dissolved ions use (aq).", "", []),
    ("Conditions above arrow", "Heat (Δ), sunlight, or catalyst written above arrow when needed.", "placeholder", {"label": "Conditions: Δ, sunlight, catalyst"}, "Shows how reaction is carried out.", "CaCO₃ → CaO + CO₂ often needs heat (Δ).", "Δ or 'heat' above arrow for thermal decomposition.", "", "", []),
    ("Reversible arrow (intro)", "Some equations use ⇌ for reversible reactions — both directions possible.", "formula_panel", {"formula": "A + B ⇌ C + D", "note": "Reversible reaction"}, "Mentioned in NCERT context.", "N₂ + 3H₂ ⇌ 2NH₃ (Haber process idea).", "⇌ = forward and backward both occur.", "Ch 1 mainly uses single arrow →.", "", []),
    ("From observation to equation", "Activity observation → word equation → symbol equation → balance (later days).", "placeholder", {"label": "Observation → equation"}, "Process skill for exams.", "Yellow precipitate → lead nitrate + potassium iodide → lead iodide + potassium nitrate.", "Follow the four-step writing path.", "", "", []),
])

DAY4 = _build_day(4, [
    ("Writing a word equation — steps", "Identify reactants and products from experiment; write names left and right of arrow.", "placeholder", {"label": "Write word equation first"}, "Exam short-answer skill.", "Zinc + hydrochloric acid → zinc chloride + hydrogen.", "Names only; check spelling of compound names.", "", "", []),
    ("Convert words to symbols", "Replace each name with correct formula; keep + and → unchanged.", "formula_panel", {"formula": "Zinc + Hydrochloric acid → Zinc chloride + Hydrogen", "note": "Then replace with symbols"}, "Second step in equation writing.", "Zn + HCl → ZnCl₂ + H₂ (then balance).", "Check valency before writing formulae.", "HCl not HCl₂; acid formula must be correct.", "", []),
    ("Diatomic elements", "Seven elements exist as diatomic molecules in equations: H₂, N₂, O₂, F₂, Cl₂, Br₂, I₂.", "formula_panel", {"formula": "H₂ N₂ O₂ F₂ Cl₂ Br₂ I₂", "note": "Always diatomic as elements"}, "Critical for correct symbol equations.", "Write O₂ not O when oxygen gas reacts.", "Never write single O or H for gases.", "Carbon and metals are written as atoms (C, Fe, Zn).", "", []),
    ("Ionic compounds in equations", "Write formula as in textbook: NaCl, CaCO₃, Pb(NO₃)₂, KI, BaSO₄.", "placeholder", {"label": "Ionic formulae in equations"}, "Uses formulae from earlier classes.", "Lead nitrate Pb(NO₃)₂ — two nitrate ions per lead.", "Brackets group polyatomic ions: (NO₃)₂.", "", "", []),
    ("Example — burning magnesium", "Word: Magnesium + Oxygen → Magnesium oxide. Symbol: Mg + O₂ → MgO.", "formula_panel", {"formula": "Mg + O₂ → MgO", "note": "Unbalanced symbol equation"}, "Classic Ch 1 example.", "From Activity 1.1.", "Two O on left, one on right — needs balancing.", "", "", []),
    ("Example — zinc and HCl", "Zn(s) + 2HCl(aq) → ZnCl₂(aq) + H₂(g) — displacement + acid reaction.", "formula_panel", {"formula": "Zn + 2HCl → ZnCl₂ + H₂", "note": "Balanced form"}, "Activity 1.3 full equation.", "State symbols optional in early steps.", "One Zn displaces H from acid.", "", "", []),
    ("Example — lead nitrate + KI", "Pb(NO₃)₂(aq) + 2KI(aq) → PbI₂(s) + 2KNO₃(aq).", "formula_panel", {"formula": "Pb(NO₃)₂ + 2KI → PbI₂ + 2KNO₃", "note": "Double displacement"}, "Activity 1.2 balanced form.", "PbI₂ is insoluble yellow precipitate.", "Exchange of ions between two compounds.", "", "", []),
    ("Adding state symbols", "After balancing, add (s), (l), (g), (aq) from observation.", "placeholder", {"label": "Add state symbols last"}, "Polishes exam answers.", "H₂(g) for bubbles; PbI₂(s) for precipitate.", "State symbols match what you see in lab.", "Do not guess (aq) if unsure — ask or infer from context.", "", []),
    ("Common writing errors", "Wrong formulae, missing diatomic O₂/H₂, unbalanced atoms, using = instead of →.", "placeholder", {"label": "Common equation errors"}, "Prevention checklist.", "Mg + O → MgO is wrong (need O₂).", "Check diatomics and balance before submitting.", "", "", []),
    ("Practice pattern for exams", "Read question → word equation → symbol equation → balance → state symbols.", "placeholder", {"label": "Exam writing pattern"}, "Five-step habit.", "3-mark question often wants balanced equation with states.", "Memorise the sequence.", "", "", []),
])

DAY5 = _build_day(5, [
    ("Balanced chemical equation", "Balanced equation has equal number of atoms of each element on both sides.", "formula_panel", {"formula": "Atoms: reactants = products", "note": "Balanced equation"}, "Central idea of section 1.1.2.", "2Mg + O₂ → 2MgO balances Mg and O.", "Same atoms each side — nothing created or destroyed.", "Balancing changes coefficients only, not subscripts.", "", "", ["balanced equation"]),
    ("Law of conservation of mass", "Mass is neither created nor destroyed in a chemical reaction — total mass of reactants equals total mass of products.", "formula_panel", {"formula": "Mass of reactants = Mass of products", "note": "Lavoisier (1774)"}, "Why we must balance equations.", "Closed flask experiment: mass unchanged after reaction.", "Atoms rearrange; total mass stays same.", "Mass may seem to change if gas escapes open container.", "", "", ["conservation of mass"]),
    ("Lavoisier's contribution", "Antoine Lavoisier (1774) established conservation of mass by careful weighing.", "placeholder", {"label": "Lavoisier — conservation of mass"}, "Historical note in NCERT.", "Revolutionised chemistry with the balance.", "Conservation of mass → must balance equations.", "", "", []),
    ("Coefficients vs subscripts", "Coefficients (front numbers) may change when balancing; subscripts inside formulae must never change.", "formula_panel", {"formula": "2H₂O not H₄O₂", "note": "Never change subscripts"}, "Most important balancing rule.", "To balance H in H₂ + O₂ → H₂O, use 2H₂O not H₂O₂.", "Only coefficients change; formulae stay fixed.", "Changing subscripts creates wrong compounds.", "", "", []),
    ("Why Mg + O₂ → MgO is unbalanced", "One O on product side but two O atoms in O₂ reactant — oxygen not conserved.", "formula_panel", {"formula": "Mg + O₂ → MgO", "note": "Unbalanced — 2 O left, 1 O right"}, "Diagnostic example.", "Fix: 2Mg + O₂ → 2MgO.", "Count each element before declaring balanced.", "", "", []),
    ("Balanced magnesium burning", "2Mg(s) + O₂(g) → 2MgO(s) — two Mg and two O on each side.", "formula_panel", {"formula": "2Mg + O₂ → 2MgO", "note": "Balanced"}, "Standard balanced answer for Activity 1.1.", "Coefficients 2, 1, 2 balance atoms.", "Exam full marks: balanced + states.", "", "", []),
    ("Hit-and-trial method preview", "NCERT balances by hit-and-trial: adjust coefficients until all elements match.", "placeholder", {"label": "Hit-and-trial balancing"}, "Leads to Day 6 detail.", "Start with most complex molecule or an element appearing once.", "Trial coefficients systematically.", "", "", []),
    ("Atom counting checklist", "List each element; count atoms on left and right; adjust coefficients until equal.", "placeholder", {"label": "Count atoms each side"}, "Universal balancing algorithm.", "Fe + O₂ → Fe₂O₃ needs 4Fe + 3O₂ → 2Fe₂O₃.", "Element-by-element count.", "Polyatomic ions unchanged: count (SO₄) as unit if same both sides.", "", "", []),
    ("Mass conservation in open systems", "If gas escapes (CO₂, H₂), mass of open system appears to decrease — still conserved in universe.", "formula_panel", {"formula": "Closed system: Δm = 0", "note": "Open system may lose gas mass"}, "Explains apparent mass loss demos.", "CaCO₃ heated in open tube — CO₂ leaves.", "Weigh in closed container to verify conservation.", "Burning candle mass loss is CO₂ and H₂O leaving.", "", []),
    ("Balanced vs unbalanced", "Unbalanced equation violates conservation of mass; exam answers must be balanced unless asked otherwise.", "placeholder", {"label": "Always balance for full marks"}, "Exam discipline.", "Zn + HCl → ZnCl₂ + H₂ needs coefficient 2 on HCl.", "Final answer = balanced symbol equation.", "", "", []),
])

DAY6 = _build_day(6, [
    ("Hit-and-trial balancing — steps", "Write formulae → count atoms → change coefficients → recount until balanced.", "placeholder", {"label": "Hit-and-trial steps"}, "NCERT prescribed method for Class 10.", "Balance Fe₂O₃ formation from Fe + O₂ last.", "Repeat until every element matches.", "", "", []),
    ("Start with complex molecule", "Begin balancing with the compound containing most atoms (often largest formula).", "placeholder", {"label": "Start with complex formula"}, "Practical tip reduces trial error.", "For Ca(OH)₂ + CO₂ type, start with Ca(OH)₂.", "Fix big molecule coefficient first.", "", "", []),
    ("Balance hydrogen and oxygen last", "H and O often appear in multiple products — balance other elements first.", "placeholder", {"label": "Balance H and O last"}, "Common balancing strategy.", "Combustion equations: balance C, then H, then O.", "Save O₂ coefficient for the end.", "", "", []),
    ("Example — Fe + H₂O", "3Fe + 4H₂O → Fe₃O₄ + 4H₂ — steam over red-hot iron.", "formula_panel", {"formula": "3Fe + 4H₂O → Fe₃O₄ + 4H₂", "note": "Balanced"}, "NCERT combination/displacement context.", "Fe₃O₄ is iron(II,III) oxide.", "Coefficients 3, 4, 1, 4.", "", "", []),
    ("Example — aluminium + oxygen", "4Al + 3O₂ → 2Al₂O₃ — aluminium oxide formation.", "formula_panel", {"formula": "4Al + 3O₂ → 2Al₂O₃", "note": "Balanced"}, "Protective oxide on aluminium utensils.", "Al₂O₃ layer prevents further corrosion.", "LCM trick for O atoms: 6 each side.", "", "", []),
    ("Example — C + O₂", "C + O₂ → CO₂ — complete combustion of carbon.", "formula_panel", {"formula": "C + O₂ → CO₂", "note": "Already balanced"}, "Simple combination — one of each.", "Burning coal in plenty of air.", "Often already balanced — still verify.", "", "", []),
    ("Polyatomic ion as unit", "If ion unchanged both sides (e.g. SO₄²⁻), balance (SO₄) as a group.", "formula_panel", {"formula": "Count (NO₃) as one unit", "note": "Polyatomic ion trick"}, "Speeds balancing double displacement.", "Pb(NO₃)₂ + 2KI → PbI₂ + 2KNO₃.", "Do not split NO₃ into N and O separately if ion intact.", "", "", []),
    ("Fractional coefficients trick", "If stuck, use fractional coefficients temporarily, then multiply all by denominator.", "placeholder", {"label": "Fractional coefficient trick"}, "Advanced balancing aid.", "C₄H₁₀ + O₂: use 13/2 O₂ then double all.", "Clear fractions in final answer.", "Exam answer must have whole-number coefficients.", "", "", []),
    ("Verify your balance", "Recheck every element count after balancing — one error invalidates equation.", "placeholder", {"label": "Verify atom counts"}, "Self-check habit.", "2H₂ + O₂ → 2H₂O: H=4, O=2 each side.", "30 seconds verification saves marks.", "", "", []),
    ("Balancing exam questions", "Typical 2–3 mark: balance given skeleton equation or write full balanced equation.", "placeholder", {"label": "Balancing exam practice"}, "Day 6 skill consolidation.", "Practice Fe + CuSO₄, CaCO₃ decomposition, NaOH + HCl.", "Show balanced equation clearly.", "", "", []),
])

DAY7 = _build_day(7, [
    ("Combination reaction definition", "Two or more substances combine to form a single product — A + B → AB.", "formula_panel", {"formula": "A + B → AB", "note": "Combination reaction"}, "First reaction type in NCERT.", "2Mg + O₂ → 2MgO.", "Many reactants → one product.", "Combination is not the same as decomposition reverse only in name — check direction.", "", "", ["combination reaction"]),
    ("Combination — carbon and oxygen", "Carbon burns in oxygen to form carbon dioxide: C + O₂ → CO₂.", "formula_panel", {"formula": "C + O₂ → CO₂", "note": "Combustion combination"}, "Exothermic combination.", "Complete combustion in sufficient O₂.", "CO₂ is single product.", "Insufficient O₂ gives CO — still combination but different product.", "", "", []),
    ("Quick lime and water", "Calcium oxide reacts with water to form calcium hydroxide (slaked lime) — exothermic.", "formula_panel", {"formula": "CaO + H₂O → Ca(OH)₂", "note": "Slaking of lime"}, "NCERT daily-life combination.", "Heat released; used in whitewashing.", "CaO (quick lime) + water → slaked lime.", "", "", []),
    ("Calcium hydroxide in whitewash", "Ca(OH)₂ applied on walls reacts slowly with CO₂ to form CaCO₃ (whitewash hardens).", "formula_panel", {"formula": "Ca(OH)₂ + CO₂ → CaCO₃ + H₂O", "note": "Whitewash setting"}, "Follow-up to slaking reaction.", "White coating on walls over days.", "Not all combination — this is also double displacement with CO₂.", "", "", []),
    ("Burning coal and coke", "Combustion of carbon-containing fuels is combination with oxygen.", "placeholder", {"label": "Fuel + O₂ → oxides"}, "Energy applications.", "C + O₂ → CO₂ releases heat for industry.", "Combustion = combination with O₂.", "", "", []),
    ("Formation of water", "2H₂ + O₂ → 2H₂O — combination of hydrogen and oxygen.", "formula_panel", {"formula": "2H₂ + O₂ → 2H₂O", "note": "Combination"}, "Classic simple combination.", "Explosive mixture — used in fuel cells idea.", "Two elements → one compound.", "", "", []),
    ("Rusting as combination (preview)", "Iron combines with oxygen and water vapour to form rust — combination with multiple reactants.", "formula_panel", {"formula": "Fe + O₂ + H₂O → rust", "note": "Slow combination"}, "Links to Day 13 corrosion.", "Brown flaky coating on iron.", "Rusting is oxidation + combination over time.", "", "", []),
    ("Exothermic combination", "Many combination reactions release heat — CaO + H₂O, burning Mg.", "placeholder", {"label": "Heat released in combination"}, "Energy aspect of type.", "Touching slaked lime paste feels hot.", "Combination often exothermic, not always.", "", "", []),
    ("Combination vs decomposition", "Combination: many → one. Decomposition: one → many. Opposite direction.", "formula_panel", {"formula": "Combination: A+B→AB | Decomposition: AB→A+B", "note": "Opposite types"}, "Compare reaction types.", "Mg + O₂ vs heating MgO (hard to reverse).", "Arrow direction and product count distinguish types.", "", "", []),
    ("Identify combination in equation", "Single product on right with two or more reactants → combination.", "placeholder", {"label": "Spot combination type"}, "Exam classification skill.", "4Fe + 3O₂ → 2Fe₂O₃ is combination (also redox).", "Count products: exactly one main product.", "One product can be a compound with multiple elements.", "", "", []),
])

DAY8 = _build_day(8, [
    ("Decomposition reaction definition", "Single reactant breaks into two or more simpler products — AB → A + B.", "formula_panel", {"formula": "AB → A + B", "note": "Decomposition reaction"}, "Second reaction type.", "2HgO → 2Hg + O₂ on heating.", "One reactant → multiple products.", "", "", ["decomposition reaction"]),
    ("Thermal decomposition", "Decomposition by heat — write Δ or 'Heat' above arrow.", "formula_panel", {"formula": "CaCO₃ → CaO + CO₂", "note": "Δ above arrow"}, "Most common subtype in NCERT.", "Limestone heated in kiln.", "Heat breaks bonds in compound.", "Thermal decomposition needs continuous heat supply.", "", "", ["thermal decomposition"]),
    ("Calcium carbonate decomposition", "CaCO₃(s) → CaO(s) + CO₂(g) — basis of lime industry.", "formula_panel", {"formula": "CaCO₃ → CaO + CO₂", "note": "Balanced"}, "Major NCERT example.", "CO₂ turns lime water milky if tested.", "Limestone → quick lime + carbon dioxide.", "", "", []),
    ("Ferrous sulphate decomposition", "Green crystals of FeSO₄·7H₂O heat to brown residue; SO₂ and SO₃ gases evolve.", "formula_panel", {"formula": "2FeSO₄ → Fe₂O₃ + SO₂ + SO₃", "note": "Thermal decomposition"}, "NCERT lab observation — colour change + gas.", "Green → brown; smell of burning sulphur.", "Heat breaks ferrous sulphate.", "", "", []),
    ("Electrolytic decomposition", "Decomposition by passing electric current — electrolysis of water.", "formula_panel", {"formula": "2H₂O → 2H₂ + O₂", "note": "Electrolysis"}, "Second subtype.", "Electrolysis of water gives H₂ at cathode, O₂ at anode.", "Electricity splits compound.", "Needs electrolyte/acid for water demo in lab.", "", "", ["electrolytic decomposition"]),
    ("Photolytic decomposition", "Decomposition using sunlight — photodecomposition.", "formula_panel", {"formula": "2AgCl → 2Ag + Cl₂", "note": "Sunlight"}, "Third subtype; silver chloride in sunlight.", "White AgCl turns grey in sunlight.", "Light energy breaks AgCl.", "Photography used AgCl light sensitivity.", "", "", ["photolytic decomposition"]),
    ("Silver bromide in sunlight", "2AgBr → 2Ag + Br₂ — similar to AgCl; used in photographic films.", "formula_panel", {"formula": "2AgBr → 2Ag + Br₂", "note": "Sunlight"}, "NCERT photography connection.", "Film darkens on exposure to light.", "Light decomposes silver halides.", "", "", []),
    ("Decomposition of mercury oxide", "2HgO → 2Hg + O₂ — historical preparation of oxygen.", "formula_panel", {"formula": "2HgO → 2Hg + O₂", "note": "Heat"}, "Classic red oxide decomposition.", "Red HgO yields silvery mercury + O₂.", "Lab O₂ source in old methods.", "", "", []),
    ("Energy for decomposition", "Decomposition usually needs energy input (heat, light, or electricity) — endothermic overall.", "placeholder", {"label": "Decomposition needs energy"}, "Opposite of many combinations.", "Keep burner on for CaCO₃ decomposition.", "Break bonds → absorb energy.", "Not all decomposition is endothermic step-by-step but input is required to start.", "", "", []),
    ("Classify decomposition subtype", "Look at condition above arrow: Δ = thermal, sunlight = photolytic, electricity = electrolytic.", "placeholder", {"label": "Classify decomposition type"}, "Exam classification.", "FeSO₄ heated → thermal. AgCl in sun → photolytic.", "Condition tells the subtype.", "", "", []),
])

DAY9 = _build_day(9, [
    ("Displacement reaction definition", "More reactive element displaces less reactive element from its compound.", "formula_panel", {"formula": "A + BC → AC + B", "note": "A displaces B"}, "Third reaction type.", "Zn + CuSO₄ → ZnSO₄ + Cu.", "Reactivity series decides if displacement occurs.", "Both metals must be involved for metal displacement.", "", "", ["displacement reaction"]),
    ("Reactivity series role", "Metal higher in reactivity series displaces metal lower from salt solution.", "placeholder", {"label": "Reactivity series"}, "Predicts displacement feasibility.", "Zn above Cu — displaces Cu from CuSO₄.", "Higher metal kicks out lower metal.", "Hydrogen also has place in series vs metals.", "", "", ["reactivity series"]),
    ("Iron and copper sulphate", "Fe + CuSO₄ → FeSO₄ + Cu — iron displaces copper; blue fades, brown Cu deposits.", "formula_panel", {"formula": "Fe + CuSO₄ → FeSO₄ + Cu", "note": "Blue → green + brown Cu"}, "Classic NCERT displacement demo.", "Copper coats iron nail.", "More reactive Fe displaces Cu.", "", "", []),
    ("Zinc and copper sulphate", "Zn + CuSO₄ → ZnSO₄ + Cu — zinc is more reactive than copper.", "formula_panel", {"formula": "Zn + CuSO₄ → ZnSO₄ + Cu", "note": "Displacement"}, "Same pattern as iron example.", "Zn granules in blue solution → red-brown deposit.", "Zn above Cu in series.", "", "", []),
    ("Zinc and dilute HCl", "Zn + 2HCl → ZnCl₂ + H₂ — zinc displaces hydrogen from acid.", "formula_panel", {"formula": "Zn + 2HCl → ZnCl₂ + H₂", "note": "Displacement from acid"}, "Activity 1.3 classified as displacement.", "Metal displaces H from dilute acid.", "Acid reaction is displacement of hydrogen.", "Not all metals react with dilute HCl — check reactivity.", "", "", []),
    ("Copper and silver nitrate", "Cu + 2AgNO₃ → Cu(NO₃)₂ + 2Ag — copper displaces silver.", "formula_panel", {"formula": "Cu + 2AgNO₃ → Cu(NO₃)₂ + 2Ag", "note": "Silver mirror on copper"}, "NCERT example for displacement.", "Silver crystals on copper wire.", "Cu more reactive than Ag.", "", "", []),
    ("No reaction — copper and zinc sulphate", "Cu + ZnSO₄ → no reaction — copper less reactive than zinc.", "placeholder", {"label": "No displacement — lower metal"}, "Negative prediction important.", "Copper wire in ZnSO₄ stays unchanged.", "Lower metal cannot displace higher.", "Exam trick: predict 'no reaction'.", "", "", []),
    ("Displacement and colour change", "Solution colour may change as different metal ion forms (blue Cu²⁺ → pale green Fe²⁺).", "placeholder", {"label": "Colour change in displacement"}, "Observable sign.", "CuSO₄ blue to FeSO₄ pale green.", "Ion colour change indicates displacement.", "", "", []),
    ("Single displacement vs double", "Single displacement: one element swaps. Double displacement: ions exchange between compounds.", "formula_panel", {"formula": "Single: A+BC→AC+B | Double: AB+CD→AD+CB", "note": "Compare types"}, "Preview Day 10 contrast.", "Fe + CuSO₄ is single displacement.", "One element replaced vs ion exchange.", "", "", []),
    ("Exam tip — predict products", "Use reactivity series: if metal A above B, A + salt of B → salt of A + B.", "placeholder", {"label": "Predict displacement products"}, "Problem-solving template.", "Mg + CuSO₄ → MgSO₄ + Cu (Mg above Cu).", "Series above → displaces; below → no reaction.", "", "", []),
])

DAY10 = _build_day(10, [
    ("Double displacement definition", "Exchange of ions between two compounds — AB + CD → AD + CB.", "formula_panel", {"formula": "AB + CD → AD + CB", "note": "Double displacement"}, "Fourth reaction type.", "Na₂SO₄ + BaCl₂ → BaSO₄ + 2NaCl.", "Two compounds swap partners.", "", "", ["double displacement reaction"]),
    ("Precipitation reactions", "Double displacement often forms insoluble precipitate when product is insoluble.", "formula_panel", {"formula": "Pb(NO₃)₂ + 2KI → PbI₂ ↓ + 2KNO₃", "note": "Precipitate formation"}, "Activity 1.2 model.", "Yellow PbI₂ precipitates.", "Insoluble product = precipitate reaction.", "", "", []),
    ("Barium sulphate test", "BaCl₂ + Na₂SO₄ → BaSO₄ (white precipitate) + 2NaCl — test for sulphate.", "formula_panel", {"formula": "BaCl₂ + Na₂SO₄ → BaSO₄ + 2NaCl", "note": "White precipitate"}, "Standard qualitative test.", "White ppt insoluble in dil HCl.", "BaSO₄ white precipitate.", "", "", []),
    ("Neutralisation reaction", "Acid + base → salt + water — special double displacement.", "formula_panel", {"formula": "NaOH + HCl → NaCl + H₂O", "note": "Neutralisation"}, "Links acids-bases chapter.", "H⁺ from acid + OH⁻ from base → H₂O.", "Acid + base = salt + water.", "Neutralisation is exothermic.", "", "", ["neutralisation"]),
    ("Activity 1.2 revisited", "Lead nitrate + potassium iodide — ions Pb²⁺ and I⁻ meet to form insoluble PbI₂.", "placeholder", {"label": "Ion exchange — PbI₂"}, "Mechanism view.", "Pb²⁺(aq) + 2I⁻(aq) → PbI₂(s).", "Exchange: Pb pairs with I, K stays with NO₃.", "", "", []),
    ("Sodium sulphate + barium chloride", "Na₂SO₄(aq) + BaCl₂(aq) → BaSO₄(s) + 2NaCl(aq) — ion exchange.", "formula_panel", {"formula": "Na₂SO₄ + BaCl₂ → BaSO₄ + 2NaCl", "note": "Balanced"}, "NCERT textbook example.", "Ba²⁺ + SO₄²⁻ → BaSO₄ white solid.", "Double displacement with precipitate.", "", "", []),
    ("Soluble vs insoluble products", "Reaction goes to completion when one product is insoluble (precipitate) or gas escapes.", "placeholder", {"label": "Insoluble product drives reaction"}, "Why precipitate forms.", "BaSO₄ insoluble — leaves solution.", "Insoluble or gaseous product favours forward reaction.", "", "", []),
    ("Writing double displacement", "Split reactants into ions mentally; swap partners; write products with correct formulae.", "placeholder", {"label": "Swap ion partners"}, "Writing skill.", "AB + CD: A goes with D, C goes with B.", "Check valency after swap.", "", "", []),
    ("Double displacement without precipitate", "If all products soluble, reaction may still occur (neutralisation) — not always visible precipitate.", "formula_panel", {"formula": "HCl + NaOH → NaCl + H₂O", "note": "No precipitate — still double displacement"}, "Avoid equating type with precipitate only.", "Clear solution before and after.", "Double displacement includes neutralisation.", "", "", []),
    ("Identify reaction type quickly", "Two compounds react, two products, no single element displacing another → likely double displacement.", "placeholder", {"label": "Spot double displacement"}, "Exam speed skill.", "BaCl₂ + Na₂SO₄ pattern.", "Two ionic compounds exchanging ions.", "", "", []),
])

DAY11 = _build_day(11, [
    ("Oxidation definition (oxygen)", "Oxidation is gain of oxygen by a substance.", "formula_panel", {"formula": "Oxidation = gain of O", "note": "NCERT definition 1"}, "First redox definition in Ch 1.", "2Mg + O₂ → 2MgO: Mg gains O — oxidised.", "Gain of oxygen = oxidation.", "", "", ["oxidation"]),
    ("Oxidation definition (hydrogen)", "Oxidation is also loss of hydrogen by a substance.", "formula_panel", {"formula": "Oxidation = loss of H", "note": "NCERT definition 2"}, "Second definition — broader.", "H₂S → S: H₂S loses H — oxidised.", "Loss of H counts as oxidation.", "Use both O and H rules in organic context later.", "", "", []),
    ("Reduction definition (oxygen)", "Reduction is loss of oxygen by a substance.", "formula_panel", {"formula": "Reduction = loss of O", "note": "NCERT definition 1"}, "Pair with oxidation.", "CuO + H₂ → Cu + H₂O: CuO loses O — reduced.", "Loss of oxygen = reduction.", "", "", ["reduction"]),
    ("Reduction definition (hydrogen)", "Reduction is gain of hydrogen by a substance.", "formula_panel", {"formula": "Reduction = gain of H", "note": "NCERT definition 2"}, "Fourth definition.", "Cl₂ + H₂ → 2HCl: Cl₂ gains H — reduced.", "Gain of H counts as reduction.", "", "", []),
    ("Oxidising agent", "Substance that gives oxygen or removes hydrogen — itself gets reduced.", "formula_panel", {"formula": "Oxidising agent → reduced", "note": "O₂, Cl₂ common examples"}, "Agent does opposite to itself.", "O₂ oxidises Mg; O₂ is reduced to O²⁻ in MgO.", "Oxidising agent gets reduced.", "Agent name describes what it does to others.", "", "", ["oxidising agent"]),
    ("Reducing agent", "Substance that removes oxygen or gives hydrogen — itself gets oxidised.", "formula_panel", {"formula": "Reducing agent → oxidised", "note": "C, H₂, CO common"}, "Pair concept.", "Carbon reduces CuO to Cu; C is oxidised to CO₂.", "Reducing agent gets oxidised.", "", "", ["reducing agent"]),
    ("Redox reaction", "Reaction where oxidation and reduction occur together — one species loses O while another gains O.", "formula_panel", {"formula": "Redox = Oxidation + Reduction", "note": "Always paired"}, "Central Ch 1 redox idea.", "Zn + CuO → ZnO + Cu.", "Oxidation and reduction simultaneous.", "Cannot have one without the other in same reaction.", "", "", ["redox reaction"]),
    ("Example — copper oxide + hydrogen", "CuO + H₂ → Cu + H₂O: CuO reduced (loses O); H₂ oxidised (gains O as H₂O).", "formula_panel", {"formula": "CuO + H₂ → Cu + H₂O", "note": "CuO reduced, H₂ oxidised"}, "Classic redox identification.", "Black CuO turns brown Cu.", "Track O: moves from CuO to H₂.", "", "", []),
    ("Example — zinc + copper oxide", "Zn + CuO → ZnO + Cu — Zn oxidised; CuO reduced.", "formula_panel", {"formula": "Zn + CuO → ZnO + Cu", "note": "Redox + displacement"}, "NCERT redox example.", "ZnO forms; copper metal appears.", "Zn is reducing agent; CuO is oxidising agent.", "", "", []),
    ("Identify oxidised and reduced species", "Ask: who gained O or lost H? (oxidised). Who lost O or gained H? (reduced).", "placeholder", {"label": "Identify oxidised / reduced"}, "Exam redox skill.", "In 2Mg + O₂ → 2MgO: Mg oxidised, O₂ reduced.", "Apply four definitions systematically.", "O₂ is often reduced in combustion.", "", "", []),
])

DAY12 = _build_day(12, [
    ("Oxidation in everyday life", "NCERT section 1.3 — rusting, rancidity, and combustion are oxidation in daily life.", "placeholder", {"label": "Oxidation around us"}, "Connects redox to real world.", "Food spoils; iron rusts; fuels burn.", "Many daily changes involve oxidation.", "", "", []),
    ("Rancidity introduction", "Fats and oils oxidise on exposure to air — smell and taste turn unpleasant.", "placeholder", {"label": "Rancidity — fat oxidation"}, "Leads to Day 14 detail.", "Stale chips smell off.", "Oxidation of unsaturated fats.", "Rancidity is not bacterial spoilage alone.", "", "", ["rancidity"]),
    ("Corrosion introduction", "Corrosion is gradual destruction of metals by moisture, air, and chemicals.", "placeholder", {"label": "Corrosion of metals"}, "Leads to Day 13 detail.", "Iron gate rusts in humid weather.", "Metal + environment → damage.", "All corrosion involves oxidation of metal.", "", "", ["corrosion"]),
    ("Combustion as rapid oxidation", "Burning fuels is fast oxidation — substance reacts with O₂ releasing heat and light.", "formula_panel", {"formula": "Fuel + O₂ → oxides + heat", "note": "Rapid oxidation"}, "Energy in daily life.", "LPG burns to CO₂ and H₂O.", "Combustion = fast oxidation.", "", "", []),
    ("Antioxidants in food", "Antioxidants added to oily foods slow oxidation — prevent rancidity.", "placeholder", {"label": "Antioxidants prevent rancidity"}, "Prevention strategy.", "BHA, BHT in packaged snacks.", "Antioxidants reduce O₂ attack on fats.", "", "", []),
    ("Nitrogen flushing packaging", "Chips packed in nitrogen gas — reduces O₂ contact, delays rancidity.", "placeholder", {"label": "N₂ flushing in food packs"}, "NCERT prevention method.", "Bag feels puffed with N₂.", "Exclude O₂ to slow oxidation.", "", "", []),
    ("Refrigeration and airtight storage", "Cold and sealed containers slow oxidation of food fats.", "placeholder", {"label": "Cold + airtight storage"}, "Household prevention.", "Oil in fridge lasts longer.", "Less O₂ and lower temperature slow rancidity.", "", "", []),
    ("Galvanisation preview", "Iron coated with zinc prevents rust — zinc oxidises preferentially.", "placeholder", {"label": "Zinc coating on iron"}, "Links corrosion prevention.", "Galvanised buckets and pipes.", "Sacrificial protection by zinc.", "Detailed in Day 13.", "", []),
    ("Painting and greasing iron", "Paint or grease layer blocks air and moisture from iron surface.", "placeholder", {"label": "Paint / grease barrier"}, "Barrier protection method.", "Ship hulls painted; tools oiled.", "Physical barrier stops O₂ and H₂O.", "", "", []),
    ("Redox in respiration (idea)", "Food oxidised in body releases energy — slow controlled oxidation.", "formula_panel", {"formula": "Glucose + O₂ → CO₂ + H₂O + energy", "note": "Cellular respiration"}, "Biology-chemistry link.", "Breathing supplies O₂ for oxidation of food.", "Life processes use controlled redox.", "Simplified — full path is multi-step.", "", "", []),
])

DAY13 = _build_day(13, [
    ("Corrosion definition", "Corrosion is oxidation of metals by moisture, air, acids, and gases in environment.", "formula_panel", {"formula": "Metal + O₂ + H₂O → oxide/hydroxide", "note": "Slow oxidation"}, "Section 1.3.1 focus.", "Iron rust is most familiar example.", "Corrosion weakens structures.", "", "", ["corrosion"]),
    ("Rusting of iron", "Iron reacts with oxygen and water vapour to form hydrated iron(III) oxide — rust.", "formula_panel", {"formula": "4Fe + 3O₂ + xH₂O → 2Fe₂O₃·xH₂O", "note": "Rust formula (approx.)"}, "NCERT rust equation.", "Brown flaky deposit on iron.", "Needs both O₂ and H₂O.", "Rust is hydrated oxide, not pure Fe₂O₃ only.", "", "", ["rusting"]),
    ("Conditions for rusting", "Iron rusts when both oxygen and water (or water vapour) are present.", "placeholder", {"label": "O₂ + H₂O needed for rust"}, "Prevention targets these.", "Dry oxygen alone rusts slowly; wet air fast.", "Remove O₂ or H₂O to prevent rust.", "Paint stops both; silica gel reduces moisture.", "", "", []),
    ("Corrosion of other metals", "Silver tarnishes (Ag₂S); copper green carbonate; aluminium forms protective Al₂O₃ layer.", "placeholder", {"label": "Silver, copper, aluminium corrosion"}, "Beyond iron.", "Silver blackens in sulphur-containing air.", "Al oxide layer protects inner metal.", "Green patina on copper statues.", "", "", []),
    ("Economic cost of corrosion", "Replacing rusted bridges, pipes, and vehicles costs huge money annually.", "placeholder", {"label": "Cost of corrosion"}, "Why prevention matters.", "Rusted car body needs repair.", "Prevention cheaper than replacement.", "", "", []),
    ("Galvanisation", "Coating iron with thin layer of zinc — zinc corrodes first (sacrificial protection).", "placeholder", {"label": "Galvanisation — Zn coat"}, "NCERT prevention method.", "Galvanised iron sheets (GI sheets).", "Zinc protects even if scratched (partially).", "", "", ["galvanisation"]),
    ("Painting and greasing", "Paint, grease, or oil forms barrier — keeps O₂ and moisture away from metal.", "placeholder", {"label": "Barrier coating"}, "Simple home method.", "Gate painted every few years.", "Barrier method blocks contact.", "", "", []),
    ("Alloying against corrosion", "Stainless steel (Fe + Cr + Ni) resists rust better than pure iron.", "placeholder", {"label": "Stainless steel alloy"}, "Structural prevention.", "Kitchen sinks and surgical tools.", "Chromium forms protective oxide.", "", "", []),
    ("Sacrificial protection", "More reactive metal (zinc, magnesium) connected to iron corrodes instead of iron.", "formula_panel", {"formula": "Zn → Zn²⁺ + 2e⁻", "note": "Zinc oxidises first"}, "Ship hulls use zinc blocks.", "Zinc blocks on ships.", "Reactive metal sacrifices itself.", "", "", []),
    ("Exam answers on corrosion", "Define corrosion → give rust equation → state conditions → list prevention (galvanisation, paint, alloying).", "placeholder", {"label": "Corrosion exam template"}, "Structured long answer.", "3–5 mark corrosion question pattern.", "Four-part answer scores well.", "", "", []),
])

DAY14 = _build_day(14, [
    ("Rancidity definition", "Rancidity is oxidation of fats and oils in food, causing bad smell and taste.", "formula_panel", {"formula": "Fat + O₂ → oxidised products (off smell)", "note": "Slow oxidation of food"}, "Section 1.3.2.", "Stale oil in open bottle.", "O₂ attacks double bonds in fats.", "", "", ["rancidity"]),
    ("Foods prone to rancidity", "Oily and fatty foods — chips, butter, nuts, fried snacks, ghee.", "placeholder", {"label": "Oily / fatty foods"}, "Identify at-risk items.", "Packaged namkeen goes stale in humid air.", "Unsaturated fats oxidise faster.", "", "", []),
    ("Signs of rancidity", "Sharp unpleasant smell, stale taste, sometimes yellowish discolouration.", "placeholder", {"label": "Smell and taste change"}, "Consumer detection.", "Old peanuts taste bitter.", "If it smells off, likely rancid.", "Not all discolouration is rancidity.", "", "", []),
    ("Role of oxygen in rancidity", "Oxygen from air oxidises unsaturated fatty acids in oils.", "formula_panel", {"formula": "Unsaturated fat + O₂ → peroxides → off odours", "note": "Oxidation chain"}, "Mechanism simplified.", "Open jar of oil oxidises over weeks.", "Limit O₂ exposure to prevent.", "", "", []),
    ("Antioxidants", "Chemicals added to food that prevent oxidation — BHT, BHA, vitamin E.", "placeholder", {"label": "Antioxidants in food industry"}, "NCERT prevention list.", "Listed on chip packet ingredients.", "Antioxidants donate electrons to block O₂ damage.", "", "", ["antioxidant"]),
    ("Nitrogen gas packaging", "Flush bags with N₂ — displaces O₂, slows rancidity of fried snacks.", "placeholder", {"label": "N₂ packaging for chips"}, "Common industry practice.", "Puffed sealed chip bags.", "Inert gas reduces oxidation rate.", "", "", []),
    ("Refrigeration", "Lower temperature slows oxidation reactions — store butter and oils in fridge.", "placeholder", {"label": "Refrigerate fats and oils"}, "Home prevention.", "Ghee solidifies in fridge; lasts longer.", "Cold slows chemical reaction rate.", "", "", []),
    ("Airtight containers", "Reduce O₂ contact — store nuts and oils in sealed jars.", "placeholder", {"label": "Airtight storage"}, "Simple household habit.", "Tight lid on pickle oil.", "Less air → less oxidation.", "", "", []),
    ("Rancidity vs corrosion comparison", "Both are oxidation: rancidity affects organic fats; corrosion affects metals.", "formula_panel", {"formula": "Both = oxidation by O₂", "note": "Rancidity (food) | Corrosion (metal)"}, "Compare Ch 1 end topics.", "Rust on iron; stale smell in oil.", "Same chemistry idea, different materials.", "", "", []),
    ("Exam answer on rancidity", "Define rancidity → cause (O₂ oxidation of fats) → prevention (antioxidants, N₂, fridge, airtight).", "placeholder", {"label": "Rancidity exam template"}, "Parallel to corrosion answer.", "List three prevention methods for marks.", "Structured answer like corrosion.", "", "", []),
])

DAY15 = _build_day(15, [
    ("Four reaction types summary", "Combination, decomposition, displacement, double displacement — classify every NCERT example.", "formula_panel", {"formula": "4 types: Combo | Decomp | Displace | Double displace", "note": "Ch 1 reaction types"}, "Mixed review anchor.", "CaCO₃ → thermal decomposition.", "Memorise one exemplar per type.", "", "", []),
    ("Combination exemplars", "C + O₂ → CO₂; CaO + H₂O → Ca(OH)₂; 2Mg + O₂ → 2MgO.", "formula_panel", {"formula": "A + B → AB", "note": "Three NCERT examples"}, "Quick recall set.", "Single product on right.", "Many → one.", "", "", []),
    ("Decomposition exemplars", "CaCO₃ → CaO + CO₂ (Δ); 2AgCl → 2Ag + Cl₂ (sunlight); 2H₂O → 2H₂ + O₂ (electricity).", "formula_panel", {"formula": "AB → A + B", "note": "Thermal | Photo | Electrolytic"}, "Three subtypes with examples.", "Condition above arrow identifies subtype.", "One → many.", "", "", []),
    ("Displacement exemplars", "Fe + CuSO₄ → FeSO₄ + Cu; Zn + 2HCl → ZnCl₂ + H₂; Cu + 2AgNO₃ → Cu(NO₃)₂ + 2Ag.", "formula_panel", {"formula": "A + BC → AC + B", "note": "Check reactivity series"}, "Metal displacement set.", "More reactive displaces less reactive.", "Use series to predict.", "", "", []),
    ("Double displacement exemplars", "Pb(NO₃)₂ + 2KI → PbI₂ + 2KNO₃; BaCl₂ + Na₂SO₄ → BaSO₄ + 2NaCl; NaOH + HCl → NaCl + H₂O.", "formula_panel", {"formula": "AB + CD → AD + CB", "note": "Precipitate or neutralisation"}, "Three classic equations.", "Ion exchange between compounds.", "Two compound reactants.", "", "", []),
    ("Redox quick check", "Who gained O or lost H? Oxidised. Who lost O or gained H? Reduced.", "placeholder", {"label": "Redox identification drill"}, "Cross-cutting skill.", "Zn + CuO → Zn oxidised, CuO reduced.", "Four definition checklist.", "", "", []),
    ("Signs of reaction recap", "State, colour, gas, temperature — link each Activity 1.1–1.3 to signs.", "placeholder", {"label": "Activities 1.1–1.3 signs"}, "Tie intro to labs.", "1.1 heat+light; 1.2 colour; 1.3 gas.", "Match activity to sign observed.", "", "", []),
    ("Balancing mixed drill", "Balance: Fe + H₂O → Fe₃O₄ + H₂; Al + O₂ → Al₂O₃; FeSO₄ → Fe₂O₃ + SO₂ + SO₃.", "placeholder", {"label": "Mixed balancing practice"}, "Skills integration.", "Coefficients 3-4-1-4 for steam-iron.", "Verify all atoms after each.", "", "", []),
    ("Common exam mistakes", "Unbalanced equations, wrong diatomics, misclassified reaction type, confusing agent with process.", "placeholder", {"label": "Avoid common mistakes"}, "Error prevention review.", "O₂ not O; check type before naming redox.", "Read question twice.", "", "", []),
    ("Mixed review complete", "You can now classify, balance, and explain redox for all major Ch 1 reactions.", "placeholder", {"label": "Mixed review complete"}, "Bridge to Day 16 exam prep.", "Practice past NCERT intext questions.", "Types + equations + redox together.", "", "", []),
])

DAY16 = _build_day(16, [
    ("NCERT summary — chemical reactions", "Chemical reactions change reactants to products; observed by state, colour, gas, temperature.", "placeholder", {"label": "NCERT summary — reactions"}, "Official 'What you have learnt' alignment.", "Four signs from section 1.1.", "Match textbook summary bullets.", "", "", []),
    ("NCERT summary — equations", "Word and balanced symbol equations represent reactions; mass conserved.", "formula_panel", {"formula": "Reactants → Products (balanced)", "note": "Conservation of mass"}, "Summary equation points.", "Lavoisier conservation law.", "Balanced equations mandatory.", "", "", []),
    ("NCERT summary — reaction types", "Combination, decomposition, displacement, double displacement with NCERT examples each.", "placeholder", {"label": "Four reaction types summary"}, "Summary classification.", "One example each for 4-mark question.", "Name type + give equation.", "", "", []),
    ("NCERT summary — redox", "Oxidation: gain O or loss H. Reduction: loss O or gain H. Occur together in redox.", "formula_panel", {"formula": "Oxidation ↔ Reduction", "note": "Redox paired"}, "Summary redox definitions.", "CuO + H₂ example.", "Four definitions verbatim for exams.", "", "", []),
    ("NCERT summary — daily life", "Corrosion (rusting) and rancidity are oxidation; prevented by barriers, galvanisation, antioxidants, N₂.", "placeholder", {"label": "Corrosion & rancidity summary"}, "Application summary.", "List prevention for each.", "Link to section 1.3.", "", "", []),
    ("Must-know balanced equations", "2Mg + O₂ → 2MgO; CaCO₃ → CaO + CO₂; Zn + 2HCl → ZnCl₂ + H₂; Pb(NO₃)₂ + 2KI → PbI₂ + 2KNO₃.", "formula_panel", {"formula": "Top 4 Ch 1 equations", "note": "Memorise balanced"}, "Exam high-frequency set.", "Write with state symbols when asked.", "Drill until automatic.", "", "", []),
    ("Activity equations for exams", "Activity 1.1 MgO; 1.2 PbI₂ precipitate; 1.3 H₂ evolution — know all three balanced.", "placeholder", {"label": "Activities 1.1–1.3 equations"}, "Lab-based questions.", "Describe observation + equation.", "Observation + balanced equation = full marks.", "", "", []),
    ("Long answer template — reaction type", "Define type → give general form → write NCERT example → state observation.", "placeholder", {"label": "Long answer template"}, "3–5 mark structure.", "Displacement: define, A+BC→AC+B, Fe+CuSO₄.", "Four-step template.", "", "", []),
    ("MCQ anchors", "Conservation of mass → balance; reactivity series → displacement; precipitate → double displacement.", "placeholder", {"label": "MCQ quick anchors"}, "Practice tab preview.", "Unbalanced equation always wrong choice.", "Use rules to eliminate options.", "", "", []),
    ("Unit 1 complete", "Unit 1 Chemical Reactions and Equations complete — all 160 cards; proceed to Practice when unlocked.", "placeholder", {"label": "Unit 1 complete — 160 cards"}, "Completion card.", "200 MCQs in bank when available.", "Concepts done → practice.", "", "", []),
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
    1: "Chemical Reactions Around Us",
    2: "Signs of a Chemical Reaction",
    3: "Chemical Equations — Introduction",
    4: "Writing Chemical Equations",
    5: "Balanced Equations & Conservation of Mass",
    6: "Balancing Chemical Equations",
    7: "Combination Reactions",
    8: "Decomposition Reactions",
    9: "Displacement Reactions",
    10: "Double Displacement Reactions",
    11: "Oxidation and Reduction",
    12: "Oxidation in Everyday Life",
    13: "Corrosion",
    14: "Rancidity",
    15: "Reaction Types — Mixed Review",
    16: "Equations, Redox & Exam Prep",
}
