"""Download new brand logos from Simple Icons (jsDelivr CDN)."""
import os, re, sys, time, urllib.request
try:
    import truststore; truststore.inject_into_ssl()
except ImportError:
    pass
import cairosvg

OUT = os.path.join(os.path.dirname(__file__), "brand_logos")
CDN = "https://cdn.jsdelivr.net/npm/simple-icons@latest/icons"

def colorize(svg, color):
    return re.sub(r'<svg ', f'<svg fill="#{color}" ', svg, count=1)

def dl(fname, slug, color):
    out = os.path.join(OUT, f"{fname}.png")
    if os.path.exists(out) and os.path.getsize(out) > 500:
        return "skip"
    url = f"{CDN}/{slug}.svg"
    try:
        req = urllib.request.Request(url, headers={"User-Agent":"Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as r:
            svg = r.read().decode("utf-8")
        svg = colorize(svg, color)
        cairosvg.svg2png(bytestring=svg.encode(), write_to=out, output_width=512, output_height=512, background_color="white")
        return "ok"
    except Exception as e:
        return f"FAIL:{e}"

# (filename, simple-icons slug, hex color)
BRANDS = [
    # Tech
    ("telegram","telegram","26A5E4"),("signal","signal","3A76F0"),("skype","skype","00AFF0"),
    ("google","google","4285F4"),("amazon","amazon","FF9900"),("uber","uber","000000"),
    ("lyft","lyft","FF00BF"),("paypal","paypal","003087"),("shopify","shopify","7AB55C"),
    ("adobe","adobe","FF0000"),("ibm","ibm","052FAD"),("intel","intel","0071C5"),
    ("amd","amd","ED1C24"),("nvidia","nvidia","76B900"),("figma","figma","F24E1E"),
    ("notion","notion","000000"),("brave","brave","FB542B"),("samsung","samsung","1428A0"),
    ("linkedin","linkedin","0A66C2"),("cloudflare","cloudflare","F38020"),("wordpress","wordpress","21759B"),
    # Food
    ("cocacola","cocacola","F40009"),("chipotle","chipotle","A81612"),
    ("pizzahut","pizzahut","EE3A23"),("popeyes","popeyes","F47920"),
    ("krispykreme","krispykreme","00A857"),("baskinrobbins","baskinrobbins","FF0099"),
    ("doordash","doordash","FF3008"),("grubhub","grubhub","F63440"),("ubereats","ubereats","06C167"),
    ("nespresso","nespresso","000000"),("timhortons","timhortons","C8102E"),
    ("gatorade","gatorade","FC4C02"),("nestle","nestle","009CA6"),
    ("mountaindew","mountaindew","1A8B1A"),("sprite","sprite","008B47"),("fanta","fanta","F58220"),
    ("dairyqueen","dairyqueen","ED1C24"),("panera","panerabread","456E16"),
    ("sonic","sonicdrivein","F2A71B"),("fiveguys","fiveguys","D2232A"),
    ("heineken","heineken","00A100"),("budweiser","budweiser","C8102E"),
    # Sports
    ("reebok","reebok","000000"),("newbalance","newbalance","CF0A2C"),
    ("asics","asics","003E7E"),("fila","fila","27346A"),("jordan","jordan","000000"),
    ("oakley","oakley","000000"),("columbia","columbia","1473B6"),("patagonia","patagonia","262626"),
    ("ufc","ufc","D20A0A"),("formula1","formula1","E10600"),
    ("premierleague","premierleague","3D195B"),("nhl","nhl","000000"),
    ("mlb","mlb","041E42"),("speedo","speedo","001489"),("wilson","wilson","EE1B24"),
    ("champion","champion","0066CC"),("kappa","kappa","303F9E"),("arcteryx","arcteryx","000000"),
    ("mls","mls","000000"),
    # Cars
    ("hyundai","hyundai","002C5F"),("kia","kia","05141F"),("nissan","nissan","C3002F"),
    ("mazda","mazda","101010"),("honda","honda","CC0000"),("volvo","volvo","003057"),
    ("landrover","landrover","005A2B"),("bentley","bentley","333333"),
    ("rollsroyce","rollsroyce","662483"),("astonmartin","astonmartin","006837"),
    ("mclaren","mclaren","FF0000"),("bugatti","bugatti","BE0030"),
    ("maserati","maserati","0C2340"),("alfaromeo","alfaromeo","981E32"),
    ("fiat","fiat","941711"),("jeep","jeep","262626"),("dodge","dodge","000000"),
    ("cadillac","cadillac","C0272D"),("lexus","lexus","000000"),
    ("rivian","rivian","324B48"),("polestar","polestar","000000"),("lucid","lucidmotors","000000"),
    # Entertainment
    ("hulu","hulu","1CE783"),("hbo","hbo","000000"),("paramount","paramountplus","0064FF"),
    ("sony","sony","000000"),("sega","sega","0060A8"),("atari","atari","E4202E"),
    ("ea","ea","000000"),("ubisoft","ubisoft","000000"),
    ("riotgames","riotgames","D32936"),("rockstargames","rockstargames","FCAF17"),
    ("crunchyroll","crunchyroll","F47521"),("applemusic","applemusic","FA243C"),
    ("amazonmusic","amazonmusic","25D8FD"),("soundcloud","soundcloud","FF5500"),
    ("deezer","deezer","A238FF"),("activision","activision","000000"),
    ("warnerbros","warnerbros","004DB4"),("marvel","marvel","EC1D24"),
    ("cartoonnetwork","cartoonnetwork","000000"),("nickelodeon","nickelodeon","F57D25"),
    ("valve","valve","F74843"),("mojang","mojangstudios","EF323D"),
    ("primevideo","primevideo","1A98FF"),("dc","dc","0078F0"),
    # Fashion
    ("vans","vans","000000"),("gucci","gucci","000000"),("louisvuitton","louisvuitton","000000"),
    ("chanel","chanel","000000"),("burberry","burberry","000000"),("zara","zara","000000"),
    ("hm","handm","E50010"),("uniqlo","uniqlo","FF0000"),
    ("lululemon","lululemon","D31334"),("supreme","supreme","000000"),
    ("timberland","timberland","000000"),("drmartens","drmartens","000000"),
    ("birkenstock","birkenstock","040404"),("rolex","rolex","006039"),
    ("costco","costco","005DAA"),("walmart","walmart","0071CE"),
    ("dior","dior","000000"),("prada","prada","000000"),
    ("gap","gap","000000"),("swatch","swatch","000000"),
    ("casio","casio","000000"),("omega","omega","000000"),
]

os.makedirs(OUT, exist_ok=True)
ok = skip = fail = 0
failed_list = []
for i,(f,s,c) in enumerate(BRANDS,1):
    r = dl(f,s,c)
    if r == "skip":
        skip += 1
    elif r == "ok":
        ok += 1
        print(f"  [{i}/{len(BRANDS)}] {f}: OK")
    else:
        fail += 1
        failed_list.append((f,s,r))
        print(f"  [{i}/{len(BRANDS)}] {f}: {r}")
    time.sleep(0.3)

print(f"\nDone! OK:{ok} Skip:{skip} Fail:{fail}")
if failed_list:
    print("Failed:")
    for f,s,r in failed_list:
        print(f"  {f} ({s}): {r}")
