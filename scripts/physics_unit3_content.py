"""Full concept card content for Harshit Physics Unit 3 — Days 1–16 (Ch 11 Electricity)."""

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


DAY1 = _build_day(
    1,
    [
        ("Electricity in daily life", "Electricity is a controllable, convenient form of energy used in homes, schools, hospitals and industries.", "electric_circuit", {"highlight": "overview"}, "Most modern devices depend on electric circuits.", "Lights, fans and phones all need electricity.", "Electricity = controlled energy via circuits.", "", "", []),
        ("What is electric current?", "When electric charge flows through a conductor (like a metallic wire), we say there is an electric current in it.", "electric_circuit", {"highlight": "current_flow"}, "Current is moving charge — like water current in a river.", "Torch bulb glows when charges flow through it.", "Flow of charge in conductor = current.", "", "", ["electric current"]),
        ("Electrons carry current in wires", "In metallic wires, electrons constitute the flow of charges that make up electric current.", "electric_circuit", {"highlight": "electrons"}, "Electrons are mobile in metals.", "Copper wires in home circuits carry electron drift.", "Metallic current = electron flow.", "Current is not always positive charges in reality.", "", []),
        ("Conventional current direction", "Conventionally, current direction is taken as opposite to electron flow — as if positive charges move from cell + to −.", "electric_circuit", {"highlight": "conventional"}, "Historical convention before electrons were known.", "Arrow on circuit diagrams shows conventional current.", "Conventional current: + terminal to − terminal.", "Do not draw electrons moving the same way as conventional arrow.", "", []),
        ("Electric circuit", "A continuous and closed path for electric current is called an electric circuit.", "electric_circuit", {"highlight": "closed_path"}, "Break anywhere stops the current.", "Open switch → torch off; closed switch → bulb on.", "Closed loop needed for steady current.", "Open circuit ≠ zero voltage always.", "", ["electric circuit"]),
        ("Role of a switch", "A switch makes or breaks the conducting link between the cell and the bulb (or other component).", "electric_circuit", {"highlight": "switch"}, "Controls current without removing the cell.", "Wall switch completes room light circuit.", "Switch ON = closed path; OFF = break.", "", "", []),
        ("Cell and battery in a torch", "Cells (or a battery in proper order) provide flow of charges — current — through the torch bulb.", "electric_circuit", {"highlight": "cell"}, "The source drives charge around the loop.", "Two AA cells in series in a torch.", "Cell/battery pushes charges in circuit.", "", "", ["cell"]),
        ("Circuit must be closed", "If the circuit is broken anywhere, current stops and the bulb does not glow.", "electric_circuit", {"mode": "open_circuit"}, "Explains why loose connections fail.", "Unplugged wire → no current.", "Open circuit → no current.", "", "", []),
        ("Rate of flow of charge", "Electric current is the rate of flow of electric charges through a cross-section: amount of charge per unit time.", "formula_panel", {"formula": "I = Q / t", "label": "Electric current"}, "Links measurable Q and t to current.", "More charge passing per second = larger current.", "Current = charge flowing per second.", "I is not the same as total charge Q.", "", ["ampere"]),
        ("Water current analogy", "Just as flowing water is water current, flowing electric charge is electric current.", "electric_circuit", {"mode": "analogy"}, "Analogy helps before formulas.", "River current vs wire current.", "Moving charges ↔ moving water.", "Water and charge analogies break at atomic scale.", "", []),
    ],
)

DAY2 = _build_day(
    2,
    [
        ("Current formula I = Q/t", "If net charge Q flows across a cross-section in time t, current I = Q/t.", "formula_panel", {"formula": "I = Q / t", "label": "Eq. 11.1"}, "Central numerical formula for current.", "0.5 A for 600 s → Q = 300 C (Example 11.1).", "I = Q/t; rearrange for Q = It.", "Use t in seconds for SI.", "", []),
        ("Coulomb — unit of charge", "SI unit of charge is coulomb (C). One coulomb equals charge of about 6 × 10¹⁸ electrons.", "formula_panel", {"formula": "1 C ≈ 6×10¹⁸ electrons", "label": "Coulomb"}, "Connects electron charge to macroscopic Q.", "Electron charge = 1.6 × 10⁻¹⁹ C each.", "Charge unit: coulomb (C).", "", "", ["coulomb"]),
        ("Ampere — unit of current", "One ampere (A) is flow of one coulomb of charge per second: 1 A = 1 C/s.", "formula_panel", {"formula": "1 A = 1 C / 1 s", "label": "Ampere"}, "Named after André-Marie Ampère.", "2 A means 2 coulombs pass each second.", "1 A = 1 C per second.", "Do not write A as coulomb alone.", "", ["ampere"]),
        ("Milliampere and microampere", "Small currents: 1 mA = 10⁻³ A; 1 µA = 10⁻⁶ A.", "formula_panel", {"formula": "mA, µA prefixes", "label": "Small currents"}, "Electronic devices often use mA.", "LED might draw a few mA.", "mA and µA for tiny currents.", "", "", []),
        ("Ammeter", "An ammeter measures electric current. It is always connected in series in the circuit.", "electric_circuit", {"highlight": "ammeter"}, "Must carry the current you measure.", "Ammeter in series with bulb in Fig 11.1.", "Ammeter in series only.", "Never connect ammeter in parallel across battery.", "", ["ammeter"]),
        ("Schematic diagram Fig 11.1", "NCERT Fig 11.1: cell, bulb, ammeter and plug key in one closed loop.", "electric_circuit", {"mode": "fig_11_1"}, "Standard diagram to copy in exams.", "Draw and label all four parts.", "Cell → bulb → ammeter → key → back to cell.", "", "", []),
        ("Current direction in diagram", "In the diagram, conventional current flows from positive terminal of cell, through bulb and ammeter, back to negative terminal.", "electric_circuit", {"highlight": "direction"}, "Matches conventional current rule.", "Arrow from + of cell through external circuit.", "+ to − through external path.", "", "", []),
        ("Example 11.1 idea", "I = 0.5 A for t = 10 min = 600 s → Q = It = 300 C flows through the bulb.", "formula_panel", {"formula": "Q = I × t", "label": "Charge calculation"}, "Typical NCERT numerical.", "Convert minutes to seconds first.", "Q = It; watch time units.", "", "", []),
        ("Electrons vs convention revisited", "Electrons move from − to + inside external wire, but we draw current from + to −.", "electric_circuit", {"mode": "electron_vs_conventional"}, "Both descriptions coexist in Class 10.", "Exam diagrams use conventional arrows.", "Convention opposite to electron drift.", "", "", []),
        ("What an electric circuit means", "A circuit means a closed conducting path connecting source, switch, load and meters as needed.", "electric_circuit", {"mode": "definition"}, "NCERT Q1 answer anchor.", "Torch wiring is a simple circuit.", "Closed path + source + components.", "", "", []),
    ],
)

