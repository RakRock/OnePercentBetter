"""Full concept card content for Harshit Physics Unit 4 — Days 1–16 (Ch 12 Magnetism)."""

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
    ("Electricity and magnetism linked", "A current-carrying wire behaves like a magnet — electricity and magnetism are related.", "current_magnetic_field", {"highlight": "overview"}, "Ch 12 builds on Ch 11 heating effect.", "Activity 12.1 compass deflects near wire.", "Current produces magnetic effect.", "", "", []),
    ("Oersted's discovery", "In 1820 Oersted found a compass needle deflected when current passed through a nearby wire.", "current_magnetic_field", {"highlight": "oersted"}, "First link between electricity and magnetism.", "Accidental lab observation changed physics.", "Oersted: current → magnetism.", "", "", []),
    ("Activity 12.1 setup", "Thick copper wire between X and Y; compass nearby; key closed → needle deflects.", "current_magnetic_field", {"mode": "activity_12_1"}, "Standard intro demo Fig 12.1.", "Wire perpendicular to paper plane.", "Deflection proves magnetic effect of current.", "", "", []),
    ("Compass as small magnet", "A compass needle is a small bar magnet — free to rotate horizontally.", "magnetic_field_lines", {"highlight": "compass"}, "Used to detect magnetic fields.", "Needle points roughly north-south.", "Compass needle = tiny magnet.", "", "", []),
    ("Magnetic effect vs heating", "Ch 11: heating effect of current. Ch 12: magnetic effect and electromagnetic devices.", "current_magnetic_field", {"mode": "compare_ch11"}, "Two major effects of current.", "Heater hot; wire near compass deflects.", "Same current, different effects.", "", "", []),
    ("Reverse possibility", "If current makes magnetism, moving magnets can produce electricity — studied later as electromagnetic induction.", "current_magnetic_field", {"mode": "reverse"}, "Foreshadows generator idea.", "Dynamic microphones use related physics.", "Magnetism ↔ electricity both ways.", "", "", []),
    ("Electromagnets preview", "This chapter includes electromagnets — magnetism from electric current in coils.", "solenoid_field", {"highlight": "electromagnet"}, "Practical application thread.", "Crane lifting scrap iron.", "Coil + iron core = electromagnet.", "", "", []),
    ("Unit of field strength", "Magnetic field strength unit oersted named after Hans Christian Oersted.", "formula_panel", {"formula": "oersted (Oe)", "label": "Honour"}, "Historical note in NCERT.", "Field strength has magnitude.", "Oersted unit for field strength.", "", "", []),
    ("Deflection meaning", "Compass deflection means the wire's current produced a magnetic field that acted on the needle.", "current_magnetic_field", {"highlight": "deflection"}, "Interpretation of Activity 12.1.", "Needle moves from north alignment.", "Deflection = magnetic force on needle.", "", "", []),
    ("Metallic conductor required", "Magnetic effect shown with metallic conductor carrying current — standard lab copper wire.", "current_magnetic_field", {"mode": "conductor"}, "Current must flow in conductor.", "Thick copper wire in activities.", "Metallic wire + current → field.", "", "", []),
])

DAY2 = _build_day(2, [
    ("Magnetic field definition", "Region around a magnet where magnetic force can be detected is called magnetic field.", "magnetic_field_lines", {"highlight": "definition"}, "Field exists even without iron filings.", "Iron filings experience force in region.", "Magnetic field = region of magnetic force.", "", "", ["magnetic field"]),
    ("Bar magnet poles", "Ends of bar magnet: north-seeking (north) pole and south-seeking (south) pole.", "magnetic_field_lines", {"highlight": "poles"}, "Compass points align with Earth's field.", "Mark N and S on bar magnet diagram.", "N pole and S pole.", "", "", []),
    ("Like poles repel", "Like magnetic poles repel each other.", "magnetic_field_lines", {"mode": "repel"}, "Fundamental magnet rule.", "Two north poles push apart.", "N–N or S–S → repulsion.", "", "", []),
    ("Unlike poles attract", "Unlike magnetic poles attract each other.", "magnetic_field_lines", {"mode": "attract"}, "Pair with repulsion rule.", "N near S pulls together.", "N–S → attraction.", "", "", []),
    ("Iron filings pattern", "Iron filings around bar magnet align along field lines (Activity 12.2).", "magnetic_field_lines", {"mode": "iron_filings"}, "Fig 12.2 salt-sprinkler demo.", "Tap board gently to see pattern.", "Filings show field direction/ strength.", "", "", []),
    ("Field has direction and magnitude", "Magnetic field is a vector quantity — both direction and strength matter.", "magnetic_field_lines", {"highlight": "vector"}, "NCERT explicit statement.", "Stronger field stronger force on pole.", "Field = direction + magnitude.", "", "", []),
    ("Field line direction convention", "Direction of field = direction a free north pole would move. Lines emerge from N, enter S.", "magnetic_field_lines", {"highlight": "direction"}, "Arrows on Fig 12.4.", "North pole of compass moves along field.", "Lines out of N, into S (outside magnet).", "", "", []),
    ("Field lines inside magnet", "Inside bar magnet, field lines go from south pole to north pole — closed curves.", "magnetic_field_lines", {"highlight": "inside"}, "Completes closed loop picture.", "Continue lines inside magnet body.", "Inside: S → N.", "Do not stop lines at surface only.", "", []),
    ("Closer lines stronger field", "Crowded field lines mean stronger magnetic field; spread lines mean weaker field.", "magnetic_field_lines", {"highlight": "strength"}, "Visual density = strength.", "Near poles lines crowded.", "Close lines = strong field.", "", "", []),
    ("Field lines never cross", "Two field lines never intersect — otherwise compass would show two directions at one point.", "magnetic_field_lines", {"highlight": "no_cross"}, "NCERT Q3 property.", "Impossible for needle at intersection.", "No two lines cross.", "", "", []),
])

