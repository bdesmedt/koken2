from datetime import datetime, timedelta

ALL_DAYS = ["Maandag", "Dinsdag", "Woensdag", "Donderdag", "Vrijdag", "Zaterdag", "Zondag"]
ALL_DAYS_SHORT = ["Ma", "Di", "Wo", "Do", "Vr", "Za", "Zo"]

DUTCH_MONTHS = {
    1: "januari", 2: "februari", 3: "maart", 4: "april",
    5: "mei", 6: "juni", 7: "juli", 8: "augustus",
    9: "september", 10: "oktober", 11: "november", 12: "december",
}


def format_date_dutch(dt: datetime) -> str:
    return f"{dt.day} {DUTCH_MONTHS[dt.month]}"


def format_date_full(dt: datetime) -> str:
    day_name = ALL_DAYS[dt.weekday()]
    return f"{day_name} {dt.day} {DUTCH_MONTHS[dt.month]} {dt.year}"


def time_ago(timestamp_str: str) -> str:
    try:
        ts = datetime.fromisoformat(timestamp_str)
    except (ValueError, TypeError):
        return ""
    diff = datetime.now() - ts
    seconds = diff.total_seconds()
    if seconds < 60:
        return "zojuist"
    elif seconds < 3600:
        m = int(seconds // 60)
        return f"{m} min geleden"
    elif seconds < 86400:
        h = int(seconds // 3600)
        return f"{h} uur geleden"
    elif seconds < 604800:
        d = int(seconds // 86400)
        return f"{d} dag{'en' if d > 1 else ''} geleden"
    else:
        w = int(seconds // 604800)
        return f"{w} {'weken' if w > 1 else 'week'} geleden"


def star_rating(rating: float, max_stars: int = 5) -> str:
    full = int(rating)
    half = 1 if rating - full >= 0.5 else 0
    empty = max_stars - full - half
    return "★" * full + "½" * half + "☆" * empty


def difficulty_display(level: str) -> str:
    mapping = {
        "easy": "🟢 Makkelijk",
        "medium": "🟡 Gemiddeld",
        "hard": "🔴 Moeilijk",
    }
    return mapping.get(level, "🟡 Gemiddeld")


def format_duration(minutes: int) -> str:
    if minutes < 60:
        return f"{minutes} min"
    hours = minutes // 60
    mins = minutes % 60
    if mins == 0:
        return f"{hours} uur"
    return f"{hours} uur {mins} min"


def parse_slot_key(slot_key: str) -> dict:
    """Parse a slot key like '2026-W06-Maandag' into components."""
    parts = slot_key.split("-")
    if len(parts) >= 3:
        return {
            "year": parts[0],
            "week": parts[1],
            "day": "-".join(parts[2:]),
        }
    return {"year": "", "week": "", "day": ""}


INGREDIENT_SUBSTITUTIONS = {
    "boter": ["margarine", "kokosolie", "olijfolie"],
    "melk": ["havermelk", "sojamelk", "amandelmelk", "kokosmelk"],
    "ei": ["lijnzaad + water", "appelmoes", "banaan", "aquafaba"],
    "bloem": ["amandelmeel", "kokosmeel", "havermeel", "rijstmeel"],
    "suiker": ["honing", "ahornsiroop", "stevia", "dadelsiroop"],
    "room": ["kokosroom", "cashewroom", "haverroom"],
    "kaas": ["gist vlokken", "cashew kaas", "tofu"],
    "kip": ["tofu", "tempeh", "seitan", "kikkererwten"],
    "gehakt": ["linzen", "bonen", "walnoten gehakt", "soja gehakt"],
    "rijst": ["quinoa", "couscous", "bulgur", "bloemkoolrijst"],
    "pasta": ["courgette noedels", "rijstnoedels", "glasnoedels"],
    "aardappel": ["zoete aardappel", "knolselderij", "bloemkool"],
    "slagroom": ["kokosslagroom", "cashewroom"],
    "paneermeel": ["havervlokken", "gemalen noten", "cornflakes"],
    "sojasaus": ["kokos aminos", "tamari", "worcestersaus"],
    "ui": ["prei", "sjalot", "lente-ui"],
    "knoflook": ["knoflookpoeder", "asafoetida"],
    "tomaat": ["rode paprika", "pompoen puree"],
    "spinazie": ["boerenkool", "snijbiet", "rucola"],
    "champignons": ["aubergine", "courgette", "tempeh"],
}

UNIT_CONVERSIONS = {
    "cups_to_ml": 236.588,
    "oz_to_g": 28.3495,
    "lb_to_kg": 0.453592,
    "inch_to_cm": 2.54,
    "fahrenheit_to_celsius": lambda f: (f - 32) * 5 / 9,
    "tbsp_to_ml": 14.787,
    "tsp_to_ml": 4.929,
    "gallon_to_l": 3.785,
}

QUICK_RECIPES = [
    {
        "name": "Pasta Aglio e Olio",
        "time": 20, "difficulty": "easy",
        "tags": ["Italiaans", "Pasta", "Snel (<30 min)", "Budget"],
        "ingredients": ["400g spaghetti", "6 tenen knoflook", "olijfolie", "chili vlokken", "peterselie", "parmezaan"],
        "instructions": ["Kook pasta al dente", "Bak gesneden knoflook in olijfolie", "Voeg chili vlokken toe", "Meng pasta door de olie", "Garneer met peterselie en parmezaan"],
    },
    {
        "name": "Shakshuka",
        "time": 25, "difficulty": "easy",
        "tags": ["Midden-Oosters", "Gezond", "Snel (<30 min)", "Vegetarisch"],
        "ingredients": ["1 blik tomaten", "4 eieren", "ui", "paprika", "knoflook", "komijn", "paprikapoeder"],
        "instructions": ["Bak ui en paprika", "Voeg knoflook en kruiden toe", "Voeg tomaten toe en laat inkoken", "Maak kuiltjes en breek eieren erin", "Dek af tot eieren gestold zijn"],
    },
    {
        "name": "Teriyaki Roerbak",
        "time": 20, "difficulty": "easy",
        "tags": ["Aziatisch", "Snel (<30 min)", "Rijst"],
        "ingredients": ["300g kip/tofu", "broccoli", "paprika", "wortel", "sojasaus", "honing", "gember", "rijst"],
        "instructions": ["Kook rijst", "Snijd groenten", "Bak kip/tofu", "Voeg groenten toe", "Meng teriyaki saus en giet erover"],
    },
    {
        "name": "Caprese Salade",
        "time": 10, "difficulty": "easy",
        "tags": ["Italiaans", "Salade", "Snel (<30 min)", "Vegetarisch", "Gezond"],
        "ingredients": ["tomaten", "mozzarella", "basilicum", "olijfolie", "balsamico", "peper en zout"],
        "instructions": ["Snijd tomaten en mozzarella in plakken", "Leg afwisselend op een bord", "Garneer met basilicum", "Besprenkel met olijfolie en balsamico"],
    },
    {
        "name": "Chili con Carne",
        "time": 45, "difficulty": "medium",
        "tags": ["Mexicaans", "Comfort food", "Eenpansgerecht"],
        "ingredients": ["500g gehakt", "blik kidneybonen", "blik tomaten", "ui", "paprika", "chilipoeder", "komijn", "rijst"],
        "instructions": ["Bak gehakt met ui", "Voeg paprika en kruiden toe", "Voeg tomaten en bonen toe", "Laat 30 min sudderen", "Serveer met rijst"],
    },
]