DAY3 = _build_day(
    3,
    [
        ("Potential difference drives current", "Charges flow in a wire only if there is electric potential difference (electric pressure) along the conductor.", "electric_circuit", {"highlight": "pd_drive"}, "Like water flowing due to height difference.", "Battery creates pressure difference for electrons.", "No PD → no sustained current.", "", "", ["potential difference"]),
        ("Water pressure analogy", "Water does not flow in a horizontal tube unless one end is at higher pressure — same idea for charge.", "electric_circuit", {"mode": "water_analogy"}, "Explains need for a source.", "Tank at height pushes water through pipe.", "PD is electrical 'pressure difference'.", "", "", []),
        ("Cell maintains PD", "Chemical action in a cell generates potential difference across terminals even when no current is drawn.", "electric_circuit", {"highlight": "cell"}, "Battery stores chemical energy.", "Multimeter reads ~1.5 V on new dry cell.", "Cell creates PD across terminals.", "", "", []),
        ("Potential difference definition", "PD between two points = work done per unit charge moved between them: V = W/Q.", "formula_panel", {"formula": "V = W / Q", "label": "Eq. 11.2"}, "Links energy and charge.", "Moving 2 C with 12 J work → V = 6 V.", "V = W/Q.", "W is work in joules, Q in coulombs.", "", ["volt"]),
        ("Volt — unit of PD", "One volt: 1 joule of work per coulomb — 1 V = 1 J/C.", "formula_panel", {"formula": "1 V = 1 J / 1 C", "label": "Volt"}, "Named after Alessandro Volta.", "1 V between points means 1 J/C work.", "1 V = 1 J per coulomb.", "", "", ["volt"]),
        ("Voltmeter", "Potential difference is measured with a voltmeter connected in parallel across the two points.", "electric_circuit", {"highlight": "voltmeter"}, "Parallel so it doesn't redirect all current.", "Voltmeter across bulb measures bulb PD.", "Voltmeter in parallel.", "Do not put voltmeter in series.", "", ["voltmeter"]),
        ("Work and charge Example 11.2", "Q = 2 C across 12 V → W = VQ = 24 J of work done on the charge.", "formula_panel", {"formula": "W = VQ", "label": "Work on charge"}, "Reverse of V = W/Q.", "6 V battery moving 1 C does 6 J work.", "W = V × Q.", "", "", []),
        ("Battery expends energy", "To maintain current, the cell keeps converting stored chemical energy — expending it in the circuit.", "electric_circuit", {"mode": "energy"}, "Source energy becomes heat/light/motion in load.", "Battery runs down after long use.", "Cell supplies energy continuously while current flows.", "", "", []),
        ("Saying '1 V between points'", "1 V between two points means 1 J of work is done to move 1 C from one point to the other.", "formula_panel", {"formula": "1 V meaning", "label": "Definition"}, "NCERT conceptual question.", "Every coulomb gains 1 J energy across 1 V.", "1 V = 1 J per coulomb moved.", "", "", []),
        ("Device maintaining PD", "A cell or battery maintains potential difference across a conductor in a circuit.", "electric_circuit", {"highlight": "cell"}, "NCERT short answer.", "Generator or cell in mains/torch.", "Battery maintains PD.", "", "", []),
    ],
)

DAY4 = _build_day(
    4,
    [
        ("Circuit diagram purpose", "Schematic diagrams use standard symbols instead of realistic pictures — easier to draw and read.", "circuit_symbols", {"highlight": "overview"}, "Universal language for circuits.", "Exam answers use symbols not sketches of bulbs.", "Schematic = symbol diagram.", "", "", ["circuit diagram"]),
        ("Electric cell symbol", "One cell: long line (+) and short thick line (−).", "circuit_symbols", {"highlight": "cell"}, "Table 11.1 symbol 1.", "Single 1.5 V cell in diagrams.", "Long line = +, short thick = −.", "", "", []),
        ("Battery symbol", "Battery = combination of cells: multiple cell symbols in series.", "circuit_symbols", {"highlight": "battery"}, "Higher voltage than single cell.", "Four 1.5 V cells → 6 V battery.", "Battery = cells in series symbol.", "", "", []),
        ("Open and closed switch", "Open key: gap in line. Closed key: filled dot or bridge showing connection.", "circuit_symbols", {"highlight": "switch"}, "Switch state changes circuit continuity.", "Open plug key stops Ohm's law activity.", "Open = broken; closed = connected.", "", "", []),
        ("Wire, joint, crossing", "Straight lines for wires; dot at junction; crossing without dot means no connection.", "circuit_symbols", {"highlight": "wires"}, "Avoid fake connections in diagrams.", "Crossing lines without dot don't connect.", "Dot = joined; crossing alone = not joined.", "", "", []),
        ("Bulb and resistor symbols", "Bulb: circle with cross or filament symbol. Resistor: zig-zag or rectangle labelled R.", "circuit_symbols", {"highlight": "bulb_resistor"}, "Load and fixed resistance symbols.", "R marks nichrome wire in Ohm's law exp.", "Bulb = load; rectangle = resistor.", "", "", []),
        ("Rheostat symbol", "Variable resistance / rheostat: resistor arrow through rectangle.", "circuit_symbols", {"highlight": "rheostat"}, "Used to change current without changing voltage source.", "Dimmer and lab rheostats.", "Rheostat = variable R symbol.", "", "", ["rheostat"]),
        ("Ammeter and voltmeter symbols", "Ammeter: A in circle, series. Voltmeter: V in circle, parallel.", "circuit_symbols", {"highlight": "meters"}, "Placement matters as much as symbol.", "Redraw Q2 circuit with meters correctly.", "A in series; V in parallel.", "", "", []),
        ("Reading a full schematic", "Trace closed path: source → switch → loads → back to source; add meters correctly.", "electric_circuit", {"mode": "read_schematic"}, "Skill for exam circuit questions.", "Follow arrow from + terminal.", "Trace loop; check switch and meters.", "", "", []),
        ("Drawing exam circuits", "Use ruler, label components, show switch state and meter placement clearly.", "circuit_symbols", {"mode": "exam"}, "Series resistors Q1 style diagrams.", "3 cells of 2 V, resistors 5 Ω, 8 Ω, 12 Ω in series.", "Neat symbols + labels + correct series/parallel.", "", "", []),
    ],
)

