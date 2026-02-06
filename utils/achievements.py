"""Achievement / Gamification engine for Kookrooster."""

ACHIEVEMENTS = {
    # ── Cooking milestones ─────────────────────────────────
    "first_cook": {
        "name": "Eerste Keer!",
        "icon": "🌟",
        "description": "Je eerste maaltijd gekookt",
        "category": "cooking",
        "tier": "bronze",
        "points": 10,
    },
    "cook_5": {
        "name": "Thuiskok",
        "icon": "👨‍🍳",
        "description": "5 maaltijden gekookt",
        "category": "cooking",
        "tier": "bronze",
        "points": 25,
    },
    "cook_10": {
        "name": "Master Chef",
        "icon": "🏆",
        "description": "10 maaltijden gekookt",
        "category": "cooking",
        "tier": "silver",
        "points": 50,
    },
    "cook_25": {
        "name": "Chef de Cuisine",
        "icon": "👑",
        "description": "25 maaltijden gekookt",
        "category": "cooking",
        "tier": "gold",
        "points": 100,
    },
    "cook_50": {
        "name": "Legende",
        "icon": "🔥",
        "description": "50 maaltijden gekookt",
        "category": "cooking",
        "tier": "gold",
        "points": 250,
    },
    # ── Recipe milestones ──────────────────────────────────
    "recipe_1": {
        "name": "Receptenschrijver",
        "icon": "📝",
        "description": "Eerste recept toegevoegd",
        "category": "recipes",
        "tier": "bronze",
        "points": 10,
    },
    "recipe_5": {
        "name": "Kookboek Auteur",
        "icon": "📖",
        "description": "5 recepten toegevoegd",
        "category": "recipes",
        "tier": "silver",
        "points": 30,
    },
    "recipe_10": {
        "name": "Culinair Expert",
        "icon": "📚",
        "description": "10 recepten toegevoegd",
        "category": "recipes",
        "tier": "gold",
        "points": 75,
    },
    # ── Rating milestones ──────────────────────────────────
    "five_star": {
        "name": "Vijf Sterren",
        "icon": "⭐",
        "description": "Een 5-sterren beoordeling ontvangen",
        "category": "ratings",
        "tier": "silver",
        "points": 30,
    },
    "avg_4plus": {
        "name": "Consistent Goed",
        "icon": "📊",
        "description": "Gemiddelde rating boven de 4",
        "category": "ratings",
        "tier": "gold",
        "points": 50,
    },
    "rate_10": {
        "name": "Criticus",
        "icon": "🎭",
        "description": "10 beoordelingen gegeven",
        "category": "ratings",
        "tier": "bronze",
        "points": 15,
    },
    # ── Variety milestones ─────────────────────────────────
    "adventurer": {
        "name": "Avonturier",
        "icon": "🗺️",
        "description": "5 verschillende keukens gekookt",
        "category": "variety",
        "tier": "silver",
        "points": 40,
    },
    "world_chef": {
        "name": "Wereldkok",
        "icon": "🌍",
        "description": "10 verschillende keukens gekookt",
        "category": "variety",
        "tier": "gold",
        "points": 100,
    },
    "veggie_hero": {
        "name": "Vegetarische Held",
        "icon": "🥬",
        "description": "5 vegetarische maaltijden gekookt",
        "category": "variety",
        "tier": "silver",
        "points": 35,
    },
    # ── Streak milestones ──────────────────────────────────
    "streak_3": {
        "name": "Op Dreef",
        "icon": "🔥",
        "description": "3 keer achter elkaar gekookt",
        "category": "streaks",
        "tier": "bronze",
        "points": 20,
    },
    "streak_5": {
        "name": "Onstopbaar",
        "icon": "💪",
        "description": "5 keer achter elkaar gekookt",
        "category": "streaks",
        "tier": "silver",
        "points": 40,
    },
    "streak_10": {
        "name": "IJzeren Wil",
        "icon": "⚡",
        "description": "10 keer achter elkaar gekookt",
        "category": "streaks",
        "tier": "gold",
        "points": 100,
    },
    # ── Social milestones ──────────────────────────────────
    "social_butterfly": {
        "name": "Sociaal Dier",
        "icon": "🦋",
        "description": "10 berichten gestuurd",
        "category": "social",
        "tier": "bronze",
        "points": 15,
    },
    "generous": {
        "name": "Vrijgevig",
        "icon": "🎁",
        "description": "Een kookbeurt geruild",
        "category": "social",
        "tier": "bronze",
        "points": 10,
    },
    # ── Speed milestones ───────────────────────────────────
    "speed_demon": {
        "name": "Speed Demon",
        "icon": "⚡",
        "description": "5 snelle gerechten (<30 min) gekookt",
        "category": "special",
        "tier": "silver",
        "points": 35,
    },
    "budget_master": {
        "name": "Budget Meester",
        "icon": "💰",
        "description": "5 budget-vriendelijke maaltijden gekookt",
        "category": "special",
        "tier": "silver",
        "points": 35,
    },
    # ── Challenge milestones ───────────────────────────────
    "challenge_1": {
        "name": "Uitdager",
        "icon": "🎯",
        "description": "Eerste challenge voltooid",
        "category": "challenges",
        "tier": "bronze",
        "points": 20,
    },
    "challenge_5": {
        "name": "Challenge Kampioen",
        "icon": "🏅",
        "description": "5 challenges voltooid",
        "category": "challenges",
        "tier": "gold",
        "points": 75,
    },
}


