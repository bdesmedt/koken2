import json
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional
import streamlit as st

DATA_FILE = Path(__file__).parent.parent / "data.json"

DEFAULT_DAYS = ["Maandag", "Dinsdag", "Donderdag", "Vrijdag"]

AVATARS = [
    "👨‍🍳", "👩‍🍳", "🧑‍🍳", "🍕", "🍔", "🌮", "🍣", "🍜",
    "🥘", "🍝", "🥗", "🍲", "🧆", "🥙", "🍛", "🫕",
    "🦊", "🐻", "🐼", "🐨", "🦁", "🐯", "🐸", "🐵",
]

DIETARY_OPTIONS = [
    "Vegetarisch", "Veganistisch", "Glutenvrij", "Lactosevrij",
    "Notenvrij", "Halal", "Kosher", "Pescotarisch",
    "Keto", "Low-carb", "Suikervrij",
]

CUISINE_TAGS = [
    "Italiaans", "Aziatisch", "Mexicaans", "Nederlands", "Frans",
    "Indiaas", "Grieks", "Japans", "Thais", "Turks", "Amerikaans",
    "Midden-Oosters", "Afrikaans", "Koreaans", "Vietnamees",
]

MEAL_TAGS = [
    "Snel (<30 min)", "Comfort food", "Gezond", "BBQ", "Soep",
    "Salade", "Pasta", "Rijst", "Aardappel", "Vis", "Vlees",
    "Ovenschotel", "Eenpansgerecht", "Feestelijk", "Budget",
    "Seizoensgebonden", "Streetfood", "Ontbijt", "Brunch",
]

DIFFICULTY_LEVELS = {
    "easy": {"label": "Makkelijk", "icon": "🟢", "points": 5},
    "medium": {"label": "Gemiddeld", "icon": "🟡", "points": 10},
    "hard": {"label": "Moeilijk", "icon": "🔴", "points": 20},
}


def _gen_id() -> str:
    return uuid.uuid4().hex[:12]


def _now() -> str:
    return datetime.now().isoformat()


