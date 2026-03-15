"""
Logo Identifier — brand logo recognition quiz for Arjun.

Uses Google's free favicon API for logo images (no auth required).
Only includes brands with ICONIC SYMBOL logos (no readable text)
so the quiz requires genuine recognition, not just reading the name.
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


# Only brands with recognisable SYMBOL / ICON favicons.
# Excluded: brands whose favicon is just their name in text (LinkedIn, Honda, etc.)
QUESTION_BANK = [
    # ========== TECH & APPS (symbol-based favicons) ==========
    {
        "id": 1, "category": "tech",
        "company": "Apple", "domain": "apple.com",
        "hint": "A fruit with a bite taken out of it",
        "options": ["Apple", "Huawei", "BlackBerry", "LG"],
        "fun_fact": "The Apple logo was designed by Rob Janoff in 1977. The bite was added so it wouldn't be confused with a cherry!",
    },
    {
        "id": 2, "category": "tech",
        "company": "Instagram", "domain": "instagram.com",
        "hint": "A gradient camera icon on a purple-orange background",
        "options": ["Instagram", "VSCO", "Snapchat", "Flickr"],
        "fun_fact": "Instagram's camera icon was redesigned in 2016 from a retro Polaroid-style camera to a modern gradient!",
    },
    {
        "id": 3, "category": "tech",
        "company": "Spotify", "domain": "spotify.com",
        "hint": "Three curved lines on a green circle",
        "options": ["Spotify", "SoundCloud", "Shazam", "Deezer"],
        "fun_fact": "Spotify's green logo has three sound waves — representing music streaming to your ears!",
    },
    {
        "id": 4, "category": "tech",
        "company": "Snapchat", "domain": "snapchat.com",
        "hint": "A white ghost outline on a yellow background",
        "options": ["Snapchat", "Discord", "Waze", "Bumble"],
        "fun_fact": "Snapchat's ghost logo was hand-drawn by co-founder Evan Spiegel — it represents disappearing messages!",
    },
    {
        "id": 5, "category": "tech",
        "company": "WhatsApp", "domain": "whatsapp.com",
        "hint": "A white phone inside a speech bubble on a green background",
        "options": ["WhatsApp", "Signal", "Telegram", "Viber"],
        "fun_fact": "WhatsApp was created by two ex-Yahoo employees and bought by Facebook for $19 billion in 2014!",
    },
    {
        "id": 6, "category": "tech",
        "company": "Reddit", "domain": "reddit.com",
        "hint": "An alien face with an antenna on an orange background",
        "options": ["Reddit", "Alien Blue", "Quora", "Tumblr"],
        "fun_fact": "Reddit's alien mascot is called Snoo — short for 'what's new'!",
    },
    {
        "id": 7, "category": "tech",
        "company": "GitHub", "domain": "github.com",
        "hint": "A cat with octopus tentacles silhouette",
        "options": ["GitHub", "GitLab", "Bitbucket", "SourceForge"],
        "fun_fact": "GitHub's mascot is the Octocat — a cat with octopus tentacles. Its original name was Octopuss!",
    },
    {
        "id": 8, "category": "tech",
        "company": "Discord", "domain": "discord.com",
        "hint": "A smiling game controller face on purple/indigo",
        "options": ["Discord", "TeamSpeak", "Slack", "Guilded"],
        "fun_fact": "Discord's mascot is called Clyde — the smiling game controller face was designed to feel friendly!",
    },
    {
        "id": 9, "category": "tech",
        "company": "Twitch", "domain": "twitch.tv",
        "hint": "A speech bubble with eyes on a purple background",
        "options": ["Twitch", "Kick", "Mixer", "YouTube Gaming"],
        "fun_fact": "Twitch's 'Glitch' logo represents live chat bubbles while watching game streams!",
    },
    {
        "id": 10, "category": "tech",
        "company": "Dropbox", "domain": "dropbox.com",
        "hint": "An open blue box made of diamond shapes",
        "options": ["Dropbox", "Box", "Google Drive", "OneDrive"],
        "fun_fact": "Dropbox's open box logo was designed to look like an unfolded cardboard box from above!",
    },
    {
        "id": 11, "category": "tech",
        "company": "Airbnb", "domain": "airbnb.com",
        "hint": "A rounded symbol that looks like a letter A or a heart on a red/coral background",
        "options": ["Airbnb", "Booking.com", "Vrbo", "Trivago"],
        "fun_fact": "Airbnb's logo is called the Bélo — it combines people, places, love, and the letter A!",
    },
    {
        "id": 12, "category": "tech",
        "company": "Slack", "domain": "slack.com",
        "hint": "A hashtag-like shape made of colourful rounded bars",
        "options": ["Slack", "Trello", "Asana", "Notion"],
        "fun_fact": "Slack originally stood for 'Searchable Log of All Conversation and Knowledge'!",
    },
    {
        "id": 13, "category": "tech",
        "company": "Microsoft", "domain": "microsoft.com",
        "hint": "Four coloured squares arranged in a 2×2 grid (red, green, blue, yellow)",
        "options": ["Microsoft", "Google", "Slack", "Samsung"],
        "fun_fact": "Microsoft's four-coloured window logo represents the diversity of their products and users!",
    },
    {
        "id": 14, "category": "tech",
        "company": "TikTok", "domain": "tiktok.com",
        "hint": "A 3D-looking musical note in neon pink/blue on a dark background",
        "options": ["TikTok", "Musical.ly", "Triller", "Dubsmash"],
        "fun_fact": "TikTok's logo looks like a 3D musical note with neon colors inspired by concert stage lighting!",
    },
    {
        "id": 15, "category": "tech",
        "company": "Pinterest", "domain": "pinterest.com",
        "hint": "A stylised letter that looks like a map pin on a red background",
        "options": ["Pinterest", "Pinboard", "Yelp", "Foursquare"],
        "fun_fact": "Pinterest's 'P' logo is shaped like a map pin — because you 'pin' your interests to boards!",
    },
    {
        "id": 16, "category": "tech",
        "company": "YouTube", "domain": "youtube.com",
        "hint": "A white play-button triangle inside a red rounded rectangle",
        "options": ["YouTube", "Vimeo", "Dailymotion", "Rumble"],
        "fun_fact": "The first YouTube video, 'Me at the zoo', was uploaded on April 23, 2005 by co-founder Jawed Karim!",
    },
    {
        "id": 17, "category": "tech",
        "company": "Shazam", "domain": "shazam.com",
        "hint": "A stylised 'S' shape on a blue gradient circle",
        "options": ["Shazam", "SoundHound", "Spotify", "Deezer"],
        "fun_fact": "Shazam can identify a song in just a few seconds by matching its audio fingerprint to a database of millions!",
    },
    {
        "id": 18, "category": "tech",
        "company": "Zoom", "domain": "zoom.us",
        "hint": "A white video camera icon on a blue background",
        "options": ["Zoom", "Skype", "Google Meet", "WebEx"],
        "fun_fact": "Zoom usage jumped from 10 million to 300 million daily users during the 2020 pandemic!",
    },

    # ========== FOOD & DRINKS (symbol-based favicons) ==========
    {
        "id": 19, "category": "food",
        "company": "Starbucks", "domain": "starbucks.com",
        "hint": "A green circle with a two-tailed mermaid (siren) in the centre",
        "options": ["Starbucks", "Dunkin'", "Peet's Coffee", "Costa Coffee"],
        "fun_fact": "The Starbucks logo features a two-tailed mermaid (siren) inspired by a 16th-century Norse woodcut!",
    },
    {
        "id": 20, "category": "food",
        "company": "McDonald's", "domain": "mcdonalds.com",
        "hint": "Golden arches forming an 'M' shape on a red background",
        "options": ["McDonald's", "Burger King", "Wendy's", "In-N-Out"],
        "fun_fact": "The Golden Arches were originally part of the restaurant's actual building architecture before becoming the logo!",
    },
    {
        "id": 21, "category": "food",
        "company": "Pepsi", "domain": "pepsi.com",
        "hint": "A circle divided into red, white, and blue wavy sections",
        "options": ["Pepsi", "Coca-Cola", "RC Cola", "Dr Pepper"],
        "fun_fact": "Pepsi has redesigned its globe logo over 10 times since 1898!",
    },
    {
        "id": 22, "category": "food",
        "company": "Red Bull", "domain": "redbull.com",
        "hint": "Two red bulls charging at each other with a golden sun behind them",
        "options": ["Red Bull", "Monster", "Rockstar", "Celsius"],
        "fun_fact": "Red Bull's logo shows two bulls charging at each other — inspired by the Thai energy drink Krating Daeng!",
    },
    {
        "id": 23, "category": "food",
        "company": "KFC", "domain": "kfc.com",
        "hint": "A man's face with glasses, a goatee, and a bow tie",
        "options": ["KFC", "Popeyes", "Church's Chicken", "Boston Market"],
        "fun_fact": "Colonel Sanders' face in the KFC logo is based on the real founder who started his chicken recipe at age 65!",
    },
    {
        "id": 24, "category": "food",
        "company": "Domino's", "domain": "dominos.com",
        "hint": "A red and blue domino tile with dots",
        "options": ["Domino's", "Pizza Hut", "Papa John's", "Little Caesars"],
        "fun_fact": "The three dots on the Domino's logo represent the first three stores. They planned to add a dot per store but grew too fast!",
    },
    {
        "id": 25, "category": "food",
        "company": "Taco Bell", "domain": "tacobell.com",
        "hint": "A bell shape in purple and pink tones",
        "options": ["Taco Bell", "Chipotle", "Del Taco", "Qdoba"],
        "fun_fact": "Taco Bell was named after its founder, Glen Bell, and the bell logo is a play on his last name!",
    },
    {
        "id": 26, "category": "food",
        "company": "Chick-fil-A", "domain": "chick-fil-a.com",
        "hint": "A red icon with a chicken silhouette hidden in a letter",
        "options": ["Chick-fil-A", "Raising Cane's", "Zaxby's", "Wingstop"],
        "fun_fact": "The 'C' in Chick-fil-A's logo is cleverly shaped like a chicken — look closely at the curve!",
    },
    {
        "id": 27, "category": "food",
        "company": "Wendy's", "domain": "wendys.com",
        "hint": "A girl with red pigtails on a blue background",
        "options": ["Wendy's", "Dairy Queen", "Arby's", "Jack in the Box"],
        "fun_fact": "The Wendy's logo is based on the founder Dave Thomas's daughter, Melinda Lou 'Wendy' Thomas!",
    },

    # ========== SPORTS & OUTDOORS (symbol-based favicons) ==========
    {
        "id": 28, "category": "sports",
        "company": "Nike", "domain": "nike.com",
        "hint": "A simple curved checkmark shape (swoosh)",
        "options": ["Nike", "Adidas", "New Balance", "Reebok"],
        "fun_fact": "The Nike Swoosh was designed by graphic design student Carolyn Davidson for just $35 in 1971!",
    },
    {
        "id": 29, "category": "sports",
        "company": "Adidas", "domain": "adidas.com",
        "hint": "Three parallel diagonal stripes forming a mountain/triangle shape",
        "options": ["Adidas", "Puma", "Fila", "Kappa"],
        "fun_fact": "Adidas' three stripes were originally just to hold the shoe together — they accidentally became the logo!",
    },
    {
        "id": 30, "category": "sports",
        "company": "Puma", "domain": "puma.com",
        "hint": "A leaping big cat (cougar/puma) silhouette",
        "options": ["Puma", "Jaguar", "Adidas", "Lacoste"],
        "fun_fact": "Puma was founded by Rudolf Dassler — the brother of Adidas founder Adi Dassler! The brothers had a falling out.",
    },
    {
        "id": 31, "category": "sports",
        "company": "Under Armour", "domain": "underarmour.com",
        "hint": "Two overlapping letters that form an interlocking shape",
        "options": ["Under Armour", "Champion", "Reebok", "ASICS"],
        "fun_fact": "Under Armour's logo is two overlapping U's that also cleverly form an A!",
    },
    {
        "id": 32, "category": "sports",
        "company": "Lacoste", "domain": "lacoste.com",
        "hint": "A small green crocodile/alligator",
        "options": ["Lacoste", "Polo Ralph Lauren", "Fred Perry", "Puma"],
        "fun_fact": "The Lacoste crocodile logo was inspired by founder René Lacoste's nickname 'The Crocodile' from tennis!",
    },
    {
        "id": 33, "category": "sports",
        "company": "The North Face", "domain": "thenorthface.com",
        "hint": "Three curved lines forming a quarter-dome shape",
        "options": ["The North Face", "Patagonia", "Columbia", "Arc'teryx"],
        "fun_fact": "The North Face logo represents Half Dome, the famous rock formation in Yosemite National Park!",
    },

    # ========== CARS & TRANSPORT (symbol-based favicons) ==========
    {
        "id": 34, "category": "cars",
        "company": "Tesla", "domain": "tesla.com",
        "hint": "A stylised letter that also looks like a cross-section of an electric motor",
        "options": ["Tesla", "Rivian", "Lucid", "Polestar"],
        "fun_fact": "Tesla's 'T' logo is actually a cross-section of an electric motor — design meets engineering!",
    },
    {
        "id": 35, "category": "cars",
        "company": "BMW", "domain": "bmw.com",
        "hint": "A circle divided into four quadrants — two blue and two white",
        "options": ["BMW", "Volkswagen", "Audi", "Volvo"],
        "fun_fact": "BMW's blue and white quarters represent the colors of the Bavarian flag in Germany!",
    },
    {
        "id": 36, "category": "cars",
        "company": "Mercedes-Benz", "domain": "mercedes-benz.com",
        "hint": "A three-pointed star inside a circle",
        "options": ["Mercedes-Benz", "Lexus", "Infiniti", "Acura"],
        "fun_fact": "The three-pointed star represents Mercedes' ambition to motorise land, sea, and air transport!",
    },
    {
        "id": 37, "category": "cars",
        "company": "Ferrari", "domain": "ferrari.com",
        "hint": "A prancing horse on a yellow shield background",
        "options": ["Ferrari", "Porsche", "Lamborghini", "Maserati"],
        "fun_fact": "Ferrari's prancing horse was originally a symbol painted on a World War I Italian fighter plane!",
    },
    {
        "id": 38, "category": "cars",
        "company": "Lamborghini", "domain": "lamborghini.com",
        "hint": "A charging bull on a dark shield",
        "options": ["Lamborghini", "Ferrari", "Bugatti", "McLaren"],
        "fun_fact": "Lamborghini's bull logo reflects founder Ferruccio Lamborghini's zodiac sign — Taurus the bull!",
    },
    {
        "id": 39, "category": "cars",
        "company": "Audi", "domain": "audi.com",
        "hint": "Four interlocking rings in a horizontal row",
        "options": ["Audi", "Olympic Committee", "Volkswagen", "Volvo"],
        "fun_fact": "Audi's four rings represent the four companies that merged to create it in 1932!",
    },
    {
        "id": 40, "category": "cars",
        "company": "Porsche", "domain": "porsche.com",
        "hint": "An ornate crest with a horse, antlers, and red/black stripes",
        "options": ["Porsche", "Ferrari", "Aston Martin", "Bentley"],
        "fun_fact": "Porsche's crest features the horse from Stuttgart's coat of arms and the antlers from Württemberg!",
    },
    {
        "id": 41, "category": "cars",
        "company": "Volkswagen", "domain": "volkswagen.com",
        "hint": "Two letters stacked vertically inside a circle",
        "options": ["Volkswagen", "Volvo", "Vauxhall", "Vinfast"],
        "fun_fact": "Volkswagen means 'people's car' in German — it was originally designed to be affordable for everyone!",
    },
    {
        "id": 42, "category": "cars",
        "company": "Toyota", "domain": "toyota.com",
        "hint": "Three overlapping ovals forming a symmetrical pattern",
        "options": ["Toyota", "Mazda", "Subaru", "Nissan"],
        "fun_fact": "Toyota's overlapping ovals logo secretly contains every letter of 'TOYOTA' hidden within it!",
    },
    {
        "id": 43, "category": "cars",
        "company": "Chevrolet", "domain": "chevrolet.com",
        "hint": "A golden cross / bowtie shape",
        "options": ["Chevrolet", "Ford", "Dodge", "Chrysler"],
        "fun_fact": "The Chevy bowtie logo's origin is debated — one theory says it was inspired by wallpaper in a Paris hotel!",
    },
    {
        "id": 44, "category": "cars",
        "company": "Subaru", "domain": "subaru.com",
        "hint": "A cluster of stars on a blue oval background",
        "options": ["Subaru", "Mitsubishi", "Mazda", "Suzuki"],
        "fun_fact": "Subaru means 'unite' in Japanese. Its star logo represents the Pleiades star cluster!",
    },
    {
        "id": 45, "category": "cars",
        "company": "Mitsubishi", "domain": "mitsubishi.com",
        "hint": "Three red diamond shapes arranged in a triangle/pinwheel",
        "options": ["Mitsubishi", "Suzuki", "Subaru", "Isuzu"],
        "fun_fact": "Mitsubishi means 'three diamonds' in Japanese — exactly what the logo shows!",
    },

    # ========== ENTERTAINMENT & MEDIA (symbol-based favicons) ==========
    {
        "id": 46, "category": "entertainment",
        "company": "PlayStation", "domain": "playstation.com",
        "hint": "A 'P' standing up with an 'S' lying flat, creating a 3D-looking icon",
        "options": ["PlayStation", "Xbox", "Steam", "Atari"],
        "fun_fact": "The PS logo cleverly hides the letters P and S — the P stands upright while the S lies flat behind it!",
    },
    {
        "id": 47, "category": "entertainment",
        "company": "Xbox", "domain": "xbox.com",
        "hint": "A green sphere with a white X across it",
        "options": ["Xbox", "GeForce", "Razer", "Steam"],
        "fun_fact": "Xbox got its name from DirectX, Microsoft's graphics technology — 'DirectX Box' became 'Xbox'!",
    },
    {
        "id": 48, "category": "entertainment",
        "company": "Steam", "domain": "store.steampowered.com",
        "hint": "A circular gear with a piston/lever shape inside, in dark blue/steel tones",
        "options": ["Steam", "GOG", "Epic Games", "Origin"],
        "fun_fact": "Steam was launched in 2003 and now has over 120 million monthly active users!",
    },
    {
        "id": 49, "category": "entertainment",
        "company": "Roblox", "domain": "roblox.com",
        "hint": "A tilted grey/dark square with a circular hole in it",
        "options": ["Roblox", "Minecraft", "Fortnite", "Among Us"],
        "fun_fact": "Roblox has over 70 million daily active users and the name is a mix of 'robots' and 'blocks'!",
    },
    {
        "id": 50, "category": "entertainment",
        "company": "Twitch", "domain": "twitch.tv",
        "hint": "A speech-bubble shape with two glowing eyes on a purple background",
        "options": ["Twitch", "Kick", "YouTube Gaming", "Facebook Gaming"],
        "fun_fact": "Twitch's 'Glitch' mascot has two eyes peeking out of a speech bubble — always watching the stream!",
    },
    {
        "id": 51, "category": "entertainment",
        "company": "Discord", "domain": "discord.com",
        "hint": "A rounded robot/controller face with a wide smile on blue/indigo",
        "options": ["Discord", "Slack", "Guilded", "Element"],
        "fun_fact": "Discord was originally made for gamers but now has communities for everything from art to study groups!",
    },
    {
        "id": 52, "category": "entertainment",
        "company": "Nintendo", "domain": "nintendo.com",
        "hint": "A bold red rounded rectangle with a white letter inside",
        "options": ["Nintendo", "Netflix", "Namco", "Naughty Dog"],
        "fun_fact": "Nintendo was founded in 1889 as a playing card company — they made cards for 75 years before making games!",
    },
    {
        "id": 53, "category": "entertainment",
        "company": "Spotify", "domain": "open.spotify.com",
        "hint": "Three curved sound-wave lines on a bright green circle",
        "options": ["Spotify", "Apple Music", "Pandora", "Tidal"],
        "fun_fact": "Spotify pays artists between $0.003 and $0.005 per stream!",
    },
    {
        "id": 54, "category": "entertainment",
        "company": "Netflix", "domain": "netflix.com",
        "hint": "A bold red letter on a dark/black background",
        "options": ["Netflix", "Hulu", "HBO Max", "Paramount+"],
        "fun_fact": "Netflix started as a DVD-by-mail service in 1997 — they mailed their first DVD in 1998!",
    },
    {
        "id": 55, "category": "entertainment",
        "company": "Disney", "domain": "disney.com",
        "hint": "A castle silhouette or a cursive script signature",
        "options": ["Disney", "Universal", "Paramount", "Warner Bros."],
        "fun_fact": "Walt Disney's personal signature inspired the famous Disney logo script!",
    },
    {
        "id": 56, "category": "entertainment",
        "company": "Epic Games", "domain": "epicgames.com",
        "hint": "A dark icon with a stylised face/side profile",
        "options": ["Epic Games", "Valve", "Riot Games", "Rockstar Games"],
        "fun_fact": "Epic Games was founded by Tim Sweeney when he was in college — now they make Fortnite and Unreal Engine!",
    },

    # ========== FASHION & LIFESTYLE (symbol-based favicons) ==========
    {
        "id": 57, "category": "fashion",
        "company": "Target", "domain": "target.com",
        "hint": "A red and white bullseye (concentric circles)",
        "options": ["Target", "CVS", "Walgreens", "Kmart"],
        "fun_fact": "Target's bullseye logo is one of the most recognised in the US — their dog mascot is named Bullseye too!",
    },
    {
        "id": 58, "category": "fashion",
        "company": "IKEA", "domain": "ikea.com",
        "hint": "A blue and yellow colour scheme with bold letters in an oval",
        "options": ["IKEA", "Wayfair", "Ashley", "Crate & Barrel"],
        "fun_fact": "IKEA's name comes from founder Ingvar Kamprad's initials plus the farm and village where he grew up in Sweden!",
    },
    {
        "id": 59, "category": "fashion",
        "company": "Lacoste", "domain": "lacoste.com",
        "hint": "A small green crocodile/alligator facing right",
        "options": ["Lacoste", "Ralph Lauren", "Tommy Hilfiger", "Hugo Boss"],
        "fun_fact": "Tennis legend René Lacoste was nicknamed 'The Crocodile' for his tenacity on the court — it became the logo!",
    },
    {
        "id": 60, "category": "fashion",
        "company": "Converse", "domain": "converse.com",
        "hint": "A star inside a circle — the classic All Star emblem",
        "options": ["Converse", "Vans", "DC Shoes", "Skechers"],
        "fun_fact": "Chuck Taylor All Stars were originally basketball shoes designed in 1917 — now they're a fashion icon!",
    },
    {
        "id": 61, "category": "fashion",
        "company": "Ralph Lauren", "domain": "ralphlauren.com",
        "hint": "A polo player on horseback swinging a mallet",
        "options": ["Ralph Lauren", "U.S. Polo Assn.", "Lacoste", "Tommy Hilfiger"],
        "fun_fact": "Ralph Lauren's real name was Ralph Lifshitz — he changed it in high school and built a fashion empire!",
    },
    {
        "id": 62, "category": "fashion",
        "company": "Crocs", "domain": "crocs.com",
        "hint": "A cartoon crocodile/alligator wearing sunglasses, smiling",
        "options": ["Crocs", "Birkenstock", "Keen", "Teva"],
        "fun_fact": "Crocs were originally designed as boat shoes but became a worldwide fashion phenomenon!",
    },

    # ========== ADDITIONAL TRICKY ONES ==========
    {
        "id": 63, "category": "tech",
        "company": "Evernote", "domain": "evernote.com",
        "hint": "A green elephant head with a folded ear",
        "options": ["Evernote", "Notion", "OneNote", "Bear"],
        "fun_fact": "Evernote's elephant logo represents that elephants never forget — just like the app remembers your notes!",
    },
    {
        "id": 64, "category": "tech",
        "company": "Firefox", "domain": "mozilla.org",
        "hint": "A fox curled around a blue/purple globe",
        "options": ["Firefox", "Chrome", "Opera", "Vivaldi"],
        "fun_fact": "Firefox's logo shows a fox wrapping around the Earth — but it's actually a red panda, not a fox!",
    },
    {
        "id": 65, "category": "tech",
        "company": "Android", "domain": "android.com",
        "hint": "A green robot with antenna on top of its head",
        "options": ["Android", "Chrome OS", "Linux", "HarmonyOS"],
        "fun_fact": "The Android robot mascot is called 'Bugdroid' and was inspired by bathroom door symbols!",
    },
    {
        "id": 66, "category": "food",
        "company": "Pringles", "domain": "pringles.com",
        "hint": "A man with a large moustache and a bow-shaped hairstyle",
        "options": ["Pringles", "Lay's", "Doritos", "Cheetos"],
        "fun_fact": "The Pringles mascot is called Julius Pringles — his iconic moustache has been there since 1968!",
    },
    {
        "id": 67, "category": "cars",
        "company": "Jaguar", "domain": "jaguar.com",
        "hint": "A leaping big cat (jaguar) silhouette",
        "options": ["Jaguar", "Puma", "Bentley", "Aston Martin"],
        "fun_fact": "The Jaguar 'leaper' mascot was banned from car hoods in some countries due to pedestrian safety concerns!",
    },
    {
        "id": 68, "category": "entertainment",
        "company": "LEGO", "domain": "lego.com",
        "hint": "Bold white letters on a bright red rounded square",
        "options": ["LEGO", "Mega Bloks", "K'NEX", "Playmobil"],
        "fun_fact": "LEGO comes from the Danish words 'leg godt' meaning 'play well' — and it sells about 75 billion bricks a year!",
    },
    {
        "id": 69, "category": "food",
        "company": "Dunkin'", "domain": "dunkindonuts.com",
        "hint": "Orange and pink colours with a coffee cup shape",
        "options": ["Dunkin'", "Tim Hortons", "Krispy Kreme", "Starbucks"],
        "fun_fact": "Dunkin' dropped 'Donuts' from its name in 2019 — they wanted to be known for coffee, not just donuts!",
    },
    {
        "id": 70, "category": "tech",
        "company": "Duolingo", "domain": "duolingo.com",
        "hint": "A bright green owl with large round eyes",
        "options": ["Duolingo", "Babbel", "Rosetta Stone", "Memrise"],
        "fun_fact": "Duolingo's owl mascot is named Duo — and he's famous for guilt-tripping users who miss lessons!",
    },
    {
        "id": 71, "category": "sports",
        "company": "Ferrari", "domain": "ferrari.com",
        "hint": "A prancing horse on a yellow shield",
        "options": ["Ferrari", "Porsche", "Lamborghini", "Ducati"],
        "fun_fact": "Ferrari's prancing horse was given to Enzo Ferrari by the parents of a WWI flying ace who had it on his plane!",
    },
    {
        "id": 72, "category": "tech",
        "company": "Waze", "domain": "waze.com",
        "hint": "A smiling white ghost-like character with a blue speech bubble",
        "options": ["Waze", "Google Maps", "Apple Maps", "HERE"],
        "fun_fact": "Waze uses crowdsourced data — real drivers report traffic, accidents, and police in real time!",
    },
    {
        "id": 73, "category": "food",
        "company": "Monster Energy", "domain": "monsterenergy.com",
        "hint": "A green claw scratch mark on a black background",
        "options": ["Monster Energy", "Red Bull", "Rockstar", "G Fuel"],
        "fun_fact": "Monster's 'M' logo is actually three claw scratches that form the letter M — it looks like a monster attacked the can!",
    },
    {
        "id": 74, "category": "fashion",
        "company": "Versace", "domain": "versace.com",
        "hint": "A Greek mythological head (Medusa) in gold on a dark background",
        "options": ["Versace", "Gucci", "Dolce & Gabbana", "Prada"],
        "fun_fact": "Versace's Medusa head logo was chosen because Gianni Versace loved Greek mythology and its power symbolism!",
    },
    {
        "id": 75, "category": "tech",
        "company": "Opera", "domain": "opera.com",
        "hint": "A red 'O' shape on a dark background",
        "options": ["Opera", "Firefox", "Brave", "Vivaldi"],
        "fun_fact": "Opera was one of the first browsers to include a built-in VPN and ad blocker for free!",
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

    random.shuffle(selected)
    return selected


def get_category_counts() -> dict:
    """Return {category_id: count} for questions in each category."""
    counts = {cat_id: 0 for cat_id in CATEGORIES}
    for q in QUESTION_BANK:
        counts[q["category"]] += 1
    return counts
