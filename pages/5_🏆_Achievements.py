import streamlit as st
from utils.data_manager import get_data_manager
from utils.styles import inject_custom_css, badge_html, leaderboard_row_html, metric_card
from utils.achievements import AchievementEngine, ACHIEVEMENTS

st.set_page_config(page_title="Achievements - Kookrooster", page_icon="🏆", layout="wide")
inject_custom_css()
dm = get_data_manager()

st.markdown("## 🏆 Achievements & Gamification")

members = dm.get_members_list()
engine = AchievementEngine(dm)

tab_badges, tab_leaderboard, tab_challenges, tab_streaks = st.tabs([
    "Badges", "Leaderboard", "Challenges", "Streaks & Punten"
])

# ═══════════════════════════════════════════════════════════════════════
# TAB: BADGES
# ═══════════════════════════════════════════════════════════════════════
with tab_badges:
    st.markdown("### Jouw Achievements")

    if not members:
        st.warning("Voeg eerst leden toe.")
    else:
        member_names = [m["name"] for m in members]
        selected_name = st.selectbox("Bekijk achievements van", member_names, key="badge_member")
        member_id = dm.member_id_by_name(selected_name)

        # Check for new achievements
        new_achs = engine.check_all(member_id)
        if new_achs:
            for ach_id in new_achs:
                ach = ACHIEVEMENTS.get(ach_id, {})
                st.success(f"Nieuw! {ach['icon']} **{ach['name']}** - {ach['description']}")

        # Progress
        progress = engine.get_progress(member_id)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(metric_card("Behaald", f"{progress['earned']}/{progress['total']}"),
                        unsafe_allow_html=True)
        with col2:
            st.markdown(metric_card("Voortgang", f"{progress['percentage']:.0f}%"),
                        unsafe_allow_html=True)
        with col3:
            points = dm.data["members"].get(member_id, {}).get("points", 0)
            st.markdown(metric_card("Totaal Punten", str(points)), unsafe_allow_html=True)

        st.markdown("")
        st.progress(progress["percentage"] / 100)

        # Display achievements by category
        earned_ids = dm.data["members"].get(member_id, {}).get("achievements", [])

        categories = {
            "cooking": "Koken",
            "recipes": "Recepten",
            "ratings": "Beoordelingen",
            "variety": "Variatie",
            "streaks": "Streaks",
            "social": "Sociaal",
            "special": "Speciaal",
            "challenges": "Challenges",
        }

        for cat_key, cat_name in categories.items():
            cat_achievements = [
                (aid, ach) for aid, ach in ACHIEVEMENTS.items()
                if ach.get("category") == cat_key
            ]
            if not cat_achievements:
                continue

            st.markdown(f"#### {cat_name}")
            cols = st.columns(min(len(cat_achievements), 4))
            for i, (ach_id, ach) in enumerate(cat_achievements):
                with cols[i % min(len(cat_achievements), 4)]:
                    earned = ach_id in earned_ids
                    opacity = "1" if earned else "0.3"
                    border_color = {
                        "gold": "rgba(241,196,15,0.5)",
                        "silver": "rgba(189,195,199,0.5)",
                        "bronze": "rgba(205,127,50,0.5)",
                    }.get(ach["tier"], "rgba(255,107,53,0.3)")

                    bg = f"rgba(255,255,255,0.03)" if not earned else {
                        "gold": "linear-gradient(135deg, rgba(241,196,15,0.1), transparent)",
                        "silver": "linear-gradient(135deg, rgba(189,195,199,0.1), transparent)",
                        "bronze": "linear-gradient(135deg, rgba(205,127,50,0.1), transparent)",
                    }.get(ach["tier"], "rgba(255,107,53,0.1)")

                    st.markdown(f"""
                    <div style="
                        background: {bg};
                        border: 1px solid {border_color};
                        border-radius: 16px;
                        padding: 1rem;
                        text-align: center;
                        opacity: {opacity};
                        margin-bottom: 0.5rem;
                    ">
                        <div style="font-size: 2rem;">{ach['icon']}</div>
                        <div style="font-weight: 700; margin: 0.3rem 0;">{ach['name']}</div>
                        <div style="font-size: 0.8rem; color: rgba(255,255,255,0.6);">{ach['description']}</div>
                        <div style="font-size: 0.75rem; color: #FF6B35; margin-top: 0.3rem;">+{ach['points']} pts</div>
                    </div>
                    """, unsafe_allow_html=True)

            st.markdown("")