DAY3 = _build_day(3, [
    ("Drawing field lines with compass", "Activity 12.3: move compass step by step from N to S pole, mark points, join smooth curve.", "magnetic_field_lines", {"mode": "activity_12_3"}, "Fig 12.3 method.", "Each step south pole follows previous north position.", "Compass maps one field line.", "", "", []),
    ("Multiple field lines", "Repeat compass procedure to draw many lines — pattern like Fig 12.4.", "magnetic_field_lines", {"mode": "pattern"}, "Full field map around magnet.", "Many curves from N to S.", "Family of lines shows full field.", "", "", []),
    ("Deflection increases near poles", "Compass deflection greater when moved toward magnet poles.", "magnetic_field_lines", {"mode": "near_poles"}, "Qualitative strength check.", "Feel stronger pull near poles.", "Stronger field near poles.", "", "", []),
    ("Properties list for exams", "List: direction N→S outside; closed curves; no crossing; density shows strength.", "magnetic_field_lines", {"mode": "properties"}, "NCERT Q2 answer template.", "Four bullet properties.", "Memorise four properties.", "", "", []),
    ("Why compass deflects near magnet", "Magnet exerts force on magnetic poles of compass needle — torque rotates it.", "magnetic_field_lines", {"mode": "why_deflect"}, "NCERT Q Ch 12.1.", "Needle aligns with local field direction.", "Force on poles rotates needle.", "", "", []),
    ("Hypothetical north pole on line", "Field line path = path free north pole would tend to move.", "magnetic_field_lines", {"highlight": "definition"}, "Definition of line direction.", "Think of tiny test north pole.", "Field line = north pole path.", "", "", []),
    ("Magnetic field lines vs electric", "Magnetic lines are closed curves; electric field lines start on + and end on − (Ch 12 contrast).", "magnetic_field_lines", {"mode": "compare_electric"}, "Conceptual distinction.", "Magnet field loops closed.", "Magnetic lines always closed.", "", "", []),
    ("Uniform field representation", "Parallel equally-spaced straight lines represent uniform magnetic field.", "magnetic_field_lines", {"mode": "uniform"}, "Inside solenoid approximates this.", "Draw parallel arrows same spacing.", "Uniform = parallel equal spacing.", "", "", []),
    ("Field line diagram exam skill", "Draw bar magnet field: curves from N to S outside, continue inside S to N.", "magnetic_field_lines", {"mode": "exam_draw"}, "Diagram question practice.", "Label N and S; arrow on lines.", "Closed curves with arrows.", "", "", []),
    ("Salt sprinkler tip", "Iron filings sprinkled uniformly then board tapped gently to reveal pattern.", "magnetic_field_lines", {"mode": "technique"}, "Activity 12.2 practical tip.", "Even sprinkling before tap.", "Tap gently for clear pattern.", "", "", []),
])

DAY4 = _build_day(4, [
    ("Current produces magnetic field", "Electric current through metallic conductor produces magnetic field around it — Activity 12.1 & 12.4.", "current_magnetic_field", {"highlight": "produce"}, "Core Ch 12.2 idea.", "Wire over compass deflects needle.", "Current → magnetic field.", "", "", []),
    ("Activity 12.4 direction change", "Reverse cell connections → current direction reverses → compass deflection reverses.", "current_magnetic_field", {"mode": "activity_12_4"}, "Fig 12.5 (a) and (b).", "East deflection one way, west when reversed.", "Field direction follows current direction.", "", "", []),
    ("Straight conductor field pattern", "Magnetic field around straight current-carrying wire = concentric circles (Activity 12.5).", "current_magnetic_field", {"highlight": "concentric"}, "Fig 12.6 iron filings circles.", "Circles centered on wire.", "Concentric circles around wire.", "", "", []),
    ("Field direction at a point", "Place compass on a circle — north pole direction gives field direction at that point.", "current_magnetic_field", {"mode": "find_direction"}, "Arrow on circle tangent.", "Compass at point P on circle.", "Compass shows field direction.", "", "", []),
    ("Current magnitude effect", "Increase current → greater compass deflection → stronger magnetic field.", "current_magnetic_field", {"highlight": "current"}, "Use rheostat in Activity 12.5.", "Higher ammeter reading → bigger deflection.", "B increases with current.", "", "", []),
    ("Distance effect", "Move compass farther from wire — deflection decreases — field weaker with distance.", "current_magnetic_field", {"highlight": "distance"}, "Compare points P and Q.", "Circles grow larger farther out.", "Field weaker farther from wire.", "", "", []),
    ("Larger circles farther out", "Concentric circles representing field become larger as distance from wire increases.", "current_magnetic_field", {"mode": "circles_size"}, "Fig 12.6 visual.", "Outer circles wider radius.", "Distance ↑ → circle radius ↑.", "", "", []),
    ("Wire vertical in cardboard", "Activity 12.5: wire through cardboard center normal to plane — circles in plane.", "current_magnetic_field", {"mode": "setup"}, "3D setup simplified to 2D diagram.", "Wire perpendicular to paper.", "Field circles lie in cardboard plane.", "", "", []),
    ("Pattern depends on shape", "Magnetic field pattern depends on shape of conductor — straight, loop, solenoid differ.", "current_magnetic_field", {"mode": "shape"}, "Leads to sections 12.2.3–12.2.4.", "Bend wire into loop pattern changes.", "Shape of conductor sets pattern.", "", "", []),
    ("Field reverses with current", "Reversing current through straight wire reverses direction of magnetic field at every point.", "current_magnetic_field", {"mode": "reverse"}, "Check in Activity 12.5.", "Swap battery terminals.", "Opposite current → opposite field.", "", "", []),
])

