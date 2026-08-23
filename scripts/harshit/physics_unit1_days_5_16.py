"""Full concept card content for Harshit Physics Unit 1 — Days 5–16."""

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


def _day5() -> list:
    d = 5
    return [
        _card(f"u1_d{d}_c01", "Object at infinity", "When the object is very far away, its rays reaching the mirror are nearly parallel to the principal axis.", "concave_image", {"position": "infinity"}, "This is the starting case for many concave-mirror ray diagrams.", "A distant tree or the Sun acts like an object at infinity.", "Parallel rays → image forms at focus F.", "Infinity here means very far, not literally endless in problems.", "", ["object at infinity"]),
        _card(f"u1_d{d}_c02", "Object beyond C", "The object lies outside the centre of curvature — farther from the mirror than point C.", "concave_image", {"position": "beyond_C"}, "Image location and size change predictably as the object moves along the axis.", "Place a candle beyond C on your marked principal axis.", "Object beyond C → real, inverted, diminished image between F and C.", "Beyond C means object distance > R = 2f.", "", ["centre of curvature"]),
        _card(f"u1_d{d}_c03", "Object at C", "The object is placed exactly at the centre of curvature C on the principal axis.", "concave_image", {"position": "at_C"}, "A special symmetric case: object and image distances are equal.", "Object at C gives image also at C.", "Object at C → image at C, same size, inverted, real.", "At C is not the same as at F.", "", ["object distance"]),
        _card(f"u1_d{d}_c04", "Image position", "Image position tells where rays actually meet (real) or appear to meet (virtual) after reflection.", "concave_image", {"highlight": "image_point"}, "You locate it on a ray diagram where reflected rays cross.", "Mark where two reflected rays intersect — that is the image point.", "Real image: rays cross; virtual: extend rays backward.", "Position is measured from pole P along the axis.", "", ["image distance"]),
        _card(f"u1_d{d}_c05", "Image size", "Image size compares how tall the image is relative to the object — enlarged, same, or diminished.", "concave_image", {"highlight": "size_compare"}, "Size helps classify the image without doing calculations first.", "A small distant image on a screen is diminished.", "Compare heights along a vertical line through the axis.", "Size is not the same as magnification sign.", "", ["magnification"]),
        _card(f"u1_d{d}_c06", "Image orientation", "Orientation means whether the image is erect (same way up) or inverted (upside down).", "concave_image", {"highlight": "inverted"}, "Real images from concave mirrors are usually inverted.", "A candle flame inverted on a screen is upside down.", "Inverted ≠ reversed left-right only — top becomes bottom.", "Virtual images in concave mirrors can be erect.", "", ["inverted image"]),
        _card(f"u1_d{d}_c07", "Real image", "A real image forms where reflected light rays actually meet. It can be projected onto a screen.", "concave_image", {"highlight": "real_screen"}, "Real images carry light energy to a screen.", "Activity 9.3: candle image on paper is a real image.", "Real image = rays actually intersect.", "Real does not mean erect.", "", ["real image"]),
        _card(f"u1_d{d}_c08", "Screen formation", "If a screen is placed at the image position, a sharp real image can be seen on the screen.", "concave_image", {"highlight": "screen"}, "Screens catch light — only real images can be captured this way.", "Move a paper screen until the candle image is sharpest.", "Only real images form on a screen.", "Virtual images cannot be obtained on a screen.", "", ["screen"]),
        _card(f"u1_d{d}_c09", "Diminished image", "A diminished image is smaller than the object in height.", "concave_image", {"position": "beyond_C", "highlight": "diminished"}, "Common when the object is far from a concave mirror.", "Distant object beyond C → small inverted image.", "Diminished means shorter arrow, not farther away.", "Diminished refers to height, not distance.", "", ["diminished image"]),
        _card(f"u1_d{d}_c10", "Same-sized image", "When the object is at C, the concave mirror gives a real, inverted image the same size as the object.", "concave_image", {"position": "at_C", "highlight": "same_size"}, "The equal-distance case at C is worth remembering before moving the object closer.", "Object height equals image height when object is at C.", "Same size at C only (for standard cases).", "Same size does not mean erect.", "", ["same-sized image"]),
    ]


