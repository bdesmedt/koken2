import streamlit as st
from datetime import datetime
from utils.data_manager import get_data_manager, CUISINE_TAGS
from utils.styles import inject_custom_css, metric_card
from utils.helpers import star_rating

st.set_page_config(page_title="Statistieken - Kookrooster", page_icon="📊", layout="wide")
inject_custom_css()
dm = get_data_manager()

st.markdown("## 📊 Statistieken & Inzichten")

members = dm.get_members_list()

if not members:
    st.info("Voeg eerst leden toe om statistieken te zien.")
    st.stop()

tab_overview, tab_personal, tab_food, tab_costs = st.tabs([
    "Groepsoverzicht", "Persoonlijk", "Eetpatroon", "Kosten Analyse"
])

# ═══════════════════════════════════════════════════════════════════════
# TAB: GROUP OVERVIEW
# ═══════════════════════════════════════════════════════════════════════
with tab_overview:
    st.markdown("### Groepsoverzicht")

    # Key metrics
    total_slots = dm.get_total_slots()
    filled = len(dm.data["rooster"])
    completed = sum(1 for s in dm.data["rooster"].values() if s.get("status") == "completed")
    total_recipes = len(dm.data["recipes"])
    total_expenses = sum(e["amount"] for e in dm.data.get("expenses", []))

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.markdown(metric_card("Totaal Slots", str(total_slots)), unsafe_allow_html=True)
    with col2:
        pct = f"{filled/total_slots*100:.0f}%" if total_slots else "0%"
        st.markdown(metric_card("Bezetting", pct), unsafe_allow_html=True)
    with col3:
        st.markdown(metric_card("Gekookt", str(completed)), unsafe_allow_html=True)
    with col4:
        st.markdown(metric_card("Recepten", str(total_recipes)), unsafe_allow_html=True)
    with col5:
        st.markdown(metric_card("Totaal Kosten", f"€{total_expenses:.0f}"), unsafe_allow_html=True)

    st.markdown("")

    # Cooking distribution chart
    st.markdown("### Kookbeurten per Lid")
    counts = dm.count_cooking_times()
    target = total_slots / len(members) if members else 0

    for member in sorted(members, key=lambda m: counts.get(m["id"], 0), reverse=True):
        count = counts.get(member["id"], 0)
        progress = count / target if target > 0 else 0
        diff = count - target

        col1, col2, col3 = st.columns([2, 4, 1])
        with col1:
            st.markdown(f"**{member['avatar']} {member['name']}**")
        with col2:
            st.progress(min(progress, 1.0))
        with col3:
            color = "#2ecc71" if abs(diff) <= 1 else ("#e74c3c" if diff < -1 else "#f1c40f")
            st.markdown(f"<span style='color:{color};font-weight:700;'>{count}</span> / ~{target:.0f}",
                        unsafe_allow_html=True)

    # Fairness score
    if counts:
        values = list(counts.values())
        avg = sum(values) / len(values) if values else 0
        variance = sum((v - avg) ** 2 for v in values) / len(values) if values else 0
        fairness = max(0, 100 - variance * 10)
        st.markdown("")
        st.markdown(f"**Eerlijkheidsscore:** {fairness:.0f}/100")
        st.progress(min(fairness / 100, 1.0))
        if fairness >= 80:
            st.success("Uitstekende verdeling!")
        elif fairness >= 50:
            st.warning("Redelijke verdeling. Overweeg het auto-invullen te gebruiken.")
        else:
            st.error("Ongelijke verdeling. Gebruik auto-invullen voor een eerlijker rooster.")

    # Menu completion
    st.markdown("---")
    st.markdown("### Status Overzicht")

    col1, col2, col3 = st.columns(3)
    with col1:
        slots_with_menu = sum(1 for s in dm.data["rooster"].values() if s.get("gerecht"))
        menu_pct = slots_with_menu / filled * 100 if filled else 0
        st.markdown(metric_card("Menu's Ingevuld", f"{menu_pct:.0f}%"), unsafe_allow_html=True)
    with col2:
        rated_slots = sum(1 for s in dm.data["rooster"].values() if s.get("rating_avg", 0) > 0)
        st.markdown(metric_card("Beoordeeld", str(rated_slots)), unsafe_allow_html=True)
    with col3:
        all_ratings = [s["rating_avg"] for s in dm.data["rooster"].values() if s.get("rating_avg", 0) > 0]
        overall_avg = sum(all_ratings) / len(all_ratings) if all_ratings else 0
        st.markdown(metric_card("Gem. Rating", f"{overall_avg:.1f}" if overall_avg else "-"),
                    unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════
# TAB: PERSONAL STATS
# ═══════════════════════════════════════════════════════════════════════
with tab_personal:
    st.markdown("### Persoonlijke Statistieken")

    member_names = [m["name"] for m in members]
    selected_name = st.selectbox("Selecteer lid", member_names, key="stats_member")
    member_id = dm.member_id_by_name(selected_name)
    member = dm.data["members"].get(member_id, {})

    # Personal metrics
    cook_count = sum(1 for s in dm.data["rooster"].values() if s.get("member_id") == member_id)
    completed_count = sum(1 for s in dm.data["rooster"].values()
                          if s.get("member_id") == member_id and s.get("status") == "completed")
    recipe_count = sum(1 for r in dm.data["recipes"].values() if r.get("created_by") == member_id)
    my_ratings = [s["rating_avg"] for s in dm.data["rooster"].values()
                  if s.get("member_id") == member_id and s.get("rating_avg", 0) > 0]
    avg_rating = sum(my_ratings) / len(my_ratings) if my_ratings else 0

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(metric_card("Kookbeurten", str(cook_count)), unsafe_allow_html=True)
    with col2:
        st.markdown(metric_card("Afgerond", str(completed_count)), unsafe_allow_html=True)
    with col3:
        st.markdown(metric_card("Recepten", str(recipe_count)), unsafe_allow_html=True)
    with col4:
        st.markdown(metric_card("Gem. Rating",
                                f"{avg_rating:.1f}" if avg_rating else "-"),
                    unsafe_allow_html=True)

    st.markdown("")

    # Profile details
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### Profiel")
        st.markdown(f"**Avatar:** {member.get('avatar', '👤')}")
        st.markdown(f"**Rol:** {member.get('role', 'member').title()}")
        st.markdown(f"**Punten:** {member.get('points', 0)}")
        st.markdown(f"**Huidige streak:** {member.get('streak', 0)}")
        st.markdown(f"**Beste streak:** {member.get('best_streak', 0)}")

        if member.get("dietary_restrictions"):
            st.markdown(f"**Dieet:** {', '.join(member['dietary_restrictions'])}")
        if member.get("allergies"):
            st.markdown(f"**Allergieen:** {', '.join(member['allergies'])}")

    with col2:
        st.markdown("#### Achievements")
        earned = member.get("achievements", [])
        if earned:
            from utils.achievements import ACHIEVEMENTS
            for ach_id in earned:
                ach = ACHIEVEMENTS.get(ach_id, {})
                st.markdown(f"{ach.get('icon', '🏆')} **{ach.get('name', '')}** - {ach.get('description', '')}")
        else:
            st.caption("Nog geen achievements. Ga koken!")

    # Cooking history
    st.markdown("---")
    st.markdown("#### Kookgeschiedenis")
    my_meals = [
        (sk, s) for sk, s in dm.data["rooster"].items()
        if s.get("member_id") == member_id
    ]
    my_meals.sort(key=lambda x: x[0], reverse=True)

    if my_meals:
        for sk, slot in my_meals[:10]:
            status_icon = "✅" if slot.get("status") == "completed" else "📅"
            rating_str = star_rating(slot["rating_avg"]) if slot.get("rating_avg", 0) > 0 else ""
            st.markdown(f"{status_icon} **{slot.get('gerecht', 'Onbekend')}** - {sk} {rating_str}")
    else:
        st.caption("Nog geen kookbeurten.")


# ═══════════════════════════════════════════════════════════════════════
# TAB: FOOD PATTERNS
# ═══════════════════════════════════════════════════════════════════════
with tab_food:
    st.markdown("### Eetpatroon Analyse")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Favoriete Keuken")
        cuisine_dist = dm.get_cuisine_distribution()
        if cuisine_dist:
            sorted_cuisine = sorted(cuisine_dist.items(), key=lambda x: x[1], reverse=True)
            for cuisine, count in sorted_cuisine:
                bar_length = count / max(cuisine_dist.values()) if cuisine_dist.values() else 0
                st.markdown(f"**{cuisine}** ({count})")
                st.progress(bar_length)
        else:
            st.caption("Voeg tags toe aan recepten voor keuken-analyse.")

    with col2:
        st.markdown("#### Populaire Tags")
        tag_dist = {}
        for recipe in dm.data["recipes"].values():
            for tag in recipe.get("tags", []):
                tag_dist[tag] = tag_dist.get(tag, 0) + 1

        if tag_dist:
            sorted_tags = sorted(tag_dist.items(), key=lambda x: x[1], reverse=True)[:10]
            for tag, count in sorted_tags:
                st.markdown(f"`{tag}` - {count}x")
        else:
            st.caption("Voeg tags toe aan recepten.")

    # Variety score
    st.markdown("---")
    st.markdown("#### Variatie Score")

    unique_dishes = set()
    unique_cuisines = set()
    for slot in dm.data["rooster"].values():
        if slot.get("gerecht"):
            unique_dishes.add(slot["gerecht"].lower().strip())
        gerecht_id = slot.get("gerecht_id", "")
        if gerecht_id:
            recipe = dm.data["recipes"].get(gerecht_id, {})
            for tag in recipe.get("tags", []):
                if tag in CUISINE_TAGS:
                    unique_cuisines.add(tag)

    total_cooked = sum(1 for s in dm.data["rooster"].values() if s.get("gerecht"))
    variety_score = (len(unique_dishes) / total_cooked * 100) if total_cooked else 0

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(metric_card("Unieke Gerechten", str(len(unique_dishes))), unsafe_allow_html=True)
    with col2:
        st.markdown(metric_card("Unieke Keukens", str(len(unique_cuisines))), unsafe_allow_html=True)
    with col3:
        st.markdown(metric_card("Variatie Score", f"{variety_score:.0f}%"), unsafe_allow_html=True)

    # Dietary balance
    st.markdown("---")
    st.markdown("#### Dieet Verdeling")

    dietary_count = {}
    for recipe in dm.data["recipes"].values():
        for d in recipe.get("dietary", []):
            dietary_count[d] = dietary_count.get(d, 0) + 1

    if dietary_count:
        cols = st.columns(min(len(dietary_count), 4))
        for i, (diet, count) in enumerate(sorted(dietary_count.items(), key=lambda x: x[1], reverse=True)):
            with cols[i % min(len(dietary_count), 4)]:
                st.markdown(f"**{diet}**")
                st.markdown(f"{count} recepten")
    else:
        st.caption("Voeg dieet labels toe aan recepten.")


# ═══════════════════════════════════════════════════════════════════════
# TAB: COST ANALYSIS
# ═══════════════════════════════════════════════════════════════════════
with tab_costs:
    st.markdown("### Kosten Analyse")

    expenses = dm.data.get("expenses", [])
    if not expenses:
        st.info("Geen uitgaven geregistreerd.")
    else:
        total = sum(e["amount"] for e in expenses)
        avg_per_meal = total / len(expenses) if expenses else 0
        per_person_total = total / len(members) if members else 0

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(metric_card("Totaal", f"€{total:.2f}"), unsafe_allow_html=True)
        with col2:
            st.markdown(metric_card("Gem. per Maaltijd", f"€{avg_per_meal:.2f}"), unsafe_allow_html=True)
        with col3:
            st.markdown(metric_card("Per Persoon Totaal", f"€{per_person_total:.2f}"), unsafe_allow_html=True)
        with col4:
            max_expense = max(e["amount"] for e in expenses)
            st.markdown(metric_card("Duurste Maaltijd", f"€{max_expense:.2f}"), unsafe_allow_html=True)

        # Spending per member
        st.markdown("---")
        st.markdown("#### Uitgaven per Lid")

        member_spending = {m["id"]: 0 for m in members}
        for exp in expenses:
            if exp["paid_by"] in member_spending:
                member_spending[exp["paid_by"]] += exp["amount"]

        for mid, amount in sorted(member_spending.items(), key=lambda x: x[1], reverse=True):
            name = dm.get_member_display(mid)
            bar = amount / max(member_spending.values()) if max(member_spending.values()) > 0 else 0
            col1, col2, col3 = st.columns([2, 3, 1])
            with col1:
                st.markdown(f"**{name}**")
            with col2:
                st.progress(bar)
            with col3:
                st.markdown(f"€{amount:.2f}")

        # Budget tracking
        max_budget = dm.data["group"].get("max_budget", 0)
        if max_budget > 0:
            st.markdown("---")
            st.markdown("#### Budget Tracking")
            over_budget = sum(1 for e in expenses if e["amount"] > max_budget)
            st.info(f"Budget limiet: €{max_budget:.2f} per maaltijd")
            if over_budget:
                st.warning(f"{over_budget} maaltijd(en) boven budget")
            else:
                st.success("Alle maaltijden binnen budget!")