DAY5 = _build_day(5, [
    ("Right-hand thumb rule", "Hold current-carrying straight conductor in right hand: thumb = current direction, curled fingers = field line direction.", "right_hand_rule", {"highlight": "rule"}, "Fig 12.7 — essential rule.", "Thumb along wire current, fingers curl around.", "Thumb → I; fingers → B.", "", "", ["right-hand thumb rule"]),
    ("Maxwell's corkscrew rule", "Same rule as corkscrew: turning screw in current direction gives rotation of field.", "right_hand_rule", {"mode": "corkscrew"}, "NCERT footnote alternative name.", "Corkscrew rotation = field direction.", "Equivalent to right-hand thumb rule.", "", "", []),
    ("Example 12.1 east-west wire", "Current east to west: field below/above wire clockwise from east end, anticlockwise from west.", "right_hand_rule", {"mode": "example_12_1"}, "Apply rule in horizontal plane.", "Power line overhead field direction.", "Practice with horizontal wires.", "", "", []),
    ("Circular loop field", "Current through circular loop: concentric circles merge; at centre field lines appear straight.", "current_magnetic_field", {"mode": "circular_loop"}, "Fig 12.8.", "Arcs become straight at loop centre.", "Loop centre: straight field lines.", "", "", []),
    ("All loop sections same direction at centre", "Right-hand rule on each segment — contributions add same direction inside loop.", "right_hand_rule", {"mode": "loop_centre"}, "Why centre field is uniform-ish.", "Every part of loop helps same way.", "Inside loop field lines same sense.", "", "", []),
    ("n turns multiply field", "Coil with n turns: field n times single turn — same current direction in each turn adds.", "solenoid_field", {"highlight": "n_turns"}, "Quantitative loop coil idea.", "More turns stronger electromagnet.", "n turns → n × field of one turn.", "", "", []),
    ("Activity 12.6 circular coil", "Many-turn coil through cardboard; iron filings show field pattern when current flows.", "current_magnetic_field", {"mode": "activity_12_6"}, "Fig 12.9.", "Rectangular cardboard two holes.", "Multi-turn coil filing pattern.", "", "", []),
    ("Clockwise current loop — inside field", "Clockwise current in loop in table plane — apply RH rule: field inside points into table (standard convention).", "right_hand_rule", {"mode": "clockwise_loop"}, "NCERT Q solenoid section Q1.", "Practice inside vs outside loop.", "Inside/outside opposite by rule.", "", "", []),
    ("Solenoid definition", "Solenoid = many circular turns of insulated copper wire wrapped closely in cylinder shape.", "solenoid_field", {"highlight": "definition"}, "Fig 12.10.", "Coil looks like cylinder of wire.", "Tight cylindrical coil = solenoid.", "", "", ["solenoid"]),
    ("Solenoid like bar magnet", "Field outside solenoid resembles bar magnet — one end N-like, other S-like.", "solenoid_field", {"highlight": "bar_magnet"}, "Compare Fig 12.10 with 12.4.", "Iron filings similar patterns.", "Solenoid mimics bar magnet externally.", "", "", []),
])

DAY6 = _build_day(6, [
    ("Uniform field inside solenoid", "Inside solenoid field lines parallel straight lines — field same at all inside points (uniform).", "solenoid_field", {"highlight": "uniform"}, "NCERT MCQ answer (d).", "Parallel lines equal spacing inside.", "Inside solenoid: uniform B.", "", "", []),
    ("Electromagnet formation", "Strong solenoid field magnetises soft iron core placed inside — electromagnet.", "solenoid_field", {"mode": "electromagnet"}, "Fig 12.11 steel rod in coil.", "Switch on current → magnetise iron.", "Solenoid + soft iron = electromagnet.", "", "", ["electromagnet"]),
    ("Soft iron core", "Soft iron easily magnetised and demagnetised — ideal for temporary electromagnets.", "solenoid_field", {"highlight": "soft_iron"}, "Core material choice.", "Crane electromagnet drops load when off.", "Soft iron core for electromagnets.", "", "", []),
    ("Force on current in magnetic field", "Magnet exerts force on current-carrying conductor placed in magnetic field.", "flemings_left_hand", {"highlight": "force"}, "Section 12.3 Ampere idea.", "Activity 12.7 aluminium rod moves.", "Current in B field → force.", "", "", []),
    ("Activity 12.7 setup", "Aluminium rod between horseshoe magnet poles; current B to A; rod displaces left.", "flemings_left_hand", {"mode": "activity_12_7"}, "Fig 12.12.", "Rod suspended horizontally.", "Rod jumps when current + field.", "", "", []),
    ("Reverse current reverses force", "Reverse rod current direction → displacement direction reverses (right instead of left).", "flemings_left_hand", {"mode": "reverse_current"}, "Shows force ∝ current direction.", "Swap battery on rod.", "Flip current → flip force.", "", "", []),
    ("Reverse field reverses force", "Swap magnet poles (field down instead of up) → force direction reverses again.", "flemings_left_hand", {"mode": "reverse_field"}, "Third variable in Activity 12.7.", "Turn magnet over.", "Flip B → flip force.", "", "", []),
    ("Maximum force when perpendicular", "Force largest when current and magnetic field are perpendicular.", "flemings_left_hand", {"highlight": "perpendicular"}, "Optimal geometry for motor force.", "Rod between poles field ⊥ rod.", "I ⊥ B → maximum force.", "", "", []),
    ("Fleming's left-hand rule", "Stretch thumb, forefinger, middle finger mutually ⊥: forefinger = B, middle = I, thumb = force/motion.", "flemings_left_hand", {"highlight": "rule"}, "Fig 12.13.", "FBI mnemonic order for left hand.", "First=B, second=I, thumb=F.", "Use left hand not right.", "", ["Fleming's left-hand rule"]),
    ("Force perpendicular to both", "Force direction perpendicular to both current and magnetic field.", "flemings_left_hand", {"mode": "perpendicular_force"}, "3D geometry of motor force.", "Thumb out when B and I in plane.", "F ⊥ I and F ⊥ B.", "", "", []),
])