DAY5 = _build_day(
    5,
    [
        ("Ohm's law statement", "Potential difference V across a metallic conductor is directly proportional to current I through it, at constant temperature.", "ohms_law_graph", {"highlight": "statement"}, "Core law of Ch 11.", "Double V → double I for ohmic conductor.", "V ∝ I at constant temperature.", "Ohm's law fails if temperature changes much.", "", ["Ohm's law"]),
        ("V = IR form", "From Ohm's law: V/I = constant = R, so V = IR.", "formula_panel", {"formula": "V = I R", "label": "Ohm's law"}, "Most used form in numericals.", "12 V across 4 Ω → I = 3 A.", "V = IR.", "", "", []),
        ("Resistance R", "R = V/I is resistance — property of conductor to resist charge flow. SI unit: ohm (Ω).", "formula_panel", {"formula": "R = V / I", "label": "Resistance"}, "Higher R → less current for same V.", "1 V and 1 A → R = 1 Ω.", "R = V/I; unit ohm Ω.", "", "", ["resistance", "ohm"]),
        ("One ohm defined", "1 Ω: when V = 1 V produces I = 1 A through conductor.", "formula_panel", {"formula": "1 Ω = 1 V / 1 A", "label": "Definition of ohm"}, "Links volt and ampere.", "Household small resistor values in ohms to kilohms.", "1 Ω = 1 volt per ampere.", "", "", []),
        ("V–I graph", "Plot of V vs I for ohmic wire is straight line through origin — slope gives R.", "ohms_law_graph", {"highlight": "graph"}, "Fig 11.3 straight line = Ohm's law verified.", "V/I same for each row in Activity 11.1 table.", "Linear V–I graph → constant R.", "Line not through origin → check zero error.", "", []),
        ("Activity 11.1 pattern", "Increase cells → both V and I increase; ratio V/I stays approximately constant.", "ohms_law_graph", {"mode": "activity"}, "Lab evidence for constant R.", "Nichrome wire XY in circuit Fig 11.2.", "V/I constant for same wire at same temperature.", "", "", []),
        ("I = V/R", "Current I = V/R — current inversely proportional to resistance for fixed voltage.", "formula_panel", {"formula": "I = V / R", "label": "Current form"}, "Thicker/shorter wire → lower R → higher I.", "Same 6 V: 20 Ω lamp vs 4 Ω conductor different current.", "Double R → half I (same V).", "", "", []),
        ("Good conductor vs resistor", "Same-size good conductor: low R; resistor: appreciable R; insulator: very high R.", "resistance_wire", {"mode": "compare"}, "Activity 11.2 different ammeter readings.", "Nichrome vs copper same size — different I.", "Insulator >> resistor >> good conductor.", "", "", []),
        ("Why components differ in current", "Different components offer different resistance — electrons retarded differently.", "resistance_wire", {"highlight": "cause"}, "Microscopic explanation in NCERT.", "Torch bulb vs 10 W bulb same voltage different I.", "More R → less current.", "", "", []),
        ("Temperature condition", "Ohm's law holds provided temperature of conductor remains the same.", "ohms_law_graph", {"highlight": "temperature"}, "Filament heats up — R changes when glowing.", "Cold vs hot bulb filament resistance differs.", "Constant temperature assumption for ideal Ohm's law.", "", "", []),
    ],
)

DAY6 = _build_day(
    6,
    [
        ("Rheostat / variable resistance", "Device to regulate current without changing voltage source — changes R in circuit.", "circuit_symbols", {"highlight": "rheostat"}, "Used in labs and dimmers.", "Slide rheostat in Ohm's law experiment.", "Variable R controls current.", "", "", ["rheostat"]),
        ("Length and resistance", "For uniform wire, R ∝ l — double length doubles resistance (same material, same area).", "resistance_wire", {"highlight": "length"}, "Activity 11.3: ammeter halves when length doubles.", "2l nichrome → half the current.", "Longer wire → more R.", "", "", []),
        ("Area and resistance", "R ∝ 1/A — thicker wire (larger cross-section) has lower resistance.", "resistance_wire", {"highlight": "area"}, "Thick wires used for high current.", "Thicker nichrome → higher ammeter reading.", "Thicker wire → less R.", "", "", []),
        ("Material affects resistance", "Same length and area, different materials give different R — depends on resistivity ρ.", "resistance_wire", {"highlight": "material"}, "Copper vs nichrome comparison in activity.", "Copper wire vs nichrome same dimensions.", "Nature of material matters.", "", "", []),
        ("Combined proportionality", "R ∝ l and R ∝ 1/A combined: R = ρ l / A.", "formula_panel", {"formula": "R = ρ l / A", "label": "Eq. 11.10"}, "Central formula for wire resistance.", "Double length and halve area → R × 4.", "R = ρl/A.", "", "", ["resistivity"]),
        ("Resistivity ρ", "ρ (rho) is constant for material; SI unit Ω m. Characteristic property.", "formula_panel", {"formula": "ρ = R A / l", "label": "Resistivity"}, "Depends on material not shape.", "Silver low ρ; rubber very high ρ.", "ρ in Ω m; material property.", "", "", ["resistivity"]),
        ("Conductors vs insulators", "Metals/alloys: ρ ~ 10⁻⁸–10⁻⁶ Ω m (conductors). Rubber/glass: ~10¹²–10¹⁷ Ω m (insulators).", "resistance_wire", {"mode": "table"}, "Table 11.2 orders of magnitude.", "Copper for wires; rubber for insulation.", "Low ρ = conductor; high ρ = insulator.", "", "", []),
        ("Alloys vs pure metals", "Alloys usually higher ρ than constituent metals; resist oxidation at high temperature.", "heating_element", {"highlight": "alloy"}, "Used in heating elements and nichrome.", "Nichrome in heater; tungsten in bulb.", "Alloys for heating devices.", "Alloy ρ higher but stable at heat.", "", []),
        ("Example 11.5 scaling", "Same material: l halved and A doubled → R becomes 1/4 of original (4 Ω → 1 Ω).", "formula_panel", {"formula": "R scales with l/A", "label": "Example 11.5"}, "Common exam ratio question.", "Track l and A factors separately.", "R × (l ratio)/(A ratio).", "", "", []),
        ("Thick vs thin wire question", "Thick wire of same material conducts more easily — lower R, more current from same source.", "resistance_wire", {"mode": "thick_thin"}, "NCERT Q2 style.", "Power cables are thick copper.", "Thick = low R = easier current.", "", "", []),
    ],
)

