"""
State-level map data for Sangeetha's GK app.

Provides:
  - Base64-encoded state map images for HTML embedding.
  - Coordinate database mapping location names to (x%, y%) positions within each state.
  - HTML renderer that overlays a pulsing marker on a state map at a given location.
"""

import base64
import os

_STATE_MAPS_DIR = os.path.join(os.path.dirname(__file__), "state_maps")
_STATE_B64_CACHE: dict[str, str] = {}


def _get_state_b64(state_key: str) -> str | None:
    """Load a state map as a base64 data URI (cached)."""
    if state_key in _STATE_B64_CACHE:
        return _STATE_B64_CACHE[state_key]
    path = os.path.join(_STATE_MAPS_DIR, f"{state_key}.png")
    if not os.path.exists(path):
        return None
    with open(path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    uri = f"data:image/png;base64,{encoded}"
    _STATE_B64_CACHE[state_key] = uri
    return uri


# Map display names of states / UTs to their file-name keys
STATE_KEY_MAP: dict[str, str] = {
    # ── 28 States ──
    "Andhra Pradesh":       "andhra_pradesh",
    "Arunachal Pradesh":    "arunachal_pradesh",
    "Assam":                "assam",
    "Bihar":                "bihar",
    "Chhattisgarh":         "chhattisgarh",
    "Goa":                  "goa",
    "Gujarat":              "gujarat",
    "Haryana":              "haryana",
    "Himachal Pradesh":     "himachal_pradesh",
    "Jharkhand":            "jharkhand",
    "Karnataka":            "karnataka",
    "Kerala":               "kerala",
    "Madhya Pradesh":       "madhya_pradesh",
    "Maharashtra":          "maharashtra",
    "Manipur":              "manipur",
    "Meghalaya":            "meghalaya",
    "Mizoram":              "mizoram",
    "Nagaland":             "nagaland",
    "Odisha":               "odisha",
    "Punjab":               "punjab",
    "Rajasthan":            "rajasthan",
    "Sikkim":               "sikkim",
    "Tamil Nadu":           "tamil_nadu",
    "Telangana":            "telangana",
    "Tripura":              "tripura",
    "Uttar Pradesh":        "uttar_pradesh",
    "Uttarakhand":          "uttarakhand",
    "West Bengal":          "west_bengal",

    # ── 8 Union Territories ──
    "Andaman and Nicobar Islands": "andaman_nicobar",
    "Andaman and Nicobar":  "andaman_nicobar",
    "Chandigarh":           "chandigarh",
    "Dadra and Nagar Haveli and Daman and Diu": "dadra_daman_diu",
    "Daman and Diu":        "dadra_daman_diu",
    "Dadra and Nagar Haveli": "dadra_daman_diu",
    "Delhi":                "delhi",
    "NCT of Delhi":         "delhi",
    "New Delhi":            "delhi",
    "Jammu and Kashmir":    "jammu_and_kashmir",
    "Ladakh":               "ladakh",
    "Lakshadweep":          "lakshadweep",
    "Puducherry":           "puducherry",
    "Pondicherry":          "puducherry",
}


# ── Intra-state location coordinates as (x%, y%) on the state map image ──
# These are approximate positions calibrated to AI-generated state map images.
# x% = horizontal (0=left, 100=right), y% = vertical (0=top, 100=bottom)

STATE_LOCATIONS: dict[str, dict[str, tuple[float, float]]] = {

    # ── KARNATAKA ──
    "karnataka": {
        "Bengaluru":        (58, 62),
        "Bangalore":        (58, 62),
        "Mysuru":           (48, 72),
        "Mysore":           (48, 72),
        "Mangaluru":        (22, 68),
        "Mangalore":        (22, 68),
        "Hubli":            (32, 40),
        "Dharwad":          (32, 38),
        "Belgaum":          (22, 28),
        "Belagavi":         (22, 28),
        "Hampi":            (48, 38),
        "Badami":           (35, 35),
        "Gulbarga":         (60, 22),
        "Kalaburagi":       (60, 22),
        "Raichur":          (55, 35),
        "Shimoga":          (38, 52),
        "Shivamogga":       (38, 52),
        "Hassan":           (40, 62),
        "Chitradurga":      (48, 48),
        "Udupi":            (22, 58),
        "Bidar":            (68, 12),
        "Kaveri":           (50, 68),
        "Cauvery":          (50, 68),
        "Tungabhadra":      (45, 38),
        "Krishna":          (42, 30),
        "Sharavathi":       (28, 55),
        "Nethravathi":      (25, 72),
        "Kabini":           (48, 75),
        "Hemavathi":        (42, 60),
        "Arkavathi":        (55, 65),
        "Coorg":            (38, 76),
        "Kodagu":           (38, 76),
        "Mysore Palace":    (48, 72),
        "Gol Gumbaz":       (28, 32),
    },

    # ── TAMIL NADU ──
    "tamil_nadu": {
        "Chennai":          (72, 18),
        "Madurai":          (48, 72),
        "Coimbatore":       (28, 55),
        "Trichy":           (48, 58),
        "Tiruchirappalli":  (48, 58),
        "Salem":            (38, 42),
        "Tirunelveli":      (42, 88),
        "Thanjavur":        (55, 62),
        "Tanjore":          (55, 62),
        "Kanchipuram":      (68, 22),
        "Mahabalipuram":    (75, 25),
        "Rameswaram":       (58, 82),
        "Ooty":             (22, 48),
        "Kodaikanal":       (38, 68),
        "Pondicherry":      (72, 38),
        "Puducherry":       (72, 38),
        "Vellore":          (55, 25),
        "Erode":            (32, 48),
        "Kaveri":           (42, 55),
        "Cauvery":          (42, 55),
        "Vaigai":           (50, 72),
        "Tamiraparani":     (42, 88),
        "Bhavani":          (32, 50),
        "Amaravathi":       (38, 55),
        "Moyar":            (25, 50),
        "Brihadeeswarar Temple": (55, 62),
        "Meenakshi Temple": (48, 72),
        "Meenakshi Amman Temple": (48, 72),
        "Konark Sun Temple": (55, 62),
        "Nilgiri":          (22, 48),
    },

    # ── KERALA ──
    "kerala": {
        "Thiruvananthapuram": (52, 88),
        "Kochi":            (45, 55),
        "Cochin":           (45, 55),
        "Kozhikode":        (38, 28),
        "Calicut":          (38, 28),
        "Thrissur":         (42, 42),
        "Alappuzha":        (42, 65),
        "Alleppey":         (42, 65),
        "Kollam":           (48, 78),
        "Kannur":           (42, 18),
        "Palakkad":         (48, 35),
        "Munnar":           (55, 48),
        "Wayanad":          (45, 15),
        "Kottayam":         (50, 62),
        "Idukki":           (55, 52),
        "Periyar":          (55, 50),
        "Pamba":            (52, 68),
        "Bharathappuzha":   (44, 38),
        "Chaliyar":         (40, 25),
        "Nila":             (44, 38),
    },

    # ── ANDHRA PRADESH ──
    "andhra_pradesh": {
        "Amaravati":        (42, 52),
        "Visakhapatnam":    (68, 22),
        "Vizag":            (68, 22),
        "Vijayawada":       (45, 50),
        "Tirupati":         (52, 78),
        "Guntur":           (42, 55),
        "Nellore":          (55, 68),
        "Kurnool":          (30, 48),
        "Rajahmundry":      (58, 35),
        "Kakinada":         (65, 32),
        "Anantapur":        (25, 58),
        "Srisailam":        (35, 48),
        "Krishna":          (45, 48),
        "Godavari":         (60, 30),
        "Pennar":           (48, 72),
        "Chitravathi":      (28, 62),
        "Tungabhadra":      (22, 42),
    },

    # ── TELANGANA ──
    "telangana": {
        "Hyderabad":        (40, 55),
        "Warangal":         (62, 35),
        "Nizamabad":        (38, 22),
        "Karimnagar":       (55, 25),
        "Khammam":          (68, 52),
        "Nalgonda":         (52, 60),
        "Medak":            (35, 38),
        "Adilabad":         (42, 8),
        "Mahbubnagar":      (32, 68),
        "Charminar":        (40, 55),
        "Golconda Fort":    (38, 52),
        "Godavari":         (60, 28),
        "Krishna":          (50, 65),
    },

    # ── MAHARASHTRA ──
    "maharashtra": {
        "Mumbai":           (18, 58),
        "Pune":             (25, 60),
        "Nagpur":           (72, 32),
        "Nashik":           (25, 42),
        "Aurangabad":       (38, 42),
        "Solapur":          (40, 62),
        "Kolhapur":         (28, 72),
        "Thane":            (18, 55),
        "Amravati":         (62, 32),
        "Latur":            (52, 58),
        "Sangli":           (32, 68),
        "Ajanta":           (38, 38),
        "Ellora":           (38, 40),
        "Gateway of India": (18, 58),
        "Shirdi":           (30, 45),
        "Lonavala":         (22, 58),
        "Mahabaleshwar":    (25, 65),
        "Ratnagiri":        (18, 68),
        "Godavari":         (50, 38),
        "Krishna":          (35, 68),
        "Tapi":             (32, 28),
    },

    # ── RAJASTHAN ──
    "rajasthan": {
        "Jaipur":           (62, 48),
        "Jodhpur":          (32, 48),
        "Udaipur":          (38, 68),
        "Jaisalmer":        (15, 42),
        "Bikaner":          (35, 28),
        "Ajmer":            (50, 50),
        "Pushkar":          (48, 48),
        "Kota":             (62, 62),
        "Bharatpur":        (72, 45),
        "Mount Abu":        (25, 65),
        "Chittorgarh":      (48, 62),
        "Amber Fort":       (62, 46),
        "Hawa Mahal":       (62, 48),
        "Mehrangarh Fort":  (32, 48),
        "Ranthambore":      (65, 52),
        "Chambal":          (68, 58),
        "Aravalli":         (42, 55),
    },

    # ── GUJARAT ──
    "gujarat": {
        "Ahmedabad":        (52, 42),
        "Surat":            (48, 68),
        "Vadodara":         (52, 55),
        "Rajkot":           (28, 45),
        "Bhavnagar":        (38, 58),
        "Jamnagar":         (18, 40),
        "Junagadh":         (22, 55),
        "Gandhinagar":      (52, 40),
        "Kutch":            (20, 22),
        "Rann of Kutch":    (25, 18),
        "Gir":              (25, 60),
        "Dwarka":           (8, 42),
        "Somnath":          (22, 62),
        "Dandi":            (42, 68),
        "Sabarmati Ashram": (52, 42),
        "Sabarmati":        (52, 38),
        "Narmada":          (52, 62),
    },

    # ── UTTAR PRADESH ──
    "uttar_pradesh": {
        "Lucknow":          (55, 48),
        "Agra":             (30, 55),
        "Varanasi":         (80, 50),
        "Kanpur":           (48, 52),
        "Prayagraj":        (68, 52),
        "Allahabad":        (68, 52),
        "Noida":            (25, 32),
        "Meerut":           (22, 28),
        "Mathura":          (28, 48),
        "Ayodhya":          (65, 40),
        "Aligarh":          (30, 42),
        "Jhansi":           (28, 68),
        "Taj Mahal":        (30, 55),
        "Fatehpur Sikri":   (32, 55),
        "Red Fort":         (22, 30),
        "Sarnath":          (80, 50),
        "Ganga":            (60, 45),
        "Yamuna":           (28, 42),
    },

    # ── MADHYA PRADESH ──
    "madhya_pradesh": {
        "Bhopal":           (42, 48),
        "Indore":           (28, 55),
        "Jabalpur":         (62, 38),
        "Gwalior":          (40, 18),
        "Ujjain":           (30, 50),
        "Rewa":             (72, 32),
        "Sagar":            (52, 38),
        "Sanchi":           (45, 42),
        "Khajuraho":        (62, 28),
        "Pachmarhi":        (52, 48),
        "Orchha":           (48, 25),
        "Mandu":            (25, 55),
        "Narmada":          (40, 52),
        "Chambal":          (35, 22),
        "Sanchi Stupa":     (45, 42),
        "Buland Darwaza":   (45, 18),
    },

    # ── WEST BENGAL ──
    "west_bengal": {
        "Kolkata":          (55, 68),
        "Darjeeling":       (42, 8),
        "Siliguri":         (38, 12),
        "Howrah":           (55, 68),
        "Asansol":          (38, 52),
        "Durgapur":         (40, 55),
        "Murshidabad":      (52, 48),
        "Santiniketan":     (45, 52),
        "Sundarbans":       (62, 78),
        "Digha":            (55, 78),
        "Victoria Memorial": (55, 68),
        "Hooghly":          (52, 62),
        "Ganga":            (50, 55),
    },

    # ── ODISHA ──
    "odisha": {
        "Bhubaneswar":      (58, 48),
        "Puri":             (62, 52),
        "Cuttack":          (58, 45),
        "Rourkela":         (32, 18),
        "Sambalpur":        (32, 30),
        "Berhampur":        (58, 65),
        "Konark":           (65, 50),
        "Chilika":          (60, 58),
        "Simlipal":         (52, 22),
        "Mahanadi":         (48, 38),
        "Konark Sun Temple": (65, 50),
    },

    # ── BIHAR ──
    "bihar": {
        "Patna":            (42, 38),
        "Gaya":             (48, 55),
        "Nalanda":          (48, 48),
        "Bodh Gaya":        (48, 58),
        "Rajgir":           (52, 50),
        "Vaishali":         (38, 28),
        "Muzaffarpur":      (38, 22),
        "Bhagalpur":        (72, 38),
        "Darbhanga":        (45, 15),
        "Ganga":            (45, 35),
    },

    # ── PUNJAB ──
    "punjab": {
        "Chandigarh":       (72, 28),
        "Amritsar":         (28, 22),
        "Ludhiana":         (48, 42),
        "Jalandhar":        (38, 35),
        "Patiala":          (58, 55),
        "Bathinda":         (35, 62),
        "Pathankot":        (32, 12),
        "Golden Temple":    (28, 22),
        "Jallianwala Bagh": (28, 22),
        "Sutlej":           (50, 48),
    },

    # ── GOA ──
    "goa": {
        "Panaji":           (35, 32),
        "Margao":           (45, 62),
        "Vasco da Gama":    (28, 52),
        "Mapusa":           (38, 22),
        "Old Goa":          (45, 35),
        "Calangute":        (32, 25),
        "Anjuna":           (30, 20),
        "Mandovi":          (38, 30),
    },

    # ── JHARKHAND ──
    "jharkhand": {
        "Ranchi":           (48, 48),
        "Jamshedpur":       (62, 62),
        "Dhanbad":          (58, 28),
        "Bokaro":           (55, 32),
        "Deoghar":          (52, 18),
        "Hazaribagh":       (45, 35),
    },

    # ── CHHATTISGARH ──
    "chhattisgarh": {
        "Raipur":           (48, 45),
        "Bilaspur":         (45, 32),
        "Durg":             (40, 48),
        "Korba":            (52, 28),
        "Jagdalpur":        (58, 72),
        "Rajnandgaon":      (35, 48),
        "Mahanadi":         (48, 35),
    },

    # ── UTTARAKHAND ──
    "uttarakhand": {
        "Dehradun":         (32, 42),
        "Haridwar":         (35, 55),
        "Rishikesh":        (32, 50),
        "Nainital":         (55, 52),
        "Mussoorie":        (28, 40),
        "Almora":           (58, 45),
        "Badrinath":        (42, 18),
        "Kedarnath":        (35, 25),
        "Valley of Flowers": (38, 15),
        "Jim Corbett":      (52, 58),
        "Ganga":            (35, 48),
    },

    # ── HIMACHAL PRADESH ──
    "himachal_pradesh": {
        "Shimla":           (58, 58),
        "Manali":           (35, 28),
        "Dharamshala":      (22, 38),
        "Kullu":            (38, 32),
        "Dalhousie":        (18, 28),
        "Kasauli":          (62, 62),
        "Spiti":            (52, 15),
        "Kinnaur":          (60, 35),
        "Mandi":            (38, 45),
    },

    # ── JAMMU AND KASHMIR ──
    "jammu_and_kashmir": {
        "Srinagar":         (38, 35),
        "Jammu":            (32, 72),
        "Gulmarg":          (32, 32),
        "Pahalgam":         (45, 38),
        "Leh":              (65, 20),
        "Ladakh":           (68, 18),
        "Kargil":           (52, 25),
        "Sonamarg":         (42, 32),
        "Dal Lake":         (38, 35),
        "Vaishno Devi":     (30, 65),
        "Indus":            (62, 22),
    },

    # ── ASSAM ──
    "assam": {
        "Guwahati":         (28, 48),
        "Dispur":           (28, 48),
        "Jorhat":           (62, 42),
        "Dibrugarh":        (75, 38),
        "Silchar":          (55, 72),
        "Tezpur":           (38, 38),
        "Nagaon":           (42, 48),
        "Kaziranga":        (48, 42),
        "Majuli":           (55, 35),
        "Brahmaputra":      (45, 42),
    },

    # ── HARYANA ──
    "haryana": {
        "Chandigarh":       (52, 12),
        "Gurugram":         (42, 72),
        "Gurgaon":          (42, 72),
        "Faridabad":        (48, 75),
        "Ambala":           (48, 15),
        "Panipat":          (45, 42),
        "Karnal":           (48, 28),
        "Hisar":            (22, 42),
        "Rohtak":           (35, 55),
        "Kurukshetra":      (48, 22),
        "Yamuna":           (50, 60),
    },

    # ══════════════════════════════════════════════
    # REMAINING 7 STATES (Northeast India)
    # ══════════════════════════════════════════════

    # ── ARUNACHAL PRADESH ──
    "arunachal_pradesh": {
        "Itanagar":         (28, 58),
        "Tawang":           (12, 28),
        "Ziro":             (32, 48),
        "Pasighat":         (58, 62),
        "Along":            (42, 58),
        "Bomdila":          (18, 38),
        "Namdapha":         (78, 48),
        "Sela Pass":        (15, 32),
        "Brahmaputra":      (45, 70),
    },

    # ── MANIPUR ──
    "manipur": {
        "Imphal":           (48, 45),
        "Churachandpur":    (42, 68),
        "Thoubal":          (55, 48),
        "Bishnupur":        (42, 52),
        "Ukhrul":           (58, 28),
        "Loktak Lake":      (42, 55),
        "Kangla Fort":      (48, 45),
    },

    # ── MEGHALAYA ──
    "meghalaya": {
        "Shillong":         (58, 48),
        "Tura":             (18, 38),
        "Cherrapunji":      (55, 58),
        "Sohra":            (55, 58),
        "Mawsynram":        (52, 55),
        "Jowai":            (68, 48),
        "Dawki":            (72, 55),
        "Nongpoh":          (52, 38),
        "Living Root Bridges": (55, 58),
    },

    # ── MIZORAM ──
    "mizoram": {
        "Aizawl":           (42, 32),
        "Lunglei":          (38, 62),
        "Champhai":         (62, 38),
        "Serchhip":         (48, 48),
        "Kolasib":          (38, 18),
        "Saiha":            (45, 82),
        "Blue Mountain":    (40, 55),
    },

    # ── NAGALAND ──
    "nagaland": {
        "Kohima":           (42, 55),
        "Dimapur":          (28, 38),
        "Mokokchung":       (52, 35),
        "Tuensang":         (68, 32),
        "Mon":              (62, 15),
        "Wokha":            (42, 38),
        "Zunheboto":        (55, 42),
        "Hornbill Festival": (42, 55),
    },

    # ── SIKKIM ──
    "sikkim": {
        "Gangtok":          (55, 55),
        "Namchi":           (48, 72),
        "Pelling":          (28, 48),
        "Ravangla":         (38, 65),
        "Lachung":          (48, 22),
        "Yuksom":           (25, 55),
        "Kanchenjunga":     (32, 18),
        "Tsomgo Lake":      (65, 52),
        "Nathula Pass":     (68, 48),
    },

    # ── TRIPURA ──
    "tripura": {
        "Agartala":         (35, 42),
        "Udaipur":          (38, 58),
        "Dharmanagar":      (42, 12),
        "Kailashahar":      (45, 22),
        "Ambassa":          (42, 32),
        "Neermahal":        (38, 52),
        "Unakoti":          (45, 18),
    },

    # ══════════════════════════════════════════════
    # 8 UNION TERRITORIES
    # ══════════════════════════════════════════════

    # ── ANDAMAN AND NICOBAR ISLANDS ──
    "andaman_nicobar": {
        "Port Blair":       (48, 38),
        "Havelock Island":  (52, 32),
        "Neil Island":      (50, 35),
        "Cellular Jail":    (48, 38),
        "Ross Island":      (50, 40),
        "Baratang":         (45, 28),
        "Diglipur":         (48, 12),
        "Car Nicobar":      (45, 62),
        "Great Nicobar":    (48, 88),
        "Indira Point":     (48, 95),
    },

    # ── CHANDIGARH ──
    "chandigarh": {
        "Chandigarh":       (50, 50),
        "Rock Garden":      (42, 35),
        "Sukhna Lake":      (62, 28),
        "Capitol Complex":  (45, 25),
        "Rose Garden":      (48, 55),
        "Sector 17":        (50, 50),
    },

    # ── DADRA AND NAGAR HAVELI AND DAMAN AND DIU ──
    "dadra_daman_diu": {
        "Daman":            (32, 35),
        "Diu":              (18, 68),
        "Silvassa":         (55, 22),
        "Dadra":            (58, 18),
        "Nagar Haveli":     (55, 22),
    },

    # ── DELHI (NCT) ──
    "delhi": {
        "New Delhi":        (45, 55),
        "Delhi":            (48, 42),
        "Old Delhi":        (48, 32),
        "Red Fort":         (50, 30),
        "India Gate":       (48, 52),
        "Qutub Minar":      (38, 72),
        "Lotus Temple":     (55, 62),
        "Humayun's Tomb":   (52, 48),
        "Chandni Chowk":    (48, 30),
        "Connaught Place":  (45, 45),
        "Rashtrapati Bhavan": (40, 48),
        "Parliament House": (42, 48),
        "Jantar Mantar":    (45, 45),
        "Yamuna":           (58, 38),
    },

    # ── JAMMU AND KASHMIR (already in original set) ──
    # "jammu_and_kashmir" defined above

    # ── LADAKH ──
    "ladakh": {
        "Leh":              (42, 48),
        "Kargil":           (22, 45),
        "Pangong Lake":     (68, 48),
        "Nubra Valley":     (45, 25),
        "Zanskar":          (25, 58),
        "Khardung La":      (42, 32),
        "Tso Moriri":       (55, 68),
        "Magnetic Hill":    (38, 48),
        "Shanti Stupa":     (42, 48),
        "Indus":            (40, 50),
    },

    # ── LAKSHADWEEP ──
    "lakshadweep": {
        "Kavaratti":        (48, 48),
        "Agatti":           (42, 35),
        "Minicoy":          (48, 82),
        "Bangaram":         (45, 32),
        "Andrott":          (48, 42),
        "Kalpeni":          (48, 58),
        "Kadmat":           (48, 28),
    },

    # ── PUDUCHERRY ──
    "puducherry": {
        "Puducherry":       (50, 50),
        "Pondicherry":      (50, 50),
        "Karaikal":         (48, 72),
        "Mahe":             (28, 18),
        "Yanam":            (72, 15),
        "Auroville":        (55, 38),
        "Promenade Beach":  (55, 52),
        "French Quarter":   (50, 48),
    },
}


def get_state_key(state_name: str) -> str | None:
    """Convert a state display name to its file-system key."""
    if not state_name:
        return None

    # Exact match
    if state_name in STATE_KEY_MAP:
        return STATE_KEY_MAP[state_name]

    # Case-insensitive match
    lower = state_name.lower().strip()
    for display, key in STATE_KEY_MAP.items():
        if display.lower() == lower:
            return key

    # Partial match
    for display, key in STATE_KEY_MAP.items():
        if lower in display.lower() or display.lower() in lower:
            return key

    return None


def get_state_location_coords(
    state_key: str, location_name: str
) -> tuple[float, float] | None:
    """Look up coordinates for a location within a state map."""
    if not state_key or not location_name:
        return None

    locs = STATE_LOCATIONS.get(state_key, {})
    if not locs:
        return None

    # Exact match
    if location_name in locs:
        return locs[location_name]

    # Case-insensitive
    lower = location_name.lower().strip()
    for key, coords in locs.items():
        if key.lower() == lower:
            return coords

    # Partial match
    for key, coords in locs.items():
        if lower in key.lower() or key.lower() in lower:
            return coords

    # Fallback: center of the map
    return (50, 50)


def render_state_map_with_marker(
    state_name: str, location_name: str, label: str = ""
) -> str | None:
    """Return HTML for a state map with a pulsing marker at the given location.

    Returns None if the state map image doesn't exist.
    """
    state_key = get_state_key(state_name)
    if not state_key:
        return None

    state_b64 = _get_state_b64(state_key)
    if not state_b64:
        return None

    coords = get_state_location_coords(state_key, location_name)
    if not coords:
        coords = (50, 50)

    x, y = coords
    display_label = label or location_name
    display_state = state_name

    return f"""
    <div style="position:relative;display:inline-block;width:100%;max-width:380px;
                margin:0.5rem auto;border-radius:20px;overflow:hidden;
                box-shadow:0 4px 20px rgba(0,0,0,0.12);">
        <img src="{state_b64}" style="width:100%;display:block;border-radius:20px;" />
        <!-- State name header -->
        <div style="position:absolute;top:6px;left:50%;transform:translateX(-50%);z-index:12;
                    background:rgba(240,147,251,0.9);color:white;padding:4px 14px;border-radius:12px;
                    font-size:0.75rem;font-weight:700;white-space:nowrap;
                    box-shadow:0 2px 8px rgba(0,0,0,0.15);">
            🗺️ {display_state}
        </div>
        <!-- Pulsing marker -->
        <div style="position:absolute;left:{x}%;top:{y}%;transform:translate(-50%,-50%);z-index:10;">
            <div style="
                width:18px;height:18px;
                background:#ef4444;
                border:3px solid white;
                border-radius:50%;
                box-shadow:0 0 0 3px #ef4444, 0 2px 8px rgba(0,0,0,0.3);
                animation: state-pulse 1.5s ease-in-out infinite;
            "></div>
        </div>
        <!-- Location label -->
        <div style="position:absolute;left:{x}%;top:{min(y + 5, 92)}%;transform:translateX(-50%);z-index:10;
                    background:rgba(0,0,0,0.8);color:white;padding:3px 10px;border-radius:8px;
                    font-size:0.65rem;font-weight:600;white-space:nowrap;
                    box-shadow:0 2px 6px rgba(0,0,0,0.2);">
            📍 {display_label}
        </div>
    </div>
    <style>
        @keyframes state-pulse {{
            0%   {{ box-shadow: 0 0 0 3px #ef4444, 0 0 0 6px rgba(239,68,68,0.4); }}
            50%  {{ box-shadow: 0 0 0 5px #ef4444, 0 0 0 14px rgba(239,68,68,0.15); }}
            100% {{ box-shadow: 0 0 0 3px #ef4444, 0 0 0 6px rgba(239,68,68,0.4); }}
        }}
    </style>
    """
