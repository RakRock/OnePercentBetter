"""
Logo Identifier — brand logo recognition quiz for Arjun.

Uses locally downloaded brand logos from Simple Icons for crisp display.
Curated set of iconic brands an 11-year-old would recognise (70+ logos).
"""

import random

CATEGORIES = {
    "tech": {
        "name": "Tech & Apps",
        "emoji": "💻",
        "color": "#3b82f6",
        "description": "Technology companies and popular apps",
    },
    "food": {
        "name": "Food & Drinks",
        "emoji": "🍔",
        "color": "#ef4444",
        "description": "Restaurants, snacks & beverage brands",
    },
    "sports": {
        "name": "Sports & Outdoors",
        "emoji": "⚽",
        "color": "#10b981",
        "description": "Athletic brands and sports organisations",
    },
    "cars": {
        "name": "Cars & Transport",
        "emoji": "🚗",
        "color": "#f59e0b",
        "description": "Automobile and transportation brands",
    },
    "entertainment": {
        "name": "Entertainment & Media",
        "emoji": "🎮",
        "color": "#8b5cf6",
        "description": "Games, streaming & media companies",
    },
    "fashion": {
        "name": "Fashion & Lifestyle",
        "emoji": "👟",
        "color": "#ec4899",
        "description": "Clothing, shoes & lifestyle brands",
    },
}

LOGO_SIZE = 256


def get_logo_url(domain: str) -> str:
    return f"https://www.google.com/s2/favicons?domain={domain}&sz={LOGO_SIZE}"


