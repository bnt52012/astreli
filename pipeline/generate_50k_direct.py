"""
╔══════════════════════════════════════════════════════════════════════╗
║  AdGenAI — 50 000 Scénarios via Appels Directs (pas de Batch API)   ║
║                                                                      ║
║  30 000 mannequin + 20 000 produit = 50 000 total                   ║
║  Classé par industrie dans dataset/scenarios/{industrie}/            ║
║                                                                      ║
║  Usage :                                                             ║
║    python3 generate_50k_direct.py                                    ║
║                                                                      ║
║  Reprend automatiquement là où il s'est arrêté si interrompu.       ║
╚══════════════════════════════════════════════════════════════════════╝
"""

import os
import json
import time
import argparse
import concurrent.futures
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

BASE_DIR = Path("dataset/scenarios")
PROGRESS_FILE = BASE_DIR / "_progress_direct.json"
BASE_DIR.mkdir(parents=True, exist_ok=True)

# ═══════════════════════════════════════════════════════════
# 50 000 SCÉNARIOS — 30 000 MANNEQUIN + 20 000 PRODUIT
# ═══════════════════════════════════════════════════════════

INDUSTRIES = {
    "luxury": {
        "name": "Luxury Fashion & Maroquinerie",
        "personnage": 5500, "produit": 2500,
        "brands": ["Chanel", "Hermès", "Louis Vuitton", "Dior", "Gucci", "Prada", "Valentino", "Balenciaga", "Bottega Veneta", "Saint Laurent", "Givenchy", "Fendi", "Loewe", "Celine", "Burberry", "Versace", "Alexander McQueen", "Tom Ford", "Dolce & Gabbana", "Balmain"],
        "products": ["leather handbag", "silk scarf", "designer coat", "evening gown", "cashmere sweater", "leather boots", "statement necklace", "designer sunglasses", "monogram wallet", "tweed jacket", "cocktail dress", "leather belt", "designer sneakers", "trench coat", "clutch bag", "fur stole", "silk blouse", "tailored suit", "leather gloves", "designer hat"],
    },
    "beauty": {
        "name": "Beauty & Cosmetics",
        "personnage": 3500, "produit": 2000,
        "brands": ["L'Oréal Paris", "Estée Lauder", "MAC Cosmetics", "Charlotte Tilbury", "NARS", "Dior Beauty", "YSL Beauty", "Tom Ford Beauty", "Fenty Beauty", "La Mer", "Chanel Beauty", "Guerlain", "Lancôme", "Clinique", "Pat McGrath Labs", "Hourglass", "Tatcha", "Drunk Elephant", "Glossier", "Rare Beauty"],
        "products": ["foundation", "lipstick", "mascara", "face serum", "eye palette", "skincare cream", "highlighter", "blush compact", "setting spray", "face oil", "concealer", "bronzer", "lip gloss", "eye cream", "toner", "sheet mask", "primer", "brow pencil", "lip liner", "powder compact"],
    },
    "fragrance": {
        "name": "Fragrance & Parfum",
        "personnage": 3000, "produit": 2000,
        "brands": ["Chanel Fragrance", "Dior Parfums", "Tom Ford Private Blend", "Le Labo", "Byredo", "Maison Francis Kurkdjian", "Jo Malone", "Acqua di Parma", "Diptyque", "Creed", "Penhaligon's", "Frederic Malle", "Amouage", "Initio", "Parfums de Marly", "Xerjoff", "Memo Paris", "Maison Margiela Replica", "Aesop", "Serge Lutens"],
        "products": ["eau de parfum bottle", "cologne flacon", "perfume atomizer", "scented candle", "fragrance gift set", "travel spray", "perfume oil", "room diffuser", "solid perfume", "discovery set", "body mist", "aftershave", "incense", "linen spray", "perfumed soap", "scented sachet", "fragrance layering set", "extrait de parfum", "eau de toilette", "home fragrance collection"],
    },
    "jewelry_watches": {
        "name": "Jewelry & Watches",
        "personnage": 3000, "produit": 2000,
        "brands": ["Rolex", "Cartier", "Tiffany & Co.", "Bulgari", "Van Cleef & Arpels", "Chopard", "Piaget", "Omega", "Patek Philippe", "Harry Winston", "Graff", "Boucheron", "Chaumet", "Messika", "Pomellato", "Jaeger-LeCoultre", "Audemars Piguet", "IWC", "Vacheron Constantin", "Breitling"],
        "products": ["diamond ring", "gold bracelet", "luxury watch", "pearl necklace", "sapphire earrings", "platinum cufflinks", "emerald pendant", "tennis bracelet", "chronograph watch", "cocktail ring", "diamond stud earrings", "chain necklace", "signet ring", "dress watch", "dive watch", "tourbillon", "brooch", "charm bracelet", "tiara", "watch winder"],
    },
    "fashion": {
        "name": "Accessible Premium Fashion",
        "personnage": 3000, "produit": 1500,
        "brands": ["Sandro", "Maje", "COS", "Massimo Dutti", "Reiss", "AllSaints", "Theory", "Zadig & Voltaire", "Isabel Marant", "Acne Studios", "A.P.C.", "Ganni", "Self-Portrait", "Jacquemus", "Nanushka", "Totême", "The Kooples", "Ba&sh", "Claudie Pierlot", "Equipment"],
        "products": ["tailored blazer", "linen dress", "leather jacket", "wool coat", "silk blouse", "designer jeans", "midi skirt", "knit sweater", "trench coat", "ankle boots", "wrap dress", "cashmere cardigan", "wide-leg trousers", "denim jacket", "pleated skirt", "silk camisole", "oversized shirt", "leather tote", "wool scarf", "suede boots"],
    },
    "automotive": {
        "name": "Premium & Luxury Automotive",
        "personnage": 2000, "produit": 2000,
        "brands": ["Mercedes-Benz", "BMW", "Porsche", "Range Rover", "Audi", "Lexus", "Maserati", "Aston Martin", "Bentley", "Tesla", "Rolls-Royce", "Ferrari", "Lamborghini", "McLaren", "Volvo Premium", "Genesis", "Lucid Motors", "Rivian", "Polestar", "Jaguar"],
        "products": ["luxury sedan", "sports car", "SUV", "electric vehicle", "convertible", "grand tourer", "luxury interior", "alloy wheels", "leather steering wheel", "key fob", "dashboard display", "headlight design", "grille detail", "rear light design", "engine detail", "carbon fiber trim", "infotainment system", "panoramic roof", "performance exhaust", "aerodynamic kit"],
    },
    "sport": {
        "name": "Premium Sport & Athleisure",
        "personnage": 2500, "produit": 1000,
        "brands": ["Nike Premium", "Lululemon", "On Running", "Adidas Premium", "Arc'teryx", "Rapha", "Tracksmith", "Satisfy Running", "Vuori", "Alo Yoga", "Hoka", "Salomon", "New Balance Premium", "Asics Premium", "The North Face Summit", "Patagonia", "Canada Goose", "Gymshark Premium", "Rhone", "Ten Thousand"],
        "products": ["running shoes", "yoga mat", "performance jacket", "training leggings", "sports watch", "cycling jersey", "hiking boots", "gym bag", "compression top", "trail running shoes", "sports bra", "running shorts", "climbing harness", "ski jacket", "wetsuit", "boxing gloves", "tennis racket", "golf club", "swim goggles", "fitness tracker"],
    },
    "food_beverage": {
        "name": "Premium Food & Beverage",
        "personnage": 1500, "produit": 2500,
        "brands": ["Nespresso", "Dom Pérignon", "Godiva", "Ladurée", "Veuve Clicquot", "Hennessy", "La Maison du Chocolat", "TWG Tea", "Ruinart", "Moët & Chandon", "Krug", "Macallan", "Grey Goose", "Patrón", "Illy", "Pierre Hermé", "Fauchon", "Mariage Frères", "Fortnum & Mason", "Clase Azul"],
        "products": ["champagne bottle", "chocolate box", "espresso machine", "wine bottle", "macaron tower", "caviar tin", "tea set", "cocktail", "gourmet cheese platter", "artisan bread", "truffle box", "whiskey decanter", "olive oil bottle", "honey jar", "foie gras terrine", "smoked salmon", "aged balsamic vinegar", "matcha set", "coffee capsules", "crystal wine glass"],
    },
    "tech": {
        "name": "Premium Tech",
        "personnage": 1500, "produit": 1500,
        "brands": ["Apple", "Bang & Olufsen", "Leica", "Dyson", "Bose", "Sony Premium", "Hasselblad", "DJI", "Sonos", "Master & Dynamic", "Devialet", "Naim Audio", "Bowers & Wilkins", "Sennheiser", "KEF", "McIntosh", "Technics Premium", "Cambridge Audio", "Focal", "Linn"],
        "products": ["smartphone", "wireless headphones", "camera", "laptop", "smart speaker", "drone", "smartwatch", "turntable", "studio monitor", "VR headset", "tablet", "wireless earbuds", "portable speaker", "gaming console", "e-reader", "mechanical keyboard", "monitor", "soundbar", "projector", "robot vacuum"],
    },
    "travel": {
        "name": "Luxury Travel & Hospitality",
        "personnage": 2000, "produit": 1000,
        "brands": ["Aman Resorts", "Four Seasons", "Ritz-Carlton", "Emirates First Class", "Singapore Airlines Suites", "Belmond", "Mandarin Oriental", "Six Senses", "One&Only", "Rosewood", "Park Hyatt", "Waldorf Astoria", "St. Regis", "Peninsula Hotels", "Bulgari Hotels", "Cheval Blanc", "Raffles", "Banyan Tree", "Soneva", "Oberoi Hotels"],
        "products": ["luxury suite", "infinity pool", "private jet interior", "yacht deck", "spa treatment room", "rooftop terrace", "beachfront villa", "mountain lodge", "champagne lounge", "first class cabin", "overwater bungalow", "private island", "helicopter transfer", "safari lodge", "ice hotel suite", "treehouse villa", "underwater restaurant", "desert camp", "penthouse suite", "private beach cabana"],
    },
    "real_estate": {
        "name": "Luxury Real Estate",
        "personnage": 1500, "produit": 1000,
        "brands": ["Sotheby's International Realty", "Christie's Real Estate", "Knight Frank", "Engel & Völkers", "Barnes International", "Compass Luxury", "Douglas Elliman", "Coldwell Banker Global Luxury", "Savills", "JLL Luxury", "Beauchamp Estates", "Strutt & Parker", "The Agency", "Hilton & Hyland", "Brown Harris Stevens", "Corcoran", "Nest Seekers", "Aaron Kirman Group", "Halstead", "Eklund Gomes"],
        "products": ["penthouse interior", "villa exterior", "swimming pool", "rooftop terrace", "gourmet kitchen", "master suite", "wine cellar", "home cinema", "garden landscape", "marble bathroom", "walk-in closet", "library study", "garage collection", "entrance hall", "dining room", "outdoor kitchen", "infinity edge pool", "courtyard", "glass staircase", "smart home system"],
    },
    "home_design": {
        "name": "Premium Home & Design",
        "personnage": 1000, "produit": 1000,
        "brands": ["Roche Bobois", "B&B Italia", "Poltrona Frau", "Minotti", "Cassina", "Flos", "Artemide", "Louis Poulsen", "Tom Dixon", "Moooi", "Hermès Maison", "Ralph Lauren Home", "Ligne Roset", "Knoll", "Fritz Hansen", "Vitra", "Baccarat", "Lalique", "Christofle", "Bernardaud"],
        "products": ["designer sofa", "pendant lamp", "dining table", "armchair", "crystal vase", "silk cushion", "designer rug", "bookshelf", "coffee table", "floor lamp", "ceramic bowl", "wall mirror", "side table", "desk chair", "console table", "candle holder", "tableware set", "wine glass set", "blanket throw", "sculpture"],
    },
}