DAY7 = _build_day(
    7,
    [
        ("Resistors in series — layout", "Resistors connected end to end between same path — same current through each.", "resistors_series", {"highlight": "layout"}, "Fig 11.6 three resistors in one loop.", "Christmas old lights sometimes series.", "Series = one after another.", "", "", ["series"]),
        ("Same current in series", "In series combination, current is same through every resistor and every part of circuit.", "resistors_series", {"highlight": "current"}, "Activity 11.4 ammeter same anywhere.", "Ammeter before or after R₂ same reading.", "I same everywhere in series.", "Current is NOT shared in series.", "", []),
        ("PD adds in series", "Total PD across series combination equals sum of PDs across individual resistors: V = V₁ + V₂ + V₃.", "resistors_series", {"highlight": "voltage"}, "Activity 11.5 voltmeter readings.", "6 V battery split across lamp and resistor.", "V_total = V₁ + V₂ + V₃.", "", "", []),
        ("Equivalent series resistance", "Rₛ = R₁ + R₂ + R₃ — series equivalent greater than any single resistor.", "formula_panel", {"formula": "R_s = R1 + R2 + R3", "label": "Series resistance"}, "Eq. 11.14.", "20 Ω lamp + 4 Ω resistor → 24 Ω total.", "Series R adds directly.", "", "", []),
        ("Example 11.7 outline", "Lamp 20 Ω + conductor 4 Ω on 6 V: R=24 Ω, I=0.25 A, V₁=5 V, V₂=1 V.", "resistors_series", {"mode": "example"}, "Full NCERT worked example.", "Total R first, then I = V/R, then each V=IR.", "Series numerical: add R, find I, split V.", "", "", []),
        ("Resistors in parallel — layout", "Resistors connected between same two points X and Y — same PD across each branch.", "resistors_parallel", {"highlight": "layout"}, "Fig 11.7 household branches.", "Home lights in parallel across mains.", "Parallel = same two nodes.", "", "", ["parallel"]),
        ("Current splits in parallel", "Total current equals sum of branch currents: I = I₁ + I₂ + I₃.", "resistors_parallel", {"highlight": "current"}, "Activity 11.6.", "More branches → more total current.", "I splits among branches.", "Current is NOT same in parallel branches.", "", []),
        ("Same PD in parallel", "Potential difference across each parallel resistor equals PD across the combination.", "resistors_parallel", {"highlight": "voltage"}, "Each appliance gets full mains PD (ideal).", "12 V across each of R₁, R₂, R₃ in Ex 11.8.", "Same V on each parallel branch.", "", "", []),
        ("Parallel equivalent formula", "1/Rₚ = 1/R₁ + 1/R₂ + 1/R₃ — equivalent R less than smallest individual.", "formula_panel", {"formula": "1/Rp = 1/R1 + 1/R2 + 1/R3", "label": "Parallel resistance"}, "Eq. 11.18.", "Two 10 Ω parallel → 5 Ω.", "Reciprocals add for parallel.", "", "", []),
        ("Example 11.8 idea", "5 Ω, 10 Ω, 30 Ω parallel on 12 V: each branch I = V/R; total I = sum; Rₚ = 3 Ω.", "resistors_parallel", {"mode": "example"}, "Standard three-resistor parallel problem.", "I₁=2.4 A, I₂=1.2 A, I₃=0.4 A, total 4 A.", "Each V/R then add I; then find Rₚ.", "", "", []),
    ],
)

DAY8 = _build_day(
    8,
    [
        ("Series R greater than parts", "Series equivalent resistance is greater than any individual resistance.", "resistors_series", {"mode": "compare"}, "More resistors in series → harder for current.", "Adding 4 Ω to lamp increases total R.", "R_s > each R_i.", "", "", []),
        ("Parallel R less than smallest", "Parallel equivalent is less than the smallest individual resistance.", "resistors_parallel", {"mode": "compare"}, "More parallel paths → easier overall flow.", "Two equal resistors parallel → half each value.", "R_p < smallest R_i.", "", "", []),
        ("Series impractical at home", "Series circuit: same current everywhere — one failure breaks all; not used for household appliances.", "resistors_series", {"mode": "domestic"}, "NCERT explains why homes use parallel.", "Old series fairy lights all off if one bulb fails.", "Domestic circuits mainly parallel.", "", "", []),
        ("Parallel domestic advantage", "Each appliance gets full PD; independent switching; one branch off doesn't stop others.", "resistors_parallel", {"mode": "domestic"}, "Why fridge and TV work independently.", "Turn off kitchen light — TV still on.", "Parallel for household wiring.", "", "", []),
        ("Mixed circuits strategy", "Replace parallel groups by equivalent R, then add series parts (Example 11.9 method).", "resistors_parallel", {"mode": "mixed"}, "Step-by-step reduction.", "R′ for parallel pair, R″ for triple, then add.", "Simplify parallel blocks first.", "", "", []),
        ("Heating effect intro", "When current flows through resistor, source energy dissipated as heat — heating effect of current.", "heating_element", {"highlight": "overview"}, "Fan warm, heater hot — same physics.", "Electric iron gets hot on current.", "Current through R produces heat.", "", "", ["heating effect"]),
        ("Power P = VI", "Rate of energy: P = VI — electric power in watts.", "formula_panel", {"formula": "P = V I", "label": "Electric power"}, "Eq. 11.19/11.22.", "110 W bulb at 220 V, 0.5 A.", "P = VI.", "", "", ["electric power"]),
        ("Heat H = VIt", "Energy (heat) in time t: H = VIt.", "formula_panel", {"formula": "H = V I t", "label": "Heat energy"}, "Eq. 11.20.", "Energy supplier = VI × time.", "H = VIt joules.", "", "", []),
        ("Joule's law H = I²Rt", "Heat produced H = I²Rt — directly ∝ I², R, and t.", "formula_panel", {"formula": "H = I² R t", "label": "Joule's law"}, "Eq. 11.21 — most used for heat.", "Double current → 4× heat (same R,t).", "H ∝ I², R, t.", "", "", ["Joule's law"]),
        ("P = I²R and P = V²/R", "Equivalent power forms: P = I²R = V²/R.", "formula_panel", {"formula": "P = I²R = V²/R", "label": "Power forms"}, "Pick form matching known quantities.", "Known V and R → P = V²/R.", "Three power formulas equivalent.", "", "", []),
    ],
)