# ═══════════════════════════════════════════════════════════════════════
# TAB: LEADERBOARD
# ═══════════════════════════════════════════════════════════════════════
with tab_leaderboard:
    st.markdown("### Leaderboard")

    if not members:
        st.info("Voeg leden toe om de leaderboard te zien.")
    else:
        lb_type = st.radio(
            "Ranglijst",
            ["Punten", "Kookbeurten", "Gemiddelde Rating", "Achievements", "Streaks"],
            horizontal=True,
        )

        if lb_type == "Punten":
            sorted_members = sorted(
                members,
                key=lambda m: dm.data["members"].get(m["id"], {}).get("points", 0),
                reverse=True,
            )
            for rank, member in enumerate(sorted_members, 1):
                points = dm.data["members"].get(member["id"], {}).get("points", 0)
                st.markdown(
                    leaderboard_row_html(rank, member["name"], member["avatar"],
                                         f"{points}", f"{points} punten"),
                    unsafe_allow_html=True,
                )

        elif lb_type == "Kookbeurten":
            counts = dm.count_cooking_times()
            sorted_by_cook = sorted(members, key=lambda m: counts.get(m["id"], 0), reverse=True)
            for rank, member in enumerate(sorted_by_cook, 1):
                count = counts.get(member["id"], 0)
                st.markdown(
                    leaderboard_row_html(rank, member["name"], member["avatar"],
                                         str(count), f"{count}x gekookt"),
                    unsafe_allow_html=True,
                )

        elif lb_type == "Gemiddelde Rating":
            member_ratings = {}
            for slot in dm.data["rooster"].values():
                mid = slot.get("member_id", "")
                if slot.get("rating_avg", 0) > 0 and mid:
                    if mid not in member_ratings:
                        member_ratings[mid] = []
                    member_ratings[mid].append(slot["rating_avg"])

            rated_members = []
            for member in members:
                ratings = member_ratings.get(member["id"], [])
                avg = sum(ratings) / len(ratings) if ratings else 0
                rated_members.append((member, avg, len(ratings)))

            rated_members.sort(key=lambda x: x[1], reverse=True)
            for rank, (member, avg, count) in enumerate(rated_members, 1):
                if avg > 0:
                    from utils.helpers import star_rating
                    st.markdown(
                        leaderboard_row_html(rank, member["name"], member["avatar"],
                                             f"{avg:.1f}", f"{star_rating(avg)} ({count} ratings)"),
                        unsafe_allow_html=True,
                    )

        elif lb_type == "Achievements":
            sorted_by_ach = sorted(
                members,
                key=lambda m: len(dm.data["members"].get(m["id"], {}).get("achievements", [])),
                reverse=True,
            )
            for rank, member in enumerate(sorted_by_ach, 1):
                ach_count = len(dm.data["members"].get(member["id"], {}).get("achievements", []))
                total = len(ACHIEVEMENTS)
                st.markdown(
                    leaderboard_row_html(rank, member["name"], member["avatar"],
                                         f"{ach_count}/{total}", f"{ach_count} achievements"),
                    unsafe_allow_html=True,
                )

        elif lb_type == "Streaks":
            sorted_by_streak = sorted(
                members,
                key=lambda m: dm.data["members"].get(m["id"], {}).get("best_streak", 0),
                reverse=True,
            )
            for rank, member in enumerate(sorted_by_streak, 1):
                streak = dm.data["members"].get(member["id"], {}).get("best_streak", 0)
                current = dm.data["members"].get(member["id"], {}).get("streak", 0)
                st.markdown(
                    leaderboard_row_html(rank, member["name"], member["avatar"],
                                         f"{streak}", f"Beste: {streak} | Nu: {current}"),
                    unsafe_allow_html=True,
                )


