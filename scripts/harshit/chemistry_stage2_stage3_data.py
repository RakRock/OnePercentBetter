"""UNIT_DATA for Harshit Chemistry units 1–4 — Stage 2 & 3 seed source.

Used by seed_chemistry_stage2_stage3.py to populate ncert_source.json and exercise_bank.json.
"""

from __future__ import annotations

UNIT_DATA = {1: {'meta': {'unit_id': 1, 'chapter': 1, 'pdf': 'jesc101.pdf', 'title': 'Chemical Reactions and Equations'},
     'activities': [{'id': '1.1',
                     'title': 'Burning magnesium ribbon',
                     'summary': 'Clean Mg ribbon with sandpaper; burn in air; collect white magnesium oxide ash.',
                     'concept_ids': ['u1_d1_c05', 'u1_d1_c06', 'u1_d5_c06'],
                     'stage2_day': 17},
                    {'id': '1.2',
                     'title': 'Lead nitrate and potassium iodide',
                     'summary': 'Mix Pb(NO₃)₂ and KI solutions; observe yellow precipitate of lead iodide.',
                     'concept_ids': ['u1_d2_c07', 'u1_d10_c02', 'u1_d10_c03'],
                     'stage2_day': 17},
                    {'id': '1.3',
                     'title': 'Zinc with dilute acid',
                     'summary': 'Add dilute HCl or H₂SO₄ to zinc granules; test hydrogen gas with burning splint.',
                     'concept_ids': ['u1_d2_c09', 'u1_d9_c04', 'u1_d2_c10'],
                     'stage2_day': 17},
                    {'id': '1.4',
                     'title': 'Quick lime with water',
                     'summary': 'Add water to calcium oxide; feel temperature rise as slaked lime forms.',
                     'concept_ids': ['u1_d7_c03', 'u1_d7_c04', 'u1_d7_c08'],
                     'stage2_day': 18},
                    {'id': '1.5',
                     'title': 'Heating ferrous sulphate',
                     'summary': 'Heat green FeSO₄·7H₂O crystals; observe colour change and SO₂/SO₃ gases.',
                     'concept_ids': ['u1_d8_c04', 'u1_d8_c01', 'u1_d8_c02'],
                     'stage2_day': 18},
                    {'id': '1.6',
                     'title': 'Heating lead nitrate',
                     'summary': 'Heat lead nitrate powder; observe brown NO₂ fumes and residue.',
                     'concept_ids': ['u1_d8_c02', 'u1_d8_c01', 'u1_d11_c01'],
                     'stage2_day': 18},
                    {'id': '1.7',
                     'title': 'Electrolysis of water',
                     'summary': 'Pass current through acidified water; collect H₂ and O₂ in inverted tubes.',
                     'concept_ids': ['u1_d8_c05', 'u1_d8_c06', 'u1_d8_c07'],
                     'stage2_day': 19},
                    {'id': '1.8',
                     'title': 'Silver chloride in sunlight',
                     'summary': 'Expose white AgCl to sunlight; it turns grey as silver and chlorine form.',
                     'concept_ids': ['u1_d8_c06', 'u1_d8_c07', 'u1_d8_c08'],
                     'stage2_day': 19},
                    {'id': '1.9',
                     'title': 'Iron nails in copper sulphate',
                     'summary': 'Immerse iron in CuSO₄; blue colour fades and brown copper deposits on iron.',
                     'concept_ids': ['u1_d9_c04', 'u1_d9_c05', 'u1_d9_c06'],
                     'stage2_day': 19},
                    {'id': '1.10',
                     'title': 'Barium chloride and sodium sulphate',
                     'summary': 'Mix solutions; white BaSO₄ precipitate forms.',
                     'concept_ids': ['u1_d10_c02', 'u1_d10_c03', 'u1_d10_c04'],
                     'stage2_day': 20},
                    {'id': '1.11',
                     'title': 'Heating copper powder',
                     'summary': 'Heat copper in air; black CuO forms; reduction with hydrogen gives copper back.',
                     'concept_ids': ['u1_d11_c01', 'u1_d11_c03', 'u1_d11_c06'],
                     'stage2_day': 20}],
     'exercise_mcqs': [{'num': 1,
                        'question': 'Which of the statements about the reaction below are incorrect?\n'
                                    '2PbO(s) + C(s) → 2Pb(s) + CO₂(g)\n'
                                    '(a) Lead is getting reduced.\n'
                                    '(b) Carbon dioxide is getting oxidised.\n'
                                    '(c) Carbon is getting oxidised.\n'
                                    '(d) Lead oxide is getting reduced.',
                        'options': ['(i) (a) and (b)', '(ii) (a) and (c)', '(iii) (a), (b) and (c)', '(iv) all'],
                        'answer': 0,
                        'explanation': 'PbO loses oxygen (reduced); C gains oxygen (oxidised to CO₂). Statements (a) '
                                       'and (b) are incorrect.',
                        'misconception': 'oxidation_reduction_swap',
                        'source': 'NCERT Ch 1 Exercises Q1'},
                       {'num': 2,
                        'question': 'Fe₂O₃ + 2Al → Al₂O₃ + 2Fe\nThe above reaction is an example of a',
                        'options': ['combination reaction',
                                    'double displacement reaction',
                                    'decomposition reaction',
                                    'displacement reaction'],
                        'answer': 3,
                        'explanation': 'Aluminium displaces iron from iron(III) oxide — a displacement (thermit-type) '
                                       'reaction.',
                        'misconception': 'displacement_reactivity_error',
                        'source': 'NCERT Ch 1 Exercises Q2'},
                       {'num': 3,
                        'question': 'What happens when dilute hydrochloric acid is added to iron filings? Tick the '
                                    'correct answer.',
                        'options': ['Hydrogen gas and iron chloride are produced.',
                                    'Chlorine gas and iron hydroxide are produced.',
                                    'No reaction takes place.',
                                    'Iron salt and water are produced.'],
                        'answer': 0,
                        'explanation': 'Fe + 2HCl → FeCl₂ + H₂ — hydrogen gas evolves and iron(II) chloride forms.',
                        'misconception': 'displacement_reactivity_error',
                        'source': 'NCERT Ch 1 Exercises Q3'}],
     'intext_samples': [{'ref': 'Section 1.1 — Activity 1.1',
                         'question': 'Why should a magnesium ribbon be cleaned before burning in air?',
                         'options': ['To increase its weight before burning',
                                     'To remove the oxide layer so it burns readily',
                                     'To make it shine for observation only',
                                     'To convert it to magnesium oxide first'],
                         'answer': 1,
                         'explanation': 'Magnesium ribbon is cleaned with sandpaper to remove the oxide coating that '
                                        'would otherwise slow reaction with oxygen.',
                         'misconception': 'physical_vs_chemical_change',
                         'source': 'NCERT Ch 1 Intext Q1'},
                        {'ref': 'Section 1.1.2 — balancing',
                         'question': 'Is Mg + O₂ → MgO a balanced chemical equation?',
                         'options': ['Yes, atoms are equal on both sides',
                                     'No, oxygen atoms are not equal',
                                     'No, magnesium atoms are not equal',
                                     'It is a physical change equation'],
                         'answer': 1,
                         'explanation': 'Left side has 2 O atoms in O₂ but only 1 O in MgO — the equation is '
                                        'unbalanced until written as 2Mg + O₂ → 2MgO.',
                         'misconception': 'unbalanced_equation_accepted',
                         'source': 'NCERT Ch 1 Intext'},
                        {'ref': 'Section 1.2.1 — combination',
                         'question': 'CaO + H₂O → Ca(OH)₂ releases heat. This reaction is best described as',
                         'options': ['endothermic combination',
                                     'exothermic combination',
                                     'decomposition',
                                     'double displacement'],
                         'answer': 1,
                         'explanation': 'Calcium oxide and water combine to form a single product (slaked lime) with '
                                        'release of heat — exothermic combination.',
                         'misconception': 'physical_vs_chemical_change',
                         'source': 'NCERT Ch 1 Intext'},
                        {'ref': 'Section 1.2.3 — displacement',
                         'question': 'When an iron nail is dipped in blue copper sulphate solution, the solution turns '
                                     'pale green because',
                         'options': ['iron dissolves without reaction',
                                     'Fe²⁺ ions replace Cu²⁺ in solution',
                                     'copper oxidises iron to rust',
                                     'water evaporates from the solution'],
                         'answer': 1,
                         'explanation': 'Fe displaces Cu from CuSO₄ forming FeSO₄ (pale green); copper metal deposits '
                                        'on the nail.',
                         'misconception': 'displacement_reactivity_error',
                         'source': 'NCERT Ch 1 Intext'},
                        {'ref': 'Section 1.2.5 — redox',
                         'question': 'In CuO + H₂ → Cu + H₂O, which substance is reduced?',
                         'options': ['H₂', 'CuO', 'H₂O', 'Cu'],
                         'answer': 1,
                         'explanation': 'CuO loses oxygen and is reduced to Cu; H₂ is oxidised to H₂O.',
                         'misconception': 'oxidation_reduction_swap',
                         'source': 'NCERT Ch 1 Intext'}],
     'exercise_meta': {'active': True,
                       'stage': 3,
                       'range': 'Exercises Q4–Q20',
                       'note': 'Exam-style written questions. Chapter 1 has 3 MCQs (Stage 2) and 17 long-form '
                               'exercises here.',
                       'chapter': 'NCERT Class 10 Science Ch 1',
                       'pdf': 'jesc101.pdf'},
     'exercises': [{'id': 'u1_ex_q04',
                    'num': 4,
                    'type': 'explain',
                    'marks': 3,
                    'question': 'What is a balanced chemical equation? Why should chemical equations be balanced?',
                    'hints': ['Count atoms of each element on LHS and RHS.',
                              'Balancing follows the law of conservation of mass.',
                              'Coefficients change; subscripts in formulae do not.'],
                    'model_answer': 'A **balanced chemical equation** has an equal number of atoms of each element on '
                                    'both sides of the arrow.\n'
                                    '\n'
                                    'Equations must be balanced because of the **law of conservation of mass** — mass '
                                    'is neither created nor destroyed in a chemical reaction. Atoms are only '
                                    'rearranged, so the total number of atoms of each element must remain the same '
                                    'before and after the reaction.',
                    'marking_points': ['Definition of balanced equation (equal atoms each side)',
                                       'Law of conservation of mass stated',
                                       'Link: balancing ensures mass/atoms conserved'],
                    'common_mistakes': ['Saying balancing changes subscripts inside formulae',
                                        'Giving examples without defining balanced equation'],
                    'concept_ids': ['u1_d5_c01', 'u1_d5_c02', 'u1_d5_c04'],
                    'misconception': 'unbalanced_equation_accepted',
                    'guided_tool': None,
                    'ncert_ref': 'NCERT Ch 1 Exercises Q4'},
                   {'id': 'u1_ex_q05',
                    'num': 5,
                    'type': 'write_equations',
                    'marks': 5,
                    'question': 'Translate the following statements into chemical equations and then balance them.\n'
                                '(a) Hydrogen gas combines with nitrogen to form ammonia.\n'
                                '(b) Hydrogen sulphide gas burns in air to give water and sulphur dioxide.\n'
                                '(c) Barium chloride reacts with aluminium sulphate to give aluminium chloride and a '
                                'precipitate of barium sulphate.\n'
                                '(d) Potassium metal reacts with water to give potassium hydroxide and hydrogen gas.',
                    'hints': ['Write reactants on LHS and products on RHS.',
                              'Use correct formulae: N₂, H₂, NH₃, H₂S, O₂, BaCl₂, Al₂(SO₄)₃, K, KOH.',
                              'Balance by hit-and-trial; check each element.'],
                    'model_answer': '(a) **N₂(g) + 3H₂(g) → 2NH₃(g)**\n'
                                    '\n'
                                    '(b) **2H₂S(g) + 3O₂(g) → 2H₂O(l) + 2SO₂(g)**\n'
                                    '\n'
                                    '(c) **3BaCl₂(aq) + Al₂(SO₄)₃(aq) → 2AlCl₃(aq) + 3BaSO₄(s)↓**\n'
                                    '\n'
                                    '(d) **2K(s) + 2H₂O(l) → 2KOH(aq) + H₂(g)↑**',
                    'marking_points': ['All four equations with correct formulae',
                                       'All four equations balanced',
                                       'Precipitate/state for BaSO₄ where appropriate'],
                    'common_mistakes': ['Unbalanced equations', 'Wrong formulae (e.g. Al₂(SO₄)₃ written incorrectly)'],
                    'concept_ids': ['u1_d4_c01', 'u1_d4_c02', 'u1_d6_c01'],
                    'misconception': 'coefficient_subscript_confusion',
                    'guided_tool': None,
                    'ncert_ref': 'NCERT Ch 1 Exercises Q5'},
                   {'id': 'u1_ex_q06',
                    'num': 6,
                    'type': 'balance',
                    'marks': 4,
                    'question': 'Balance the following chemical equations.\n'
                                '(a) HNO₃ + Ca(OH)₂ → Ca(NO₃)₂ + H₂O\n'
                                '(b) NaOH + H₂SO₄ → Na₂SO₄ + H₂O\n'
                                '(c) NaCl + AgNO₃ → AgCl + NaNO₃\n'
                                '(d) BaCl₂ + H₂SO₄ → BaSO₄ + HCl',
                    'hints': ['Neutralisation type: adjust coefficients on water/salt.',
                              'Count N, O, H separately.',
                              'Verify atom count after balancing.'],
                    'model_answer': '(a) **2HNO₃ + Ca(OH)₂ → Ca(NO₃)₂ + 2H₂O**\n'
                                    '\n'
                                    '(b) **2NaOH + H₂SO₄ → Na₂SO₄ + 2H₂O**\n'
                                    '\n'
                                    '(c) **NaCl + AgNO₃ → AgCl + NaNO₃** (already balanced)\n'
                                    '\n'
                                    '(d) **BaCl₂ + H₂SO₄ → BaSO₄ + 2HCl**',
                    'marking_points': ['(a) 2,1,1,2', '(b) 2,1,1,2', '(c) already balanced', '(d) 1,1,1,2'],
                    'common_mistakes': ['Changing subscripts in formulae', 'Forgetting to balance H and O'],
                    'concept_ids': ['u1_d6_c01', 'u1_d6_c05', 'u1_d6_c09'],
                    'misconception': 'coefficient_subscript_confusion',
                    'guided_tool': None,
                    'ncert_ref': 'NCERT Ch 1 Exercises Q6'},
                   {'id': 'u1_ex_q07',
                    'num': 7,
                    'type': 'write_equations',
                    'marks': 4,
                    'question': 'Write the balanced chemical equations for the following reactions.\n'
                                '(a) Calcium hydroxide + Carbon dioxide → Calcium carbonate + Water\n'
                                '(b) Zinc + Silver nitrate → Zinc nitrate + Silver\n'
                                '(c) Aluminium + Copper chloride → Aluminium chloride + Copper\n'
                                '(d) Barium chloride + Potassium sulphate → Barium sulphate + Potassium chloride',
                    'hints': ['Convert names to formulae first.',
                              'Displacement: more reactive metal displaces less reactive.',
                              'Double displacement: exchange of ions.'],
                    'model_answer': '(a) **Ca(OH)₂(aq) + CO₂(g) → CaCO₃(s) + H₂O(l)**\n'
                                    '\n'
                                    '(b) **Zn(s) + 2AgNO₃(aq) → Zn(NO₃)₂(aq) + 2Ag(s)**\n'
                                    '\n'
                                    '(c) **2Al(s) + 3CuCl₂(aq) → 2AlCl₃(aq) + 3Cu(s)**\n'
                                    '\n'
                                    '(d) **BaCl₂(aq) + K₂SO₄(aq) → BaSO₄(s) + 2KCl(aq)**',
                    'marking_points': ['Four correct balanced equations', 'Correct products for each reaction type'],
                    'common_mistakes': ['Wrong valency in formulae', 'Unbalanced equations'],
                    'concept_ids': ['u1_d9_c04', 'u1_d10_c04', 'u1_d7_c03'],
                    'misconception': 'displacement_reactivity_error',
                    'guided_tool': None,
                    'ncert_ref': 'NCERT Ch 1 Exercises Q7'},
                   {'id': 'u1_ex_q08',
                    'num': 8,
                    'type': 'write_classify',
                    'marks': 5,
                    'question': 'Write the balanced chemical equation for the following and identify the type of '
                                'reaction in each case.\n'
                                '(a) Potassium bromide(aq) + Barium iodide(aq) → Potassium iodide(aq) + Barium '
                                'bromide(s)\n'
                                '(b) Zinc carbonate(s) → Zinc oxide(s) + Carbon dioxide(g)\n'
                                '(c) Hydrogen(g) + Chlorine(g) → Hydrogen chloride(g)\n'
                                '(d) Magnesium(s) + Hydrochloric acid(aq) → Magnesium chloride(aq) + Hydrogen(g)',
                    'hints': ['(a) ion exchange → double displacement/precipitation.',
                              '(b) one reactant → many products: decomposition.',
                              '(c) two → one: combination.',
                              '(d) metal displaces H: displacement.'],
                    'model_answer': '(a) **2KBr(aq) + BaI₂(aq) → 2KI(aq) + BaBr₂(s)** — **double displacement / '
                                    'precipitation** reaction.\n'
                                    '\n'
                                    '(b) **ZnCO₃(s) → ZnO(s) + CO₂(g)** — **thermal decomposition** reaction.\n'
                                    '\n'
                                    '(c) **H₂(g) + Cl₂(g) → 2HCl(g)** — **combination** reaction.\n'
                                    '\n'
                                    '(d) **Mg(s) + 2HCl(aq) → MgCl₂(aq) + H₂(g)** — **displacement** reaction.',
                    'marking_points': ['Four balanced equations', 'Correct reaction type named for each'],
                    'common_mistakes': ['Naming combination as decomposition', 'Missing precipitate in (a)'],
                    'concept_ids': ['u1_d7_c01', 'u1_d8_c01', 'u1_d9_c01', 'u1_d10_c01'],
                    'misconception': 'physical_vs_chemical_change',
                    'guided_tool': None,
                    'ncert_ref': 'NCERT Ch 1 Exercises Q8'},
                   {'id': 'u1_ex_q09',
                    'num': 9,
                    'type': 'explain',
                    'marks': 3,
                    'question': 'What does one mean by exothermic and endothermic reactions? Give examples.',
                    'hints': ['Exothermic: heat released to surroundings.',
                              'Endothermic: heat absorbed from surroundings.',
                              'Give one example of each with observation.'],
                    'model_answer': '**Exothermic reactions** release heat energy to the surroundings (temperature '
                                    'rises). Example: **CaO + H₂O → Ca(OH)₂ + heat** or burning of natural gas.\n'
                                    '\n'
                                    '**Endothermic reactions** absorb heat energy from the surroundings (temperature '
                                    'falls). Example: **2AgCl(s) → 2Ag(s) + Cl₂(g)** in sunlight.',
                    'marking_points': ['Exothermic defined with heat release',
                                       'Endothermic defined with heat absorption',
                                       'One valid example of each'],
                    'common_mistakes': ['Swapping definitions', 'Examples without stating heat flow direction'],
                    'concept_ids': ['u1_d1_c09', 'u1_d7_c08', 'u1_d8_c09'],
                    'misconception': 'physical_vs_chemical_change',
                    'guided_tool': None,
                    'ncert_ref': 'NCERT Ch 1 Exercises Q9'},
                   {'id': 'u1_ex_q10',
                    'num': 10,
                    'type': 'explain',
                    'marks': 2,
                    'question': 'Why is respiration considered an exothermic reaction? Explain.',
                    'hints': ['Respiration breaks down glucose in cells.',
                              'Energy is released for body activities.',
                              'Write the overall equation if helpful.'],
                    'model_answer': 'During **respiration**, glucose combines with oxygen in the cells and **releases '
                                    'energy** needed for life processes.\n'
                                    '\n'
                                    '**C₆H₁₂O₆(aq) + 6O₂(aq) → 6CO₂(aq) + 6H₂O(l) + energy**\n'
                                    '\n'
                                    'Since energy is **released**, respiration is an **exothermic** reaction.',
                    'marking_points': ['Glucose + oxygen in cells',
                                       'Energy released for life processes',
                                       'Conclusion: exothermic'],
                    'common_mistakes': ['Calling it endothermic', 'No mention of energy release'],
                    'concept_ids': ['u1_d7_c08', 'u1_d7_c02', 'u1_d1_c09'],
                    'misconception': 'physical_vs_chemical_change',
                    'guided_tool': None,
                    'ncert_ref': 'NCERT Ch 1 Exercises Q10'},
                   {'id': 'u1_ex_q11',
                    'num': 11,
                    'type': 'explain',
                    'marks': 3,
                    'question': 'Why are decomposition reactions called the opposite of combination reactions? Write '
                                'equations for these reactions.',
                    'hints': ['Combination: many → one.',
                              'Decomposition: one → many.',
                              'Give one equation for each type.'],
                    'model_answer': '**Combination reactions** form a **single product** from two or more reactants (A '
                                    '+ B → AB).\n'
                                    '**Decomposition reactions** break **one reactant** into two or more products (AB '
                                    '→ A + B).\n'
                                    '\n'
                                    'Combination example: **2Mg + O₂ → 2MgO**\n'
                                    '\n'
                                    'Decomposition example: **CaCO₃ → CaO + CO₂** (on heating).',
                    'marking_points': ['Combination defined (many → one)',
                                       'Decomposition defined (one → many)',
                                       'One balanced equation for each'],
                    'common_mistakes': ['Only definitions without equations', 'Reversed examples'],
                    'concept_ids': ['u1_d7_c09', 'u1_d8_c01', 'u1_d8_c02'],
                    'misconception': 'physical_vs_chemical_change',
                    'guided_tool': None,
                    'ncert_ref': 'NCERT Ch 1 Exercises Q11'},
                   {'id': 'u1_ex_q12',
                    'num': 12,
                    'type': 'write_equations',
                    'marks': 3,
                    'question': 'Write one equation each for decomposition reactions where energy is supplied in the '
                                'form of heat, light or electricity.',
                    'hints': ['Heat: thermal decomposition (Δ).',
                              'Light: photolytic (sunlight).',
                              'Electricity: electrolysis of water.'],
                    'model_answer': '**Heat:** **CaCO₃(s) → CaO(s) + CO₂(g)**\n'
                                    '\n'
                                    '**Light:** **2AgCl(s) → 2Ag(s) + Cl₂(g)** (sunlight)\n'
                                    '\n'
                                    '**Electricity:** **2H₂O(l) → 2H₂(g) + O₂(g)** (electrolysis)',
                    'marking_points': ['One valid heat decomposition',
                                       'One valid light decomposition',
                                       'One valid electrolytic decomposition'],
                    'common_mistakes': ['Using combination reactions', 'Not specifying energy form'],
                    'concept_ids': ['u1_d8_c02', 'u1_d8_c05', 'u1_d8_c04'],
                    'misconception': 'physical_vs_chemical_change',
                    'guided_tool': None,
                    'ncert_ref': 'NCERT Ch 1 Exercises Q12'},
                   {'id': 'u1_ex_q13',
                    'num': 13,
                    'type': 'explain',
                    'marks': 4,
                    'question': 'What is the difference between displacement and double displacement reactions? Write '
                                'equations for these reactions.',
                    'hints': ['Single displacement: one element replaces another.',
                              'Double displacement: exchange of ions between two compounds.',
                              'Give one balanced equation for each.'],
                    'model_answer': '**Displacement:** A **more reactive element** displaces a **less reactive '
                                    'element** from its compound.\n'
                                    'Example: **Fe(s) + CuSO₄(aq) → FeSO₄(aq) + Cu(s)**\n'
                                    '\n'
                                    '**Double displacement:** **Exchange of ions** between two compounds.\n'
                                    'Example: **Pb(NO₃)₂(aq) + 2KI(aq) → PbI₂(s) + 2KNO₃(aq)**',
                    'marking_points': ['Displacement defined with reactivity',
                                       'Double displacement defined with ion exchange',
                                       'One correct equation for each'],
                    'common_mistakes': ['Confusing the two types', 'Using same example for both'],
                    'concept_ids': ['u1_d9_c01', 'u1_d10_c01', 'u1_d10_c02'],
                    'misconception': 'displacement_reactivity_error',
                    'guided_tool': None,
                    'ncert_ref': 'NCERT Ch 1 Exercises Q13'},
                   {'id': 'u1_ex_q14',
                    'num': 14,
                    'type': 'write_equations',
                    'marks': 2,
                    'question': 'In the refining of silver, the recovery of silver from silver nitrate solution '
                                'involved displacement by copper metal. Write down the reaction involved.',
                    'hints': ['Copper is more reactive than silver.',
                              'Copper displaces silver from AgNO₃ solution.',
                              'Balance the equation.'],
                    'model_answer': '**2AgNO₃(aq) + Cu(s) → Cu(NO₃)₂(aq) + 2Ag(s)**\n'
                                    '\n'
                                    'Copper displaces silver from silver nitrate; silver is deposited and copper '
                                    'nitrate forms in solution.',
                    'marking_points': ['Balanced equation', 'Copper displaces silver (reactivity)'],
                    'common_mistakes': ['Reverse reaction suggested', 'Unbalanced equation'],
                    'concept_ids': ['u1_d9_c06', 'u1_d9_c02', 'u1_d9_c04'],
                    'misconception': 'displacement_reactivity_error',
                    'guided_tool': None,
                    'ncert_ref': 'NCERT Ch 1 Exercises Q14'},
                   {'id': 'u1_ex_q15',
                    'num': 15,
                    'type': 'explain',
                    'marks': 3,
                    'question': 'What do you mean by a precipitation reaction? Explain by giving examples.',
                    'hints': ['Precipitate = insoluble solid from solution.',
                              'Often a double displacement reaction.',
                              'Give at least one balanced example.'],
                    'model_answer': 'A **precipitation reaction** forms an **insoluble solid (precipitate)** when two '
                                    'solutions are mixed.\n'
                                    '\n'
                                    'Example 1: **Pb(NO₃)₂(aq) + 2KI(aq) → PbI₂(s)↓ + 2KNO₃(aq)**\n'
                                    '\n'
                                    'Example 2: **BaCl₂(aq) + Na₂SO₄(aq) → BaSO₄(s)↓ + 2NaCl(aq)**',
                    'marking_points': ['Precipitate defined',
                                       'Insoluble product forms',
                                       'At least one balanced example'],
                    'common_mistakes': ['Calling all double displacement precipitation', 'No example given'],
                    'concept_ids': ['u1_d10_c02', 'u1_d10_c03', 'u1_d10_c05'],
                    'misconception': 'displacement_reactivity_error',
                    'guided_tool': None,
                    'ncert_ref': 'NCERT Ch 1 Exercises Q15'},
                   {'id': 'u1_ex_q16',
                    'num': 16,
                    'type': 'explain',
                    'marks': 4,
                    'question': 'Explain the following in terms of gain or loss of oxygen with two examples each.\n'
                                '(a) Oxidation\n'
                                '(b) Reduction',
                    'hints': ['Oxidation = gain of oxygen (or loss of hydrogen).',
                              'Reduction = loss of oxygen (or gain of hydrogen).',
                              'Two examples each.'],
                    'model_answer': '(a) **Oxidation** — **gain of oxygen** by a substance.\n'
                                    'Examples: **2Mg + O₂ → 2MgO**; **2Cu + O₂ → 2CuO**.\n'
                                    '\n'
                                    '(b) **Reduction** — **loss of oxygen** by a substance.\n'
                                    'Examples: **CuO + H₂ → Cu + H₂O**; **ZnO + C → Zn + CO**.',
                    'marking_points': ['Oxidation defined',
                                       'Two oxidation examples',
                                       'Reduction defined',
                                       'Two reduction examples'],
                    'common_mistakes': ['Swapping oxidation and reduction', 'Only one example for each'],
                    'concept_ids': ['u1_d11_c01', 'u1_d11_c03', 'u1_d11_c06'],
                    'misconception': 'oxidation_reduction_swap',
                    'guided_tool': None,
                    'ncert_ref': 'NCERT Ch 1 Exercises Q16'},
                   {'id': 'u1_ex_q17',
                    'num': 17,
                    'type': 'identify',
                    'marks': 2,
                    'question': "A shiny brown coloured element 'X' on heating in air becomes black in colour. Name "
                                "the element 'X' and the black coloured compound formed.",
                    'hints': ['Brown metal that tarnishes black on heating: copper.',
                              'Copper reacts with oxygen to form copper(II) oxide.',
                              'Write name and formula.'],
                    'model_answer': 'Element **X** is **copper (Cu)**.\n'
                                    '\n'
                                    'The black compound is **copper(II) oxide (CuO)**.\n'
                                    '\n'
                                    '**2Cu(s) + O₂(g) → 2CuO(s)**',
                    'marking_points': ['X identified as copper', 'Black compound identified as CuO'],
                    'common_mistakes': ['Naming wrong metal', 'CuO not identified'],
                    'concept_ids': ['u1_d11_c01', 'u1_d12_c02', 'u1_d12_c03'],
                    'misconception': 'oxidation_reduction_swap',
                    'guided_tool': None,
                    'ncert_ref': 'NCERT Ch 1 Exercises Q17'},
                   {'id': 'u1_ex_q18',
                    'num': 18,
                    'type': 'explain',
                    'marks': 2,
                    'question': 'Why do we apply paint on iron articles?',
                    'hints': ['Iron rusts in moist air.', 'Paint blocks air and moisture.', 'Prevents corrosion.'],
                    'model_answer': 'Paint on iron articles **prevents rusting (corrosion)** by forming a **protective '
                                    'coating** that keeps **air and moisture** away from the metal surface.',
                    'marking_points': ['Prevents rusting/corrosion', 'Blocks air and moisture', 'Protective coating'],
                    'common_mistakes': ['Saying paint makes iron stronger', 'Only cosmetic reason'],
                    'concept_ids': ['u1_d13_c01', 'u1_d13_c03', 'u1_d13_c05'],
                    'misconception': 'physical_vs_chemical_change',
                    'guided_tool': None,
                    'ncert_ref': 'NCERT Ch 1 Exercises Q18'},
                   {'id': 'u1_ex_q19',
                    'num': 19,
                    'type': 'explain',
                    'marks': 2,
                    'question': 'Oil and fat containing food items are flushed with nitrogen. Why?',
                    'hints': ['Fats oxidise in air → rancidity.',
                              'Nitrogen is inert — excludes oxygen.',
                              'Extends shelf life.'],
                    'model_answer': 'Foods are flushed with **nitrogen** to **prevent oxidation** of fats and oils. '
                                    'Nitrogen is **inert** and **displaces oxygen**, slowing **rancidity** and '
                                    'increasing **shelf life**.',
                    'marking_points': ['Prevents oxidation of fats',
                                       'Nitrogen inert / excludes oxygen',
                                       'Prevents rancidity'],
                    'common_mistakes': ['Saying nitrogen reacts with food', 'Confusing with refrigeration only'],
                    'concept_ids': ['u1_d14_c01', 'u1_d14_c03', 'u1_d14_c05'],
                    'misconception': 'oxidation_reduction_swap',
                    'guided_tool': None,
                    'ncert_ref': 'NCERT Ch 1 Exercises Q19'},
                   {'id': 'u1_ex_q20',
                    'num': 20,
                    'type': 'explain',
                    'marks': 4,
                    'question': 'Explain the following terms with one example each.\n(a) Corrosion\n(b) Rancidity',
                    'hints': ['Corrosion: gradual destruction of metals.',
                              'Rancidity: oxidation of fats/oils in food.',
                              'One everyday example each.'],
                    'model_answer': '(a) **Corrosion** — gradual **destruction of metals** by reaction with '
                                    'environment.\n'
                                    'Example: **Rusting of iron** to brown flaky hydrated iron(III) oxide.\n'
                                    '\n'
                                    '(b) **Rancidity** — **oxidation** of oils/fats causing unpleasant smell and '
                                    'taste.\n'
                                    'Example: **Butter or fried food** exposed to air becomes rancid; antioxidants or '
                                    'airtight packing prevent it.',
                    'marking_points': ['Corrosion defined with example', 'Rancidity defined with example'],
                    'common_mistakes': ['Swapping the two terms', 'No examples'],
                    'concept_ids': ['u1_d13_c01', 'u1_d14_c01', 'u1_d14_c02'],
                    'misconception': 'oxidation_reduction_swap',
                    'guided_tool': None,
                    'ncert_ref': 'NCERT Ch 1 Exercises Q20'}]},
 2: {'meta': {'unit_id': 2, 'chapter': 2, 'pdf': 'jesc102.pdf', 'title': 'Acids, Bases and Salts'},
     'activities': [{'id': '2.1',
                     'title': 'Acids and bases in the laboratory',
                     'summary': 'Test HCl, H₂SO₄, HNO₃, CH₃COOH, NaOH, Ca(OH)₂, KOH, Mg(OH)₂, NH₄OH with indicators; '
                                'record colours in Table 2.1.',
                     'concept_ids': ['u2_d2_c01', 'u2_d2_c03', 'u2_d2_c06'],
                     'stage2_day': 17},
                    {'id': '2.2',
                     'title': 'Olfactory indicators',
                     'summary': 'Prepare onion cloth strips; test with dilute HCl and NaOH; try vanilla essence and '
                                'clove oil.',
                     'concept_ids': ['u2_d2_c04', 'u2_d2_c05', 'u2_d2_c07'],
                     'stage2_day': 17},
                    {'id': '2.3',
                     'title': 'Zinc with dilute sulphuric acid',
                     'summary': 'React zinc with dilute H₂SO₄; collect and test hydrogen gas by burning.',
                     'concept_ids': ['u2_d3_c01', 'u2_d3_c03', 'u2_d3_c05'],
                     'stage2_day': 17},
                    {'id': '2.4',
                     'title': 'Zinc with sodium hydroxide',
                     'summary': 'Warm zinc granules with NaOH solution; collect and test hydrogen gas evolved.',
                     'concept_ids': ['u2_d3_c06', 'u2_d3_c07', 'u2_d3_c08'],
                     'stage2_day': 17},
                    {'id': '2.5',
                     'title': 'Metal carbonates with acid',
                     'summary': 'React Na₂CO₃ and NaHCO₃ with dilute HCl; pass CO₂ through lime water.',
                     'concept_ids': ['u2_d4_c01', 'u2_d4_c03', 'u2_d4_c05'],
                     'stage2_day': 18},
                    {'id': '2.6',
                     'title': 'Acid–base neutralisation',
                     'summary': 'Add HCl to phenolphthalein–NaOH; observe colour change; add NaOH again.',
                     'concept_ids': ['u2_d6_c01', 'u2_d6_c04', 'u2_d6_c07'],
                     'stage2_day': 18},
                    {'id': '2.7',
                     'title': 'Copper oxide with acid',
                     'summary': 'Add dilute HCl to copper oxide; observe blue-green solution of copper(II) chloride.',
                     'concept_ids': ['u2_d7_c01', 'u2_d7_c03', 'u2_d7_c05'],
                     'stage2_day': 18},
                    {'id': '2.8',
                     'title': 'Non-metallic oxide with base',
                     'summary': 'Observe CO₂ from Activity 2.5 reacting with calcium hydroxide (lime water).',
                     'concept_ids': ['u2_d7_c06', 'u2_d7_c07', 'u2_d7_c08'],
                     'stage2_day': 18},
                    {'id': '2.9',
                     'title': 'Acid/base conductivity',
                     'summary': 'Test conductivity of dilute HCl, glucose, alcohol, and dilute NaOH with a bulb '
                                'circuit.',
                     'concept_ids': ['u2_d8_c01', 'u2_d8_c03', 'u2_d8_c05'],
                     'stage2_day': 19},
                    {'id': '2.10',
                     'title': 'Dilution of acid and base',
                     'summary': 'Add concentrated H₂SO₄ to water and NaOH pellets to water; note temperature change.',
                     'concept_ids': ['u2_d10_c08', 'u2_d10_c09', 'u2_d10_c10'],
                     'stage2_day': 19},
                    {'id': '2.11',
                     'title': 'pH paper on solutions',
                     'summary': 'Test dilute HCl, NaOH, lemon juice, vinegar, soap solution, and milk with pH paper.',
                     'concept_ids': ['u2_d11_c02', 'u2_d11_c04', 'u2_d11_c06'],
                     'stage2_day': 19},
                    {'id': '2.12',
                     'title': 'Soil pH testing',
                     'summary': 'Collect soil samples; shake with water; filter; test filtrate with pH paper.',
                     'concept_ids': ['u2_d12_c01', 'u2_d12_c03', 'u2_d12_c05'],
                     'stage2_day': 19},
                    {'id': '2.13',
                     'title': 'Plants and soil pH',
                     'summary': 'Grow Hydrangea, Clematis, or other plants; relate growth to soil acidity/alkalinity.',
                     'concept_ids': ['u2_d12_c06', 'u2_d12_c07', 'u2_d12_c08'],
                     'stage2_day': 20},
                    {'id': '2.14',
                     'title': 'Family of salts',
                     'summary': 'Test pH of salts NaCl, Na₂CO₃, NaHCO₃, KNO₃, NH₄Cl with pH paper or universal '
                                'indicator.',
                     'concept_ids': ['u2_d13_c01', 'u2_d13_c03', 'u2_d13_c05'],
                     'stage2_day': 20},
                    {'id': '2.15',
                     'title': 'Water of crystallisation',
                     'summary': 'Heat hydrated copper sulphate; add water to white anhydrous sample; observe colour '
                                'return.',
                     'concept_ids': ['u2_d15_c06', 'u2_d15_c07', 'u2_d15_c08'],
                     'stage2_day': 20}],
     'exercise_mcqs': [{'num': 1,
                        'question': 'A solution turns red litmus blue, its pH is likely to be',
                        'options': ['1', '4', '5', '10'],
                        'answer': 3,
                        'explanation': 'Basic solutions turn red litmus blue; pH > 7 — here pH 10.',
                        'misconception': 'ph_scale_reversed',
                        'source': 'NCERT Ch 2 Exercises Q1'},
                       {'num': 2,
                        'question': 'A solution reacts with crushed egg-shells to give a gas that turns lime-water '
                                    'milky. The solution contains',
                        'options': ['NaCl', 'HCl', 'LiCl', 'KCl'],
                        'answer': 1,
                        'explanation': 'Egg shells contain CaCO₃; acids release CO₂ that turns lime water milky — HCl '
                                       'is an acid.',
                        'misconception': 'litmus_colour_confusion',
                        'source': 'NCERT Ch 2 Exercises Q2'},
                       {'num': 3,
                        'question': '10 mL of a solution of NaOH is found to be completely neutralised by 8 mL of a '
                                    'given solution of HCl. If we take 20 mL of the same solution of NaOH, the amount '
                                    'HCl solution (the same solution as before) required to neutralise it will be',
                        'options': ['4 mL', '8 mL', '12 mL', '16 mL'],
                        'answer': 3,
                        'explanation': 'Double the NaOH volume requires double the HCl: 2 × 8 mL = 16 mL.',
                        'misconception': 'neutralisation_products_error',
                        'source': 'NCERT Ch 2 Exercises Q3'},
                       {'num': 4,
                        'question': 'Which one of the following types of medicines is used for treating indigestion?',
                        'options': ['Antibiotic', 'Analgesic', 'Antacid', 'Antiseptic'],
                        'answer': 2,
                        'explanation': 'Antacids neutralise excess stomach acid to relieve indigestion.',
                        'misconception': 'neutralisation_products_error',
                        'source': 'NCERT Ch 2 Exercises Q4'}],
     'intext_samples': [{'ref': 'Section 2.1 — brass vessels',
                         'question': 'Why should curd and sour substances not be kept in brass and copper vessels?',
                         'options': ['They improve taste',
                                     'Acids react with metal to form toxic compounds',
                                     'They cool faster',
                                     'They become alkaline'],
                         'answer': 1,
                         'explanation': 'Acids in curd react with copper/brass (Cu/Zn) forming salts that can be '
                                        'harmful.',
                         'misconception': 'litmus_colour_confusion',
                         'source': 'NCERT Ch 2 Intext Q1'},
                        {'ref': 'Section 2.1.2 — metal + acid',
                         'question': 'Which gas is usually liberated when an acid reacts with a metal?',
                         'options': ['Oxygen', 'Nitrogen', 'Hydrogen', 'Carbon dioxide'],
                         'answer': 2,
                         'explanation': 'Acid + metal → salt + hydrogen gas (e.g. Zn + HCl → ZnCl₂ + H₂).',
                         'misconception': 'neutralisation_products_error',
                         'source': 'NCERT Ch 2 Intext Q2'},
                        {'ref': 'Section 2.2.1 — ions in water',
                         'question': 'Why does an aqueous solution of an acid conduct electricity?',
                         'options': ['Due to water only',
                                     'Due to H⁺ (hydronium) ions in solution',
                                     'Due to undissociated acid molecules',
                                     'Acids are always metals'],
                         'answer': 1,
                         'explanation': 'Acids produce H⁺(aq) ions in water which carry current.',
                         'misconception': 'indicator_in_acid_base_confusion',
                         'source': 'NCERT Ch 2 Intext Q2.2'},
                        {'ref': 'Section 2.2.1 — dilution',
                         'question': 'While diluting an acid, why is it recommended that the acid should be added to '
                                     'water and not water to the acid?',
                         'options': ['Water is heavier',
                                     'Adding water to acid can cause splashing due to large heat release',
                                     'Acid evaporates in water',
                                     'Water neutralises acid instantly'],
                         'answer': 1,
                         'explanation': 'Dilution is highly exothermic; adding water to concentrated acid can splash '
                                        'hot acid — add acid to water slowly.',
                         'misconception': 'dilution_order_wrong',
                         'source': 'NCERT Ch 2 Intext Q4'},
                        {'ref': 'Section 2.3 — pH scale',
                         'question': 'A neutral solution has a pH of',
                         'options': ['0', '7', '14', '1'],
                         'answer': 1,
                         'explanation': 'pH 7 is neutral; below 7 acidic, above 7 basic.',
                         'misconception': 'ph_scale_reversed',
                         'source': 'NCERT Ch 2 Intext'},
                        {'ref': 'Section 2.4.2 — salt pH',
                         'question': 'An aqueous solution of sodium carbonate turns red litmus blue. It is',
                         'options': ['acidic', 'basic', 'neutral', 'amphoteric'],
                         'answer': 1,
                         'explanation': 'Na₂CO₃ is a salt of strong base and weak acid — its solution is basic.',
                         'misconception': 'ph_scale_reversed',
                         'source': 'NCERT Ch 2 Intext'}],
     'exercise_meta': {'active': True,
                       'stage': 3,
                       'range': 'Exercises Q5–Q15',
                       'note': 'Exam-style written questions. Chapter 2 has 4 MCQs (Stage 2) and 11 long-form '
                               'exercises here.',
                       'chapter': 'NCERT Class 10 Science Ch 2',
                       'pdf': 'jesc102.pdf'},
     'exercises': [{'id': 'u2_ex_q05',
                    'num': 5,
                    'type': 'write_equations',
                    'marks': 4,
                    'question': 'Write word equations and then balanced equations for the reaction taking place when '
                                '–\n'
                                '(a) dilute sulphuric acid reacts with zinc granules.\n'
                                '(b) dilute hydrochloric acid reacts with magnesium ribbon.\n'
                                '(c) dilute sulphuric acid reacts with aluminium powder.\n'
                                '(d) dilute hydrochloric acid reacts with iron filings.',
                    'hints': ['Acid + metal → salt + hydrogen.',
                              'Use correct formulae and balance.',
                              'Include state symbols where appropriate.'],
                    'model_answer': '(a) Zinc + Sulphuric acid → Zinc sulphate + Hydrogen\n'
                                    '**Zn(s) + H₂SO₄(aq) → ZnSO₄(aq) + H₂(g)**\n'
                                    '\n'
                                    '(b) Magnesium + Hydrochloric acid → Magnesium chloride + Hydrogen\n'
                                    '**Mg(s) + 2HCl(aq) → MgCl₂(aq) + H₂(g)**\n'
                                    '\n'
                                    '(c) Aluminium + Sulphuric acid → Aluminium sulphate + Hydrogen\n'
                                    '**2Al(s) + 3H₂SO₄(aq) → Al₂(SO₄)₃(aq) + 3H₂(g)**\n'
                                    '\n'
                                    '(d) Iron + Hydrochloric acid → Iron(II) chloride + Hydrogen\n'
                                    '**Fe(s) + 2HCl(aq) → FeCl₂(aq) + H₂(g)**',
                    'marking_points': ['Four word equations',
                                       'Four balanced symbol equations',
                                       'Hydrogen as product in each'],
                    'common_mistakes': ['Writing water instead of hydrogen', 'Unbalanced equations'],
                    'concept_ids': ['u2_d3_c01', 'u2_d3_c03', 'u2_d3_c05'],
                    'misconception': 'neutralisation_products_error',
                    'guided_tool': None,
                    'ncert_ref': 'NCERT Ch 2 Exercises Q5'},
                   {'id': 'u2_ex_q06',
                    'num': 6,
                    'type': 'activity',
                    'marks': 3,
                    'question': 'Compounds such as alcohols and glucose also contain hydrogen but are not categorised '
                                'as acids. Describe an Activity to prove it.',
                    'hints': ['Set up bulb circuit with dilute HCl and with glucose/ethanol solutions.',
                              'Acids ionise in water to give H⁺; glucose/ethanol do not.',
                              'Compare bulb glow.'],
                    'model_answer': '**Activity:** Connect a bulb circuit with dilute **HCl**, **glucose solution**, '
                                    'and **ethanol solution** separately.\n'
                                    '\n'
                                    'The bulb **glows brightly** with dilute HCl (H⁺ ions conduct electricity) but '
                                    '**does not glow** (or glows very dimly) with glucose or ethanol solutions because '
                                    'they **do not produce H⁺ ions** in water despite containing hydrogen.\n'
                                    '\n'
                                    'Hence they are **not acids**.',
                    'marking_points': ['Circuit test described',
                                       'HCl conducts / bulb glows',
                                       'Glucose or ethanol does not ionise to H⁺',
                                       'Conclusion: not acids'],
                    'common_mistakes': ['Saying all hydrogen-containing compounds are acids',
                                        'No experimental description'],
                    'concept_ids': ['u2_d8_c01', 'u2_d8_c03', 'u2_d8_c04'],
                    'misconception': 'indicator_in_acid_base_confusion',
                    'guided_tool': None,
                    'ncert_ref': 'NCERT Ch 2 Exercises Q6'},
                   {'id': 'u2_ex_q07',
                    'num': 7,
                    'type': 'explain',
                    'marks': 2,
                    'question': 'Why does distilled water not conduct electricity, whereas rain water does?',
                    'hints': ['Distilled water has almost no ions.',
                              'Rain water dissolves CO₂ and other gases forming acids.',
                              'More ions → conducts.'],
                    'model_answer': '**Distilled water** is almost pure H₂O with **very few ions**, so it is a **poor '
                                    'conductor**.\n'
                                    '\n'
                                    '**Rain water** dissolves **CO₂** and other gases from the atmosphere forming '
                                    '**carbonic acid** and other electrolytes, producing **ions** that make it conduct '
                                    'electricity.',
                    'marking_points': ['Distilled water — few/no ions',
                                       'Rain water — acidic gases dissolve',
                                       'Ions enable conduction'],
                    'common_mistakes': ['Saying pure water always conducts',
                                        'No mention of dissolved gases in rain water'],
                    'concept_ids': ['u2_d8_c05', 'u2_d8_c06', 'u2_d8_c07'],
                    'misconception': 'indicator_in_acid_base_confusion',
                    'guided_tool': None,
                    'ncert_ref': 'NCERT Ch 2 Exercises Q7'},
                   {'id': 'u2_ex_q08',
                    'num': 8,
                    'type': 'explain',
                    'marks': 2,
                    'question': 'Why does dry HCl gas not show acidic behaviour in the absence of water?',
                    'hints': ['Acidic character needs H⁺ ions.',
                              'HCl ionises only in presence of water.',
                              'Dry gas has no free ions.'],
                    'model_answer': '**Dry HCl gas** does not show acidic behaviour because **acids produce H⁺ '
                                    '(hydronium) ions in aqueous solution**. Without water, HCl molecules do **not '
                                    'ionise**, so no H⁺ ions are available to show acidic properties (no effect on dry '
                                    'litmus, no conductivity).',
                    'marking_points': ['H⁺ ions needed for acidic behaviour',
                                       'Water required for ionisation of HCl',
                                       'Dry HCl has no free H⁺'],
                    'common_mistakes': ['Saying HCl is never acidic', 'Confusing with dry litmus test only'],
                    'concept_ids': ['u2_d8_c02', 'u2_d8_c03', 'u2_d8_c04'],
                    'misconception': 'indicator_in_acid_base_confusion',
                    'guided_tool': None,
                    'ncert_ref': 'NCERT Ch 2 Exercises Q8'},
                   {'id': 'u2_ex_q09',
                    'num': 9,
                    'type': 'analyse',
                    'marks': 4,
                    'question': 'Five solutions A, B, C, D and E when tested with universal indicator showed pH as 4, '
                                '1, 11, 7 and 9, respectively. Which solution is\n'
                                '(a) neutral?\n'
                                '(b) strongly alkaline?\n'
                                '(c) strongly acidic?\n'
                                '(d) weakly acidic?\n'
                                '(e) weakly alkaline?\n'
                                'Arrange the pH in increasing order of hydrogen-ion concentration.',
                    'hints': ['pH 7 = neutral.',
                              'Lower pH = more H⁺ = more acidic.',
                              'Higher pH = less H⁺ = more basic.'],
                    'model_answer': '(a) **Neutral:** D (pH 7)\n'
                                    '(b) **Strongly alkaline:** C (pH 11)\n'
                                    '(c) **Strongly acidic:** B (pH 1)\n'
                                    '(d) **Weakly acidic:** A (pH 4)\n'
                                    '(e) **Weakly alkaline:** E (pH 9)\n'
                                    '\n'
                                    '**Increasing H⁺ concentration** (decreasing pH): **C(11) < E(9) < D(7) < A(4) < '
                                    'B(1)** i.e. **11, 9, 7, 4, 1** for pH values from least to most H⁺.',
                    'marking_points': ['(a) D',
                                       '(b) C',
                                       '(c) B',
                                       '(d) A',
                                       '(e) E',
                                       'Correct pH order for H⁺ concentration'],
                    'common_mistakes': ['Reversing pH scale', 'Wrong neutral identification'],
                    'concept_ids': ['u2_d11_c02', 'u2_d11_c04', 'u2_d11_c06'],
                    'misconception': 'ph_scale_reversed',
                    'guided_tool': None,
                    'ncert_ref': 'NCERT Ch 2 Exercises Q9'},
                   {'id': 'u2_ex_q10',
                    'num': 10,
                    'type': 'explain',
                    'marks': 3,
                    'question': 'Equal lengths of magnesium ribbons are taken in test tubes A and B. Hydrochloric acid '
                                '(HCl) is added to test tube A, while acetic acid (CH₃COOH) is added to test tube B. '
                                'Amount and concentration taken for both the acids are same. In which test tube will '
                                'the fizzing occur more vigorously and why?',
                    'hints': ['Strong acid vs weak acid.',
                              'HCl fully ionises; acetic acid partially.',
                              'More H⁺ → faster reaction.'],
                    'model_answer': 'Fizzing occurs more vigorously in **test tube A (HCl)**.\n'
                                    '\n'
                                    '**HCl** is a **strong acid** — it produces **more H⁺ ions** at the same '
                                    'concentration.\n'
                                    '\n'
                                    '**Acetic acid** is a **weak acid** — it ionises only partially, so fewer H⁺ ions '
                                    'are available; reaction with Mg is **slower** and fizzing is less vigorous.',
                    'marking_points': ['Test tube A (HCl) identified',
                                       'HCl is strong acid / more H⁺',
                                       'Acetic acid is weak / partial ionisation'],
                    'common_mistakes': ['Choosing test tube B', 'Saying both react equally always'],
                    'concept_ids': ['u2_d3_c04', 'u2_d8_c08', 'u2_d11_c03'],
                    'misconception': 'ph_scale_reversed',
                    'guided_tool': None,
                    'ncert_ref': 'NCERT Ch 2 Exercises Q10'},
                   {'id': 'u2_ex_q11',
                    'num': 11,
                    'type': 'explain',
                    'marks': 2,
                    'question': 'Fresh milk has a pH of 6. How do you think the pH will change as it turns into curd? '
                                'Explain your answer.',
                    'hints': ['Curd formation involves lactic acid bacteria.',
                              'Acids lower pH.',
                              'pH below 6 → more acidic.'],
                    'model_answer': 'As milk turns into **curd**, its **pH decreases** (becomes **less than 6**, more '
                                    'acidic).\n'
                                    '\n'
                                    'Lactic acid bacteria convert lactose to **lactic acid**, increasing H⁺ '
                                    'concentration and lowering pH.',
                    'marking_points': ['pH decreases / becomes more acidic',
                                       'Lactic acid formed during curdling',
                                       'pH falls below 6'],
                    'common_mistakes': ['Saying pH increases', 'No explanation of lactic acid'],
                    'concept_ids': ['u2_d11_c05', 'u2_d11_c07', 'u2_d11_c08'],
                    'misconception': 'ph_scale_reversed',
                    'guided_tool': None,
                    'ncert_ref': 'NCERT Ch 2 Exercises Q11'},
                   {'id': 'u2_ex_q12',
                    'num': 12,
                    'type': 'explain',
                    'marks': 3,
                    'question': 'A milkman adds a very small amount of baking soda to fresh milk.\n'
                                '(a) Why does he shift the pH of the fresh milk from 6 to slightly alkaline?\n'
                                '(b) Why does this milk take a long time to set as curd?',
                    'hints': ['Baking soda is NaHCO₃ — basic salt.',
                              'Higher pH slows bacterial acid production.',
                              'Link to curd setting time.'],
                    'model_answer': '(a) **Baking soda (sodium hydrogencarbonate)** is mildly **basic**; it '
                                    '**neutralises** slight acidity and shifts pH from 6 to **slightly alkaline**.\n'
                                    '\n'
                                    '(b) Curd forms when lactic acid bacteria produce acid, lowering pH. **Alkaline '
                                    'milk** retards this process, so the milk **takes longer to set** as curd.',
                    'marking_points': ['(a) baking soda is basic / raises pH',
                                       '(b) alkaline medium slows curdling / acid production'],
                    'common_mistakes': ['Saying baking soda makes milk acidic', 'No link to bacterial action'],
                    'concept_ids': ['u2_d13_c04', 'u2_d13_c06', 'u2_d11_c05'],
                    'misconception': 'ph_scale_reversed',
                    'guided_tool': None,
                    'ncert_ref': 'NCERT Ch 2 Exercises Q12'},
                   {'id': 'u2_ex_q13',
                    'num': 13,
                    'type': 'explain',
                    'marks': 2,
                    'question': 'Plaster of Paris should be stored in a moisture-proof container. Explain why?',
                    'hints': ['Plaster of Paris is CaSO₄·½H₂O.',
                              'Reacts with water to form gypsum.',
                              'Moisture causes setting/hardening.'],
                    'model_answer': '**Plaster of Paris** (calcium sulphate hemihydrate) **reacts with '
                                    'moisture/water** to form **gypsum (CaSO₄·2H₂O)**, a hard mass that **cannot be '
                                    'used** for moulding.\n'
                                    '\n'
                                    'Hence it must be stored in a **moisture-proof container**.',
                    'marking_points': ['Reacts with moisture/water',
                                       'Forms gypsum / hard mass',
                                       'Must stay dry for use'],
                    'common_mistakes': ['Saying it dissolves only', 'No equation or product named'],
                    'concept_ids': ['u2_d15_c06', 'u2_d15_c07', 'u2_d15_c08'],
                    'misconception': 'neutralisation_products_error',
                    'guided_tool': None,
                    'ncert_ref': 'NCERT Ch 2 Exercises Q13'},
                   {'id': 'u2_ex_q14',
                    'num': 14,
                    'type': 'explain',
                    'marks': 3,
                    'question': 'What is a neutralisation reaction? Give two examples.',
                    'hints': ['Acid + base → salt + water.', 'H⁺ + OH⁻ → H₂O.', 'Give two balanced examples.'],
                    'model_answer': 'A **neutralisation reaction** is the reaction between an **acid and a base** to '
                                    'form **salt and water**.\n'
                                    '\n'
                                    '**H⁺(aq) + OH⁻(aq) → H₂O(l)**\n'
                                    '\n'
                                    'Examples:\n'
                                    '1. **NaOH(aq) + HCl(aq) → NaCl(aq) + H₂O(l)**\n'
                                    '2. **Ca(OH)₂(aq) + H₂SO₄(aq) → CaSO₄(aq) + 2H₂O(l)**',
                    'marking_points': ['Definition: acid + base → salt + water', 'Two correct examples'],
                    'common_mistakes': ['Products as hydrogen and oxygen gas', 'Only one example'],
                    'concept_ids': ['u2_d6_c01', 'u2_d6_c04', 'u2_d6_c07'],
                    'misconception': 'neutralisation_products_error',
                    'guided_tool': None,
                    'ncert_ref': 'NCERT Ch 2 Exercises Q14'},
                   {'id': 'u2_ex_q15',
                    'num': 15,
                    'type': 'explain',
                    'marks': 3,
                    'question': 'Give two important uses of washing soda and baking soda.',
                    'hints': ['Washing soda = Na₂CO₃·10H₂O.', 'Baking soda = NaHCO₃.', 'One use each minimum.'],
                    'model_answer': '**Washing soda (Na₂CO₃·10H₂O):**\n'
                                    '• Used in **glass, soap, and paper industries**.\n'
                                    '• Used for **cleaning** and **removing permanent hardness** of water.\n'
                                    '\n'
                                    '**Baking soda (NaHCO₃):**\n'
                                    '• Used as **antacid** (neutralises stomach acid).\n'
                                    '• Used in **baking** (releases CO₂ with mild acid) and **fire extinguishers**.',
                    'marking_points': ['At least two uses of washing soda', 'At least two uses of baking soda'],
                    'common_mistakes': ['Swapping the two compounds', 'Vague uses without naming compound'],
                    'concept_ids': ['u2_d14_c03', 'u2_d14_c05', 'u2_d15_c01'],
                    'misconception': 'neutralisation_products_error',
                    'guided_tool': None,
                    'ncert_ref': 'NCERT Ch 2 Exercises Q15'}]},
 3: {'meta': {'unit_id': 3, 'chapter': 3, 'pdf': 'jesc103.pdf', 'title': 'Metals and Non-metals'},
     'activities': [{'id': '3.1',
                     'title': 'Appearance and hardness of metals',
                     'summary': 'Observe iron, copper, aluminium, magnesium; clean with sandpaper; compare lustre and '
                                'cut with knife.',
                     'concept_ids': ['u3_d1_c03', 'u3_d1_c05', 'u3_d1_c07'],
                     'stage2_day': 17},
                    {'id': '3.2',
                     'title': 'Malleability, ductility, sonority',
                     'summary': 'Beat metals with hammer; draw wires; tap metals — note malleability, ductility, and '
                                'sonorous sound.',
                     'concept_ids': ['u3_d2_c01', 'u3_d2_c03', 'u3_d2_c05'],
                     'stage2_day': 17},
                    {'id': '3.3',
                     'title': 'Heat and electrical conductivity',
                     'summary': 'Heat metal wire with pin in wax; test metals in electric circuit with bulb.',
                     'concept_ids': ['u3_d3_c01', 'u3_d3_c03', 'u3_d3_c05'],
                     'stage2_day': 17},
                    {'id': '3.4',
                     'title': 'Non-metal properties',
                     'summary': 'Test carbon (coal), sulphur, iodine for lustre, malleability, conductivity — compare '
                                'with metals.',
                     'concept_ids': ['u3_d4_c01', 'u3_d4_c03', 'u3_d4_c05'],
                     'stage2_day': 17},
                    {'id': '3.5',
                     'title': 'Burning metals',
                     'summary': 'Burn magnesium ribbon, copper wire, and aluminium foil in air; observe flame and '
                                'residue.',
                     'concept_ids': ['u3_d6_c01', 'u3_d6_c03', 'u3_d6_c05'],
                     'stage2_day': 18},
                    {'id': '3.6',
                     'title': 'Metals with water',
                     'summary': 'Add Na, Ca, Mg, Al, Fe, Cu, to cold/hot water or steam; compare reactions.',
                     'concept_ids': ['u3_d7_c01', 'u3_d7_c03', 'u3_d7_c05'],
                     'stage2_day': 18},
                    {'id': '3.7',
                     'title': 'Displacement reactions',
                     'summary': 'Place metal strips in salt solutions (CuSO₄, ZnSO₄, FeSO₄, AgNO₃); observe colour '
                                'changes and deposits.',
                     'concept_ids': ['u3_d9_c01', 'u3_d9_c03', 'u3_d9_c05'],
                     'stage2_day': 18},
                    {'id': '3.8',
                     'title': 'Burning sulphur',
                     'summary': 'Burn sulphur powder; test gas with litmus paper; note acidic oxide formation.',
                     'concept_ids': ['u3_d8_c01', 'u3_d8_c03', 'u3_d8_c05'],
                     'stage2_day': 19},
                    {'id': '3.9',
                     'title': 'Reactions with oxygen',
                     'summary': 'Burn samples of metals and non-metals in air; classify oxides as '
                                'basic/acidic/neutral.',
                     'concept_ids': ['u3_d6_c04', 'u3_d8_c04', 'u3_d8_c06'],
                     'stage2_day': 19},
                    {'id': '3.10',
                     'title': 'Ionic compound properties',
                     'summary': 'Test NaCl, MgCl₂, etc. for melting point, solubility, and conductivity solid vs '
                                'solution.',
                     'concept_ids': ['u3_d11_c03', 'u3_d11_c06', 'u3_d12_c02'],
                     'stage2_day': 19},
                    {'id': '3.11',
                     'title': 'Extraction of metals',
                     'summary': 'Discuss reduction of metal oxides with carbon; electrolytic reduction for '
                                'high-reactivity metals.',
                     'concept_ids': ['u3_d13_c01', 'u3_d13_c03', 'u3_d13_c05'],
                     'stage2_day': 20},
                    {'id': '3.12',
                     'title': 'Electrolytic refining',
                     'summary': 'Study diagram of electrolytic refining of copper — anode, cathode, electrolyte.',
                     'concept_ids': ['u3_d14_c01', 'u3_d14_c03', 'u3_d14_c05'],
                     'stage2_day': 20},
                    {'id': '3.13',
                     'title': 'Corrosion conditions',
                     'summary': 'Iron nails in test tubes A (air+water), B (boiled water+oil), C (dry air/CaCl₂); '
                                'compare rusting.',
                     'concept_ids': ['u3_d16_c02', 'u3_d16_c04', 'u3_d16_c06'],
                     'stage2_day': 20}],
     'exercise_mcqs': [{'num': 1,
                        'question': 'Which of the following pairs will give displacement reactions?',
                        'options': ['NaCl solution and copper metal',
                                    'MgCl₂ solution and aluminium metal',
                                    'FeSO₄ solution and silver metal',
                                    'AgNO₃ solution and copper metal'],
                        'answer': 3,
                        'explanation': 'Cu is more reactive than Ag; Cu + 2AgNO₃ → Cu(NO₃)₂ + 2Ag.',
                        'misconception': 'displacement_reactivity_error',
                        'source': 'NCERT Ch 3 Exercises Q1'},
                       {'num': 2,
                        'question': 'Which of the following methods is suitable for preventing an iron frying pan from '
                                    'rusting?',
                        'options': ['Applying grease',
                                    'Applying paint',
                                    'Applying a coating of zinc',
                                    'All of the above'],
                        'answer': 3,
                        'explanation': 'Grease, paint, and galvanisation (zinc coating) all prevent rust by blocking '
                                       'air and moisture.',
                        'misconception': 'corrosion_prevention_wrong',
                        'source': 'NCERT Ch 3 Exercises Q2'},
                       {'num': 3,
                        'question': 'An element reacts with oxygen to give a compound with a high melting point. This '
                                    'compound is also soluble in water. The element is likely to be',
                        'options': ['calcium', 'carbon', 'silicon', 'iron'],
                        'answer': 0,
                        'explanation': 'Calcium forms basic oxide CaO (high mp) which gives soluble Ca(OH)₂ with '
                                       'water.',
                        'misconception': 'metal_nonmetal_property_swap',
                        'source': 'NCERT Ch 3 Exercises Q3'},
                       {'num': 4,
                        'question': 'Food cans are coated with tin and not with zinc because',
                        'options': ['zinc is costlier than tin',
                                    'zinc has a higher melting point than tin',
                                    'zinc is more reactive than tin',
                                    'zinc is less reactive than tin'],
                        'answer': 2,
                        'explanation': 'Zinc is more reactive than tin; it could react with food acids — tin is less '
                                       'reactive and safer as coating.',
                        'misconception': 'reactivity_series_order_error',
                        'source': 'NCERT Ch 3 Exercises Q4'}],
     'intext_samples': [{'ref': 'Section 3.1 — lustre',
                         'question': 'Metals in their pure state have a shining surface. This property is called',
                         'options': ['ductility', 'metallic lustre', 'sonority', 'malleability'],
                         'answer': 1,
                         'explanation': 'The shining surface of pure metals is called metallic lustre.',
                         'misconception': 'metal_nonmetal_property_swap',
                         'source': 'NCERT Ch 3 Intext'},
                        {'ref': 'Section 3.2 — malleability',
                         'question': 'Metals that can be beaten into thin sheets are called',
                         'options': ['ductile', 'brittle', 'malleable', 'sonorous'],
                         'answer': 2,
                         'explanation': 'Malleability is the property of being beaten into thin sheets.',
                         'misconception': 'metal_nonmetal_property_swap',
                         'source': 'NCERT Ch 3 Intext'},
                        {'ref': 'Section 3.3 — ionic bond',
                         'question': 'Ionic compounds are formed by',
                         'options': ['sharing of electrons',
                                     'transfer of electrons from metal to non-metal',
                                     'transfer of protons',
                                     'metallic bonding only'],
                         'answer': 1,
                         'explanation': 'Metal atoms lose electrons; non-metals gain them — ionic bond forms.',
                         'misconception': 'ionic_bond_covalent_confusion',
                         'source': 'NCERT Ch 3 Intext'},
                        {'ref': 'Section 3.4 — reactivity',
                         'question': 'Which metal can displace copper from CuSO₄ solution?',
                         'options': ['Ag', 'Au', 'Zn', 'Cu'],
                         'answer': 2,
                         'explanation': 'Zinc is above copper in the reactivity series and displaces Cu from CuSO₄.',
                         'misconception': 'displacement_reactivity_error',
                         'source': 'NCERT Ch 3 Intext'},
                        {'ref': 'Section 3.5 — corrosion',
                         'question': 'Galvanisation protects iron because zinc',
                         'options': ['is prettier than iron',
                                     'forms a barrier and sacrificial coating',
                                     'makes iron heavier',
                                     'reacts with iron to form alloy'],
                         'answer': 1,
                         'explanation': 'Zinc coats iron and corrodes preferentially, protecting the iron underneath.',
                         'misconception': 'corrosion_prevention_wrong',
                         'source': 'NCERT Ch 3 Intext'}],
     'exercise_meta': {'active': True,
                       'stage': 3,
                       'range': 'Exercises Q5–Q16',
                       'note': 'Exam-style written questions. Chapter 3 has 4 MCQs (Stage 2) and 12 long-form '
                               'exercises here.',
                       'chapter': 'NCERT Class 10 Science Ch 3',
                       'pdf': 'jesc103.pdf'},
     'exercises': [{'id': 'u3_ex_q05',
                    'num': 5,
                    'type': 'explain',
                    'marks': 4,
                    'question': 'You are given a hammer, a battery, a bulb, wires and a switch.\n'
                                '(a) How could you use them to distinguish between samples of metals and non-metals?\n'
                                '(b) Assess the usefulness of these tests in distinguishing between metals and '
                                'non-metals.',
                    'hints': ['Metals: malleable, conduct electricity.',
                              'Non-metals: brittle, poor conductors (except graphite).',
                              'Some exceptions exist — tests not 100% definitive.'],
                    'model_answer': '(a) **Hammer test:** Beat sample — if it flattens into a sheet without breaking, '
                                    'it is **malleable (metal)**; if it breaks into pieces, likely **non-metal**.\n'
                                    '\n'
                                    '**Circuit test:** Complete circuit with sample between terminals — if **bulb '
                                    'glows**, sample **conducts** like a **metal**; if not, likely **non-metal** '
                                    '(graphite is an exception).\n'
                                    '\n'
                                    '(b) These tests are **useful but not always conclusive** — some metals are '
                                    'brittle (e.g. zinc at room temp), and graphite conducts though a non-metal.',
                    'marking_points': ['(a) malleability test described',
                                       '(a) conductivity test described',
                                       '(b) usefulness assessed with limitation'],
                    'common_mistakes': ['Only one test described',
                                        'Saying tests work for all elements without exception'],
                    'concept_ids': ['u3_d2_c01', 'u3_d3_c01', 'u3_d4_c01'],
                    'misconception': 'metal_nonmetal_property_swap',
                    'guided_tool': None,
                    'ncert_ref': 'NCERT Ch 3 Exercises Q5'},
                   {'id': 'u3_ex_q06',
                    'num': 6,
                    'type': 'explain',
                    'marks': 3,
                    'question': 'What are amphoteric oxides? Give two examples of amphoteric oxides.',
                    'hints': ['React with both acids and bases.',
                              'Al₂O₃ and ZnO are NCERT examples.',
                              'Give balanced reaction idea.'],
                    'model_answer': '**Amphoteric oxides** react with **both acids and bases** to form salt and '
                                    'water.\n'
                                    '\n'
                                    'Examples: **Aluminium oxide (Al₂O₃)** and **Zinc oxide (ZnO)**.\n'
                                    '\n'
                                    'E.g. **Al₂O₃ + 6HCl → 2AlCl₃ + 3H₂O** and **Al₂O₃ + 2NaOH → 2NaAlO₂ + H₂O**.',
                    'marking_points': ['Definition: reacts with acid and base', 'Two examples (Al₂O₃, ZnO)'],
                    'common_mistakes': ['Calling basic oxides amphoteric', 'Only one example'],
                    'concept_ids': ['u3_d6_c06', 'u3_d6_c07', 'u3_d6_c08'],
                    'misconception': 'metal_nonmetal_property_swap',
                    'guided_tool': None,
                    'ncert_ref': 'NCERT Ch 3 Exercises Q6'},
                   {'id': 'u3_ex_q07',
                    'num': 7,
                    'type': 'recall',
                    'marks': 2,
                    'question': 'Name two metals which will displace hydrogen from dilute acids, and two metals which '
                                'will not.',
                    'hints': ['Above hydrogen in reactivity series displace H.',
                              'Cu, Ag, Au below hydrogen do not.',
                              'Examples: Zn, Mg vs Cu, Ag.'],
                    'model_answer': '**Displace hydrogen:** e.g. **Zinc (Zn)** and **Magnesium (Mg)** — react with '
                                    'dilute acids giving H₂.\n'
                                    '\n'
                                    '**Do not displace hydrogen:** e.g. **Copper (Cu)** and **Silver (Ag)** — below '
                                    'hydrogen in activity series.',
                    'marking_points': ['Two metals that displace H', 'Two metals that do not'],
                    'common_mistakes': ['Including metals below hydrogen in first list', 'Wrong examples'],
                    'concept_ids': ['u3_d9_c04', 'u3_d10_c02', 'u3_d10_c06'],
                    'misconception': 'reactivity_series_order_error',
                    'guided_tool': None,
                    'ncert_ref': 'NCERT Ch 3 Exercises Q7'},
                   {'id': 'u3_ex_q08',
                    'num': 8,
                    'type': 'explain',
                    'marks': 3,
                    'question': 'In the electrolytic refining of a metal M, what would you take as the anode, the '
                                'cathode and the electrolyte?',
                    'hints': ['Impure metal = anode (dissolves).',
                              'Pure metal strip = cathode (deposited).',
                              'Salt solution of metal = electrolyte.'],
                    'model_answer': '**Anode:** **Impure metal M** (thick block)\n'
                                    '**Cathode:** **Thin strip of pure metal M**\n'
                                    '**Electrolyte:** **Acidified aqueous solution of a salt of M** (e.g. for copper: '
                                    'acidified CuSO₄)\n'
                                    '\n'
                                    'Pure metal deposits on cathode; soluble impurities go to solution; insoluble '
                                    'impurities form anode mud.',
                    'marking_points': ['Anode = impure metal',
                                       'Cathode = pure metal strip',
                                       'Electrolyte = salt solution of the metal'],
                    'common_mistakes': ['Swapping anode and cathode', 'Wrong electrolyte'],
                    'concept_ids': ['u3_d14_c01', 'u3_d14_c03', 'u3_d14_c05'],
                    'misconception': 'ionic_bond_covalent_confusion',
                    'guided_tool': None,
                    'ncert_ref': 'NCERT Ch 3 Exercises Q8'},
                   {'id': 'u3_ex_q09',
                    'num': 9,
                    'type': 'explain_diagram',
                    'marks': 4,
                    'question': 'Pratyush took sulphur powder on a spatula and heated it. He collected the gas evolved '
                                'by inverting a test tube over it, as shown in figure below.\n'
                                '(a) What will be the action of gas on\n'
                                '(i) dry litmus paper?\n'
                                '(ii) moist litmus paper?\n'
                                '(b) Write a balanced chemical equation for the reaction taking place.',
                    'hints': ['Sulphur burns to SO₂.',
                              'SO₂ forms acid with water → affects moist litmus.',
                              'Dry litmus unchanged.'],
                    'model_answer': '(a) Gas is **sulphur dioxide (SO₂)**.\n'
                                    '(i) **Dry litmus:** **no change** (no acid without water).\n'
                                    '(ii) **Moist litmus:** **turns red** (SO₂ + H₂O → H₂SO₃, acidic).\n'
                                    '\n'
                                    '(b) **S(s) + O₂(g) → SO₂(g)**',
                    'marking_points': ['SO₂ identified',
                                       '(i) no effect on dry litmus',
                                       '(ii) moist litmus turns red',
                                       'Balanced equation S + O₂ → SO₂'],
                    'common_mistakes': ['Saying SO₂ is basic', 'Wrong gas identified as H₂'],
                    'concept_ids': ['u3_d8_c01', 'u3_d8_c03', 'u3_d8_c05'],
                    'misconception': 'metal_nonmetal_property_swap',
                    'guided_tool': None,
                    'ncert_ref': 'NCERT Ch 3 Exercises Q9'},
                   {'id': 'u3_ex_q10',
                    'num': 10,
                    'type': 'explain',
                    'marks': 2,
                    'question': 'State two ways to prevent the rusting of iron.',
                    'hints': ['Barrier methods block air/water.', 'Galvanisation, painting, oiling, alloying.'],
                    'model_answer': 'Two ways to prevent rusting of iron:\n'
                                    '1. **Painting / oiling / greasing** — forms a **protective coating** preventing '
                                    'contact with air and moisture.\n'
                                    '2. **Galvanisation** — coating iron with **zinc** which prevents rust even if '
                                    'coating is scratched (sacrificial protection).',
                    'marking_points': ['Two distinct valid methods', 'Explanation of how each prevents rust'],
                    'common_mistakes': ['Only one method', 'Methods that do not stop air/moisture contact'],
                    'concept_ids': ['u3_d16_c02', 'u3_d16_c04', 'u3_d16_c06'],
                    'misconception': 'corrosion_prevention_wrong',
                    'guided_tool': None,
                    'ncert_ref': 'NCERT Ch 3 Exercises Q10'},
                   {'id': 'u3_ex_q11',
                    'num': 11,
                    'type': 'recall',
                    'marks': 1,
                    'question': 'What type of oxides are formed when non-metals combine with oxygen?',
                    'hints': ['Non-metal oxides are acidic or neutral.',
                              'Examples: SO₂ acidic, CO neutral.',
                              'Contrast with basic metal oxides.'],
                    'model_answer': 'When **non-metals** combine with oxygen, **acidic oxides** or **neutral oxides** '
                                    'are formed (e.g. **SO₂, CO₂** are acidic; **CO, H₂O** are neutral).',
                    'marking_points': ['Acidic or neutral oxides stated', 'Contrast with basic metal oxides optional'],
                    'common_mistakes': ['Saying basic oxides', 'No type named'],
                    'concept_ids': ['u3_d8_c04', 'u3_d8_c06', 'u3_d8_c08'],
                    'misconception': 'metal_nonmetal_property_swap',
                    'guided_tool': None,
                    'ncert_ref': 'NCERT Ch 3 Exercises Q11'},
                   {'id': 'u3_ex_q12',
                    'num': 12,
                    'type': 'explain',
                    'marks': 5,
                    'question': 'Give reasons\n'
                                '(a) Platinum, gold and silver are used to make jewellery.\n'
                                '(b) Sodium, potassium and lithium are stored under oil.\n'
                                '(c) Aluminium is a highly reactive metal, yet it is used to make utensils for '
                                'cooking.\n'
                                '(d) Carbonate and sulphide ores are usually converted into oxides during the process '
                                'of extraction.',
                    'hints': ['(a) lustre, low reactivity.',
                              '(b) react violently with air/water.',
                              '(c) protective Al₂O₃ layer.',
                              '(d) oxides easier to reduce.'],
                    'model_answer': '(a) **Pt, Au, Ag** are **lustrous** and **least reactive** — do not tarnish '
                                    'easily → suitable for jewellery.\n'
                                    '\n'
                                    '(b) **Na, K, Li** are **highly reactive** — react with **moist air/water**; '
                                    'stored under **oil** to exclude air and moisture.\n'
                                    '\n'
                                    '(c) **Al** forms a **stable oxide layer (Al₂O₃)** that prevents further corrosion '
                                    '— safe and durable for utensils despite reactivity.\n'
                                    '\n'
                                    '(d) **Carbonate/sulphide ores** are converted to **oxides** '
                                    '(calcination/roasting) because **oxides are easier to reduce** to metal than '
                                    'carbonates or sulphides.',
                    'marking_points': ['(a) lustrous + low reactivity',
                                       '(b) highly reactive — kept from air/water',
                                       '(c) protective Al₂O₃ layer',
                                       '(d) oxides easier to reduce'],
                    'common_mistakes': ['Incomplete reasons', 'Swapping (b) and (c) explanations'],
                    'concept_ids': ['u3_d1_c03', 'u3_d7_c01', 'u3_d13_c01'],
                    'misconception': 'reactivity_series_order_error',
                    'guided_tool': None,
                    'ncert_ref': 'NCERT Ch 3 Exercises Q12'},
                   {'id': 'u3_ex_q13',
                    'num': 13,
                    'type': 'explain',
                    'marks': 2,
                    'question': 'You must have seen tarnished copper vessels being cleaned with lemon or tamarind '
                                'juice. Explain why these sour substances are effective in cleaning the vessels.',
                    'hints': ['Tarnish = basic copper carbonate.',
                              'Acids in lemon/tamarind react with it.',
                              'Product washes away.'],
                    'model_answer': 'Tarnished copper has a **green coating of basic copper carbonate** '
                                    '(CuCO₃·Cu(OH)₂) formed by reaction with moist CO₂.\n'
                                    '\n'
                                    '**Lemon/tamarind juice** contains **acids** that **react with the basic '
                                    'tarnish**, dissolving it and restoring the shiny copper surface.',
                    'marking_points': ['Tarnish is basic copper carbonate',
                                       'Acids in juice react with basic coating',
                                       'Coating removed — copper shines'],
                    'common_mistakes': ['Saying tarnish is acidic', 'No mention of acid-base reaction'],
                    'concept_ids': ['u3_d16_c01', 'u3_d6_c05', 'u3_d8_c04'],
                    'misconception': 'corrosion_prevention_wrong',
                    'guided_tool': None,
                    'ncert_ref': 'NCERT Ch 3 Exercises Q13'},
                   {'id': 'u3_ex_q14',
                    'num': 14,
                    'type': 'differentiate',
                    'marks': 4,
                    'question': 'Differentiate between metal and non-metal on the basis of their chemical properties.',
                    'hints': ['Ion formation, oxides, reaction with water/acids.',
                              'At least 3–4 contrast points.',
                              'Examples help.'],
                    'model_answer': '| Property | Metals | Non-metals |\n'
                                    '|---|---|---|\n'
                                    '| **Valence electrons** | Lose e⁻ → **cations** | Gain e⁻ → **anions** |\n'
                                    '| **Oxides** | **Basic** (some amphoteric) | **Acidic/neutral** |\n'
                                    '| **With water** | Some react (Na, Ca) | Generally do not |\n'
                                    '| **With dilute acids** | Above H in series give H₂ | Do **not** displace H from '
                                    'dilute acids |\n'
                                    '| **Nature of bonds** | Metallic / ionic in compounds | Covalent in compounds |',
                    'marking_points': ['At least 3 valid chemical contrasts', 'Examples for metal and non-metal'],
                    'common_mistakes': ['Listing only physical properties', 'Fewer than 3 differences'],
                    'concept_ids': ['u3_d6_c01', 'u3_d8_c04', 'u3_d9_c04'],
                    'misconception': 'metal_nonmetal_property_swap',
                    'guided_tool': None,
                    'ncert_ref': 'NCERT Ch 3 Exercises Q14'},
                   {'id': 'u3_ex_q15',
                    'num': 15,
                    'type': 'reasoning',
                    'marks': 3,
                    'question': 'A man went door to door posing as a goldsmith. He promised to bring back the glitter '
                                'of old and dull gold ornaments. An unsuspecting lady gave a set of gold bangles to '
                                'him which he dipped in a particular solution. The bangles sparkled like new but their '
                                'weight was reduced drastically. The lady was upset but after a futile argument the '
                                'man beat a hasty retreat. Can you play the detective to find out the nature of the '
                                'solution he had used?',
                    'hints': ['Gold unreactive to simple acids.',
                              'Aqua regia dissolves gold.',
                              'Weight loss = gold removed.'],
                    'model_answer': 'The solution was likely **aqua regia** — a **3:1 mixture of concentrated HCl and '
                                    'HNO₃**.\n'
                                    '\n'
                                    '**Aqua regia** can **dissolve gold** (even though gold does not react with '
                                    "individual acids). Some gold dissolved during 'cleaning', reducing weight while "
                                    'surface looked shiny initially.',
                    'marking_points': ['Aqua regia identified or HCl + HNO₃ mixture',
                                       'Dissolves gold',
                                       'Explains weight loss'],
                    'common_mistakes': ['Saying dilute HCl alone', 'No link to weight loss'],
                    'concept_ids': ['u3_d10_c08', 'u3_d10_c09', 'u3_d1_c03'],
                    'misconception': 'reactivity_series_order_error',
                    'guided_tool': None,
                    'ncert_ref': 'NCERT Ch 3 Exercises Q15'},
                   {'id': 'u3_ex_q16',
                    'num': 16,
                    'type': 'explain',
                    'marks': 2,
                    'question': 'Give reasons why copper is used to make hot water tanks and not steel (an alloy of '
                                'iron).',
                    'hints': ['Copper resists corrosion in hot water.',
                              'Steel/iron rusts.',
                              'Copper good conductor — not main reason here.'],
                    'model_answer': '**Copper** does **not react** with **hot water or steam** easily and is '
                                    '**corrosion-resistant** in hot water systems.\n'
                                    '\n'
                                    '**Steel (iron)** would **rust** when constantly in contact with hot water and '
                                    'air, making it unsuitable for hot water tanks.',
                    'marking_points': ['Copper unreactive / corrosion resistant in hot water', 'Steel/iron rusts'],
                    'common_mistakes': ['Saying copper is cheaper', 'Only mentioning conductivity'],
                    'concept_ids': ['u3_d16_c02', 'u3_d3_c01', 'u3_d7_c05'],
                    'misconception': 'corrosion_prevention_wrong',
                    'guided_tool': None,
                    'ncert_ref': 'NCERT Ch 3 Exercises Q16'}]},
 4: {'meta': {'unit_id': 4, 'chapter': 4, 'pdf': 'jesc104.pdf', 'title': 'Carbon and its Compounds'},
     'activities': [{'id': '4.1',
                     'title': 'Carbon in daily objects',
                     'summary': 'List items used since morning; sort into metal, glass/clay, carbon-compound columns.',
                     'concept_ids': ['u4_d1_c01', 'u4_d1_c03', 'u4_d1_c05'],
                     'stage2_day': 17},
                    {'id': '4.2',
                     'title': 'Homologous series of alcohols',
                     'summary': 'Compare formulae and masses of CH₃OH, C₂H₅OH, C₃H₇OH, C₄H₉OH; identify homologous '
                                'pattern.',
                     'concept_ids': ['u4_d5_c01', 'u4_d5_c03', 'u4_d5_c05'],
                     'stage2_day': 17},
                    {'id': '4.3',
                     'title': 'Models of carbon compounds',
                     'summary': 'Use molecular model kits to build methane, ethane, ethene, ethyne structures.',
                     'concept_ids': ['u4_d2_c01', 'u4_d2_c04', 'u4_d2_c06'],
                     'stage2_day': 17},
                    {'id': '4.4',
                     'title': 'Burning carbon compounds',
                     'summary': 'Burn small samples; test flame and residue; relate to saturated/unsaturated nature.',
                     'concept_ids': ['u4_d4_c01', 'u4_d4_c03', 'u4_d4_c06'],
                     'stage2_day': 18},
                    {'id': '4.5',
                     'title': 'Bromine water test',
                     'summary': 'Add bromine water to hydrocarbon samples; note decolourisation with unsaturated '
                                'compounds.',
                     'concept_ids': ['u4_d4_c04', 'u4_d4_c07', 'u4_d4_c08'],
                     'stage2_day': 18},
                    {'id': '4.6',
                     'title': 'Functional group identification',
                     'summary': 'Build and name alcohols, aldehydes, ketones, carboxylic acids from model kits.',
                     'concept_ids': ['u4_d6_c04', 'u4_d7_c02', 'u4_d7_c05'],
                     'stage2_day': 18},
                    {'id': '4.7',
                     'title': 'Esterification',
                     'summary': 'Warm ethanol and acetic acid with conc. H₂SO₄; smell fruity ester formed.',
                     'concept_ids': ['u4_d8_c01', 'u4_d8_c03', 'u4_d8_c05'],
                     'stage2_day': 19},
                    {'id': '4.8',
                     'title': 'Saponification',
                     'summary': 'Heat vegetable oil with NaOH; add salt to precipitate soap.',
                     'concept_ids': ['u4_d13_c01', 'u4_d13_c03', 'u4_d13_c05'],
                     'stage2_day': 19},
                    {'id': '4.9',
                     'title': 'Hydrogenation of oil',
                     'summary': 'Discuss nickel-catalysed addition of H₂ to vegetable oil forming vanaspati ghee.',
                     'concept_ids': ['u4_d9_c01', 'u4_d9_c03', 'u4_d9_c05'],
                     'stage2_day': 19},
                    {'id': '4.10',
                     'title': 'Ethanol reactions',
                     'summary': 'Study reactions of ethanol — combustion, oxidation to ethanoic acid, esterification.',
                     'concept_ids': ['u4_d11_c01', 'u4_d11_c03', 'u4_d11_c05'],
                     'stage2_day': 20},
                    {'id': '4.11',
                     'title': 'Soap vs detergent in hard water',
                     'summary': 'Shake soap and detergent solutions separately in hard water; compare foam and scum.',
                     'concept_ids': ['u4_d13_c04', 'u4_d13_c06', 'u4_d13_c08'],
                     'stage2_day': 20},
                    {'id': '4.12',
                     'title': 'Micelle demonstration',
                     'summary': 'Discuss how soap forms micelles around oily dirt in water.',
                     'concept_ids': ['u4_d13_c07', 'u4_d13_c09', 'u4_d13_c10'],
                     'stage2_day': 20}],
     'exercise_mcqs': [{'num': 1,
                        'question': 'Ethane, with the molecular formula C₂H₆ has',
                        'options': ['6 covalent bonds', '7 covalent bonds', '8 covalent bonds', '9 covalent bonds'],
                        'answer': 1,
                        'explanation': 'C₂H₆ has 1 C–C + 6 C–H = 7 single covalent bonds.',
                        'misconception': 'saturated_unsaturated_swap',
                        'source': 'NCERT Ch 4 Exercises Q1'},
                       {'num': 2,
                        'question': 'Butanone is a four-carbon compound with the functional group',
                        'options': ['carboxylic acid', 'aldehyde', 'ketone', 'alcohol'],
                        'answer': 2,
                        'explanation': 'Butanone (CH₃COC₂H₅) contains the ketone (–CO–) functional group.',
                        'misconception': 'functional_group_naming_error',
                        'source': 'NCERT Ch 4 Exercises Q2'},
                       {'num': 3,
                        'question': 'While cooking, if the bottom of the vessel is getting blackened on the outside, '
                                    'it means that',
                        'options': ['the food is not cooked completely',
                                    'the fuel is not burning completely',
                                    'the fuel is wet',
                                    'the fuel is burning completely'],
                        'answer': 1,
                        'explanation': 'Black soot from incomplete combustion deposits on the vessel bottom.',
                        'misconception': 'addition_substitution_confusion',
                        'source': 'NCERT Ch 4 Exercises Q3'}],
     'intext_samples': [{'ref': 'Section 4.1 — covalent bond',
                         'question': 'Carbon compounds are generally poor conductors because they have',
                         'options': ['ionic bonds',
                                     'covalent bonds with shared electrons',
                                     'free electrons like metals',
                                     'metallic bonds'],
                         'answer': 1,
                         'explanation': 'Carbon compounds form covalent bonds — no free ions/electrons in solid state.',
                         'misconception': 'ionic_covalent_confusion',
                         'source': 'NCERT Ch 4 Intext'},
                        {'ref': 'Section 4.2 — catenation',
                         'question': 'Carbon forms a large number of compounds mainly due to',
                         'options': ['ionic bonding',
                                     'catenation and tetravalency',
                                     'metallic nature',
                                     'high melting point'],
                         'answer': 1,
                         'explanation': 'Catenation (self-linking) and tetravalency give carbon its versatility.',
                         'misconception': 'ionic_covalent_confusion',
                         'source': 'NCERT Ch 4 Intext'},
                        {'ref': 'Section 4.3 — saturated hydrocarbons',
                         'question': 'The general formula of alkanes is',
                         'options': ['CₙH₂ₙ', 'CₙH₂ₙ₊₂', 'CₙH₂ₙ₋₂', 'CₙHₙ'],
                         'answer': 1,
                         'explanation': 'Alkanes are saturated with formula CₙH₂ₙ₊₂.',
                         'misconception': 'saturated_unsaturated_swap',
                         'source': 'NCERT Ch 4 Intext'},
                        {'ref': 'Section 4.4 — bromine test',
                         'question': 'Bromine water decolourises when added to',
                         'options': ['ethane', 'propane', 'ethene', 'butane'],
                         'answer': 2,
                         'explanation': 'Ethene (unsaturated) undergoes addition with bromine; alkanes do not '
                                        'decolourise bromine water.',
                         'misconception': 'addition_substitution_confusion',
                         'source': 'NCERT Ch 4 Intext'},
                        {'ref': 'Section 4.5 — ethanol',
                         'question': 'On adding alkaline KMnO₄ to ethanol and warming, ethanol is oxidised to',
                         'options': ['ethene', 'ethanoic acid', 'ethanal', 'methane'],
                         'answer': 1,
                         'explanation': 'Alkaline KMnO₄ oxidises ethanol (primary alcohol) to ethanoic acid.',
                         'misconception': 'functional_group_naming_error',
                         'source': 'NCERT Ch 4 Intext'},
                        {'ref': 'Section 4.6 — soaps',
                         'question': 'Soap does not work well in hard water because it forms',
                         'options': ['micelles', 'scum with Ca²⁺/Mg²⁺ ions', 'more lather', 'detergent'],
                         'answer': 1,
                         'explanation': 'Soap reacts with Ca²⁺ and Mg²⁺ in hard water forming insoluble scum.',
                         'misconception': 'soap_detergent_hard_water_error',
                         'source': 'NCERT Ch 4 Intext'}],
     'exercise_meta': {'active': True,
                       'stage': 3,
                       'range': 'Exercises Q4–Q15',
                       'note': 'Exam-style written questions. Chapter 4 has 3 MCQs (Stage 2) and 12 long-form '
                               'exercises here.',
                       'chapter': 'NCERT Class 10 Science Ch 4',
                       'pdf': 'jesc104.pdf'},
     'exercises': [{'id': 'u4_ex_q04',
                    'num': 4,
                    'type': 'explain',
                    'marks': 3,
                    'question': 'Explain the nature of the covalent bond using the bond formation in CH₃Cl.',
                    'hints': ['C and H/Cl share electrons.', 'Single shared pairs.', 'Complete outer shells.'],
                    'model_answer': 'A **covalent bond** is formed by **sharing of electron pairs** between atoms so '
                                    'each achieves a **stable outer shell**.\n'
                                    '\n'
                                    'In **CH₃Cl**: carbon shares **3 electrons** with three H atoms and **1 electron** '
                                    'with Cl — **four single covalent bonds**; each atom gets a noble-gas-like outer '
                                    'configuration.',
                    'marking_points': ['Covalent bond = shared electron pair',
                                       'CH₃Cl has 4 single bonds',
                                       'Atoms achieve stable outer shell'],
                    'common_mistakes': ['Describing ionic transfer for CH₃Cl', 'Wrong bond count'],
                    'concept_ids': ['u4_d2_c01', 'u4_d2_c04', 'u4_d2_c06'],
                    'misconception': 'ionic_covalent_confusion',
                    'guided_tool': None,
                    'ncert_ref': 'NCERT Ch 4 Exercises Q4'},
                   {'id': 'u4_ex_q05',
                    'num': 5,
                    'type': 'diagram',
                    'marks': 4,
                    'question': 'Draw the electron dot structures for\n'
                                '(a) ethanoic acid.\n'
                                '(b) H₂S.\n'
                                '(c) propanone.\n'
                                '(d) F₂.',
                    'hints': ['Show shared pairs as dots/crosses.',
                              'Ethanoic acid: COOH group.',
                              'Propanone: C=O between carbons.'],
                    'model_answer': '(a) **Ethanoic acid (CH₃COOH):** methyl group bonded to carboxyl — C=O and O–H on '
                                    'same carbon.\n'
                                    '\n'
                                    '(b) **H₂S:** H–S–H with two lone pairs on S.\n'
                                    '\n'
                                    '(c) **Propanone (CH₃COCH₃):** central C=O with CH₃ groups on both sides.\n'
                                    '\n'
                                    '(d) **F₂:** F–F single bond with three lone pairs on each F.',
                    'marking_points': ['Four correct electron dot structures', 'Correct number of bonds in each'],
                    'common_mistakes': ['Ionic structure shown', 'Missing lone pairs on heteroatoms'],
                    'concept_ids': ['u4_d2_c04', 'u4_d6_c04', 'u4_d7_c02'],
                    'misconception': 'ionic_covalent_confusion',
                    'guided_tool': None,
                    'ncert_ref': 'NCERT Ch 4 Exercises Q5'},
                   {'id': 'u4_ex_q06',
                    'num': 6,
                    'type': 'explain',
                    'marks': 3,
                    'question': 'What is an homologous series? Explain with an example.',
                    'hints': ['Same functional group.',
                              'Successive members differ by CH₂.',
                              'Gradation in physical properties.'],
                    'model_answer': 'A **homologous series** is a family of compounds with the **same functional '
                                    'group** and **similar chemical properties**, successive members differing by a '
                                    '**–CH₂–** unit.\n'
                                    '\n'
                                    'Example: **Alcohols** — CH₃OH (methanol), C₂H₅OH (ethanol), C₃H₇OH (propanol) … '
                                    'differ by CH₂; boiling points increase with chain length.',
                    'marking_points': ['Definition with functional group + CH₂ difference',
                                       'Example series named',
                                       'Similar chemical properties mentioned'],
                    'common_mistakes': ['No CH₂ difference stated', 'Wrong example (not a series)'],
                    'concept_ids': ['u4_d5_c01', 'u4_d5_c03', 'u4_d5_c05'],
                    'misconception': 'functional_group_naming_error',
                    'guided_tool': None,
                    'ncert_ref': 'NCERT Ch 4 Exercises Q6'},
                   {'id': 'u4_ex_q07',
                    'num': 7,
                    'type': 'differentiate',
                    'marks': 4,
                    'question': 'How can ethanol and ethanoic acid be differentiated on the basis of their physical '
                                'and chemical properties?',
                    'hints': ['Smell, pH, reaction with Na₂CO₃.',
                              'Ethanoic acid is sour / turns blue litmus red.',
                              'Ethanol neutral — no reaction with carbonates.'],
                    'model_answer': '**Physical:** Ethanol has **pleasant alcoholic odour**; ethanoic acid has '
                                    '**pungent vinegar smell**. Ethanoic acid **turns blue litmus red** (acidic); '
                                    'ethanol is **neutral**.\n'
                                    '\n'
                                    '**Chemical:** Ethanoic acid reacts with **Na₂CO₃/NaHCO₃** to evolve **CO₂**; '
                                    'ethanol does **not**. Ethanoic acid **esterifies** with alcohol in presence of '
                                    'acid catalyst; ethanol alone does not show this as acid.',
                    'marking_points': ['At least one physical difference',
                                       'At least one chemical test (e.g. carbonate reaction)',
                                       'Correct observation for each'],
                    'common_mistakes': ['Only physical or only chemical', 'Swapping properties'],
                    'concept_ids': ['u4_d11_c01', 'u4_d12_c01', 'u4_d12_c03'],
                    'misconception': 'functional_group_naming_error',
                    'guided_tool': None,
                    'ncert_ref': 'NCERT Ch 4 Exercises Q7'},
                   {'id': 'u4_ex_q08',
                    'num': 8,
                    'type': 'explain',
                    'marks': 3,
                    'question': 'Why does micelle formation take place when soap is added to water? Will a micelle be '
                                'formed in other solvents such as ethanol also?',
                    'hints': ['Soap has hydrophobic tail and hydrophilic head.',
                              'Micelles trap oily dirt.',
                              'Ethanol dissolves both — no micelles.'],
                    'model_answer': 'Soap molecules have a **hydrophobic hydrocarbon tail** and **hydrophilic ionic '
                                    'head**. In water, tails cluster inward away from water while heads face outward → '
                                    '**micelle**.\n'
                                    '\n'
                                    'In **ethanol**, soap **dissolves** uniformly — **micelles do not form** because '
                                    'ethanol solubilises both polar and non-polar parts.',
                    'marking_points': ['Hydrophobic/hydrophilic parts described',
                                       'Micelle structure in water',
                                       'No micelles in ethanol — reason given'],
                    'common_mistakes': ['No mention of dual nature of soap', 'Saying micelles form in ethanol'],
                    'concept_ids': ['u4_d13_c07', 'u4_d13_c09', 'u4_d13_c10'],
                    'misconception': 'soap_detergent_hard_water_error',
                    'guided_tool': None,
                    'ncert_ref': 'NCERT Ch 4 Exercises Q8'},
                   {'id': 'u4_ex_q09',
                    'num': 9,
                    'type': 'explain',
                    'marks': 2,
                    'question': 'Why are carbon and its compounds used as fuels for most applications?',
                    'hints': ['Burn in oxygen releasing large energy.',
                              'Hydrocarbons combust to CO₂ and H₂O.',
                              'Readily available (coal, petroleum, natural gas).'],
                    'model_answer': 'Carbon compounds (hydrocarbons) **burn in oxygen** releasing **large amounts of '
                                    'heat energy** with **controlled flame**.\n'
                                    '\n'
                                    'They are **abundant** (coal, petroleum, natural gas, LPG) and **easy to '
                                    'store/transport**, making them ideal **fuels** for homes, industry, and vehicles.',
                    'marking_points': ['Exothermic combustion',
                                       'Hydrocarbons as energy source',
                                       'Availability/practical use'],
                    'common_mistakes': ['Saying they are nuclear fuels', 'No energy release mentioned'],
                    'concept_ids': ['u4_d4_c01', 'u4_d10_c01', 'u4_d10_c03'],
                    'misconception': 'addition_substitution_confusion',
                    'guided_tool': None,
                    'ncert_ref': 'NCERT Ch 4 Exercises Q9'},
                   {'id': 'u4_ex_q10',
                    'num': 10,
                    'type': 'explain',
                    'marks': 3,
                    'question': 'Explain the formation of scum when hard water is treated with soap.',
                    'hints': ['Hard water has Ca²⁺ and Mg²⁺.',
                              'Soap is sodium/potassium salt of fatty acids.',
                              'Insoluble Ca/Mg salts = scum.'],
                    'model_answer': '**Hard water** contains **Ca²⁺ and Mg²⁺ ions**. Soap (sodium stearate etc.) '
                                    'reacts with these ions to form **insoluble calcium/magnesium salts** of fatty '
                                    'acids — **scum** — instead of lather.\n'
                                    '\n'
                                    '2C₁₇H₃₅COONa + Ca²⁺ → (C₁₇H₃₅COO)₂Ca ↓ + 2Na⁺',
                    'marking_points': ['Ca²⁺/Mg²⁺ in hard water',
                                       'Insoluble salt formed with soap',
                                       'Scum reduces lather'],
                    'common_mistakes': ['Scum is soap itself', 'No mention of calcium/magnesium ions'],
                    'concept_ids': ['u4_d13_c04', 'u4_d13_c06', 'u4_d13_c08'],
                    'misconception': 'soap_detergent_hard_water_error',
                    'guided_tool': None,
                    'ncert_ref': 'NCERT Ch 4 Exercises Q10'},
                   {'id': 'u4_ex_q11',
                    'num': 11,
                    'type': 'explain',
                    'marks': 2,
                    'question': 'What change will you observe if you test soap with litmus paper (red and blue)?',
                    'hints': ['Soap is basic salt of strong base + weak acid.',
                              'Turns red litmus blue.',
                              'Blue litmus unchanged.'],
                    'model_answer': 'Soap solution is **basic** (salt of strong base NaOH/KOH and weak fatty acid).\n'
                                    '\n'
                                    '**Red litmus turns blue**; **blue litmus stays blue** (no change).',
                    'marking_points': ['Soap is basic', 'Red litmus → blue', 'Blue litmus unchanged'],
                    'common_mistakes': ['Saying soap is acidic', 'Both litmus papers turn red'],
                    'concept_ids': ['u4_d13_c02', 'u4_d13_c04', 'u4_d13_c06'],
                    'misconception': 'soap_detergent_hard_water_error',
                    'guided_tool': None,
                    'ncert_ref': 'NCERT Ch 4 Exercises Q11'},
                   {'id': 'u4_ex_q12',
                    'num': 12,
                    'type': 'explain',
                    'marks': 3,
                    'question': 'What is hydrogenation? What is its industrial application?',
                    'hints': ['Addition of H₂ to unsaturated compounds.',
                              'Nickel catalyst.',
                              'Vanaspati ghee from vegetable oils.'],
                    'model_answer': '**Hydrogenation** is the **addition of hydrogen** to an **unsaturated compound** '
                                    '(alkene/vegetable oil) in presence of a **catalyst** (Ni/Pd/Pt).\n'
                                    '\n'
                                    '**Industrial use:** Manufacture of **vanaspati ghee** by hydrogenating '
                                    '**vegetable oils** (liquid) to **saturated fats** (semi-solid).',
                    'marking_points': ['Hydrogenation defined as H₂ addition',
                                       'Catalyst mentioned',
                                       'Vanaspati / vegetable oil example'],
                    'common_mistakes': ['Calling it substitution', 'No industrial application'],
                    'concept_ids': ['u4_d9_c01', 'u4_d9_c03', 'u4_d9_c05'],
                    'misconception': 'addition_substitution_confusion',
                    'guided_tool': None,
                    'ncert_ref': 'NCERT Ch 4 Exercises Q12'},
                   {'id': 'u4_ex_q13',
                    'num': 13,
                    'type': 'identify',
                    'marks': 2,
                    'question': 'Which of the following hydrocarbons undergo addition reactions: C₂H₆, C₃H₈, C₃H₆, '
                                'C₂H₂ and CH₄.',
                    'hints': ['Addition in unsaturated (double/triple bond).',
                              'Alkenes and alkynes.',
                              'Alkanes undergo substitution.'],
                    'model_answer': 'Hydrocarbons that undergo **addition reactions** are **unsaturated** ones: **C₃H₆ '
                                    '(propene)** and **C₂H₂ (ethyne)**.\n'
                                    '\n'
                                    '**C₂H₆, C₃H₈, CH₄** are **saturated alkanes** — undergo **substitution**, not '
                                    'addition.',
                    'marking_points': ['C₃H₆ and C₂H₂ identified', 'Reason: unsaturated / double or triple bond'],
                    'common_mistakes': ['Including alkanes', 'All five listed'],
                    'concept_ids': ['u4_d4_c01', 'u4_d4_c03', 'u4_d9_c01'],
                    'misconception': 'addition_substitution_confusion',
                    'guided_tool': None,
                    'ncert_ref': 'NCERT Ch 4 Exercises Q13'},
                   {'id': 'u4_ex_q14',
                    'num': 14,
                    'type': 'explain',
                    'marks': 2,
                    'question': 'Give a test that can be used to differentiate between saturated and unsaturated '
                                'hydrocarbons.',
                    'hints': ['Bromine water test.', 'Unsaturated decolourises.', 'Saturated — no change.'],
                    'model_answer': 'Add **bromine water** (reddish-brown) to the hydrocarbon.\n'
                                    '\n'
                                    '**Unsaturated** hydrocarbon **decolourises** bromine water (addition reaction).\n'
                                    '\n'
                                    '**Saturated** hydrocarbon **does not decolourise** bromine water.',
                    'marking_points': ['Bromine water test described',
                                       'Different observation for saturated vs unsaturated'],
                    'common_mistakes': ['Using litmus test', 'Wrong reagent'],
                    'concept_ids': ['u4_d4_c04', 'u4_d4_c07', 'u4_d4_c08'],
                    'misconception': 'saturated_unsaturated_swap',
                    'guided_tool': None,
                    'ncert_ref': 'NCERT Ch 4 Exercises Q14'},
                   {'id': 'u4_ex_q15',
                    'num': 15,
                    'type': 'explain',
                    'marks': 4,
                    'question': 'Explain the mechanism of the cleaning action of soaps.',
                    'hints': ['Hydrophobic tail dissolves in oil.',
                              'Hydrophilic head in water.',
                              'Micelles washed away.'],
                    'model_answer': 'Soap **cleans** by **emulsifying oily dirt**:\n'
                                    '1. Soap molecules have **hydrophobic tail** (dissolves in oil/grease) and '
                                    '**hydrophilic head** (in water).\n'
                                    '2. In water, molecules form **micelles** — tails inward trapping oil, heads '
                                    'outward.\n'
                                    '3. **Agitation** breaks grease into droplets surrounded by soap.\n'
                                    '4. Micelles stay **dispersed** in water and are **rinsed away**, removing dirt.',
                    'marking_points': ['Dual nature of soap molecule',
                                       'Micelle formation',
                                       'Oil trapped inside micelle',
                                       'Rinsing removes dirt'],
                    'common_mistakes': ['Only saying soap is basic', 'No micelle/emulsification'],
                    'concept_ids': ['u4_d13_c07', 'u4_d13_c09', 'u4_d13_c10'],
                    'misconception': 'soap_detergent_hard_water_error',
                    'guided_tool': None,
                    'ncert_ref': 'NCERT Ch 4 Exercises Q15'}]}}