DAY9 = _build_day(
    9,
    [
        ("Watt unit", "1 watt = 1 joule per second = power when 1 A flows at 1 V.", "formula_panel", {"formula": "1 W = 1 V × 1 A", "label": "Watt"}, "SI power unit.", "60 W bulb vs 100 W brighter.", "1 W = 1 VA.", "", "", ["watt"]),
        ("Kilowatt and kWh", "1 kW = 1000 W. Commercial energy unit: kilowatt-hour (kWh) — 'unit' on electricity bill.", "formula_panel", {"formula": "1 kWh = 3.6×10⁶ J", "label": "Energy billing"}, "Energy = power × time.", "400 W fridge 8 h/day × 30 days = 96 kWh.", "kWh = kW × hours.", "kWh is energy not power.", "", []),
        ("We pay for energy not electrons", "Electricity bill charges for energy to move electrons through devices — not for consuming electrons.", "electric_power", {"mode": "billing"}, "NCERT 'More to Know' box.", "Electrons circulate; energy is converted at load.", "Billed for energy (kWh).", "", "", []),
        ("Electric iron power Example", "840 W max and 360 W min at 220 V → different I and R settings.", "electric_power", {"mode": "example_11_10"}, "Example 11.10.", "Higher power → higher current.", "P = VI gives I; R = V/I.", "", "", []),
        ("Heating element glows", "Heating element high R, high heat; connecting cord low R — cord doesn't glow.", "heating_element", {"highlight": "cord_vs_element"}, "NCERT Q1 heating section.", "Nichrome coil hot; copper wire cool.", "Heat ∝ R; element designed for heat.", "", "", []),
        ("Bulb filament", "Tungsten filament high melting point (3380°C), thermally isolated, in inactive gas.", "heating_element", {"highlight": "bulb"}, "Most power becomes heat; small part light.", "Filament white-hot at operating current.", "Tungsten + gas fill for bulb life.", "", "", []),
        ("Fuse protection", "Fuse wire in series melts when current too high — breaks circuit, protects appliances.", "electric_circuit", {"highlight": "fuse"}, "Rated 1 A, 5 A, etc. for domestic use.", "1 kW iron at 220 V needs ~5 A fuse.", "Fuse = series safety device.", "", "", ["fuse"]),
        ("Choosing fuse rating", "Fuse slightly above normal operating current — e.g. 5 A fuse for ~4.5 A appliance.", "electric_circuit", {"mode": "fuse_rating"}, "Example 11.7.1 calculation.", "I = P/V for rated power.", "Fuse rating > normal I but < dangerous I.", "", "", []),
        ("Heating applications", "Electric iron, toaster, oven, kettle, heater use Joule heating deliberately.", "heating_element", {"mode": "applications"}, "Useful conversion of electrical to thermal energy.", "Toaster coils red hot.", "Joule heat for cooking and warmth.", "", "", []),
        ("Undesirable heating", "Unwanted heat in motors/wires wastes energy and can damage components.", "heating_element", {"mode": "undesirable"}, "Design ventilation for gadgets.", "Laptop fan removes waste heat.", "Not all heating is useful.", "", "", []),
    ],
)

# Days 10–16: applications, numerics, exam prep
DAY10 = _build_day(10, [
    ("Ohm's law numerical pattern", "Given any two of V, I, R find the third using V=IR or R=V/I.", "formula_panel", {"formula": "V = I R", "label": "Numerical triad"}, "Universal solve strategy.", "220 V, 1200 Ω → I = 0.18 A.", "Identify known pair → use V=IR.", "", "", []),
    ("Example 11.3 bulbs vs heater", "Same 220 V: 1200 Ω bulb draws 0.18 A; 100 Ω heater draws 2.2 A.", "electric_power", {"mode": "compare_current"}, "Lower R → higher I at same V.", "Heater warms faster — more current.", "Same V: small R → large I.", "", "", []),
    ("Example 11.4 doubling V", "If R fixed, doubling V doubles I (60 V,4 A → 120 V,8 A when R=15 Ω).", "ohms_law_graph", {"mode": "double_v"}, "Linear Ohm's law scaling.", "Heater on higher setting if R unchanged.", "V ∝ I when R constant.", "", "", []),
    ("Resistivity numerical", "ρ = RA/l; use consistent metres for l and A (A = πd²/4).", "formula_panel", {"formula": "ρ = R A / l", "label": "Example 11.5"}, "Identify material from Table 11.2.", "R=26 Ω, l=1 m, d=0.3 mm → manganese.", "Convert mm² to m² for A.", "", "", []),
    ("Half PD half current", "If R constant and V halved, I halves (NCERT Q3 resistors section).", "ohms_law_graph", {"mode": "half_v"}, "Direct Ohm proportion.", "Dimmer reduces effective voltage.", "V halved → I halved if R fixed.", "", "", []),
    ("Series voltmeter reading Q", "V across 12 Ω in series with 5 Ω and 8 Ω on 6 V three-cell: find I then V=IR.", "resistors_series", {"mode": "exam"}, "Redraw Q2 style.", "Total R=25 Ω, I=6/25 A, V₁₂=IR.", "Series: total R, then split V.", "", "", []),
    ("Parallel branch currents", "Each parallel I = V/R_branch; total I sum.", "resistors_parallel", {"mode": "exam"}, "Example 11.8 template.", "12 V on 5,10,30 Ω parallel.", "Same V each branch.", "", "", []),
    ("Heat from charge", "Q through PD: H = VQ; 96000 C through 50 V in 1 h gives energy.", "formula_panel", {"formula": "H = V Q", "label": "Charge heat"}, "NCERT heating Q2.", "Energy = charge × voltage.", "H = VQ when all charge moved.", "", "", []),
    ("Heat in 30 s", "H = I²Rt: 5 A through 20 Ω for 30 s → H = 15000 J.", "formula_panel", {"formula": "H = I² R t", "label": "Example style"}, "Substitute SI units.", "Iron Example Q3.", "t in seconds.", "", "", []),
    ("Motor power Q", "P = VI; energy = P × t. 5 A at 220 V → P = 1100 W.", "electric_power", {"mode": "motor"}, "End-of-chapter Q2.", "2 h energy = 1100 W × 7200 s or kWh method.", "P then E = Pt.", "", "", []),
])