DAY7 = _build_day(7, [
    ("Devices using motor effect", "Electric motor, generator, loudspeaker, microphone, measuring instruments use conductor in magnetic field.", "flemings_left_hand", {"mode": "devices"}, "NCERT device list.", "Motor turns electrical to mechanical.", "Left-hand rule devices list.", "", "", []),
    ("Example 12.2 electron", "Electron at right angles to field — conventional current opposite to motion → force into page (d).", "flemings_left_hand", {"mode": "electron"}, "Reverse current for electrons.", "Current direction opposite electron velocity.", "Electrons: reverse current direction.", "", "", []),
    ("Velocity can change in B field", "Proton in magnetic field: velocity and momentum direction change; speed may stay same.", "flemings_left_hand", {"mode": "proton_q"}, "NCERT Q velocity/momentum.", "Magnetic force can turn path.", "Direction changes in uniform B.", "", "", []),
    ("Increase current increases displacement", "Activity 12.7: larger current → larger rod displacement (stronger force).", "flemings_left_hand", {"highlight": "current"}, "Qualitative prediction.", "Rheostat up → bigger kick.", "More I → more force.", "", "", []),
    ("Stronger magnet more displacement", "Stronger horseshoe magnet → greater displacement of rod.", "flemings_left_hand", {"highlight": "magnet"}, "Field strength effect.", "Replace with stronger magnet.", "Stronger B → more force.", "", "", []),
    ("Longer rod more force", "Longer conductor in field experiences greater force (more length in B).", "flemings_left_hand", {"mode": "length"}, "Activity 12.7 extension question.", "More wire in magnetic gap.", "Longer rod → larger force.", "", "", []),
    ("Alpha particle deflection", "Positive charge projected west, deflected north → magnetic field upward (More to Know Q3 d).", "flemings_left_hand", {"mode": "alpha"}, "Apply left-hand rule carefully.", "Force direction from FBI rule.", "Use charge sign for current direction.", "", "", []),
    ("MRI connection", "Weak nerve currents produce tiny magnetic fields — MRI uses body magnetism in medicine.", "formula_panel", {"formula": "MRI uses body fields", "label": "More to Know"}, "NCERT medicine box.", "Heart and brain fields imaged.", "Magnetism used in medical imaging.", "", "", []),
    ("Earth's field comparison", "Body fields ~ one-billionth of Earth's field — extremely weak.", "magnetic_field_lines", {"mode": "mri_weak"}, "Scale appreciation.", "Need sensitive instruments for MRI.", "Biofields very weak.", "", "", []),
    ("Ampere's suggestion", "Ampere: magnet must exert equal and opposite force on current-carrying conductor.", "flemings_left_hand", {"mode": "ampere"}, "Newton's third law spirit.", "Action on magnet and conductor.", "Mutual force between magnet and wire.", "", "", []),
])

DAY8 = _build_day(8, [
    ("Domestic mains supply", "Home electric power from mains via overhead lines or underground cables.", "domestic_circuit", {"highlight": "mains"}, "Section 12.4.", "220 V supply in India.", "Mains brings power to meter board.", "", "", []),
    ("Live wire", "Live wire (red insulation) — positive side of 220 V supply.", "domestic_circuit", {"highlight": "live"}, "Dangerous to touch bare live.", "Red wire in domestic circuit.", "Live = red, high potential.", "", "", ["live wire"]),
    ("Neutral wire", "Neutral wire (black insulation) — negative return at ~0 V reference.", "domestic_circuit", {"highlight": "neutral"}, "Completes circuit with live.", "Black wire returns current.", "Neutral = black.", "", "", ["neutral wire"]),
    ("220 V in India", "Potential difference between live and neutral is 220 V in our country.", "formula_panel", {"formula": "220 V mains", "label": "Domestic PD"}, "Standard supply voltage.", "Appliances rated 220 V.", "Live–neutral = 220 V.", "", "", []),
    ("Earth wire", "Earth wire (green insulation) connected to metal plate buried deep in ground.", "domestic_circuit", {"highlight": "earth"}, "Safety for metal-bodied appliances.", "Green wire to ground plate.", "Earth = green, safety.", "", "", ["earth wire"]),
    ("Earth wire purpose", "Provides low-resistance path for leakage current — keeps appliance body at earth potential.", "domestic_circuit", {"mode": "earth_why"}, "Prevents severe shock.", "Refrigerator metal body earthed.", "Earth prevents shock from leakage.", "", "", []),
    ("Meter board and main fuse", "Live and neutral enter electricity meter through main fuse, then main switch to house circuits.", "domestic_circuit", {"mode": "meter"}, "Fig 12.15 schematic.", "Meter measures consumption.", "Fuse at meter protects installation.", "", "", []),
    ("Two circuit ratings", "Often 15 A circuit for high-power devices (geyser, cooler) and 5 A for bulbs, fans.", "domestic_circuit", {"highlight": "ratings"}, "Separate circuit capacity.", "Heavy appliances on 15 A line.", "15 A high power; 5 A lights/fans.", "", "", []),
    ("Appliances in parallel", "Each appliance connected parallel across live and neutral — same 220 V each.", "domestic_circuit", {"highlight": "parallel"}, "Fig 12.15 each branch parallel.", "Fan and bulb same voltage.", "Domestic = parallel branches.", "Series would divide voltage wrongly.", "", []),
    ("Separate appliance switches", "Each appliance has its own ON/OFF switch on live side branch.", "domestic_circuit", {"mode": "switches"}, "Independent control.", "Switch off fan, light stays on.", "One switch per appliance.", "", "", []),
])