# ═══════════════════════════════════════════════════════════
# PROMPTS
# ═══════════════════════════════════════════════════════════

SYSTEM_PERSONNAGE = """You are a world-class advertising creative director. Generate a REALISTIC ad scenario for a high-end brand featuring a human model. Decompose into scenes.

Return JSON:
{"brand":"","industry":"","product":"","campaign_name":"","target_audience":"","mood":"","duration_total_seconds":30,"mode":"personnage_et_produit","scenario_text":"5-15 lines","scenes":[{"index":1,"scene_type":"personnage|produit|transition","description":"French","prompt_image":"DETAILED English, lens, lighting, color, composition, 3-5 sentences","prompt_video":"English animation, 2-3 sentences","duration_seconds":4.0,"camera_movement":"static|pan_left|pan_right|zoom_in|zoom_out|tracking|orbit|crane_up|dolly_in|steadicam","transition":"fade|cut|dissolve|wipe|match_cut","needs_mannequin":true,"needs_decor_ref":false,"archetype":"product_hero|lifestyle|portrait|product_interaction|establishing|macro_detail|motion_action|endframe|silhouette|pov|hands_only|reveal|slow_motion"}]}

3-8 scenes, mix types, ALWAYS end with endframe. Each unique. Vary everything."""

SYSTEM_PRODUIT = """You are a world-class advertising creative director specializing in product photography. Generate a product-only ad scenario (NO human). Focus on beauty, craftsmanship, materials.

Return JSON:
{"brand":"","industry":"","product":"","campaign_name":"","target_audience":"","mood":"","duration_total_seconds":20,"mode":"produit_uniquement","scenario_text":"3-10 lines","scenes":[{"index":1,"scene_type":"produit|transition","description":"French","prompt_image":"DETAILED English, macro lens, studio lighting, textures, 3-5 sentences","prompt_video":"English animation, rotation, orbit, 2-3 sentences","duration_seconds":3.0,"camera_movement":"static|orbit|zoom_in|zoom_out|pan_left|dolly_in|crane_down","transition":"fade|cut|dissolve|wipe","needs_mannequin":false,"needs_decor_ref":true,"archetype":"product_hero|macro_detail|reveal|ingredient|endframe|slow_motion|reflection"}]}

3-6 scenes, NO humans, texture focus, ALWAYS end with endframe. Each unique."""