DAY11 = _build_day(11, [
    ("Tungsten for filament", "High melting point prevents melt at glowing temperature.", "heating_element", {"highlight": "tungsten"}, "Material choice for bulbs.", "3380°C melting point.", "Tungsten filament in bulbs.", "", "", []),
    ("Nichrome in heaters", "Nichrome alloy high ρ, resists oxidation at red heat.", "heating_element", {"highlight": "nichrome"}, "Heating coils material.", "Electric iron nichrome wire.", "Nichrome for heating elements.", "", "", []),
    ("Copper for transmission", "Low ρ copper/aluminium for power lines — minimal energy loss as heat.", "resistance_wire", {"highlight": "copper"}, "Table 11.2 conductors.", "Thick copper wires from pole to home.", "Copper: low ρ conductor.", "", "", []),
    ("Insulator role", "Rubber/plastic insulation prevents accidental contact — very high ρ.", "resistance_wire", {"mode": "insulator"}, "Safety around conductors.", "Cord plastic cover.", "Insulators block current.", "", "", []),
    ("Temperature and ρ", "Both R and ρ vary with temperature — mention when filament heats.", "resistance_wire", {"mode": "temperature"}, "Cold resistance lower than hot.", "Bulb inrush current when switched on.", "R changes if temperature changes.", "", "", []),
    ("Activity 11.2 summary", "Same voltage, different components → different I because R differs.", "resistance_wire", {"mode": "activity"}, "Qualitative before formula.", "Swap nichrome, torch bulb, 10 W bulb.", "Component R sets current.", "", "", []),
    ("Activity 11.3 summary", "Vary l, A, material separately — observe ammeter change.", "resistance_wire", {"mode": "activity_11_3"}, "Empirical R factors.", "Four wire configurations Fig 11.5.", "l up → I down; A up → I up.", "", "", []),
    ("Series same I proof idea", "Charge conservation: same current through series elements each second.", "resistors_series", {"mode": "why"}, "Conceptual why for Activity 11.4.", "One path → one flow rate.", "Single loop → same I.", "", "", []),
    ("Parallel same V idea", "Wires connect same two points → same potential difference.", "resistors_parallel", {"mode": "why"}, "Conceptual for Activity 11.6.", "Both ends of each R at X and Y.", "Parallel branches same V.", "", "", []),
    ("Equivalent resistor concept", "Single R that replaces network giving same V and I from source.", "resistors_series", {"mode": "equivalent"}, "Used in all combination problems.", "24 Ω replaces lamp+resistor series.", "Equivalent R simplifies circuit.", "", "", []),
])

DAY12 = _build_day(12, [
    ("Draw series circuit exam", "Battery + key + ammeter + resistors in one loop; voltmeter across one resistor.", "circuit_symbols", {"mode": "exam_series"}, "NCERT Q1 series.", "Label each R and cell emf.", "Series exam diagram checklist.", "", "", []),
    ("Ammeter placement", "Always series — carries full circuit current.", "electric_circuit", {"highlight": "ammeter"}, "Wrong placement gives wrong/fault reading.", "Never parallel ammeter with load.", "Ammeter in series only.", "", "", []),
    ("Voltmeter placement", "Always parallel across component whose PD you need.", "electric_circuit", {"highlight": "voltmeter"}, "High resistance avoids draining circuit.", "Across 12 Ω resistor in Q2.", "Voltmeter parallel only.", "", "", []),
    ("Three resistors 6 Ω each", "Can make 9 Ω series, 2 Ω parallel, or mixed — NCERT exercise Q11.", "resistors_parallel", {"mode": "six_ohm_three"}, "Creative combination question.", "Series: 18 Ω; parallel: 2 Ω.", "Same R different connections → different R_eq.", "", "", []),
    ("Series PD division", "V_i = I R_i; larger R gets larger share of voltage in series.", "resistors_series", {"highlight": "division"}, "Lamp 20 Ω gets more V than 4 Ω on same I.", "V split proportional to R.", "Big R → big V drop in series.", "", "", []),
    ("Parallel current division", "I_i = V/R_i; smaller R branch takes more current.", "resistors_parallel", {"highlight": "division"}, "5 Ω branch takes more I than 30 Ω at same V.", "Low R path draws more I.", "Small R → large branch I.", "", "", []),
    ("Two resistors parallel shortcut", "R_eq = R₁R₂/(R₁+R₂) for two in parallel only.", "formula_panel", {"formula": "R_eq = R1 R2 / (R1+R2)", "label": "Two parallel"}, "Faster than reciprocals.", "Two 10 Ω → 5 Ω.", "Product over sum for two.", "", "", []),
    ("Energy unit conversion", "1 kWh = 3.6 × 10⁶ J — use for cost problems.", "formula_panel", {"formula": "1 kWh = 3.6×10⁶ J", "label": "Billing"}, "Example 11.13 refrigerator cost.", "96 kWh × Rs 3 = Rs 288.", "Convert W and hours to kWh.", "", "", []),
    ("Example 11.12 bulb power", "P = VI = 220 × 0.5 = 110 W.", "electric_power", {"mode": "bulb"}, "Simple power calc.", "Power in joules per second.", "P = VI directly.", "", "", []),
    ("Purely resistive circuit", "If only resistors connected to battery, source energy all dissipated as heat.", "heating_element", {"mode": "pure_resistive"}, "Fig 11.13.", "Theoretical 100% heat in ideal R circuit.", "Resistive load → heating effect.", "", "", []),
])