DAY9 = _build_day(9, [
    ("Electric fuse in domestic circuit", "Fuse prevents damage from overloading and short circuit — studied in Ch 11, applied here.", "domestic_circuit", {"highlight": "fuse"}, "Links Ch 11 and 12.", "Joule heat melts fuse wire.", "Fuse = essential safety device.", "", "", ["fuse"]),
    ("Short circuit", "Live and neutral directly contact — resistance drops — current abruptly increases.", "domestic_circuit", {"mode": "short"}, "Damaged insulation cause.", "Spark and huge current flow.", "Short circuit = sudden high I.", "", "", ["short circuit"]),
    ("Overloading", "Too many appliances or voltage surge draws current beyond safe limit.", "domestic_circuit", {"mode": "overload"}, "Too many on one socket.", "Multiple heaters one socket dangerous.", "Overload = excessive current.", "", "", ["overloading"]),
    ("Fuse melts to break circuit", "High current heats fuse wire (Joule heating) until it melts and breaks circuit.", "domestic_circuit", {"mode": "fuse_action"}, "Ch 11 H=I²Rt applied.", "Thin fuse wire designed to melt first.", "Fuse melts → circuit open.", "", "", []),
    ("Safety measures two", "Earth wire and electric fuse — two common safety measures (NCERT Q1).", "domestic_circuit", {"mode": "safety_two"}, "Exam short answer.", "Green earth + fuse at meter.", "Earth wire + fuse.", "", "", []),
    ("2 kW oven on 5 A circuit", "2 kW at 220 V needs ~9 A — exceeds 5 A rating → overload, fuse should blow.", "domestic_circuit", {"mode": "oven_example"}, "NCERT Q2 calculation.", "P=VI → I=P/V ≈ 9.1 A.", "Check I against circuit rating.", "", "", []),
    ("Avoid overloading precautions", "Not too many appliances on one socket; proper insulation; correct fuse rating.", "domestic_circuit", {"mode": "precautions"}, "NCERT Q3 prevention.", "Spread high-power devices.", "Avoid many high-P devices together.", "", "", []),
    ("Metallic body appliances", "Press, toaster, fan, fridge — metal body should be earthed.", "domestic_circuit", {"highlight": "metallic"}, "Leakage to body without earth is dangerous.", "Three-pin plug with earth pin.", "Earth metallic appliances.", "", "", []),
    ("AC mains frequency", "Domestic AC supply 220 V, 50 Hz in India (NCERT summary).", "formula_panel", {"formula": "220 V, 50 Hz AC", "label": "Mains"}, "What you have learnt box.", "Alternating current from grid.", "220 V, 50 Hz standard.", "", "", []),
    ("Schematic Fig 12.15", "Read domestic circuit diagram: meter, fuse, main switch, parallel branches, earth.", "domestic_circuit", {"mode": "fig_12_15"}, "Diagram interpretation skill.", "Trace live from meter to loads.", "Know Fig 12.15 layout.", "", "", []),
])

# Days 10–16: review, numerics, exam prep
DAY10 = _build_day(10, [
    ("Long straight wire field MCQ", "Field = concentric circles around wire — not radial, not parallel to wire.", "current_magnetic_field", {"mode": "mcq_wire"}, "Exercise Q1 answer (d) pattern.", "Circles centered on conductor.", "Concentric circles — correct option.", "", "", []),
    ("Solenoid interior MCQ", "Inside long solenoid carrying current field is same at all points — uniform.", "solenoid_field", {"mode": "mcq_solenoid"}, "Section Q3 (d).", "Parallel field lines inside.", "Uniform inside solenoid.", "", "", []),
    ("Draw field around bar magnet", "Exam task: N→S outside, closed curves, arrows, no crossing.", "magnetic_field_lines", {"mode": "exam"}, "NCERT Q12.2.1.", "Include inside magnet direction.", "Standard bar magnet diagram.", "", "", []),
    ("Draw field around straight wire", "Circles around wire; arrow direction from right-hand rule.", "current_magnetic_field", {"mode": "exam"}, "Combine with RH rule.", "Mark current direction on wire.", "Concentric circles + RH rule.", "", "", []),
    ("Compare solenoid and magnet", "External field similar; solenoid field can switch off with current.", "solenoid_field", {"mode": "compare"}, "Electromagnet advantage.", "Bar magnet permanent; solenoid temporary.", "Solenoid controllable magnet.", "", "", []),
    ("Motor effect summary", "Current perpendicular to B experiences force given by Fleming's left-hand rule.", "flemings_left_hand", {"mode": "summary"}, "One-line motor principle.", "Thumb = motion in motor context.", "Left hand FBI for force.", "", "", []),
    ("Generator vs motor preview", "Motor: electrical → mechanical (force on current). Generator: opposite (induction later).", "flemings_left_hand", {"mode": "motor_gen"}, "Direction of energy conversion.", "Motor uses left-hand rule force.", "Motor converts electric to motion.", "", "", []),
    ("Domestic parallel why", "Equal 220 V to each appliance; independent operation.", "domestic_circuit", {"mode": "why_parallel"}, "Conceptual domestic wiring.", "Unlike series dimming problem.", "Parallel for equal voltage.", "", "", []),
    ("Colour coding wires", "Red live, black neutral, green earth — know insulation colours.", "domestic_circuit", {"highlight": "colours"}, "Exam identification.", "Three-colour wire system.", "Red-black-green coding.", "", "", []),
    ("Ch 11 fuse link", "Fuse principle from Ch 11 heating effect — melt on excess current.", "domestic_circuit", {"mode": "ch11_link"}, "Cross-chapter connection.", "I²R heat in fuse wire.", "Same fuse physics as Ch 11.", "", "", []),
])