def _day6() -> list:
    d = 6
    return [
        _card(f"u1_d{d}_c01", "Object between C and F", "The object sits between centre C and focus F — closer to the mirror than C but beyond F.", "concave_image", {"position": "between_C_F"}, "Image moves beyond C and grows as the object approaches F.", "Candle between C and F → large real image beyond C.", "Between C and F → real, inverted, enlarged, beyond C.", "This region is not the same as inside F.", "", []),
        _card(f"u1_d{d}_c02", "Object at F", "The object is placed exactly at the principal focus F of the concave mirror.", "concave_image", {"position": "at_F"}, "Reflected rays become parallel — image forms at infinity.", "Object at F → parallel reflected rays, no sharp screen image.", "At F → image at infinity (theoretically).", "At F is a limiting case, not a sharp image position.", "", []),
        _card(f"u1_d{d}_c03", "Object between F and P", "The object is between focus F and pole P — very close to the mirror.", "concave_image", {"position": "between_F_P"}, "Only here does a concave mirror give a virtual, erect, enlarged image.", "Face close to a shaving mirror — enlarged erect view.", "Inside F → virtual, erect, enlarged, behind mirror.", "Do not confuse with object beyond C.", "", []),
        _card(f"u1_d{d}_c04", "Enlarged image", "An enlarged image is taller than the object.", "concave_image", {"highlight": "enlarged"}, "Magnification magnitude greater than 1 in size comparison.", "Make-up mirror shows an enlarged face.", "Enlarged = bigger height, not necessarily real.", "Enlarged virtual images are possible inside F.", "", []),
        _card(f"u1_d{d}_c05", "Image beyond C", "For an object between C and F, the real image forms beyond centre C.", "concave_image", {"position": "between_C_F", "highlight": "image_beyond_C"}, "Image distance increases as object nears F.", "Object slides toward F → image slides farther past C.", "Object between C and F → image beyond C.", "", "", []),
        _card(f"u1_d{d}_c06", "Image at infinity", "When the object is at F, reflected rays are parallel and the image is said to be at infinity.", "concave_image", {"position": "at_F", "highlight": "infinity"}, "No single meeting point on the screen in the ideal case.", "Sharp spot fails when object sits at F.", "Parallel reflected rays → image at infinity.", "Infinity in diagrams means rays do not meet in finite space.", "", []),
        _card(f"u1_d{d}_c07", "Image behind the mirror", "For a virtual image, rays appear to come from a point behind the reflecting surface.", "concave_image", {"position": "between_F_P", "highlight": "behind"}, "Draw dotted backward extensions to locate it.", "Shaving mirror image seems behind the glass.", "Virtual image location is behind the mirror.", "Behind the mirror does not mean inside the glass physically.", "", []),
        _card(f"u1_d{d}_c08", "Virtual image", "Light does not actually meet at a virtual image; the eye traces rays backward to see it.", "concave_image", {"highlight": "virtual"}, "You can see it but cannot capture it on a screen.", "Mirror face view is a virtual image.", "Virtual = apparent meeting point only.", "Virtual is visible — not invisible.", "", ["virtual image"]),
        _card(f"u1_d{d}_c09", "Erect image", "An erect image has the same vertical orientation as the object.", "concave_image", {"highlight": "erect"}, "Virtual images from concave mirrors (object inside F) are erect.", "Your upright face in a close concave mirror.", "Erect = same way up as object.", "Real images from concave mirrors are usually inverted.", "", []),
        _card(f"u1_d{d}_c10", "Changing image properties", "As the object moves from infinity toward P, image size, position, and nature change step by step.", "concave_image", {"mode": "sequence"}, "Build the full table from observations, not memorisation alone.", "Slide a candle along the axis and note each change.", "Track: position → size → nature (real/virtual) → orientation.", "Do not jump to formulas before understanding the motion picture.", "", []),
    ]


def _day7() -> list:
    d = 7
    return [
        _card(f"u1_d{d}_c01", "Convex-mirror focus", "For a convex mirror, the focus F lies behind the mirror — a virtual focus.", "mirror_focus_ray", {"mirror_type": "convex", "highlight": "F"}, "Parallel rays diverge as if from F behind the mirror.", "Rear-view mirror geometry uses virtual F.", "Convex F is always behind the reflecting surface.", "Do not place F in front of a convex mirror.", "", []),
        _card(f"u1_d{d}_c02", "Image behind a convex mirror", "Convex mirrors always form images behind the mirror for real objects in front.", "concave_image", {"mirror_type": "convex", "highlight": "behind"}, "Consistent virtual image location simplifies safety mirrors.", "Shop security mirror image appears inside the mirror.", "Convex → image behind mirror.", "", "", []),
        _card(f"u1_d{d}_c03", "Virtual convex-mirror image", "The convex-mirror image is always virtual — rays only appear to diverge from behind.", "mirror_focus_ray", {"mirror_type": "convex", "highlight": "virtual_focus"}, "No screen image is possible for ordinary objects.", "You cannot project a convex-mirror image on paper.", "Convex mirror → always virtual (for real objects).", "", "", []),
        _card(f"u1_d{d}_c04", "Erect convex-mirror image", "Convex mirrors always give erect images for objects in front of them.", "concave_image", {"mirror_type": "convex", "highlight": "erect"}, "Important for driving — up is still up.", "Rear-view car mirror keeps orientation readable.", "Convex image is erect.", "Erect here still means virtual.", "", []),
        _card(f"u1_d{d}_c05", "Diminished convex-mirror image", "Convex mirrors always produce diminished images — objects look smaller.", "concave_image", {"mirror_type": "convex", "highlight": "diminished"}, "Smaller image allows a wider scene in the same mirror area.", "Parking lot convex mirror shows many cars smaller.", "Convex → diminished.", "Diminished helps wide field of view.", "", []),
        _card(f"u1_d{d}_c06", "Wide field of view", "A convex mirror curves outward so light from a large area reflects into your eye.", "concave_image", {"mirror_type": "convex", "mode": "wide_view"}, "Used where seeing more area matters more than size.", "Road junction mirror shows traffic from two directions.", "More area, smaller objects — trade-off by design.", "", "", []),
        _card(f"u1_d{d}_c07", "Changing object position", "For convex mirrors, image stays virtual, erect, and diminished — only position shifts slightly.", "concave_image", {"mirror_type": "convex", "mode": "object_move"}, "Less dramatic changes than concave mirrors.", "Moving closer to a convex mirror — image still upright and small.", "Nature stays the same; position varies mildly.", "", "", []),
        _card(f"u1_d{d}_c08", "Concave vs convex", "Concave converges light; convex diverges. Image rules differ completely.", "spherical_mirror_labels", {"mode": "compare"}, "Pick mirror type before drawing any ray diagram.", "Spoon inside vs outside surfaces.", "Concave: varied images; convex: always virtual, erect, diminished.", "Do not apply concave ray rules to convex mirrors.", "", []),
        _card(f"u1_d{d}_c09", "Plane vs convex", "Plane mirrors give same-size virtual images; convex mirrors give diminished virtual images with wider view.", "plane_mirror_reflection", {"mode": "image_properties"}, "Choose mirror shape for the job: flat view vs wide view.", "Bathroom flat mirror vs curved shop mirror.", "Plane: same size; convex: smaller but wider.", "", "", []),
        _card(f"u1_d{d}_c10", "Rear-view mirror reasoning", "Vehicles use convex rear-view mirrors because a wider, erect, diminished view improves safety.", "concave_image", {"mirror_type": "convex", "mode": "wide_view"}, "You see more traffic even though cars look smaller.", "Cars appear farther — compensate mentally when judging distance.", "Convex rear mirror: wide + erect + diminished.", "Objects in mirror are closer than they appear — diminished effect.", "", []),
    ]