DAY13 = _build_day(13, [
    ("Define electric current exam", "Rate of flow of electric charge through a cross-section.", "formula_panel", {"formula": "I = Q/t", "label": "Definition"}, "1-mark definition.", "State SI unit ampere.", "Current = charge rate.", "", "", []),
    ("Define potential difference exam", "Work done per unit charge moved between two points.", "formula_panel", {"formula": "V = W/Q", "label": "Definition"}, "1-mark definition.", "Unit volt.", "PD = work per charge.", "", "", []),
    ("State Ohm's law exam", "V ∝ I for metallic conductor at constant temperature; V = IR.", "ohms_law_graph", {"mode": "definition"}, "Must mention temperature.", "Include R definition.", "Temperature condition essential.", "", "", []),
    ("State Joule's law exam", "H = I²Rt; heat ∝ I², R, and t.", "formula_panel", {"formula": "H = I² R t", "label": "Joule's law"}, "Heating numerical base.", "Three proportionalities.", "All three factors matter.", "", "", []),
    ("Series vs parallel summary table", "Series: same I, V adds, R adds. Parallel: same V, I adds, 1/R adds.", "resistors_series", {"mode": "summary_table"}, "Revision before practice.", "Draw comparison table from memory.", "Four rows: I, V, R, domestic use.", "", "", []),
    ("Why alloy in toaster", "Higher ρ than pure metal; does not oxidise quickly at high temperature.", "heating_element", {"mode": "alloy_why"}, "NCERT Q4 resistors section.", "Nichrome coils stay stable when hot.", "Alloy: heat + durability.", "", "", []),
    ("Better conductor iron or mercury", "Iron (lower ρ than mercury in Table 11.2).", "resistance_wire", {"mode": "table_q"}, "Table lookup skill.", "Compare ρ values.", "Lower ρ = better conductor.", "", "", []),
    ("Best conductor in table", "Silver lowest ρ (~1.60×10⁻⁸ Ω m) — best conductor listed.", "resistance_wire", {"mode": "silver"}, "Theoretical best; copper used practically.", "Silver costly for wiring.", "Silver best; copper common.", "", "", []),
    ("Electrons per coulomb", "1 C ≈ 6×10¹⁸ electrons (each 1.6×10⁻¹⁹ C).", "formula_panel", {"formula": "n = Q / e", "label": "Electron count"}, "NCERT Q3 Ch 11.1.", "Divide total charge by e.", "Use e = 1.6×10⁻¹⁹ C.", "", "", []),
    ("Circuit broken at switch", "Open switch → open circuit → no continuous path → I = 0.", "electric_circuit", {"mode": "open"}, "Concept link torch switch.", "Gap stops charge flow.", "Open circuit: no current.", "", "", []),
])

DAY14 = _build_day(14, [
    ("Long answer: Ohm's law experiment", "Describe Activity 11.1: vary cells, measure V and I, plot straight line, R = V/I constant.", "ohms_law_graph", {"mode": "long_answer"}, "3-mark lab question.", "Include nichrome wire XY.", "Method + graph + conclusion.", "", "", []),
    ("Long answer: factors affecting R", "State l, A, material; R = ρl/A; describe Activity 11.3 observations.", "resistance_wire", {"mode": "long_answer"}, "Factors question.", "Thick/long/material changes.", "Three factors with formula.", "", "", []),
    ("Long answer: series combination", "Derive R_s = R₁+R₂, same I, V = V₁+V₂ with diagram Fig 11.6.", "resistors_series", {"mode": "long_answer"}, "Derivation question.", "Activities 11.4 and 11.5.", "State laws then formula.", "", "", []),
    ("Long answer: parallel combination", "Derive 1/R_p = sum of reciprocals; same V; I = I₁+I₂.", "resistors_parallel", {"mode": "long_answer"}, "Parallel derivation.", "Activity 11.6.", "Current split + voltage same.", "", "", []),
    ("Long answer: heating effect", "Explain H = I²Rt, energy source to heat, examples iron/bulb/fuse.", "heating_element", {"mode": "long_answer"}, "Heating section essay.", "Include Joule's law.", "Energy conversion to heat.", "", "", []),
    ("Long answer: electric power", "Define P = VI, watt, kWh, billing example.", "electric_power", {"mode": "long_answer"}, "Power + energy unit.", "Example 11.13 cost.", "Power vs energy distinction.", "", "", []),
    ("MCQ: maintains PD", "Cell/battery maintains potential difference — not ammeter or resistor alone.", "electric_circuit", {"mode": "mcq"}, "Ch 11.2 Q1.", "Chemical energy in cell.", "Battery maintains PD.", "", "", []),
    ("MCQ: image at retina wrong unit", "Trap from other chapter — eye forms image at retina; electricity Q: image not here.", "electric_circuit", {"mode": "mcq_trap"}, "Cross-unit confusion.", "Electricity MCQs about R,I,V.", "Stay in Ch 11 context.", "", "", []),
    ("MCQ: ciliary muscles wrong chapter", "Lens focal change is eye unit — electricity uses rheostat for variable R.", "circuit_symbols", {"mode": "mcq_trap"}, "Avoid unit mix-ups.", "Rheostat changes R.", "Variable R = rheostat not ciliary.", "", "", []),
    ("Safety: fuse and overload", "Too high current melts fuse, stops fire risk from overheated wires.", "electric_circuit", {"highlight": "fuse"}, "Domestic safety.", "Never replace fuse with higher rating wire.", "Fuse protects from overcurrent.", "", "", []),
])