# ═══════════════════════════════════════════════════════════════════════
# TAB: CHALLENGES
# ═══════════════════════════════════════════════════════════════════════
with tab_challenges:
    st.markdown("### Challenges")
    st.caption("Maandelijkse thema's en uitdagingen voor de groep!")

    # Create new challenge
    with st.expander("Nieuwe Challenge Aanmaken"):
        with st.form("new_challenge"):
            ch_name = st.text_input("Challenge naam", placeholder="bijv. Italiaanse Week")
            ch_desc = st.text_area("Beschrijving", placeholder="Kook een week lang alleen Italiaans!")
            ch_tag = st.selectbox("Gerelateerde tag", [""] + list(set(
                tag for r in dm.data["recipes"].values() for tag in r.get("tags", [])
            )))

            col1, col2 = st.columns(2)
            with col1:
                from datetime import datetime
                ch_start = st.date_input("Startdatum", value=datetime.now())
            with col2:
                ch_end = st.date_input("Einddatum")

            if st.form_submit_button("Challenge Aanmaken", type="primary"):
                if ch_name:
                    dm.add_challenge(
                        ch_name, ch_desc, ch_tag,
                        ch_start.isoformat(), ch_end.isoformat(),
                    )
                    st.success(f"Challenge '{ch_name}' aangemaakt!")
                    st.rerun()

    # Active challenges
    st.markdown("#### Actieve Challenges")
    from datetime import datetime
    today = datetime.now().date()

    active = [
        ch for ch in dm.data["challenges"]
        if ch.get("end_date", "") >= today.isoformat()
    ]

    if active:
        for ch in active:
            participants = len(ch.get("participants", []))
            completed = len(ch.get("completed_by", []))

            st.markdown(f"""
            <div class="card-accent">
                <div style="display:flex;justify-content:space-between;align-items:center;">
                    <div>
                        <div style="font-weight:700;font-size:1.1rem;">🎯 {ch['name']}</div>
                        <div style="color:rgba(255,255,255,0.6);margin-top:0.3rem;">{ch.get('description', '')}</div>
                    </div>
                    <div style="text-align:right;">
                        <div style="font-size:0.85rem;">{participants} deelnemer(s)</div>
                        <div style="font-size:0.85rem;color:#2ecc71;">{completed} voltooid</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            if members:
                member_names_list = [m["name"] for m in members]
                join_name = st.selectbox(
                    "Doe mee als",
                    member_names_list,
                    key=f"join_ch_{ch['id']}",
                    label_visibility="collapsed",
                )
                if st.button("Doe Mee!", key=f"join_btn_{ch['id']}"):
                    join_id = dm.member_id_by_name(join_name)
                    dm.join_challenge(ch["id"], join_id)
                    st.rerun()
    else:
        st.info("Geen actieve challenges. Maak er een aan!")

    # Suggested challenges
    st.markdown("---")
    st.markdown("#### Challenge Ideeen")

    suggested = [
        ("🇮🇹 Italiaanse Week", "Kook alleen Italiaanse gerechten", "Italiaans"),
        ("🌱 Vegan Challenge", "Een week volledig plantaardig koken", "Veganistisch"),
        ("⚡ Speed Cooking", "Alle maaltijden binnen 30 minuten", "Snel (<30 min)"),
        ("🌍 Wereldreis", "Elke dag een ander land", ""),
        ("💰 Budget Battle", "Kook voor minder dan 5 euro per persoon", "Budget"),
        ("🔥 BBQ Week", "Alles van de grill", "BBQ"),
        ("🥗 Gezond Januari", "Alleen gezonde maaltijden", "Gezond"),
        ("🍜 Aziatisch Avontuur", "Ontdek de Aziatische keuken", "Aziatisch"),
    ]

    cols = st.columns(2)
    for i, (name, desc, tag) in enumerate(suggested):
        with cols[i % 2]:
            st.markdown(f"""
            <div class="card" style="padding:1rem;">
                <div style="font-weight:600;">{name}</div>
                <div style="font-size:0.85rem;color:rgba(255,255,255,0.5);">{desc}</div>
            </div>
            """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════
# TAB: STREAKS & POINTS
# ═══════════════════════════════════════════════════════════════════════
with tab_streaks:
    st.markdown("### Streaks & Punten")

    if not members:
        st.info("Voeg leden toe.")
    else:
        st.markdown("#### Huidige Streaks")
        st.caption("Hoe vaak achter elkaar heb je gekookt zonder over te slaan?")

        for member in members:
            mid = member["id"]
            m_data = dm.data["members"].get(mid, {})
            streak = m_data.get("streak", 0)
            best = m_data.get("best_streak", 0)

            streak_fire = "🔥" * min(streak, 10) if streak > 0 else "❄️"

            st.markdown(f"""
            <div class="card" style="padding:0.8rem 1rem;">
                <div style="display:flex;justify-content:space-between;align-items:center;">
                    <div>
                        <span style="font-size:1.2rem;">{member['avatar']}</span>
                        <strong>{member['name']}</strong>
                    </div>
                    <div>
                        <span style="font-size:1.3rem;">{streak_fire}</span>
                        <span style="font-weight:700;color:#FF6B35;margin-left:0.5rem;">{streak}</span>
                        <span style="color:rgba(255,255,255,0.4);font-size:0.8rem;margin-left:0.5rem;">
                            beste: {best}
                        </span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Points breakdown
        st.markdown("---")
        st.markdown("#### Hoe Verdien je Punten?")

        points_info = [
            ("Maaltijd koken", "+10 pts", "🍳"),
            ("Recept toevoegen", "+5 pts", "📖"),
            ("Achievement behalen", "+10-250 pts", "🏆"),
            ("Hoge rating ontvangen", "+bonus", "⭐"),
        ]

        cols = st.columns(len(points_info))
        for i, (action, pts, icon) in enumerate(points_info):
            with cols[i]:
                st.markdown(f"""
                <div class="metric-card">
                    <div style="font-size:2rem;">{icon}</div>
                    <div style="font-weight:600;margin:0.3rem 0;">{action}</div>
                    <div style="color:#FF6B35;font-weight:700;">{pts}</div>
                </div>
                """, unsafe_allow_html=True)