def _day8() -> list:
    d = 8
    return [
        _card(f"u1_d{d}_c01", "Ray parallel to axis", "A ray parallel to the principal axis reflects through F (concave) or appears from F (convex).", "mirror_ray_rules", {"rule": "parallel"}, "First standard ray for locating images.", "Draw incoming ray horizontal to axis.", "Parallel in → through F out (concave).", "Parallel means parallel to principal axis, not to mirror surface.", "", []),
        _card(f"u1_d{d}_c02", "Ray through F", "A ray through focus F reflects parallel to the principal axis.", "mirror_ray_rules", {"rule": "through_F"}, "Pairs with the parallel ray to locate images.", "Ray from F hits mirror, leaves parallel to axis.", "Through F → reflects parallel to axis.", "Reverse of the parallel-ray rule.", "", []),
        _card(f"u1_d{d}_c03", "Ray through C", "A ray through centre C reflects back along the same path (normal to surface at C).", "mirror_ray_rules", {"rule": "through_C"}, "Useful third ray when C is marked.", "Ray aimed at C returns on itself.", "Through C → reflects back on same line.", "C must lie on the path of the ray.", "", []),
        _card(f"u1_d{d}_c04", "Ray at pole", "A ray striking the pole P reflects symmetrically about the principal axis.", "mirror_ray_rules", {"rule": "pole"}, "Optional fourth ray when image is near P.", "Light hitting P reflects with equal angles to axis.", "At P, use reflection symmetry.", "Not every diagram needs the pole ray.", "", []),
        _card(f"u1_d{d}_c05", "Using two rays", "Any two standard rays whose intersection locates the image are enough for a complete diagram.", "mirror_ray_rules", {"rule": "two_rays"}, "More rays check your work; two are sufficient.", "Parallel + through-F rays often meet at the image.", "Two correct rays → image point.", "Do not draw random rays without rules.", "", []),
        _card(f"u1_d{d}_c06", "Reflected-ray intersection", "For a real image, draw reflected rays forward until they cross.", "mirror_ray_rules", {"highlight": "intersect"}, "Crossing point is the top of the image.", "Solid lines after mirror; meet at image.", "Real image = forward intersection.", "", "", []),
        _card(f"u1_d{d}_c07", "Backward extensions", "For virtual images, extend reflected rays backward (dotted) to find where they appear to meet.", "mirror_ray_rules", {"highlight": "backward"}, "Dotted lines mean virtual construction.", "Convex mirror: extend rays behind mirror.", "Virtual image = backward extension meet.", "Do not use dotted lines for real image formation.", "", []),
        _card(f"u1_d{d}_c08", "Locating an image", "Mark object tip, draw two standard rays, find intersection (or backward meet) — that is the image tip.", "mirror_ray_rules", {"highlight": "locate"}, "Repeat for base on axis to get full image arrow.", "Image arrow perpendicular to axis from intersection.", "Tip-to-tip mapping: object tip → image tip.", "", "", []),
        _card(f"u1_d{d}_c09", "Common ray-diagram errors", "Typical mistakes: measuring angles from mirror, swapping F and C, wrong ray after parallel incidence.", "mirror_ray_rules", {"highlight": "errors"}, "Checklist prevents most exam losses.", "If image looks wrong, redo rays from F and parallel rule.", "Verify: normal, F, C, arrow directions.", "Reflected ray is not the incident ray continued.", "", []),
        _card(f"u1_d{d}_c10", "Mirror applications", "Concave: torches, dentists' mirrors, solar devices. Convex: rear-view and security mirrors.", "mirror_ray_rules", {"mode": "applications"}, "Design follows image properties.", "Headlight reflector is concave to parallelize bulb rays.", "Match mirror type to needed image.", "Never aim concave mirrors at the Sun unsupervised.", "Teacher demo or simulation only for concentration.", []),
    ]


