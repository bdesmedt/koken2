import streamlit as st
from datetime import datetime, timedelta
from utils.data_manager import get_data_manager
from utils.styles import inject_custom_css, metric_card, activity_item_html, card
from utils.helpers import format_date_dutch, time_ago, star_rating
from utils.achievements import AchievementEngine

st.set_page_config(
    page_title="Kookrooster",
    page_icon="🍳",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_custom_css()
dm = get_data_manager()


# ── Sidebar ──────────────────────────────────────────────────
with st.sidebar:
    group_name = dm.data["group"]["name"]
    st.markdown(f"## {dm.data['group']['avatar']} {group_name}")

    members = dm.get_members_list()
    if members:
        st.markdown(f"**{len(members)} leden**")

        # Quick member selector for session
        member_names = ["Selecteer jezelf..."] + [m["name"] for m in members]
        selected_name = st.selectbox(
            "Wie ben je?",
            member_names,
            key="global_member_select",
            label_visibility="collapsed",
        )
        if selected_name != "Selecteer jezelf...":
            st.session_state["current_member"] = dm.member_id_by_name(selected_name)
            member = dm.data["members"][st.session_state["current_member"]]
            st.markdown(f"### {member['avatar']} {member['name']}")
            st.caption(f"**{member.get('points', 0)}** punten | "
                       f"**{member.get('streak', 0)}** streak")

            # Check for pending swaps
            pending = dm.get_pending_swaps(st.session_state["current_member"])
            if pending:
                st.warning(f"Je hebt **{len(pending)}** ruilverzoek(en)!")
    else:
        st.info("Nog geen leden. Ga naar Beheer om leden toe te voegen.")

    st.divider()

    # Quick stats
    if members:
        total_slots = dm.get_total_slots()
        filled = len(dm.data["rooster"])
        st.caption("ROOSTER STATUS")
        progress = filled / total_slots if total_slots > 0 else 0
        st.progress(min(progress, 1.0))
        st.caption(f"{filled}/{total_slots} ingevuld")


# ── Main Dashboard ───────────────────────────────────────────
st.markdown("""
<div class="hero-header">
    <h1>🍳 Kookrooster</h1>
    <div class="subtitle">Samen koken, samen delen!</div>
</div>
""", unsafe_allow_html=True)

members = dm.get_members_list()

if not members:
    st.markdown("### Welkom bij Kookrooster!")
    st.markdown("""
    **Kookrooster** is de ultieme app voor jouw vriendengroep om kookbeurten te organiseren,
    recepten te delen, kosten bij te houden en plezier te hebben in de keuken.

    **Ga naar** **Beheer** (in het menu links) om te beginnen met het toevoegen van leden.
    """)

    with st.expander("Wat kan je allemaal met Kookrooster?"):
        cols = st.columns(3)
        features = [
            ("📅 Slim Rooster", "Eerlijke rotatie met automatische planning"),
            ("🍽️ Recepten", "Receptenbibliotheek met ratings en favorieten"),
            ("💰 Kosten", "Automatische kostenverdeling en afrekening"),
            ("💬 Sociaal", "Chat, reacties en een Hall of Fame"),
            ("🏆 Gamification", "Achievements, punten en challenges"),
            ("📊 Statistieken", "Mooie dashboards en inzichten"),
            ("🔧 Tools", "Timers, omrekenen en substituties"),
            ("⚙️ Beheer", "Rollen, groepsinstellingen en meer"),
            ("🔄 Ruilen", "Kookbeurten ruilen met goedkeuring"),
        ]
        for i, (title, desc) in enumerate(features):
            with cols[i % 3]:
                st.markdown(f"**{title}**")
                st.caption(desc)
else:
    # ── Dashboard Metrics ────────────────────────────────────
    total_slots = dm.get_total_slots()
    filled = len(dm.data["rooster"])
    completed = sum(1 for s in dm.data["rooster"].values() if s.get("status") == "completed")
    total_recipes = len(dm.data["recipes"])

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(metric_card("Leden", str(len(members))), unsafe_allow_html=True)
    with col2:
        st.markdown(metric_card("Rooster Bezet",
                                f"{filled}/{total_slots}",
                                f"{filled/total_slots*100:.0f}%" if total_slots else "0%"),
                    unsafe_allow_html=True)
    with col3:
        st.markdown(metric_card("Gekookt", str(completed)), unsafe_allow_html=True)
    with col4:
        st.markdown(metric_card("Recepten", str(total_recipes)), unsafe_allow_html=True)

    st.markdown("")

    # ── Upcoming Meals & Activity ────────────────────────────
    col_left, col_right = st.columns([3, 2])

    with col_left:
        st.markdown("### Komende Maaltijden")

        weeks = dm.get_weeks()
        cooking_days = dm.get_cooking_days()
        today = datetime.now().date()
        upcoming = []

        for week in weeks:
            for day in cooking_days:
                slot_key = f"{week['key']}-{day}"
                slot = dm.data["rooster"].get(slot_key)
                if slot and slot.get("status") != "completed":
                    day_date = dm.get_day_date(week, day).date()
                    if day_date >= today:
                        upcoming.append({
                            "slot_key": slot_key,
                            "date": day_date,
                            "day": day,
                            "week": week["label"],
                            "member_id": slot["member_id"],
                            "gerecht": slot.get("gerecht", ""),
                            "attendees": len(slot.get("attendees", [])),
                            "rating_avg": slot.get("rating_avg", 0),
                        })

        upcoming.sort(key=lambda x: x["date"])
        upcoming = upcoming[:6]

        if upcoming:
            for meal in upcoming:
                member_name = dm.get_member_display(meal["member_id"])
                days_until = (meal["date"] - today).days
                if days_until == 0:
                    time_label = "**VANDAAG**"
                elif days_until == 1:
                    time_label = "Morgen"
                elif days_until < 7:
                    time_label = f"Over {days_until} dagen"
                else:
                    time_label = format_date_dutch(datetime.combine(meal["date"], datetime.min.time()))

                dish_text = meal["gerecht"] if meal["gerecht"] else "Menu nog niet bekend"
                attendees_text = f"{meal['attendees']} personen" if meal["attendees"] else ""

                st.markdown(f"""
                <div class="card">
                    <div style="display:flex;justify-content:space-between;align-items:flex-start;">
                        <div>
                            <div style="font-size:0.8rem;color:rgba(255,255,255,0.5);">{time_label} - {meal['day']}</div>
                            <div style="font-weight:700;font-size:1.1rem;margin:0.3rem 0;">{dish_text}</div>
                            <div style="color:rgba(255,255,255,0.7);">{member_name}</div>
                        </div>
                        <div style="text-align:right;font-size:0.8rem;color:rgba(255,255,255,0.5);">
                            {attendees_text}
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Geen komende maaltijden gepland. Ga naar het Rooster om in te schrijven!")

    with col_right:
        st.markdown("### Recente Activiteit")

        activities = dm.data.get("activity_log", [])[-15:]
        activities.reverse()

        activity_icons = {
            "signed_up": "📝",
            "cancelled": "❌",
            "cooked": "🍳",
            "recipe_added": "📖",
            "expense_added": "💰",
            "swap_requested": "🔄",
            "swap_approved": "✅",
            "achievement": "🏆",
            "joined": "👋",
            "rated": "⭐",
            "message": "💬",
        }

        if activities:
            for act in activities[:10]:
                icon = activity_icons.get(act.get("action", ""), "📌")
                time_str = time_ago(act.get("timestamp", ""))
                st.markdown(
                    activity_item_html(icon, act.get("details", ""), time_str),
                    unsafe_allow_html=True
                )
        else:
            st.caption("Nog geen activiteit.")

    # ── Fairness Overview (compact) ──────────────────────────
    st.markdown("")
    st.markdown("### Kookbeurten Verdeling")

    counts = dm.count_cooking_times()
    target = total_slots / len(members) if members else 0

    cols = st.columns(min(len(members), 6))
    for i, member in enumerate(members):
        with cols[i % min(len(members), 6)]:
            count = counts.get(member["id"], 0)
            progress = count / target if target > 0 else 0
            st.markdown(f"**{member['avatar']} {member['name']}**")
            st.progress(min(progress, 1.0))
            st.caption(f"{count} / ~{target:.0f}")

    # ── Top Recipes Preview ──────────────────────────────────
    top_recipes = dm.get_top_rated_recipes(3)
    if top_recipes:
        st.markdown("")
        st.markdown("### Top Recepten")
        cols = st.columns(3)
        for i, (rid, recipe) in enumerate(top_recipes):
            with cols[i]:
                rating = star_rating(recipe["avg_rating"])
                tags = " ".join(f"`{t}`" for t in recipe.get("tags", [])[:3])
                st.markdown(f"""
                <div class="recipe-card">
                    <div class="recipe-title">{recipe['name']}</div>
                    <div class="stars-small">{rating}</div>
                    <div style="margin-top:0.3rem;font-size:0.8rem;color:rgba(255,255,255,0.5);">
                        Gekookt: {recipe.get('times_cooked', 0)}x
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # ── Check achievements for current member ────────────────
    if "current_member" in st.session_state:
        engine = AchievementEngine(dm)
        new_achs = engine.check_all(st.session_state["current_member"])
        if new_achs:
            from utils.achievements import ACHIEVEMENTS
            for ach_id in new_achs:
                ach = ACHIEVEMENTS.get(ach_id, {})
                st.toast(f"{ach.get('icon', '🏆')} Achievement behaald: **{ach.get('name', '')}**!")