DAY11 = _build_day(11, [
    ("Field line density quiz", "Where lines crowded → stronger field; near poles and near wire with high I.", "magnetic_field_lines", {"mode": "quiz"}, "Revision.", "Compare two points on diagram.", "Density ∝ strength.", "", "", []),
    ("RH rule practice horizontal", "Practice east-west, north-south wire field directions below and above wire.", "right_hand_rule", {"mode": "practice"}, "Example 12.1 variants.", "Horizontal power lines.", "Draw circular field in plane ⊥ wire.", "", "", []),
    ("Loop vs straight field", "Straight: circles; loop: straight at centre; solenoid: uniform inside.", "current_magnetic_field", {"mode": "compare_shapes"}, "Three shapes summary.", "Shape changes field map.", "Three conductor shapes three patterns.", "", "", []),
    ("Turns and current both matter", "Stronger electromagnet: more turns AND larger current.", "solenoid_field", {"mode": "stronger"}, "Design electromagnets.", "More coils + higher I.", "n and I both increase B.", "", "", []),
    ("Left-hand rule vs thumb rule", "Thumb rule finds B from I; left-hand rule finds F on conductor in B.", "flemings_left_hand", {"mode": "two_rules"}, "Do not confuse rules.", "Different questions different rule.", "RH thumb = B; Left hand = F.", "Right hand for B, left for F.", "", []),
    ("Perpendicular requirement", "Left-hand rule simplest when I ⊥ B; force still defined generally.", "flemings_left_hand", {"highlight": "perpendicular"}, "Activity 12.7 geometry.", "Rod between pole faces.", "⊥ case for exam Fleming rule.", "", "", []),
    ("Magnetic field unit tesla note", "Class 10 uses concept; oersted named; SI field unit tesla (extension).", "formula_panel", {"formula": "Field strength units", "label": "Extension"}, "Optional enrichment.", "Oersted honours Oersted.", "Field has SI units.", "", "", []),
    ("Insulation damage hazard", "Damaged wire insulation can cause short circuit and fire risk.", "domestic_circuit", {"mode": "insulation"}, "Safety awareness.", "Frayed cord danger.", "Damaged insulation → short.", "", "", []),
    ("Main switch role", "Main switch disconnects entire house from live supply during repair.", "domestic_circuit", {"mode": "main_switch"}, "Safety procedure.", "Turn off before wiring work.", "Main switch isolates house.", "", "", []),
    ("Energy meter", "Electricity meter measures kWh consumption for billing.", "domestic_circuit", {"mode": "meter"}, "Link Ch 11 kWh.", "Meter board first device.", "Meter records energy used.", "", "", []),
])

DAY12 = _build_day(12, [
    ("Activity sequence review", "12.1 compass near wire; 12.2 filings bar magnet; 12.5 circles; 12.7 force on rod.", "current_magnetic_field", {"mode": "activities"}, "Lab sequence recall.", "Match activity to observation.", "Know key activities.", "", "", []),
    ("Properties long answer", "Write four magnetic field line properties with explanation.", "magnetic_field_lines", {"mode": "long_answer"}, "3-mark question.", "Closed, no cross, N→S, density.", "Four properties paragraph.", "", "", []),
    ("RH rule long answer", "Explain rule with diagram; apply to straight wire.", "right_hand_rule", {"mode": "long_answer"}, "Rule explanation question.", "Thumb I, fingers B.", "Statement + diagram + example.", "", "", []),
    ("Electromagnet long answer", "Solenoid + soft iron; current magnetises; uses in cranes, separators.", "solenoid_field", {"mode": "long_answer"}, "Application essay.", "Switch off demagnetises soft iron.", "Coil + core + uses.", "", "", []),
    ("Fleming rule long answer", "State rule; diagram three fingers; motor example.", "flemings_left_hand", {"mode": "long_answer"}, "Motor effect essay.", "B, I, F mutually perpendicular.", "Rule + diagram + device.", "", "", []),
    ("Domestic circuit long answer", "Describe live, neutral, earth, fuse, parallel appliances Fig 12.15.", "domestic_circuit", {"mode": "long_answer"}, "Domestic essay template.", "220 V, 15 A and 5 A circuits.", "Full domestic circuit description.", "", "", []),
    ("Short circuit vs overload", "Short: live-neutral touch; overload: too much load or voltage hike.", "domestic_circuit", {"mode": "compare_hazards"}, "Distinguish exam answers.", "Different causes same fuse action.", "Short ≠ overload cause but both high I.", "", "", []),
    ("Why two field lines never cross", "Compass would show two directions — impossible — so lines don't intersect.", "magnetic_field_lines", {"mode": "exam_why"}, "NCERT explain Q.", "Unique field direction at point.", "One direction per point.", "", "", []),
    ("Compass near bar magnet why", "Magnet field exerts torque on compass poles — needle aligns.", "magnetic_field_lines", {"mode": "exam_why"}, "Section 12.1 Q.", "Unlike poles attract alignment.", "Torque rotates needle.", "", "", []),
    ("Electron current convention", "Electron motion opposite to conventional current — reverse when using Fleming rule.", "flemings_left_hand", {"mode": "convention"}, "Example 12.2 key.", "Current opposite electron velocity.", "Flip direction for electrons.", "", "", []),
])