class DataManager:
    """Central data management for the kookrooster app."""

    def __init__(self):
        self._data = None

    @property
    def data(self) -> dict:
        if self._data is None:
            self._data = self._load()
        return self._data

    def _load(self) -> dict:
        if DATA_FILE.exists():
            with open(DATA_FILE, "r") as f:
                raw = json.load(f)
            return self._migrate(raw)
        return self._default_data()

    def save(self):
        with open(DATA_FILE, "w") as f:
            json.dump(self.data, f, indent=2, ensure_ascii=False)

    def reload(self):
        self._data = self._load()

    # ── Migration from old format ──────────────────────────────────────
    def _migrate(self, raw: dict) -> dict:
        default = self._default_data()

        # Ensure all top-level keys exist
        for key, val in default.items():
            if key not in raw:
                raw[key] = val

        # Ensure group sub-keys
        for key, val in default["group"].items():
            if key not in raw["group"]:
                raw["group"][key] = val

        # Migrate old flat format (koppels list -> members dict)
        if "koppels" in raw and raw["koppels"] and not raw.get("members"):
            for name in raw["koppels"]:
                mid = _gen_id()
                raw["members"][mid] = self._new_member(name)
            # Migrate rooster entries
            name_to_id = {m["name"]: mid for mid, m in raw["members"].items()}
            new_rooster = {}
            for slot_key, info in raw.get("rooster", {}).items():
                if isinstance(info, str):
                    koppel_name = info
                    gerecht = ""
                elif isinstance(info, dict):
                    koppel_name = info.get("koppel", "")
                    gerecht = info.get("gerecht", "")
                else:
                    continue
                mid = name_to_id.get(koppel_name, "")
                if mid:
                    new_rooster[slot_key] = self._new_slot(mid, gerecht)
            raw["rooster"] = new_rooster

        # Migrate old cooking_days/start_date to group
        if "cooking_days" in raw and raw["cooking_days"]:
            raw["group"]["cooking_days"] = raw["cooking_days"]
        if "start_date" in raw and raw["start_date"]:
            raw["group"]["start_date"] = raw["start_date"]

        # Clean up old keys
        for old_key in ["koppels", "cooking_days", "start_date", "gerechten_historie"]:
            raw.pop(old_key, None)

        return raw

    def _default_data(self) -> dict:
        return {
            "group": {
                "name": "Kookrooster Vriendengroep",
                "avatar": "🍳",
                "created_date": _now(),
                "cooking_days": DEFAULT_DAYS,
                "start_date": datetime.now().strftime("%Y-%m-%d"),
                "num_weeks": 12,
                "max_budget": 0,
                "rsvp_deadline_hours": 24,
                "swap_approval_required": True,
                "default_portions": 4,
            },
            "members": {},
            "rooster": {},
            "recipes": {},
            "expenses": [],
            "swap_requests": [],
            "absences": {},
            "challenges": [],
            "messages": [],
            "activity_log": [],
            "settlements": [],
        }

    # ── Member Management ──────────────────────────────────────────────
    def _new_member(self, name: str, avatar: str = "👨‍🍳", role: str = "member") -> dict:
        return {
            "name": name,
            "avatar": avatar,
            "role": role,
            "dietary_restrictions": [],
            "allergies": [],
            "joined_date": _now(),
            "points": 0,
            "achievements": [],
            "streak": 0,
            "best_streak": 0,
            "bio": "",
            "favorite_cuisine": "",
        }

    def add_member(self, name: str, avatar: str = "👨‍🍳", role: str = "member") -> str:
        mid = _gen_id()
        self.data["members"][mid] = self._new_member(name, avatar, role)
        if not any(m["role"] == "admin" for m in self.data["members"].values()):
            self.data["members"][mid]["role"] = "admin"
        self.log_activity(mid, "joined", f"{name} is lid geworden")
        self.save()
        return mid

    def remove_member(self, member_id: str):
        name = self.get_member_name(member_id)
        self.data["members"].pop(member_id, None)
        # Clean up rooster
        self.data["rooster"] = {
            k: v for k, v in self.data["rooster"].items()
            if v.get("member_id") != member_id
        }
        self.data["absences"].pop(member_id, None)
        self.log_activity(None, "member_removed", f"{name} is verwijderd")
        self.save()

    def get_member_name(self, member_id: str) -> str:
        member = self.data["members"].get(member_id, {})
        return member.get("name", "Onbekend")

    def get_member_avatar(self, member_id: str) -> str:
        member = self.data["members"].get(member_id, {})
        return member.get("avatar", "👤")

    def get_member_display(self, member_id: str) -> str:
        return f"{self.get_member_avatar(member_id)} {self.get_member_name(member_id)}"

    def member_id_by_name(self, name: str) -> Optional[str]:
        for mid, m in self.data["members"].items():
            if m["name"] == name:
                return mid
        return None

    def get_members_list(self) -> list:
        return [
            {"id": mid, **m}
            for mid, m in sorted(
                self.data["members"].items(),
                key=lambda x: x[1]["name"]
            )
        ]

    # ── Roster / Slot Management ───────────────────────────────────────
    def _new_slot(self, member_id: str, gerecht: str = "") -> dict:
        return {
            "member_id": member_id,
            "gerecht": gerecht,
            "gerecht_id": "",
            "status": "planned",
            "attendees": list(self.data["members"].keys()),
            "portions": self.data["group"]["default_portions"],
            "photos": [],
            "reactions": {},
            "comments": [],
            "rating_avg": 0,
            "ratings": {},
            "cost": 0,
            "paid_by": "",
            "created_at": _now(),
        }

    def sign_up(self, slot_key: str, member_id: str):
        self.data["rooster"][slot_key] = self._new_slot(member_id)
        self.log_activity(member_id, "signed_up", f"Ingeschreven voor {slot_key}")
        self.save()

    def remove_signup(self, slot_key: str):
        slot = self.data["rooster"].pop(slot_key, None)
        if slot:
            self.log_activity(slot["member_id"], "cancelled", f"Afgemeld voor {slot_key}")
        self.save()

    def set_gerecht(self, slot_key: str, gerecht: str):
        if slot_key in self.data["rooster"]:
            self.data["rooster"][slot_key]["gerecht"] = gerecht
            self.save()

    def complete_slot(self, slot_key: str):
        if slot_key in self.data["rooster"]:
            slot = self.data["rooster"][slot_key]
            slot["status"] = "completed"
            mid = slot["member_id"]
            # Award points
            self.add_points(mid, 10, "Maaltijd gekookt")
            # Update streak
            member = self.data["members"].get(mid, {})
            member["streak"] = member.get("streak", 0) + 1
            if member["streak"] > member.get("best_streak", 0):
                member["best_streak"] = member["streak"]
            self.log_activity(mid, "cooked", f"Heeft gekookt: {slot.get('gerecht', '?')}")
            self.save()

    # ── Rating ─────────────────────────────────────────────────────────
    def rate_slot(self, slot_key: str, member_id: str, rating: int):
        slot = self.data["rooster"].get(slot_key)
        if slot:
            slot["ratings"][member_id] = rating
            ratings = list(slot["ratings"].values())
            slot["rating_avg"] = sum(ratings) / len(ratings)
            self.save()

    # ── Reactions & Comments ───────────────────────────────────────────
    def add_reaction(self, slot_key: str, member_id: str, emoji: str):
        slot = self.data["rooster"].get(slot_key)
        if slot:
            slot["reactions"][member_id] = emoji
            self.save()

    def add_comment(self, slot_key: str, member_id: str, text: str):
        slot = self.data["rooster"].get(slot_key)
        if slot:
            slot["comments"].append({
                "id": _gen_id(),
                "member_id": member_id,
                "text": text,
                "timestamp": _now(),
            })
            self.save()

    # ── RSVP / Attendance ──────────────────────────────────────────────
    def rsvp(self, slot_key: str, member_id: str, attending: bool):
        slot = self.data["rooster"].get(slot_key)
        if slot:
            if attending and member_id not in slot["attendees"]:
                slot["attendees"].append(member_id)
            elif not attending and member_id in slot["attendees"]:
                slot["attendees"].remove(member_id)
            slot["portions"] = len(slot["attendees"])
            self.save()

    # ── Absence Management ─────────────────────────────────────────────
    def set_absence(self, member_id: str, slot_key: str, absent: bool):
        if member_id not in self.data["absences"]:
            self.data["absences"][member_id] = []
        if absent and slot_key not in self.data["absences"][member_id]:
            self.data["absences"][member_id].append(slot_key)
        elif not absent and slot_key in self.data["absences"][member_id]:
            self.data["absences"][member_id].remove(slot_key)
        self.save()

    def is_absent(self, member_id: str, slot_key: str) -> bool:
        return slot_key in self.data["absences"].get(member_id, [])

    # ── Swap Requests ──────────────────────────────────────────────────
    def request_swap(self, from_member: str, to_member: str, slot_key: str) -> str:
        swap_id = _gen_id()
        self.data["swap_requests"].append({
            "id": swap_id,
            "from_member": from_member,
            "to_member": to_member,
            "slot_key": slot_key,
            "status": "pending",
            "timestamp": _now(),
        })
        self.log_activity(from_member, "swap_requested",
                          f"Ruilverzoek naar {self.get_member_name(to_member)} voor {slot_key}")
        self.save()
        return swap_id

    def handle_swap(self, swap_id: str, approved: bool):
        for swap in self.data["swap_requests"]:
            if swap["id"] == swap_id:
                if approved:
                    swap["status"] = "approved"
                    slot = self.data["rooster"].get(swap["slot_key"])
                    if slot:
                        slot["member_id"] = swap["to_member"]
                    self.log_activity(swap["to_member"], "swap_approved",
                                      f"Ruil goedgekeurd voor {swap['slot_key']}")
                else:
                    swap["status"] = "rejected"
                break
        self.save()

    def get_pending_swaps(self, member_id: str) -> list:
        return [
            s for s in self.data["swap_requests"]
            if s["to_member"] == member_id and s["status"] == "pending"
        ]

    # ── Recipe Management ──────────────────────────────────────────────
    def add_recipe(self, name: str, created_by: str, **kwargs) -> str:
        rid = _gen_id()
        self.data["recipes"][rid] = {
            "name": name,
            "description": kwargs.get("description", ""),
            "ingredients": kwargs.get("ingredients", []),
            "instructions": kwargs.get("instructions", []),
            "prep_time": kwargs.get("prep_time", 0),
            "cook_time": kwargs.get("cook_time", 0),
            "difficulty": kwargs.get("difficulty", "medium"),
            "tags": kwargs.get("tags", []),
            "dietary": kwargs.get("dietary", []),
            "servings": kwargs.get("servings", 4),
            "photos": [],
            "created_by": created_by,
            "created_at": _now(),
            "avg_rating": 0,
            "ratings": {},
            "times_cooked": 0,
            "favorite_by": [],
        }
        self.add_points(created_by, 5, "Recept toegevoegd")
        self.log_activity(created_by, "recipe_added", f"Recept toegevoegd: {name}")
        self.save()
        return rid

    def rate_recipe(self, recipe_id: str, member_id: str, rating: int):
        recipe = self.data["recipes"].get(recipe_id)
        if recipe:
            recipe["ratings"][member_id] = rating
            ratings = list(recipe["ratings"].values())
            recipe["avg_rating"] = sum(ratings) / len(ratings)
            self.save()

    def toggle_favorite(self, recipe_id: str, member_id: str):
        recipe = self.data["recipes"].get(recipe_id)
        if recipe:
            if member_id in recipe["favorite_by"]:
                recipe["favorite_by"].remove(member_id)
            else:
                recipe["favorite_by"].append(member_id)
            self.save()

    def get_recipe_suggestions(self, member_id: str = None) -> list:
        """Suggest recipes based on popularity and variety."""
        recipes = list(self.data["recipes"].values())
        if not recipes:
            return []
        # Sort by rating and times cooked (prefer highly rated, less cooked)
        scored = []
        for rid, r in self.data["recipes"].items():
            score = r.get("avg_rating", 0) * 2 - r.get("times_cooked", 0) * 0.5
            scored.append((rid, r, score))
        scored.sort(key=lambda x: x[2], reverse=True)
        return [(rid, r) for rid, r, _ in scored[:5]]

    # ── Expense Management ─────────────────────────────────────────────
    def add_expense(self, slot_key: str, amount: float, paid_by: str,
                    description: str = "", split_between: list = None) -> str:
        eid = _gen_id()
        if split_between is None:
            slot = self.data["rooster"].get(slot_key, {})
            split_between = slot.get("attendees", list(self.data["members"].keys()))
        self.data["expenses"].append({
            "id": eid,
            "slot_key": slot_key,
            "amount": amount,
            "paid_by": paid_by,
            "split_between": split_between,
            "description": description,
            "date": _now(),
            "settled": False,
        })
        self.log_activity(paid_by, "expense_added",
                          f"Uitgave: {description or slot_key} - €{amount:.2f}")
        self.save()
        return eid

    def calculate_balances(self) -> dict:
        """Calculate who owes whom."""
        balances = {mid: 0.0 for mid in self.data["members"]}
        for exp in self.data["expenses"]:
            if exp.get("settled"):
                continue
            amount = exp["amount"]
            paid_by = exp["paid_by"]
            split = exp.get("split_between", [])
            if not split or paid_by not in balances:
                continue
            per_person = amount / len(split)
            balances[paid_by] += amount
            for mid in split:
                if mid in balances:
                    balances[mid] -= per_person
        return balances

    def settle_expense(self, expense_id: str):
        for exp in self.data["expenses"]:
            if exp["id"] == expense_id:
                exp["settled"] = True
                break
        self.save()

    # ── Chat / Messages ────────────────────────────────────────────────
    def send_message(self, member_id: str, text: str, slot_key: str = None):
        self.data["messages"].append({
            "id": _gen_id(),
            "member_id": member_id,
            "text": text,
            "timestamp": _now(),
            "slot_key": slot_key,
        })
        self.save()

    def get_messages(self, slot_key: str = None, limit: int = 50) -> list:
        msgs = [
            m for m in self.data["messages"]
            if m.get("slot_key") == slot_key
        ]
        return sorted(msgs, key=lambda x: x["timestamp"])[-limit:]

    # ── Challenge Management ───────────────────────────────────────────
    def add_challenge(self, name: str, description: str, tag: str,
                      start_date: str, end_date: str) -> str:
        cid = _gen_id()
        self.data["challenges"].append({
            "id": cid,
            "name": name,
            "description": description,
            "tag": tag,
            "start_date": start_date,
            "end_date": end_date,
            "participants": [],
            "completed_by": [],
            "created_at": _now(),
        })
        self.save()
        return cid

    def join_challenge(self, challenge_id: str, member_id: str):
        for ch in self.data["challenges"]:
            if ch["id"] == challenge_id and member_id not in ch["participants"]:
                ch["participants"].append(member_id)
                self.save()
                break

    # ── Points & Activity ──────────────────────────────────────────────
    def add_points(self, member_id: str, points: int, reason: str = ""):
        member = self.data["members"].get(member_id)
        if member:
            member["points"] = member.get("points", 0) + points

    def log_activity(self, member_id: Optional[str], action: str, details: str):
        self.data["activity_log"].append({
            "timestamp": _now(),
            "member_id": member_id,
            "action": action,
            "details": details,
        })
        # Keep last 500 entries
        if len(self.data["activity_log"]) > 500:
            self.data["activity_log"] = self.data["activity_log"][-500:]

    # ── Week / Calendar Helpers ────────────────────────────────────────
    def get_weeks(self, num_weeks: int = None) -> list:
        start_str = self.data["group"]["start_date"]
        if num_weeks is None:
            num_weeks = self.data["group"]["num_weeks"]
        start = datetime.strptime(start_str, "%Y-%m-%d")
        start = start - timedelta(days=start.weekday())  # Adjust to Monday
        weeks = []
        for i in range(num_weeks):
            week_start = start + timedelta(weeks=i)
            iso = week_start.isocalendar()
            weeks.append({
                "label": f"Week {iso[1]}",
                "key": f"{iso[0]}-W{iso[1]:02d}",
                "start": week_start,
                "num": iso[1],
            })
        return weeks

    def get_cooking_days(self) -> list:
        return self.data["group"]["cooking_days"]

    def get_day_date(self, week: dict, day: str) -> datetime:
        all_days = ["Maandag", "Dinsdag", "Woensdag", "Donderdag", "Vrijdag", "Zaterdag", "Zondag"]
        day_idx = all_days.index(day) if day in all_days else 0
        return week["start"] + timedelta(days=day_idx)

    # ── Statistics Helpers ─────────────────────────────────────────────
    def count_cooking_times(self) -> dict:
        counts = {mid: 0 for mid in self.data["members"]}
        for slot in self.data["rooster"].values():
            mid = slot.get("member_id", "")
            if mid in counts:
                counts[mid] += 1
        return counts

    def count_completed(self) -> dict:
        counts = {mid: 0 for mid in self.data["members"]}
        for slot in self.data["rooster"].values():
            if slot.get("status") == "completed":
                mid = slot.get("member_id", "")
                if mid in counts:
                    counts[mid] += 1
        return counts

    def get_all_gerechten(self) -> list:
        return [
            slot["gerecht"].lower().strip()
            for slot in self.data["rooster"].values()
            if slot.get("gerecht")
        ]

    def get_total_slots(self) -> int:
        return len(self.get_cooking_days()) * self.data["group"]["num_weeks"]

    def get_cuisine_distribution(self) -> dict:
        dist = {}
        for recipe in self.data["recipes"].values():
            for tag in recipe.get("tags", []):
                if tag in CUISINE_TAGS:
                    dist[tag] = dist.get(tag, 0) + 1
        return dist

    def get_top_rated_recipes(self, limit: int = 5) -> list:
        rated = [
            (rid, r) for rid, r in self.data["recipes"].items()
            if r.get("avg_rating", 0) > 0
        ]
        rated.sort(key=lambda x: x[1]["avg_rating"], reverse=True)
        return rated[:limit]

    def get_monthly_stats(self) -> dict:
        stats = {}
        for slot_key, slot in self.data["rooster"].items():
            if slot.get("status") == "completed":
                try:
                    parts = slot_key.split("-")
                    year = parts[0]
                    week = parts[1]
                    month_key = f"{year}-{week}"
                    if month_key not in stats:
                        stats[month_key] = {"meals": 0, "total_cost": 0, "avg_rating": []}
                    stats[month_key]["meals"] += 1
                    if slot.get("cost"):
                        stats[month_key]["total_cost"] += slot["cost"]
                    if slot.get("rating_avg"):
                        stats[month_key]["avg_rating"].append(slot["rating_avg"])
                except (IndexError, ValueError):
                    pass
        return stats

    # ── Auto-rotation ──────────────────────────────────────────────────
    def suggest_fair_assignment(self, slot_key: str) -> Optional[str]:
        """Suggest the member who should cook next based on fairness."""
        counts = self.count_cooking_times()
        if not counts:
            return None
        # Filter out absent members
        available = {
            mid: count for mid, count in counts.items()
            if not self.is_absent(mid, slot_key)
        }
        if not available:
            return None
        # Return the one who cooked the least
        return min(available, key=available.get)

    def auto_fill_roster(self):
        """Auto-fill empty roster slots fairly."""
        weeks = self.get_weeks()
        cooking_days = self.get_cooking_days()
        for week in weeks:
            for day in cooking_days:
                slot_key = f"{week['key']}-{day}"
                if slot_key not in self.data["rooster"]:
                    suggestion = self.suggest_fair_assignment(slot_key)
                    if suggestion:
                        self.sign_up(slot_key, suggestion)


@st.cache_resource
def get_data_manager() -> DataManager:
    return DataManager()