QUESTION_BANK = [
    # ========== TECH & APPS ==========
    {
        "id": 1, "category": "tech",
        "company": "Apple", "domain": "apple.com",
        "hint": "A fruit with a bite taken out of it",
        "options": ["Apple", "Huawei", "BlackBerry", "LG"],
        "fun_fact": "The Apple logo was designed by Rob Janoff in 1977. The bite was added so it wouldn't be confused with a cherry!",
        "image": "apple",
    },
    {
        "id": 2, "category": "tech",
        "company": "Instagram", "domain": "instagram.com",
        "hint": "A gradient camera icon on a purple-orange background",
        "options": ["Instagram", "VSCO", "Snapchat", "Flickr"],
        "fun_fact": "Instagram's camera icon was redesigned in 2016 from a retro Polaroid-style camera to a modern gradient!",
        "image": "instagram",
    },
    {
        "id": 3, "category": "tech",
        "company": "Spotify", "domain": "spotify.com",
        "hint": "Three curved lines on a green circle",
        "options": ["Spotify", "SoundCloud", "Shazam", "Deezer"],
        "fun_fact": "Spotify's green logo has three sound waves — representing music streaming to your ears!",
        "image": "spotify",
    },
    {
        "id": 4, "category": "tech",
        "company": "Snapchat", "domain": "snapchat.com",
        "hint": "A white ghost outline on a yellow background",
        "options": ["Snapchat", "Discord", "Waze", "Bumble"],
        "fun_fact": "Snapchat's ghost logo was hand-drawn by co-founder Evan Spiegel — it represents disappearing messages!",
        "image": "snapchat",
    },
    {
        "id": 5, "category": "tech",
        "company": "YouTube", "domain": "youtube.com",
        "hint": "A white play-button triangle inside a red rounded rectangle",
        "options": ["YouTube", "Vimeo", "Dailymotion", "Rumble"],
        "fun_fact": "The first YouTube video, 'Me at the zoo', was uploaded on April 23, 2005 by co-founder Jawed Karim!",
        "image": "youtube",
    },
    {
        "id": 6, "category": "tech",
        "company": "TikTok", "domain": "tiktok.com",
        "hint": "A 3D-looking musical note in neon pink/blue on a dark background",
        "options": ["TikTok", "Musical.ly", "Triller", "Dubsmash"],
        "fun_fact": "TikTok's logo looks like a 3D musical note with neon colors inspired by concert stage lighting!",
        "image": "tiktok",
    },
    {
        "id": 7, "category": "tech",
        "company": "Discord", "domain": "discord.com",
        "hint": "A smiling game controller face on purple/indigo",
        "options": ["Discord", "TeamSpeak", "Slack", "Guilded"],
        "fun_fact": "Discord's mascot is called Clyde — the smiling game controller face was designed to feel friendly!",
        "image": "discord",
    },
    {
        "id": 8, "category": "tech",
        "company": "Google", "domain": "google.com",
        "hint": "A multicoloured G in blue, red, yellow, and green",
        "options": ["Google", "Bing", "Yahoo", "DuckDuckGo"],
        "fun_fact": "Google's name comes from 'googol' — the number 1 followed by 100 zeros!",
        "image": "google",
    },
    {
        "id": 9, "category": "tech",
        "company": "Amazon", "domain": "amazon.com",
        "hint": "An arrow from A to Z under the name forming a smile",
        "options": ["Amazon", "eBay", "Alibaba", "Flipkart"],
        "fun_fact": "Amazon's arrow goes from A to Z — meaning they sell everything from A to Z!",
        "image": "amazon",
    },
    {
        "id": 10, "category": "tech",
        "company": "Microsoft", "domain": "microsoft.com",
        "hint": "Four coloured squares arranged in a 2×2 grid (red, green, blue, yellow)",
        "options": ["Microsoft", "Google", "Slack", "Samsung"],
        "fun_fact": "Microsoft's four-coloured window logo represents the diversity of their products and users!",
        "image": "microsoft",
    },
    {
        "id": 11, "category": "tech",
        "company": "WhatsApp", "domain": "whatsapp.com",
        "hint": "A white phone inside a speech bubble on a green background",
        "options": ["WhatsApp", "Signal", "Telegram", "Viber"],
        "fun_fact": "WhatsApp was created by two ex-Yahoo employees and bought by Facebook for $19 billion in 2014!",
        "image": "whatsapp",
    },
    {
        "id": 12, "category": "tech",
        "company": "Duolingo", "domain": "duolingo.com",
        "hint": "A bright green owl with large round eyes",
        "options": ["Duolingo", "Babbel", "Rosetta Stone", "Memrise"],
        "fun_fact": "Duolingo's owl mascot is named Duo — and he's famous for guilt-tripping users who miss lessons!",
        "image": "duolingo",
    },

    # ========== FOOD & DRINKS ==========
    {
        "id": 13, "category": "food",
        "company": "McDonald's", "domain": "mcdonalds.com",
        "hint": "Golden arches forming an 'M' shape on a red background",
        "options": ["McDonald's", "Burger King", "Wendy's", "In-N-Out"],
        "fun_fact": "The Golden Arches were originally part of the restaurant's actual building architecture before becoming the logo!",
        "image": "mcdonalds",
    },
    {
        "id": 14, "category": "food",
        "company": "Starbucks", "domain": "starbucks.com",
        "hint": "A green circle with a two-tailed mermaid (siren) in the centre",
        "options": ["Starbucks", "Dunkin'", "Peet's Coffee", "Costa Coffee"],
        "fun_fact": "The Starbucks logo features a two-tailed mermaid (siren) inspired by a 16th-century Norse woodcut!",
        "image": "starbucks",
    },
    {
        "id": 15, "category": "food",
        "company": "Pepsi", "domain": "pepsi.com",
        "hint": "A circle divided into red, white, and blue wavy sections",
        "options": ["Pepsi", "Coca-Cola", "RC Cola", "Dr Pepper"],
        "fun_fact": "Pepsi has redesigned its globe logo over 10 times since 1898!",
        "image": "pepsi",
    },
    {
        "id": 16, "category": "food",
        "company": "KFC", "domain": "kfc.com",
        "hint": "A man's face with glasses, a goatee, and a bow tie",
        "options": ["KFC", "Popeyes", "Church's Chicken", "Boston Market"],
        "fun_fact": "Colonel Sanders' face in the KFC logo is based on the real founder who started his chicken recipe at age 65!",
        "image": "kfc",
    },
    {
        "id": 17, "category": "food",
        "company": "Wendy's", "domain": "wendys.com",
        "hint": "A girl with red pigtails on a blue background",
        "options": ["Wendy's", "Dairy Queen", "Arby's", "Jack in the Box"],
        "fun_fact": "The Wendy's logo is based on the founder Dave Thomas's daughter, Melinda Lou 'Wendy' Thomas!",
        "image": "wendys",
    },
    {
        "id": 18, "category": "food",
        "company": "Taco Bell", "domain": "tacobell.com",
        "hint": "A bell shape in purple and pink tones",
        "options": ["Taco Bell", "Chipotle", "Del Taco", "Qdoba"],
        "fun_fact": "Taco Bell was named after its founder, Glen Bell, and the bell logo is a play on his last name!",
        "image": "tacobell",
    },
    {
        "id": 19, "category": "food",
        "company": "Chick-fil-A", "domain": "chick-fil-a.com",
        "hint": "A red icon with a chicken silhouette hidden in a letter",
        "options": ["Chick-fil-A", "Raising Cane's", "Zaxby's", "Wingstop"],
        "fun_fact": "The 'C' in Chick-fil-A's logo is cleverly shaped like a chicken — look closely at the curve!",
        "image": "chickfila",
    },
    {
        "id": 20, "category": "food",
        "company": "Red Bull", "domain": "redbull.com",
        "hint": "Two red bulls charging at each other with a golden sun behind them",
        "options": ["Red Bull", "Monster", "Rockstar", "Celsius"],
        "fun_fact": "Red Bull's logo shows two bulls charging at each other — inspired by the Thai energy drink Krating Daeng!",
        "image": "redbull",
    },
    {
        "id": 21, "category": "food",
        "company": "Pringles", "domain": "pringles.com",
        "hint": "A man with a large moustache and a bow-shaped hairstyle",
        "options": ["Pringles", "Lay's", "Doritos", "Cheetos"],
        "fun_fact": "The Pringles mascot is called Julius Pringles — his iconic moustache has been there since 1968!",
        "image": "pringles",
    },

    # ========== SPORTS & OUTDOORS ==========
    {
        "id": 22, "category": "sports",
        "company": "Nike", "domain": "nike.com",
        "hint": "A simple curved checkmark shape (swoosh)",
        "options": ["Nike", "Adidas", "New Balance", "Reebok"],
        "fun_fact": "The Nike Swoosh was designed by graphic design student Carolyn Davidson for just $35 in 1971!",
        "image": "nike",
    },
    {
        "id": 23, "category": "sports",
        "company": "Adidas", "domain": "adidas.com",
        "hint": "Three parallel diagonal stripes forming a mountain/triangle shape",
        "options": ["Adidas", "Puma", "Fila", "Kappa"],
        "fun_fact": "Adidas' three stripes were originally just to hold the shoe together — they accidentally became the logo!",
        "image": "adidas",
    },
    {
        "id": 24, "category": "sports",
        "company": "Puma", "domain": "puma.com",
        "hint": "A leaping big cat (cougar/puma) silhouette",
        "options": ["Puma", "Jaguar", "Adidas", "Lacoste"],
        "fun_fact": "Puma was founded by Rudolf Dassler — the brother of Adidas founder Adi Dassler! The brothers had a falling out.",
        "image": "puma",
    },
    {
        "id": 25, "category": "sports",
        "company": "Jordan", "domain": "jordan.com",
        "hint": "A silhouette of a basketball player jumping with legs spread",
        "options": ["Jordan", "Nike", "Adidas", "Puma"],
        "fun_fact": "The Jumpman logo is based on a photo of Michael Jordan doing a ballet move, not a basketball dunk!",
        "image": "jordan",
    },
    {
        "id": 26, "category": "sports",
        "company": "Under Armour", "domain": "underarmour.com",
        "hint": "Two overlapping letters that form an interlocking shape",
        "options": ["Under Armour", "Champion", "Reebok", "ASICS"],
        "fun_fact": "Under Armour's logo is two overlapping U's that also cleverly form an A!",
        "image": "under_armour",
    },
    {
        "id": 27, "category": "sports",
        "company": "The North Face", "domain": "thenorthface.com",
        "hint": "Three curved lines forming a quarter-dome shape",
        "options": ["The North Face", "Patagonia", "Columbia", "Arc'teryx"],
        "fun_fact": "The North Face logo represents Half Dome, the famous rock formation in Yosemite National Park!",
        "image": "north_face",
    },
    {
        "id": 28, "category": "sports",
        "company": "Premier League", "domain": "premierleague.com",
        "hint": "A lion head looking to the side with a crown",
        "options": ["Premier League", "La Liga", "Bundesliga", "Serie A"],
        "fun_fact": "The Premier League lion has been the logo since 1992 when the league was formed!",
        "image": "premierleague",
    },
    {
        "id": 29, "category": "sports",
        "company": "Formula 1", "domain": "formula1.com",
        "hint": "A red number 1 shape with speed lines",
        "options": ["Formula 1", "NASCAR", "IndyCar", "MotoGP"],
        "fun_fact": "Formula 1 cars can go from 0 to 100 mph and back to 0 in under 5 seconds!",
        "image": "formula1",
    },

    # ========== CARS & TRANSPORT ==========
    {
        "id": 30, "category": "cars",
        "company": "Tesla", "domain": "tesla.com",
        "hint": "A stylised letter that also looks like a cross-section of an electric motor",
        "options": ["Tesla", "Rivian", "Lucid", "Polestar"],
        "fun_fact": "Tesla's 'T' logo is actually a cross-section of an electric motor — design meets engineering!",
        "image": "tesla",
    },
    {
        "id": 31, "category": "cars",
        "company": "BMW", "domain": "bmw.com",
        "hint": "A circle divided into four quadrants — two blue and two white",
        "options": ["BMW", "Volkswagen", "Audi", "Volvo"],
        "fun_fact": "BMW's blue and white quarters represent the colors of the Bavarian flag in Germany!",
        "image": "bmw",
    },
    {
        "id": 32, "category": "cars",
        "company": "Mercedes-Benz", "domain": "mercedes-benz.com",
        "hint": "A three-pointed star inside a circle",
        "options": ["Mercedes-Benz", "Lexus", "Infiniti", "Acura"],
        "fun_fact": "The three-pointed star represents Mercedes' ambition to motorise land, sea, and air transport!",
        "image": "mercedes",
    },
    {
        "id": 33, "category": "cars",
        "company": "Ferrari", "domain": "ferrari.com",
        "hint": "A prancing horse on a yellow shield background",
        "options": ["Ferrari", "Porsche", "Lamborghini", "Maserati"],
        "fun_fact": "Ferrari's prancing horse was originally a symbol painted on a World War I Italian fighter plane!",
        "image": "ferrari",
    },
    {
        "id": 34, "category": "cars",
        "company": "Lamborghini", "domain": "lamborghini.com",
        "hint": "A charging bull on a dark shield",
        "options": ["Lamborghini", "Ferrari", "Bugatti", "McLaren"],
        "fun_fact": "Lamborghini's bull logo reflects founder Ferruccio Lamborghini's zodiac sign — Taurus the bull!",
        "image": "lamborghini",
    },
    {
        "id": 35, "category": "cars",
        "company": "Porsche", "domain": "porsche.com",
        "hint": "An ornate crest with a horse, antlers, and red/black stripes",
        "options": ["Porsche", "Ferrari", "Aston Martin", "Bentley"],
        "fun_fact": "Porsche's crest features the horse from Stuttgart's coat of arms and the antlers from Württemberg!",
        "image": "porsche",
    },
    {
        "id": 36, "category": "cars",
        "company": "Audi", "domain": "audi.com",
        "hint": "Four interlocking rings in a horizontal row",
        "options": ["Audi", "Olympic Committee", "Volkswagen", "Volvo"],
        "fun_fact": "Audi's four rings represent the four companies that merged to create it in 1932!",
        "image": "audi",
    },
    {
        "id": 37, "category": "cars",
        "company": "Toyota", "domain": "toyota.com",
        "hint": "Three overlapping ovals forming a symmetrical pattern",
        "options": ["Toyota", "Mazda", "Subaru", "Nissan"],
        "fun_fact": "Toyota's overlapping ovals logo secretly contains every letter of 'TOYOTA' hidden within it!",
        "image": "toyota",
    },
    {
        "id": 38, "category": "cars",
        "company": "Volkswagen", "domain": "volkswagen.com",
        "hint": "Two letters stacked vertically inside a circle",
        "options": ["Volkswagen", "Volvo", "Vauxhall", "Vinfast"],
        "fun_fact": "Volkswagen means 'people's car' in German — it was originally designed to be affordable for everyone!",
        "image": "volkswagen",
    },

    # ========== ENTERTAINMENT & MEDIA ==========
    {
        "id": 39, "category": "entertainment",
        "company": "PlayStation", "domain": "playstation.com",
        "hint": "A 'P' standing up with an 'S' lying flat, creating a 3D-looking icon",
        "options": ["PlayStation", "Xbox", "Steam", "Atari"],
        "fun_fact": "The PS logo cleverly hides the letters P and S — the P stands upright while the S lies flat behind it!",
        "image": "playstation",
    },
    {
        "id": 40, "category": "entertainment",
        "company": "Xbox", "domain": "xbox.com",
        "hint": "A green sphere with a white X across it",
        "options": ["Xbox", "GeForce", "Razer", "Steam"],
        "fun_fact": "Xbox got its name from DirectX, Microsoft's graphics technology — 'DirectX Box' became 'Xbox'!",
        "image": "xbox",
    },
    {
        "id": 41, "category": "entertainment",
        "company": "Nintendo", "domain": "nintendo.com",
        "hint": "A bold red rounded rectangle with a white letter inside",
        "options": ["Nintendo", "Netflix", "Namco", "Naughty Dog"],
        "fun_fact": "Nintendo was founded in 1889 as a playing card company — they made cards for 75 years before making games!",
        "image": "nintendo",
    },
    {
        "id": 42, "category": "entertainment",
        "company": "Netflix", "domain": "netflix.com",
        "hint": "A bold red letter on a dark/black background",
        "options": ["Netflix", "Hulu", "HBO Max", "Paramount+"],
        "fun_fact": "Netflix started as a DVD-by-mail service in 1997 — they mailed their first DVD in 1998!",
        "image": "netflix",
    },
    {
        "id": 43, "category": "entertainment",
        "company": "Disney", "domain": "disney.com",
        "hint": "A castle silhouette or a cursive script signature",
        "options": ["Disney", "Universal", "Paramount", "Warner Bros."],
        "fun_fact": "Walt Disney's personal signature inspired the famous Disney logo script!",
        "image": "disney",
    },
    {
        "id": 44, "category": "entertainment",
        "company": "Roblox", "domain": "roblox.com",
        "hint": "A tilted grey/dark square with a circular hole in it",
        "options": ["Roblox", "Minecraft", "Fortnite", "Among Us"],
        "fun_fact": "Roblox has over 70 million daily active users and the name is a mix of 'robots' and 'blocks'!",
        "image": "roblox",
    },
    {
        "id": 45, "category": "entertainment",
        "company": "LEGO", "domain": "lego.com",
        "hint": "Bold white letters on a bright red rounded square",
        "options": ["LEGO", "Mega Bloks", "K'NEX", "Playmobil"],
        "fun_fact": "LEGO comes from the Danish words 'leg godt' meaning 'play well' — and it sells about 75 billion bricks a year!",
        "image": "lego",
    },
    {
        "id": 46, "category": "entertainment",
        "company": "Marvel", "domain": "marvel.com",
        "hint": "Bold red letters on white",
        "options": ["Marvel", "DC Comics", "Dark Horse", "Image"],
        "fun_fact": "Marvel Comics nearly went bankrupt in the 1990s before the MCU saved them!",
        "image": "marvel",
    },
    {
        "id": 47, "category": "entertainment",
        "company": "Epic Games", "domain": "epicgames.com",
        "hint": "A dark icon with a stylised face/side profile",
        "options": ["Epic Games", "Valve", "Riot Games", "Rockstar Games"],
        "fun_fact": "Epic Games was founded by Tim Sweeney when he was in college — now they make Fortnite and Unreal Engine!",
        "image": "epic_games",
    },

    # ========== FASHION & LIFESTYLE ==========
    {
        "id": 48, "category": "fashion",
        "company": "Target", "domain": "target.com",
        "hint": "A red and white bullseye (concentric circles)",
        "options": ["Target", "CVS", "Walgreens", "Kmart"],
        "fun_fact": "Target's bullseye logo is one of the most recognised in the US — their dog mascot is named Bullseye too!",
        "image": "target",
    },
    {
        "id": 49, "category": "fashion",
        "company": "Converse", "domain": "converse.com",
        "hint": "A star inside a circle — the classic All Star emblem",
        "options": ["Converse", "Vans", "DC Shoes", "Skechers"],
        "fun_fact": "Chuck Taylor All Stars were originally basketball shoes designed in 1917 — now they're a fashion icon!",
        "image": "converse",
    },
    {
        "id": 50, "category": "fashion",
        "company": "Crocs", "domain": "crocs.com",
        "hint": "A cartoon crocodile/alligator wearing sunglasses, smiling",
        "options": ["Crocs", "Birkenstock", "Keen", "Teva"],
        "fun_fact": "Crocs were originally designed as boat shoes but became a worldwide fashion phenomenon!",
        "image": "crocs",
    },

    # ========== EXPANDED BANK ==========
    {
        "id": 51, "category": "tech",
        "company": "LinkedIn", "domain": "linkedin.com",
        "hint": "A simple 'in' inside a rounded square, usually blue",
        "options": ["LinkedIn", "Indeed", "Glassdoor", "Monster"],
        "fun_fact": "LinkedIn launched in 2003 and is now the largest professional networking site in the world!",
        "image": "linkedin",
    },
    {
        "id": 52, "category": "tech",
        "company": "PayPal", "domain": "paypal.com",
        "hint": "Two overlapping stylised 'P' letters — often blue and navy",
        "options": ["PayPal", "Stripe", "Venmo", "Square"],
        "fun_fact": "PayPal was started by a team that included Elon Musk before he moved on to Tesla and SpaceX!",
        "image": "paypal",
    },
    {
        "id": 53, "category": "tech",
        "company": "Samsung", "domain": "samsung.com",
        "hint": "An oval with a tilted letter inside — often blue on white",
        "options": ["Samsung", "Sony", "LG", "Panasonic"],
        "fun_fact": "Samsung began in 1938 selling groceries and noodles in Korea before becoming a tech giant!",
        "image": "samsung",
    },
    {
        "id": 54, "category": "tech",
        "company": "Uber", "domain": "uber.com",
        "hint": "A simple wordmark — often black or white — for rides and delivery",
        "options": ["Uber", "Lyft", "Bolt", "Grab"],
        "fun_fact": "Uber started in San Francisco in 2009 as 'UberCab' before dropping 'Cab' from the name!",
        "image": "uber",
    },
    {
        "id": 55, "category": "tech",
        "company": "Airbnb", "domain": "airbnb.com",
        "hint": "A looping symbol that looks like a heart, location pin, and letter A combined",
        "options": ["Airbnb", "Booking.com", "Expedia", "Vrbo"],
        "fun_fact": "Airbnb's logo is called the Bélo — meant to stand for belonging, people, places, and love!",
        "image": "airbnb",
    },
    {
        "id": 56, "category": "food",
        "company": "Coca-Cola", "domain": "coca-cola.com",
        "hint": "Famous flowing red script on white — the classic soda wordmark",
        "options": ["Coca-Cola", "Pepsi", "Dr Pepper", "Sprite"],
        "fun_fact": "Coca-Cola was invented in 1886 by pharmacist John Pemberton as a fountain drink in Atlanta!",
        "image": "cocacola",
    },
    {
        "id": 57, "category": "food",
        "company": "Burger King", "domain": "burgerking.com",
        "hint": "The name between two orange bun halves on a blue circle",
        "options": ["Burger King", "McDonald's", "Wendy's", "Five Guys"],
        "fun_fact": "Burger King's Whopper was introduced in 1957 and has been its signature sandwich for decades!",
        "image": "burgerking",
    },
    {
        "id": 58, "category": "food",
        "company": "Monster Energy", "domain": "monsterenergy.com",
        "hint": "Neon green claw marks on a black can — energy drink",
        "options": ["Monster Energy", "Rockstar", "Bang", "Celsius"],
        "fun_fact": "Monster Energy launched in 2002 — the claw logo is meant to look like a monster tearing through the can!",
        "image": "monster",
    },
    {
        "id": 59, "category": "food",
        "company": "Heineken", "domain": "heineken.com",
        "hint": "A red star with green — classic European beer branding",
        "options": ["Heineken", "Corona", "Stella Artois", "Guinness"],
        "fun_fact": "Heineken was founded in Amsterdam in 1864 and the red star has been part of its look for over a century!",
        "image": "heineken",
    },
    {
        "id": 60, "category": "sports",
        "company": "Reebok", "domain": "reebok.com",
        "hint": "A vector-style cross or delta made of sharp lines — fitness brand",
        "options": ["Reebok", "Nike", "Adidas", "ASICS"],
        "fun_fact": "The name Reebok comes from an African antelope spelled 'rhebok' in Afrikaans!",
        "image": "reebok",
    },
    {
        "id": 61, "category": "sports",
        "company": "New Balance", "domain": "newbalance.com",
        "hint": "A bold 'N' on trainers — often grey or black",
        "options": ["New Balance", "Brooks", "Saucony", "Hoka"],
        "fun_fact": "New Balance started in 1906 making arch supports before becoming famous for running shoes!",
        "image": "newbalance",
    },
    {
        "id": 62, "category": "sports",
        "company": "Champion", "domain": "champion.com",
        "hint": "A 'C' with a small flag or pennant inside — sportswear logo",
        "options": ["Champion", "Russell Athletic", "Starter", "Fila"],
        "fun_fact": "Champion invented the hooded sweatshirt in the 1930s for workers in cold warehouses!",
        "image": "champion",
    },
    {
        "id": 63, "category": "cars",
        "company": "Honda", "domain": "honda.com",
        "hint": "A stylised 'H' inside a rounded rectangle — cars and bikes",
        "options": ["Honda", "Toyota", "Mazda", "Subaru"],
        "fun_fact": "Soichiro Honda started with motorized bicycles after World War II before building the Honda Motor Company!",
        "image": "honda",
    },
    {
        "id": 64, "category": "cars",
        "company": "Ford", "domain": "ford.com",
        "hint": "Famous blue oval script — American automaker since 1903",
        "options": ["Ford", "Chevrolet", "Dodge", "GMC"],
        "fun_fact": "Henry Ford helped popularize assembly-line production, making cars affordable for millions!",
        "image": "ford",
    },
    {
        "id": 65, "category": "cars",
        "company": "Nissan", "domain": "nissan.com",
        "hint": "A silver circle with a horizontal bar and bold name — Japanese brand",
        "options": ["Nissan", "Honda", "Mitsubishi", "Suzuki"],
        "fun_fact": "Nissan was originally called Datsun in many export markets before using the Nissan name globally!",
        "image": "nissan",
    },
    {
        "id": 66, "category": "cars",
        "company": "Hyundai", "domain": "hyundai.com",
        "hint": "A slanted italic 'H' inside an oval — two people shaking hands in the design",
        "options": ["Hyundai", "Kia", "Genesis", "Daewoo"],
        "fun_fact": "Hyundai says its logo shows two people shaking hands — trust between company and customer!",
        "image": "hyundai",
    },
    {
        "id": 67, "category": "entertainment",
        "company": "Steam", "domain": "steampowered.com",
        "hint": "A dark circle with a white piston/valve icon — PC games store",
        "options": ["Steam", "Epic Games", "GOG", "Origin"],
        "fun_fact": "Steam launched in 2003 as a way to update Valve games — now it's one of the biggest PC game stores!",
        "image": "steam",
    },
    {
        "id": 68, "category": "entertainment",
        "company": "Twitch", "domain": "twitch.tv",
        "hint": "Purple background with a chat bubble and eyes — live streaming",
        "options": ["Twitch", "YouTube Gaming", "Kick", "Mixer"],
        "fun_fact": "Twitch began as a spin-off from Justin.tv and is now the go-to place for live game streams!",
        "image": "twitch",
    },
    {
        "id": 69, "category": "entertainment",
        "company": "Hulu", "domain": "hulu.com",
        "hint": "Bright green wordmark — TV shows and movies streaming",
        "options": ["Hulu", "Peacock", "Paramount+", "Discovery+"],
        "fun_fact": "Hulu launched in 2008 and became a major streaming home for many TV networks' shows and originals!",
        "image": "hulu",
    },
    {
        "id": 70, "category": "fashion",
        "company": "Gucci", "domain": "gucci.com",
        "hint": "Interlocking double 'G' — luxury Italian fashion",
        "options": ["Gucci", "Prada", "Versace", "Louis Vuitton"],
        "fun_fact": "Gucci was founded in Florence in 1921 as a luggage shop before becoming a global fashion house!",
        "image": "gucci",
    },
    {
        "id": 71, "category": "fashion",
        "company": "Zara", "domain": "zara.com",
        "hint": "Elegant serif wordmark — fast-fashion retailer from Spain",
        "options": ["Zara", "H&M", "Uniqlo", "Gap"],
        "fun_fact": "Zara's parent company Inditex can design, produce, and ship new styles in just a few weeks!",
        "image": "zara",
    },
]


def generate_quiz(num_questions: int = 10, category: str | None = None) -> list:
    """Generate a logo identification quiz with shuffled options."""
    if category and category in CATEGORIES:
        pool = [q for q in QUESTION_BANK if q["category"] == category]
    else:
        pool = list(QUESTION_BANK)

    if len(pool) < num_questions:
        num_questions = len(pool)

    selected = random.sample(pool, num_questions)

    for q in selected:
        company = q["company"]
        options = list(q["options"])
        random.shuffle(options)
        q["_shuffled_options"] = options
        q["_answer_idx"] = options.index(company)
        q["_logo_url"] = get_logo_url(q["domain"])
        q["_image"] = q.get("image")

    random.shuffle(selected)
    return selected


def get_category_counts() -> dict:
    """Return {category_id: count} for questions in each category."""
    counts = {cat_id: 0 for cat_id in CATEGORIES}
    for q in QUESTION_BANK:
        counts[q["category"]] += 1
    return counts