DAY13 = _build_day(13, [
    ("Define magnetic field", "Region where magnetic force on a pole can be detected.", "magnetic_field_lines", {"mode": "definition"}, "1-mark.", "Around magnet or current wire.", "Region of magnetic force.", "", "", []),
    ("Define solenoid", "Cylinder-shaped coil of many closely wound turns of insulated copper wire.", "solenoid_field", {"mode": "definition"}, "1-mark.", "Looks like spring of wire.", "Many turns cylindrical coil.", "", "", []),
    ("Define electromagnet", "Magnet formed by magnetising soft iron core inside current-carrying solenoid.", "solenoid_field", {"mode": "definition_em"}, "1-mark.", "Temporary magnet.", "Solenoid + soft iron core.", "", "", []),
    ("State Fleming's left-hand rule", "B = first finger, I = second finger, F = thumb, mutually perpendicular.", "flemings_left_hand", {"mode": "definition"}, "Must state fingers.", "Left hand only.", "Three fingers FBI.", "", "", []),
    ("State right-hand thumb rule", "Thumb along current, fingers curl in field direction around straight conductor.", "right_hand_rule", {"mode": "definition"}, "Pair with Fleming.", "Right hand for field from I.", "Thumb I, curl B.", "", "", []),
    ("Domestic wire colours exam", "Live red, neutral black, earth green.", "domestic_circuit", {"mode": "exam_colours"}, "Quick recall.", "Three wires three colours.", "Red-black-green.", "", "", []),
    ("220 V appliance design", "Appliances rated 220 V for Indian mains parallel connection.", "domestic_circuit", {"mode": "rating"}, "Match supply to device.", "Label on back of appliance.", "Design for 220 V mains.", "", "", []),
    ("15 A vs 5 A usage", "15 A: geyser, cooler; 5 A: bulbs, fans — match load to circuit.", "domestic_circuit", {"mode": "rating_use"}, "Prevent overload.", "Check nameplate power.", "High P needs 15 A circuit.", "", "", []),
    ("Calculate oven current", "I = P/V = 2000/220 ≈ 9.1 A > 5 A → overload on 5 A circuit.", "formula_panel", {"formula": "I = P/V", "label": "Oven check"}, "NCERT Q2 domestic.", "Compare to circuit rating.", "P/V then compare A rating.", "", "", []),
    ("Field uniform diagram", "Draw parallel equally spaced lines with arrows — uniform magnetic field.", "magnetic_field_lines", {"mode": "uniform_draw"}, "Solenoid interior Q2.", "Straight parallel arrows.", "Uniform field diagram.", "", "", []),
])

DAY14 = _build_day(14, [
    ("Chapter map", "Ch 12: field lines → current makes B → RH rule → loop/solenoid → force → Fleming → domestic.", "magnetic_field_lines", {"mode": "map"}, "Revision overview.", "Six blocks in order.", "Follow NCERT section flow.", "", "", []),
    ("Link to Unit 3 electricity", "Domestic circuits use Ch 11 fuse, power, overloading with Ch 12 wiring layout.", "domestic_circuit", {"mode": "unit3_link"}, "Cross-unit revision.", "P=VI for oven check.", "Ch 11 + Ch 12 together for mains.", "", "", []),
    ("Oersted historical", "First showed electricity causes magnetism — start of electromagnetism technology.", "current_magnetic_field", {"mode": "history"}, "Context for chapter.", "Radio, TV, fiber optics legacy.", "Oersted 1820 discovery.", "", "", []),
    ("Ampere and force", "Ampere recognised mutual force between magnet and current-carrying conductor.", "flemings_left_hand", {"mode": "history"}, "Section 12.3 intro.", "Foundation of electrodynamics.", "Ampere + force on wire.", "", "", []),
    ("MRI More to Know", "Nerve impulses create weak magnetic fields; MRI images body using magnetism.", "formula_panel", {"formula": "MRI imaging", "label": "Medicine"}, "Real-world magnetism.", "Non-invasive body imaging.", "Magnetism in medicine.", "", "", []),
    ("Loudspeaker brief", "Uses motor effect — current in magnetic field moves coil/cone to produce sound.", "flemings_left_hand", {"mode": "loudspeaker"}, "Device application.", "Reverse also works as microphone.", "Force on current → vibration → sound.", "", "", []),
    ("Electric motor brief", "Coil in magnetic field experiences torque from force — rotates (motor effect).", "flemings_left_hand", {"mode": "motor"}, "Qualitative only in Class 10.", "Split-ring commutator (extension).", "Force on coil → rotation.", "", "", []),
    ("Permanent vs electromagnet", "Bar magnet permanent; electromagnet only when current flows — controllable.", "solenoid_field", {"mode": "permanent_vs"}, "Compare advantages.", "Electromagnet can switch off.", "Electromagnet temporary.", "", "", []),
    ("Three-pin plug earth", "Third pin connects appliance metal body to earth wire for safety.", "domestic_circuit", {"mode": "three_pin"}, "Practical home safety.", "Top pin earth in many plugs.", "Earth pin protects user.", "", "", []),
    ("MCQ trap: field lines parallel to wire", "Wrong — field circles are perpendicular plane to wire, not parallel to wire.", "current_magnetic_field", {"mode": "trap"}, "Exercise distractor.", "Circles not lines along wire.", "Field ⊥ wire axis in plane.", "", "", []),
])