class AchievementEngine:
    """Check and award achievements."""

    def __init__(self, dm):
        self.dm = dm

    def check_all(self, member_id: str) -> list:
        """Check all achievements for a member, return newly earned ones."""
        member = self.dm.data["members"].get(member_id)
        if not member:
            return []

        earned = member.get("achievements", [])
        new_achievements = []

        # Cooking count
        cook_count = self._count_completed_for(member_id)
        cooking_milestones = {1: "first_cook", 5: "cook_5", 10: "cook_10", 25: "cook_25", 50: "cook_50"}
        for threshold, ach_id in cooking_milestones.items():
            if cook_count >= threshold and ach_id not in earned:
                new_achievements.append(ach_id)

        # Recipe count
        recipe_count = sum(
            1 for r in self.dm.data["recipes"].values()
            if r.get("created_by") == member_id
        )
        recipe_milestones = {1: "recipe_1", 5: "recipe_5", 10: "recipe_10"}
        for threshold, ach_id in recipe_milestones.items():
            if recipe_count >= threshold and ach_id not in earned:
                new_achievements.append(ach_id)

        # Five star rating
        for slot in self.dm.data["rooster"].values():
            if slot.get("member_id") == member_id:
                if any(r == 5 for r in slot.get("ratings", {}).values()):
                    if "five_star" not in earned:
                        new_achievements.append("five_star")
                        break

        # Average rating above 4
        all_ratings = []
        for slot in self.dm.data["rooster"].values():
            if slot.get("member_id") == member_id and slot.get("rating_avg", 0) > 0:
                all_ratings.append(slot["rating_avg"])
        if all_ratings and sum(all_ratings) / len(all_ratings) >= 4.0:
            if "avg_4plus" not in earned:
                new_achievements.append("avg_4plus")

        # Rating count (given by this member)
        rating_count = 0
        for slot in self.dm.data["rooster"].values():
            if member_id in slot.get("ratings", {}):
                rating_count += 1
        if rating_count >= 10 and "rate_10" not in earned:
            new_achievements.append("rate_10")

        # Cuisine variety
        cuisines = set()
        for slot in self.dm.data["rooster"].values():
            if slot.get("member_id") == member_id and slot.get("gerecht_id"):
                recipe = self.dm.data["recipes"].get(slot["gerecht_id"], {})
                for tag in recipe.get("tags", []):
                    from utils.data_manager import CUISINE_TAGS
                    if tag in CUISINE_TAGS:
                        cuisines.add(tag)
        if len(cuisines) >= 5 and "adventurer" not in earned:
            new_achievements.append("adventurer")
        if len(cuisines) >= 10 and "world_chef" not in earned:
            new_achievements.append("world_chef")

        # Streaks
        streak = member.get("best_streak", member.get("streak", 0))
        streak_milestones = {3: "streak_3", 5: "streak_5", 10: "streak_10"}
        for threshold, ach_id in streak_milestones.items():
            if streak >= threshold and ach_id not in earned:
                new_achievements.append(ach_id)

        # Message count
        msg_count = sum(
            1 for m in self.dm.data["messages"]
            if m.get("member_id") == member_id
        )
        if msg_count >= 10 and "social_butterfly" not in earned:
            new_achievements.append("social_butterfly")

        # Swap
        swap_count = sum(
            1 for s in self.dm.data["swap_requests"]
            if s.get("from_member") == member_id and s.get("status") == "approved"
        )
        if swap_count >= 1 and "generous" not in earned:
            new_achievements.append("generous")

        # Challenge completion
        challenge_count = sum(
            1 for ch in self.dm.data["challenges"]
            if member_id in ch.get("completed_by", [])
        )
        challenge_milestones = {1: "challenge_1", 5: "challenge_5"}
        for threshold, ach_id in challenge_milestones.items():
            if challenge_count >= threshold and ach_id not in earned:
                new_achievements.append(ach_id)

        # Award new achievements
        if new_achievements:
            for ach_id in new_achievements:
                member["achievements"].append(ach_id)
                ach = ACHIEVEMENTS.get(ach_id, {})
                self.dm.add_points(member_id, ach.get("points", 0), f"Achievement: {ach.get('name', '')}")
                self.dm.log_activity(member_id, "achievement",
                                     f"Achievement behaald: {ach.get('icon', '')} {ach.get('name', '')}")
            self.dm.save()

        return new_achievements

    def _count_completed_for(self, member_id: str) -> int:
        return sum(
            1 for s in self.dm.data["rooster"].values()
            if s.get("member_id") == member_id and s.get("status") == "completed"
        )

    def get_member_achievements(self, member_id: str) -> list:
        member = self.dm.data["members"].get(member_id, {})
        earned = member.get("achievements", [])
        return [
            {"id": ach_id, **ACHIEVEMENTS[ach_id]}
            for ach_id in earned
            if ach_id in ACHIEVEMENTS
        ]

    def get_all_achievements(self) -> list:
        return [{"id": k, **v} for k, v in ACHIEVEMENTS.items()]

    def get_progress(self, member_id: str) -> dict:
        earned = len(self.dm.data["members"].get(member_id, {}).get("achievements", []))
        total = len(ACHIEVEMENTS)
        return {
            "earned": earned,
            "total": total,
            "percentage": (earned / total * 100) if total > 0 else 0,
        }