def _day9() -> list:
    d = 9
    return [
        _card(f"u1_d{d}_c01", "Pole as origin", "In the mirror formula sign convention, pole P is taken as the origin (0) for distances.", "sign_axis", {"highlight": "P"}, "All u, v, f are measured from P.", "Distances start counting at the mirror surface.", "P = 0 on the axis.", "", "", []),
        _card(f"u1_d{d}_c02", "Direction of incident light", "Incident light is treated as travelling from left to right in standard NCERT diagrams.", "sign_axis", {"highlight": "light_direction"}, "Sets which side is positive for horizontal measurements.", "Object usually placed to the left of mirror.", "Light goes left → right.", "", "", []),
        _card(f"u1_d{d}_c03", "Positive horizontal", "Distances measured along incident light (to the right of P in standard diagrams) are positive.", "sign_axis", {"highlight": "positive_x"}, "Object distance u is usually positive for real objects in front.", "Real object in front → u positive.", "With the light: positive.", "", "", []),
        _card(f"u1_d{d}_c04", "Negative horizontal", "Distances measured against incident light (behind the mirror) are negative.", "sign_axis", {"highlight": "negative_x"}, "Virtual image distances are negative.", "Image behind mirror → v negative.", "Against the light: negative.", "", "", []),
        _card(f"u1_d{d}_c05", "Positive height", "Heights measured upward from the principal axis are positive.", "sign_axis", {"highlight": "positive_h"}, "Erect object or image arrows above axis are positive.", "Object above axis → positive height.", "Up from axis = +.", "", "", []),
        _card(f"u1_d{d}_c06", "Negative height", "Heights below the principal axis are negative — common for inverted images.", "sign_axis", {"highlight": "negative_h"}, "Magnification sign relates to orientation.", "Inverted image arrow below axis → negative h′.", "Down from axis = −.", "", "", []),
        _card(f"u1_d{d}_c07", "Sign of object distance u", "For a real object in front of the mirror, u is taken positive in the NCERT convention.", "sign_axis", {"highlight": "u"}, "Always check object placement before substituting.", "Candle in front → u > 0.", "Real object in front → u positive.", "", "", []),
        _card(f"u1_d{d}_c08", "Sign of image distance v", "Real image in front: v positive. Virtual image behind mirror: v negative.", "sign_axis", {"highlight": "v"}, "Sign of v tells real vs virtual quickly.", "Screen image → v positive; mirror face image → v negative.", "Real v +, virtual v −.", "", "", []),
        _card(f"u1_d{d}_c09", "Sign of concave-mirror focal length", "For a concave mirror, focal length f is negative in the NCERT sign convention.", "sign_axis", {"mirror_type": "concave", "highlight": "f"}, "Same side as incident light for F but f carries a sign by convention.", "Concave f = −|f| in formula work.", "Concave: f negative.", "Do not drop the minus in 1/f.", "", []),
        _card(f"u1_d{d}_c10", "Sign of convex-mirror focal length", "For a convex mirror, f is positive — focus lies behind the mirror.", "sign_axis", {"mirror_type": "convex", "highlight": "f"}, "Opposite sign to concave for f.", "Convex rear-view mirror: f positive.", "Convex: f positive.", "Mixing concave and convex signs is a common error.", "", []),
    ]


def _day10() -> list:
    d = 10
    return [
        _card(f"u1_d{d}_c01", "Object distance u", "u is the distance of the object from pole P along the principal axis.", "formula_panel", {"symbol": "u", "topic": "mirror"}, "One of three key quantities in mirror numericals.", "Object 20 cm in front → u = +20 cm.", "Measure u from P to object.", "Use cm consistently until final step if needed.", "", []),
        _card(f"u1_d{d}_c02", "Image distance v", "v is the distance of the image from pole P along the principal axis.", "formula_panel", {"symbol": "v", "topic": "mirror"}, "Solve mirror formula for v after substituting u and f with signs.", "Find v when u and f are known.", "v sign tells real vs virtual.", "", "", []),
        _card(f"u1_d{d}_c03", "Focal length f", "f links the mirror's curvature to focusing strength; insert with correct sign.", "formula_panel", {"symbol": "f", "topic": "mirror"}, "Concave f negative; convex f positive.", "f = −15 cm for concave means |f| = 15 cm.", "Always include sign of f in 1/f.", "", "", []),
        _card(f"u1_d{d}_c04", "Mirror formula", "1/v + 1/u = 1/f relates object distance, image distance, and focal length.", "formula_panel", {"symbol": "mirror_formula", "topic": "mirror"}, "Use after sign convention is clear.", "NCERT mirror numericals use this relation.", "Reciprocal form — not v = f + u.", "This is not the lens formula.", "", []),
        _card(f"u1_d{d}_c05", "Reciprocal quantities", "The mirror formula uses reciprocals — compute 1/u, 1/v, 1/f separately with signs, then combine.", "formula_panel", {"symbol": "reciprocals", "topic": "mirror"}, "Avoid algebra mistakes by writing each term clearly.", "1/20 + 1/v = 1/(−10) style layout.", "Add reciprocals, not distances directly.", "", "", []),
        _card(f"u1_d{d}_c06", "Substitution with signs", "Substitute signed u, v, f before solving — signs are part of the physics.", "formula_panel", {"symbol": "substitute", "topic": "mirror"}, "Wrong sign → wrong nature of image.", "Concave: f negative; real object: u positive.", "Signs first, numbers second.", "", "", []),
        _card(f"u1_d{d}_c07", "Magnification m", "Magnification compares image size to object size and can indicate orientation.", "formula_panel", {"symbol": "m", "topic": "mirror"}, "Connects heights and distances.", "m = −2 means inverted and twice as tall.", "m negative → inverted; |m| > 1 → enlarged.", "", "", []),
        _card(f"u1_d{d}_c08", "m = h′/h", "Magnification equals image height divided by object height (with signs for orientation).", "formula_panel", {"symbol": "m_h", "topic": "mirror"}, "Use when heights are given directly.", "h = +2 cm, h′ = −4 cm → m = −2.", "Negative m → inverted image.", "", "", []),
        _card(f"u1_d{d}_c09", "m = −v/u", "Magnification also equals minus image distance over object distance.", "formula_panel", {"symbol": "m_vu", "topic": "mirror"}, "Useful when u and v are known from the mirror formula.", "v = −30 cm, u = +15 cm → m = −(−30)/15 = +2 check signs carefully.", "m = −v/u with signed v and u.", "Do not forget the minus in −v/u.", "", []),
        _card(f"u1_d{d}_c10", "Interpreting m", "After calculating m, state: inverted/erect, enlarged/diminished/same, using sign and |m|.", "formula_panel", {"symbol": "interpret_m", "topic": "mirror"}, "Numbers must become a physical sentence.", "m = −0.5 → inverted, diminished to half.", "|m| size; sign orientation.", "", "", []),
    ]