SETTINGS = [
    "luxurious indoor with marble and gold", "Mediterranean villa outdoor",
    "minimalist white studio", "urban cityscape golden hour",
    "natural landscape dramatic sky", "architectural landmark",
    "intimate close-up shallow DOF", "cinematic wide epic",
    "evening warm practicals", "golden hour backlit",
    "rainy reflections", "snowy winter", "tropical paradise",
    "industrial loft exposed brick", "Japanese zen garden",
    "Parisian apartment", "desert dunes sunset",
    "rooftop city blue hour", "countryside road vintage",
    "backstage fashion show",
]

MANNEQUINS = [
    "European woman 25-30 elegant brown hair",
    "Asian woman 22-28 graceful black hair",
    "Black woman 25-35 powerful natural hair",
    "European man 28-35 sharp dark hair",
    "Latino man 25-32 charismatic curly hair",
    "Mixed-race woman 22-28 radiant wavy hair",
    "Middle-Eastern woman 25-30 regal dark eyes",
    "Scandinavian man 30-38 refined blonde hair",
    "South Asian woman 24-30 elegant long dark hair",
    "East Asian man 26-34 contemporary styled hair",
    "African man 28-36 commanding shaved head",
    "Brazilian woman 23-29 confident flowing hair",
    "Italian woman 27-33 classic Mediterranean beauty",
    "Korean woman 22-28 delicate porcelain skin",
    "British man 32-40 understated groomed beard",
]