DAY15 = _build_day(15, [
    ("Mastery: field line rules", "Closed curves; N out S in; no crossing; density = strength; direction = N pole motion.", "magnetic_field_lines", {"mode": "checklist"}, "Self-test.", "Recite four properties.", "Four rules memorised.", "", "", []),
    ("Mastery: two hand rules", "Right thumb: B from I in straight wire. Left hand: F on wire in B.", "right_hand_rule", {"mode": "checklist"}, "Hand rule quiz.", "Which hand which purpose.", "RH=B, LH=F.", "", "", []),
    ("Mastery: three field patterns", "Straight wire circles; loop straight at centre; solenoid uniform inside.", "current_magnetic_field", {"mode": "checklist"}, "Draw all three.", "Sketch from memory.", "Three patterns known.", "", "", []),
    ("Mastery: domestic safety", "Live red, neutral black, earth green; fuse; no overload; earth metal bodies.", "domestic_circuit", {"mode": "checklist"}, "Safety checklist.", "Oven on 5 A fails.", "Safety six points.", "", "", []),
    ("Mastery: activities", "Match 12.1 deflection, 12.2 filings, 12.5 circles, 12.7 rod force.", "current_magnetic_field", {"mode": "checklist"}, "Activity recall.", "One sentence each activity.", "Four key activities.", "", "", []),
    ("Mastery: devices list", "Motor, generator, speaker, microphone, measuring instruments — motor effect.", "flemings_left_hand", {"mode": "checklist"}, "Device recall.", "Left-hand rule applications.", "Five device types.", "", "", []),
    ("Common pitfalls", "Confuse two hand rules; forget electron current reverse; mix series domestic wiring.", "formula_panel", {"formula": "Pitfalls", "label": "Exam"}, "Error avoidance.", "Read question: B or F?", "Three common traps.", "", "", []),
    ("Numerical oven fuse", "Always I=P/V then compare fuse and circuit A rating.", "domestic_circuit", {"mode": "numerical"}, "Repeated exam style.", "2 kW example template.", "P/V vs rating.", "", "", []),
    ("Diagram exam pack", "Prepare bar magnet, straight wire circles, solenoid, Fleming hand, domestic schematic.", "magnetic_field_lines", {"mode": "diagram_pack"}, "Five diagrams practice.", "Timed drawing drill.", "Five standard diagrams.", "", "", []),
    ("Ready for practice", "160 concept cards on Magnetic Effects — Practice tab uses 200-question bank.", "magnetic_field_lines", {"mode": "complete"}, "Bridge to Stage 2.", "15 Q per session + Grok.", "Concepts done → practice.", "", "", []),
])

DAY16 = _build_day(16, [
    ("What you have learnt — poles", "Compass needle small magnet; north and south poles defined.", "magnetic_field_lines", {"mode": "ncert"}, "Official summary 1.", "Align with textbook box.", "NCERT summary point.", "", "", []),
    ("What you have learnt — field lines", "Field lines show direction and strength; closer lines stronger field.", "magnetic_field_lines", {"mode": "ncert"}, "Summary 2–4.", "Closed curves.", "Summary alignment.", "", "", []),
    ("What you have learnt — current B", "Current in wire has circular field lines; direction by right-hand rule.", "current_magnetic_field", {"mode": "ncert"}, "Summary 5–6.", "Shape affects pattern.", "RH rule in summary.", "", "", []),
    ("What you have learnt — solenoid", "Solenoid field like bar magnet; electromagnet = soft iron in solenoid.", "solenoid_field", {"mode": "ncert"}, "Summary 7–8.", "Uniform inside.", "Electromagnet summary.", "", "", []),
    ("What you have learnt — force", "Force on current in B; perpendicular case uses Fleming left-hand rule.", "flemings_left_hand", {"mode": "ncert"}, "Summary 9.", "Mutually perpendicular.", "Fleming in summary.", "", "", []),
    ("What you have learnt — domestic", "220 V AC; live red, neutral black, earth green; fuse safety.", "domestic_circuit", {"mode": "ncert"}, "Summary 10–11.", "50 Hz mentioned.", "Domestic summary bullets.", "", "", []),
    ("Exercise Q1 wire field", "Correct: concentric circles about straight wire.", "current_magnetic_field", {"mode": "exercise"}, "End chapter Q1.", "Eliminate radial/parallel options.", "(d) style concentric.", "", "", []),
    ("Exercise solenoid uniform", "Inside long solenoid field same at all points.", "solenoid_field", {"mode": "exercise"}, "Section MCQ.", "Option (d) uniform.", "Uniform interior.", "", "", []),
    ("Safety first culture", "Turn off mains before work; never bypass fuse; use earth for metal cases.", "domestic_circuit", {"mode": "safety"}, "Life skills.", "Qualified electrician for wiring.", "Safe home electricity habits.", "", "", []),
    ("Unit 4 complete", "Unit 4 Magnetic Effects complete — all 160 cards; proceed to Practice when unlocked.", "magnetic_field_lines", {"highlight": "overview", "mode": "complete"}, "Completion card.", "200 MCQs in bank.", "Unit 4 mastery path done.", "", "", []),
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
    1: "Magnetism and Electric Current",
    2: "Magnetic Field and Field Lines",
    3: "Mapping and Properties of Field Lines",
    4: "Magnetic Field due to Straight Conductor",
    5: "Right-Hand Rule, Loop and Solenoid",
    6: "Electromagnets and Force on a Conductor",
    7: "Fleming's Left-Hand Rule and Applications",
    8: "Domestic Electric Circuits — Basics",
    9: "Fuse, Short Circuit and Overloading",
    10: "Exam Diagrams and MCQ Anchors",
    11: "Mixed Review and Safety",
    12: "Long-answer Preparation",
    13: "Definitions and Numericals",
    14: "Cross-links and Real-world Uses",
    15: "Mastery Checklist",
    16: "NCERT Summary and Unit Complete",
}