def _day11() -> list:
    d = 11
    return [
        _card(f"u1_d{d}_c01", "Transparent medium", "Light can pass through a transparent medium — air, water, glass — with changed speed.", "refraction", {"mode": "transparent"}, "Refraction happens at boundaries between such media.", "Glass window lets light through but bends it.", "Transparent ≠ no refraction.", "", "", []),
        _card(f"u1_d{d}_c02", "Boundary between media", "Refraction chiefly occurs when light crosses a boundary between two different media.", "refraction", {"mode": "boundary"}, "The surface is where speed changes.", "Air–glass surface in a window pane.", "Boundary = interface between media.", "", "", []),
        _card(f"u1_d{d}_c03", "Incident ray at boundary", "The incident ray approaches the boundary; angle measured from the normal.", "refraction", {"highlight": "incident"}, "Same normal rules as reflection.", "Ray from air into glass — incident in air.", "Incident ray in first medium.", "Do not confuse with refracted ray.", "", []),
        _card(f"u1_d{d}_c04", "Refracted ray", "The refracted ray enters the second medium, bent at the boundary.", "refraction", {"highlight": "refracted"}, "Direction of bend depends on speed change.", "Pencil in water looks bent at surface.", "Refracted ray is in second medium.", "Not the reflected ray.", "", []),
        _card(f"u1_d{d}_c05", "Normal at boundary", "Draw the normal perpendicular to the boundary at the point of refraction.", "refraction", {"highlight": "normal"}, "Angles of incidence and refraction are from this normal.", "Same dashed normal idea as mirrors.", "Measure refraction angles from normal.", "Normal is to the surface, not the mirror axis only.", "", []),
        _card(f"u1_d{d}_c06", "Speed change", "Light slows down or speeds up when entering a new medium — causing bending.", "refraction", {"highlight": "speed"}, "Root cause of refraction.", "Light slower in glass than air → bends toward normal entering glass.", "Speed change → bending.", "Higher optical density usually means lower speed.", "", []),
        _card(f"u1_d{d}_c07", "Bending toward normal", "When light enters a denser (slower) medium, it bends toward the normal.", "refraction", {"mode": "toward"}, "Air to glass: ray moves closer to normal inside glass.", "Straw in water appears broken at surface.", "Into denser medium → toward normal.", "Toward normal ≠ along normal.", "", []),
        _card(f"u1_d{d}_c08", "Bending away from normal", "When light enters a rarer (faster) medium, it bends away from the normal.", "refraction", {"mode": "away"}, "Glass to air: ray moves farther from normal in air.", "Ray leaving glass slab spreads from normal.", "Into rarer medium → away from normal.", "Reverse of entering denser medium.", "", []),
        _card(f"u1_d{d}_c09", "Optically rarer medium", "The medium where light travels faster is optically rarer (e.g. air compared to glass).", "refraction", {"mode": "rarer"}, "Optical density is about light speed, not mass density alone.", "Air is rarer than glass for light.", "Rarer = faster light.", "Rare medium is not necessarily thin air only.", "", []),
        _card(f"u1_d{d}_c10", "Optically denser medium", "The medium where light travels slower is optically denser (e.g. glass compared to air).", "refraction", {"mode": "denser"}, "Explains direction of bending at a boundary.", "Glass is denser than air optically.", "Denser = slower light.", "Do not equate to physical heaviness alone.", "", []),
    ]