DURATIONS = ["10s", "15s", "20s", "30s", "45s", "60s"]
SEASONS = ["Spring/Summer", "Fall/Winter", "Holiday", "Resort/Cruise", "Evergreen"]


# ═══════════════════════════════════════════════════════════
# GÉNÉRATION
# ═══════════════════════════════════════════════════════════

def load_progress():
    if PROGRESS_FILE.exists():
        return json.loads(PROGRESS_FILE.read_text())
    return {"completed": 0, "errors": 0, "done_ids": []}


def save_progress(progress):
    with open(PROGRESS_FILE, "w") as f:
        json.dump(progress, f)


def generate_one(industry_key, industry, brand, product, idx, is_personnage, progress):
    """Génère un seul scénario via appel direct."""
    type_str = "perso" if is_personnage else "prod"
    custom_id = f"{industry_key}_{type_str}_{idx:05d}"

    # Skip si déjà fait
    if custom_id in progress["done_ids"]:
        return None

    setting = SETTINGS[idx % len(SETTINGS)]
    duration = DURATIONS[idx % len(DURATIONS)]
    season = SEASONS[idx % len(SEASONS)]

    user_msg = f"Create a {industry_key} ad for {brand} {product}. Setting: {setting}. Format: {duration}. Season: {season}."
    if is_personnage:
        mannequin = MANNEQUINS[idx % len(MANNEQUINS)]
        user_msg += f" Model: {mannequin}."
    user_msg += " Make it unique and cinematic."

    system = SYSTEM_PERSONNAGE if is_personnage else SYSTEM_PRODUIT

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0.9,
            max_tokens=2000 if is_personnage else 1500,
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user_msg},
            ],
        )

        content = response.choices[0].message.content
        ad = json.loads(content)
        ad["_custom_id"] = custom_id

        # Sauvegarder
        type_dir = "personnage" if is_personnage else "produit"
        output_dir = BASE_DIR / industry_key / type_dir
        output_dir.mkdir(parents=True, exist_ok=True)

        with open(output_dir / f"{custom_id}.json", "w", encoding="utf-8") as f:
            json.dump(ad, f, indent=2, ensure_ascii=False)

        time.sleep(1)  # pause pour éviter rate limit
        return custom_id

    except Exception as e:
        return f"ERROR:{custom_id}:{e}"