DAY15 = _build_day(15, [
    ("Chapter map", "Ch 11: current → PD → symbols → Ohm → R factors → series/parallel → heat → power.", "electric_circuit", {"mode": "map"}, "Big picture revision.", "Follow section numbers 11.1–11.8.", "Six main blocks in order.", "", "", []),
    ("Link to prior physics", "Energy W = VQ connects to work and power from earlier classes.", "formula_panel", {"formula": "W = VQ, P = W/t", "label": "Cross-link"}, "Unified energy story.", "Mechanical power analog.", "Electric energy follows same power idea.", "", "", []),
    ("Graph skills V–I", "Slope ΔV/ΔI = R for ohmic conductor; intercept should be zero.", "ohms_law_graph", {"mode": "graph_skills"}, "Graphical determination of R.", "Use two points on line.", "Slope = R.", "", "", []),
    ("Unit analysis check", "Verify formulas dimensionally: V/I → Ω; VI → W.", "formula_panel", {"formula": "Unit check", "label": "Exam tip"}, "Catch formula errors.", "Wrong unit in answer flags mistake.", "Check units in numericals.", "", "", []),
    ("Series lamp dimmer", "More resistors in series → higher R → lower I → lamp dimmer.", "resistors_series", {"mode": "conceptual"}, "Qualitative prediction.", "Extra resistor in torch line.", "Series R up → brightness down.", "", "", []),
    ("Parallel lamp independence", "Parallel branch off → others unchanged brightness.", "resistors_parallel", {"mode": "conceptual"}, "Home lighting logic.", "One bulb removed others stay on.", "Parallel branches independent.", "", "", []),
    ("High power low resistance heater", "Heater low R (100 Ω) draws large I at 220 V → high P = VI.", "electric_power", {"mode": "heater_vs_bulb"}, "Example 11.3 contrast.", "P = V²/R shows low R → high P.", "Heater: low R, high power.", "", "", []),
    ("Low power high resistance bulb", "Bulb filament high R limits current → moderate power for light.", "electric_power", {"mode": "bulb_vs_heater"}, "Designed for light not max heat.", "1200 Ω filament Example 11.3.", "Bulb: higher R, lower I.", "", "", []),
    ("Resistivity does not depend on shape", "ρ is material property; R depends on l and A.", "formula_panel", {"formula": "ρ vs R", "label": "Concept"}, "Common conceptual error.", "Thicker wire same material same ρ.", "Shape changes R not ρ.", "", "", []),
    ("Ready for practice", "160 concept cards on Electricity — use Practice tab for 15-question sessions from 200-question bank.", "electric_circuit", {"mode": "complete"}, "Bridge to Stage 2.", "Grok toggle in Practice Setup.", "Concepts first, then 200 MCQ bank.", "", "", []),
])

DAY16 = _build_day(16, [
    ("Mastery: formulas list", "I=Q/t, V=W/Q, V=IR, R=ρl/A, R_s sum, 1/R_p sum, H=I²Rt, P=VI.", "formula_panel", {"formula": "Formula sheet", "label": "Mastery"}, "Self-test all equations.", "Write from memory.", "Eight core equations.", "", "", []),
    ("Mastery: units list", "C, A, V, Ω, Ω m, W, kWh, J.", "formula_panel", {"formula": "Units", "label": "Mastery"}, "Unit quiz.", "Match quantity to unit.", "No mixing V and W.", "", "", []),
    ("Mastery: meter rules", "Ammeter series; voltmeter parallel; fuse series.", "electric_circuit", {"mode": "checklist"}, "Three wiring rules.", "Draw each correctly.", "A series, V parallel, fuse series.", "", "", []),
    ("Mastery: series vs parallel", "Recite differences for I, V, R and home wiring reason.", "resistors_parallel", {"mode": "checklist"}, "Oral exam prep.", "30-second summary each.", "Parallel for homes.", "", "", []),
    ("Mastery: heating devices", "Name iron, toaster, fuse, bulb — each uses I²Rt differently.", "heating_element", {"mode": "checklist"}, "Application recall.", "Use vs protect vs light.", "Four device roles.", "", "", []),
    ("Mastery: numerical types", "Ohm's law, ρ, series/parallel R, H, P, kWh cost — six problem types.", "electric_power", {"mode": "checklist"}, "Practice plan.", "One example each type.", "Cover all six templates.", "", "", []),
    ("Common pitfalls", "Time in seconds; mm to m for diameter; parallel reciprocal not sum; open ammeter.", "formula_panel", {"formula": "Pitfalls", "label": "Exam"}, "Last-minute errors.", "Read question units.", "Four classic mistakes.", "", "", []),
    ("Safety reminders", "Never connect ammeter in parallel; use correct fuse rating; wet hands and electricity.", "electric_circuit", {"mode": "safety"}, "Lab and home safety.", "Teacher supervision for high V.", "Respect mains voltage.", "", "", []),
    ("What you have learnt recap", "NCERT summary: current, PD, R, Ohm's law, series/parallel, heat, power.", "electric_circuit", {"mode": "ncert_summary"}, "End of chapter bullets.", "Match textbook 'What you have learnt'.", "Official summary alignment.", "", "", []),
    ("Unit 3 complete", "You finished Unit 3 Electricity — open Practice when Stage 1 is complete.", "electric_circuit", {"highlight": "overview", "mode": "complete"}, "Celebrate progress.", "200 MCQs waiting in bank.", "Unit 3 ready for practice.", "", "", []),
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
    1: "Electric Current and Circuit",
    2: "Charge, Ampere and Ammeter",
    3: "Potential Difference and Volt",
    4: "Circuit Diagrams and Symbols",
    5: "Ohm's Law",
    6: "Resistance and Resistivity",
    7: "Series and Parallel Resistors",
    8: "Heating Effect and Power Intro",
    9: "Electric Power and Applications",
    10: "Numericals — Ohm's Law and R",
    11: "Materials and Activities Review",
    12: "Exam Diagrams and Combinations",
    13: "Definitions and Table Questions",
    14: "Long-answer Preparation",
    15: "Cross-links and Concept Maps",
    16: "Unit 3 Mastery Checklist",
}