def _day12() -> list:
    d = 12
    return [
        _card(f"u1_d{d}_c01", "Air to glass", "At an air–glass boundary, light slows and bends toward the normal on entering glass.", "refraction", {"mode": "air_glass"}, "First step through a glass slab.", "Ray from air strikes glass at an angle to normal.", "Air → glass: toward normal.", "", "", []),
        _card(f"u1_d{d}_c02", "Glass to air", "Leaving glass into air, light speeds up and bends away from the normal.", "refraction", {"mode": "glass_air"}, "Second bend inside a slab.", "Emerging ray in air bends away from normal.", "Glass → air: away from normal.", "", "", []),
        _card(f"u1_d{d}_c03", "Rectangular glass slab", "A rectangular glass slab has two parallel faces — two refractions occur.", "glass_slab", {"mode": "slab"}, "Classic NCERT diagram.", "Glass plate in optics kit.", "Two surfaces: enter and leave.", "", "", []),
        _card(f"u1_d{d}_c04", "Emergent ray", "The ray leaving the slab into the original medium is the emergent ray.", "glass_slab", {"highlight": "emergent"}, "Compare direction to incident ray.", "Light exits bottom of slab back into air.", "Emergent ray is after second refraction.", "", "", []),
        _card(f"u1_d{d}_c05", "Parallel incident and emergent", "For a parallel-sided slab, emergent ray is parallel to incident ray (laterally shifted).", "glass_slab", {"highlight": "parallel"}, "Direction unchanged; position shifted.", "Look through window — scene not rotated.", "Parallel in and out for rectangular slab.", "Parallel does not mean same path line.", "", []),
        _card(f"u1_d{d}_c06", "Lateral displacement", "The emergent ray is shifted sideways relative to the incident path.", "glass_slab", {"highlight": "shift"}, "Offset depends on thickness and angle.", "Thick glass shifts the view more.", "Shift sideways, same direction.", "", "", []),
        _card(f"u1_d{d}_c07", "Angle of incidence", "In refraction, angle of incidence i is between incident ray and normal at the boundary.", "refraction", {"highlight": "angle_i"}, "Same definition style as reflection.", "Measure from normal in air before glass.", "i from normal, not from surface.", "", "", []),
        _card(f"u1_d{d}_c08", "Angle of refraction", "Angle of refraction r is between refracted ray and normal inside the second medium.", "refraction", {"highlight": "angle_r"}, "Pair with i for Snell's law at Class 10 level.", "Smaller r than i entering denser medium.", "r in second medium, from normal.", "", "", []),
        _card(f"u1_d{d}_c09", "First law of refraction", "Incident ray, refracted ray, and normal lie in the same plane.", "refraction", {"mode": "coplanar"}, "Same plane rule as reflection.", "Draw all three in one 2D diagram.", "All three coplanar.", "", "", []),
        _card(f"u1_d{d}_c10", "Snell's law (Class 10)", "n₁ sin i = n₂ sin r relates refractive indices and angles at a boundary.", "formula_panel", {"symbol": "snell", "topic": "refraction"}, "Use with angles from normal.", "Higher n side: smaller angle when entering denser medium.", "sin i / sin r = n₂/n₁.", "Use degrees in calculator carefully.", "", []),
    ]


def _day13() -> list:
    d = 13
    return [
        _card(f"u1_d{d}_c01", "Speed in vacuum c", "c is the speed of light in vacuum, approximately 3 × 10⁸ m/s.", "formula_panel", {"symbol": "c", "topic": "refraction"}, "Fastest possible speed for light.", "Used as reference in n = c/v.", "c ≈ 3 × 10⁸ m/s.", "", "", []),
        _card(f"u1_d{d}_c02", "Speed in medium v", "v is the speed of light in a material medium — always less than c.", "formula_panel", {"symbol": "v", "topic": "refraction"}, "Appears in refractive index definition.", "Light slower in water than vacuum.", "v < c in any medium.", "", "", []),
        _card(f"u1_d{d}_c03", "Absolute refractive index", "Absolute refractive index compares light speed in vacuum to speed in the medium.", "formula_panel", {"symbol": "n", "topic": "refraction"}, "Material property for optics.", "Glass has n around 1.5.", "n = c/v (absolute).", "", "", []),
        _card(f"u1_d{d}_c04", "n = c/v", "Refractive index n equals speed of light in vacuum divided by speed in the medium.", "formula_panel", {"symbol": "n_cv", "topic": "refraction"}, "Main formula for Class 10 numericals.", "If v = c/1.5, then n = 1.5.", "Bigger n → smaller v.", "n has no unit.", "", []),
        _card(f"u1_d{d}_c05", "Meaning of c", "c is constant in vacuum — the upper limit for light speed used in the formula.", "formula_panel", {"symbol": "c_meaning", "topic": "refraction"}, "Numerator in n = c/v.", "Same c for all materials in numerator.", "c is vacuum speed.", "", "", []),
        _card(f"u1_d{d}_c06", "Meaning of v", "v depends on the medium — water, glass, diamond each have different v.", "formula_panel", {"symbol": "v_meaning", "topic": "refraction"}, "Denominator sets n for each material.", "Light slowest in diamond among common examples.", "Different media → different v.", "", "", []),
        _card(f"u1_d{d}_c07", "Refractive index unitless", "n is a ratio of speeds — it has no unit.", "formula_panel", {"symbol": "n_unit", "topic": "refraction"}, "Do not write cm or m/s as unit of n.", "n = 1.33 for water — just a number.", "Refractive index: no unit.", "", "", []),
        _card(f"u1_d{d}_c08", "Higher n → lower speed", "Larger refractive index means light travels slower in that medium.", "refraction", {"mode": "n_speed"}, "Links table values to bending behaviour.", "Diamond n high → light very slow.", "High n = optically dense = slower.", "Higher n does not mean light travels faster.", "", []),
        _card(f"u1_d{d}_c09", "Comparing media", "Compare n values to see which medium is optically denser and how much light slows.", "refraction", {"mode": "compare_n"}, "Used in refraction direction questions.", "n_glass > n_air → glass denser.", "Compare n, then predict bending.", "", "", []),
        _card(f"u1_d{d}_c10", "Physical vs optical density", "A physically dense material is not always optically denser — optical density is about light speed.", "refraction", {"mode": "optical_vs_physical"}, "Avoid everyday word confusion.", "Kerosene may float on water yet have higher n.", "Optical density ≠ mass density.", "", "", []),
    ]