def run():
    """Lance la génération de tous les scénarios."""
    progress = load_progress()

    # Construire la liste de toutes les tâches
    tasks = []
    for industry_key, industry in INDUSTRIES.items():
        for i in range(industry["personnage"]):
            brand = industry["brands"][i % len(industry["brands"])]
            product = industry["products"][i % len(industry["products"])]
            tasks.append((industry_key, industry, brand, product, i, True))

        for i in range(industry["produit"]):
            brand = industry["brands"][i % len(industry["brands"])]
            product = industry["products"][i % len(industry["products"])]
            tasks.append((industry_key, industry, brand, product, i, False))

    total = len(tasks)
    already_done = len(progress["done_ids"])
    print(f"📊 Total : {total} scénarios")
    print(f"   ✅ Déjà fait : {already_done}")
    print(f"   ⏳ Restants  : {total - already_done}")
    print(f"   💰 Coût estimé restant : ~${(total - already_done) * 0.0006:.2f}")
    print(f"\n🚀 Lancement avec 5 workers parallèles...\n")

    batch_size = 100  # Sauvegarder la progression tous les 100
    count = already_done
    errors = progress["errors"]

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        for batch_start in range(0, len(tasks), batch_size):
            batch = tasks[batch_start:batch_start + batch_size]

            futures = {}
            for task_args in batch:
                industry_key, industry, brand, product, idx, is_perso = task_args
                type_str = "perso" if is_perso else "prod"
                custom_id = f"{industry_key}_{type_str}_{idx:05d}"

                if custom_id in progress["done_ids"]:
                    continue

                future = executor.submit(generate_one, *task_args, progress)
                futures[future] = custom_id

            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                if result is None:
                    continue  # skip
                elif result.startswith("ERROR:"):
                    errors += 1
                    if errors % 10 == 0:
                        print(f"   ⚠️  {errors} erreurs au total")
                    # Rate limit — pause
                    if "rate_limit" in result.lower() or "429" in result:
                        print(f"   ⏸️  Rate limit — pause 30s...")
                        time.sleep(30)
                else:
                    count += 1
                    progress["done_ids"].append(result)
                    progress["completed"] = count
                    progress["errors"] = errors

                    if count % 50 == 0:
                        pct = count / total * 100
                        industry = result.split("_")[0]
                        print(f"   📊 {count}/{total} ({pct:.1f}%) — dernier: {industry}")

            # Sauvegarder progression
            save_progress(progress)

    # Stats finales
    print(f"\n{'='*60}")
    print(f"🎉 TERMINÉ")
    print(f"   Total générés : {count}")
    print(f"   Erreurs       : {errors}")
    print(f"{'='*60}")

    # Stats par industrie
    print(f"\n   Par industrie :")
    for ik in INDUSTRIES:
        pd = BASE_DIR / ik / "personnage"
        prd = BASE_DIR / ik / "produit"
        pc = len(list(pd.glob("*.json"))) if pd.exists() else 0
        prc = len(list(prd.glob("*.json"))) if prd.exists() else 0
        target = INDUSTRIES[ik]["personnage"] + INDUSTRIES[ik]["produit"]
        print(f"      {ik:<20} : {pc+prc:>5}/{target} │ {pc} perso + {prc} prod")


def status():
    """Affiche la progression."""
    progress = load_progress()
    total = sum(i["personnage"] + i["produit"] for i in INDUSTRIES.values())
    done = len(progress["done_ids"])
    print(f"\n📊 PROGRESSION : {done}/{total} ({done/total*100:.1f}%)")
    print(f"   Erreurs : {progress['errors']}\n")

    for ik in INDUSTRIES:
        pd = BASE_DIR / ik / "personnage"
        prd = BASE_DIR / ik / "produit"
        pc = len(list(pd.glob("*.json"))) if pd.exists() else 0
        prc = len(list(prd.glob("*.json"))) if prd.exists() else 0
        target = INDUSTRIES[ik]["personnage"] + INDUSTRIES[ik]["produit"]
        pct = (pc + prc) / target * 100 if target > 0 else 0
        bar = "█" * int(pct / 5) + "░" * (20 - int(pct / 5))
        print(f"   {ik:<20} {bar} {pc+prc:>5}/{target} ({pct:.0f}%)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AdGenAI — 50k scénarios (appels directs)")
    parser.add_argument("--run", action="store_true", help="Lancer la génération")
    parser.add_argument("--status", action="store_true", help="Voir la progression")
    args = parser.parse_args()

    if args.run:
        run()
    elif args.status:
        status()
    else:
        parser.print_help()
        print("\n💡 Lancez : python3 generate_50k_direct.py --run")