def _day14() -> list:
    d = 14
    return [
        _card(f"u1_d{d}_c01", "Spherical lens", "A lens is made of two refracting spherical surfaces — converging or diverging.", "lens_labels", {"mode": "intro"}, "Base object for lens ray diagrams.", "Magnifying glass is a convex lens.", "Two curved surfaces.", "", "", []),
        _card(f"u1_d{d}_c02", "Convex lens", "A convex (converging) lens is thicker at the middle than at the edges.", "lens_labels", {"lens_type": "convex"}, "Parallel rays converge toward a real focus.", "Magnifying glass converges sunlight — teacher demo only.", "Convex = thicker middle.", "Never focus Sun on paper unsupervised.", "", []),
        _card(f"u1_d{d}_c03", "Concave lens", "A concave (diverging) lens is thinner at the middle than at the edges.", "lens_labels", {"lens_type": "concave"}, "Parallel rays diverge as if from virtual focus.", "Spectacle lens for some vision corrections.", "Concave = thinner middle.", "", "", []),
        _card(f"u1_d{d}_c04", "Optical centre O", "O is the central point of the lens through which rays pass without deviation.", "lens_labels", {"highlight": "O"}, "Key point for one standard lens ray.", "Ray through O continues straight.", "Through O → no bend.", "", "", []),
        _card(f"u1_d{d}_c05", "Principal axis", "Straight line through O perpendicular to the lens — symmetry line for diagrams.", "lens_labels", {"highlight": "axis"}, "Reference for foci and object placement.", "Horizontal line through lens centre.", "Same role as mirror principal axis.", "", "", []),
        _card(f"u1_d{d}_c06", "Two principal foci", "A lens has two foci: F₁ on the incident side and F₂ on the other side.", "lens_labels", {"highlight": "F1_F2"}, "Symmetric for thin lenses in air.", "Mark F and 2F on both sides for convex lens.", "Two foci for thin lens in air.", "", "", []),
        _card(f"u1_d{d}_c07", "Focal length", "Focal length f is distance from optical centre O to principal focus F.", "lens_labels", {"highlight": "f"}, "Use metres for power calculations.", "f = 20 cm convex lens.", "Measure f from O to F.", "", "", []),
        _card(f"u1_d{d}_c08", "Converging lens", "Convex lens converges parallel rays — real focus on far side.", "lens_ray", {"lens_type": "convex", "rule": "parallel"}, "Used for real image formation.", "Sunlight through convex lens — supervised demo only.", "Convex = converging.", "", "", []),
        _card(f"u1_d{d}_c09", "Diverging lens", "Concave lens spreads parallel rays — virtual focus on incident side.", "lens_ray", {"lens_type": "concave", "rule": "parallel"}, "Always virtual diminished images for real objects.", "Concave lens in peepholes.", "Concave = diverging.", "", "", []),
        _card(f"u1_d{d}_c10", "Thin-lens representation", "Draw a convex or concave lens as a thin vertical line with outward/inward arrow symbols.", "lens_labels", {"mode": "thin_symbol"}, "Standard NCERT shorthand.", "Double-arrow line for convex; inward for concave.", "Thin lens: single vertical line symbol.", "", "", []),
    ]


def _day15() -> list:
    d = 15
    return [
        _card(f"u1_d{d}_c01", "Ray parallel to lens axis", "Ray parallel to axis refracts through F₂ (convex) or appears from F₁ (concave).", "lens_ray", {"lens_type": "convex", "rule": "parallel"}, "First standard lens ray.", "Horizontal incoming ray bends through focus.", "Parallel → through F on far side (convex).", "", "", []),
        _card(f"u1_d{d}_c02", "Ray through principal focus", "Ray through F₁ (before lens) emerges parallel to axis after convex lens.", "lens_ray", {"lens_type": "convex", "rule": "through_F"}, "Pairs with parallel ray rule.", "Through F in → parallel out.", "Reverse of parallel-ray rule.", "", "", []),
        _card(f"u1_d{d}_c03", "Ray through optical centre", "Ray through O continues undeviated.", "lens_ray", {"lens_type": "convex", "rule": "through_O"}, "Simplest third ray.", "Straight line through middle of lens.", "O ray: no bend.", "", "", []),
        _card(f"u1_d{d}_c04", "Convex-lens real images", "Object beyond F → real, inverted image on opposite side (can screen).", "lens_image", {"lens_type": "convex", "position": "beyond_F"}, "Camera and projector principle simplified.", "Object outside F forms screen image.", "Real when object beyond F.", "", "", []),
        _card(f"u1_d{d}_c05", "Convex-lens virtual image", "Object inside F → virtual, erect, enlarged image on same side as object.", "lens_image", {"lens_type": "convex", "position": "inside_F"}, "Magnifying glass use.", "Hold lens close to book — upright big view.", "Inside F → virtual erect enlarged.", "", "", []),
        _card(f"u1_d{d}_c06", "Object at 2F", "Object at 2F gives real, inverted, same-size image at 2F on other side.", "lens_image", {"lens_type": "convex", "position": "at_2F"}, "Special symmetric case.", "Mark 2F on both sides of convex lens.", "2F object → 2F image, same size.", "", "", []),
        _card(f"u1_d{d}_c07", "Object between F and 2F", "Real, inverted, enlarged image beyond 2F.", "lens_image", {"lens_type": "convex", "position": "F_to_2F"}, "Projector-like situation.", "Slide projector object near F region.", "Between F and 2F → enlarged real image.", "", "", []),
        _card(f"u1_d{d}_c08", "Object inside F", "Virtual, erect, enlarged — magnifying glass mode.", "lens_image", {"lens_type": "convex", "position": "inside_F"}, "Same as virtual image card — applied.", "Reading fine print with magnifier.", "Inside F: magnifier.", "", "", []),
        _card(f"u1_d{d}_c09", "Concave-lens image properties", "Concave lens always gives virtual, erect, diminished image for a real object.", "lens_image", {"lens_type": "concave"}, "Only one nature — simpler than convex.", "Peephole always small upright view.", "Concave: always virtual, erect, diminished.", "", "", []),
        _card(f"u1_d{d}_c10", "Lens ray diagram", "Use any two of: parallel→F, through F→parallel, through O straight to locate image.", "lens_ray", {"lens_type": "convex", "rule": "two_rays"}, "Same strategy as mirrors.", "Draw carefully to scale on axis.", "Two good rays enough.", "", "", []),
    ]


def _day16() -> list:
    d = 16
    return [
        _card(f"u1_d{d}_c01", "Lens sign convention", "Light travels left to right; distances against light are negative; f positive for convex, negative for concave (NCERT).", "sign_axis", {"topic": "lens", "highlight": "convention"}, "Mirror and lens signs differ — learn separately.", "Convex converging lens: f positive.", "Lens signs ≠ mirror signs.", "", "", []),
        _card(f"u1_d{d}_c02", "Convex-lens focal-length sign", "Convex lens: f is positive in lens formula work.", "sign_axis", {"topic": "lens", "mirror_type": "convex", "highlight": "f"}, "Matches converging behaviour.", "f = +20 cm for convex.", "Convex f positive.", "", "", []),
        _card(f"u1_d{d}_c03", "Concave-lens focal-length sign", "Concave lens: f is negative.", "sign_axis", {"topic": "lens", "mirror_type": "concave", "highlight": "f"}, "Opposite to convex.", "f = −15 cm for concave.", "Concave f negative.", "", "", []),
        _card(f"u1_d{d}_c04", "Lens formula", "1/v − 1/u = 1/f for thin lenses — note minus on 1/u term (different from mirror formula).", "formula_panel", {"symbol": "lens_formula", "topic": "lens"}, "Most common mix-up with mirror formula.", "Check NCERT lens numericals.", "Lens: 1/v − 1/u = 1/f.", "Mirror uses plus between 1/v and 1/u.", "", []),
        _card(f"u1_d{d}_c05", "Mirror vs lens formula", "Mirror: 1/v + 1/u = 1/f. Lens: 1/v − 1/u = 1/f. Learn both with correct signs.", "formula_panel", {"symbol": "compare_formulas", "topic": "lens"}, "Write which formula before substituting.", "Label problem as mirror or lens first.", "Plus vs minus on 1/u term.", "", "", []),
        _card(f"u1_d{d}_c06", "Lens magnification", "m = h′/h = v/u for lenses (NCERT lens convention).", "formula_panel", {"symbol": "m_lens", "topic": "lens"}, "Sign of m gives orientation.", "Compare to mirror m = −v/u.", "Lens: m = v/u.", "Do not use −v/u for lens unless your text specifies mirror.", "", []),
        _card(f"u1_d{d}_c07", "Interpreting lens m", "State erect/inverted and size from sign and |m| after lens calculations.", "formula_panel", {"symbol": "interpret_m_lens", "topic": "lens"}, "Finish with words, not only numbers.", "m = +2 erect enlarged (virtual case).", "Interpret |m| and sign separately.", "", "", []),
        _card(f"u1_d{d}_c08", "Power of a lens", "Power P measures converging/diverging strength: P = 1/f when f is in metres.", "formula_panel", {"symbol": "P", "topic": "lens"}, "Used for spectacles and combinations.", "f = 0.5 m → P = +2 D convex.", "P = 1/f (f in metres).", "f must be in metres.", "", []),
        _card(f"u1_d{d}_c09", "Dioptre", "One dioptre (1 D) is the power of a lens with focal length 1 m.", "formula_panel", {"symbol": "dioptre", "topic": "lens"}, "Unit of lens power.", "P = +1 D means f = 1 m convex.", "Unit: dioptre (D).", "", "", []),
        _card(f"u1_d{d}_c10", "Focal length in metres", "Convert cm to m before using P = 1/f — divide cm by 100.", "formula_panel", {"symbol": "metres", "topic": "lens"}, "Most common lens power mistake.", "f = 25 cm = 0.25 m → P = 4 D.", "Metres in power formula.", "cm without conversion gives wrong P by 10⁴.", "", []),
    ]


DAY_BUILDERS = {
    5: ("Concave Mirror Images: Object at a Distance", _day5),
    6: ("Concave Mirror Images: Object Near the Focus", _day6),
    7: ("Convex Mirrors and Mirror Comparisons", _day7),
    8: ("Mirror Ray Diagrams and Applications", _day8),
    9: ("Mirror Sign Convention", _day9),
    10: ("Mirror Formula and Magnification", _day10),
    11: ("Introduction to Refraction", _day11),
    12: ("Glass Slab and Laws of Refraction", _day12),
    13: ("Refractive Index", _day13),
    14: ("Spherical Lenses", _day14),
    15: ("Lens Rays and Image Formation", _day15),
    16: ("Lens Formula, Magnification and Power", _day16),
}
