import streamlit as st
from datetime import datetime, timedelta
from utils.data_manager import get_data_manager
from utils.styles import inject_custom_css, roster_cell_html
from utils.helpers import format_date_dutch, ALL_DAYS

st.set_page_config(page_title="Rooster - Kookrooster", page_icon="📅", layout="wide")
inject_custom_css()
dm = get_data_manager()

st.markdown("## 📅 Kookrooster")

members = dm.get_members_list()
if not members:
    st.warning("Voeg eerst leden toe via **Beheer**.")
    st.stop()

cooking_days = dm.get_cooking_days()
if not cooking_days:
    st.warning("Selecteer eerst kookdagen in **Beheer**.")
    st.stop()

# ── View Selector ────────────────────────────────────────────────────
tab_overview, tab_signup, tab_menu, tab_swap, tab_absence = st.tabs([
    "Overzicht", "Inschrijven", "Menu Plannen", "Ruilen", "Afwezigheid"
])

weeks = dm.get_weeks()

# ═══════════════════════════════════════════════════════════════════════
# TAB: OVERVIEW
# ═══════════════════════════════════════════════════════════════════════
with tab_overview:
    st.markdown("### Rooster Overzicht")

    # View mode selector
    view = st.radio("Weergave", ["Compact", "Uitgebreid"], horizontal=True, label_visibility="collapsed")

    # Header row
    header_cols = st.columns([1.2] + [1.5] * len(cooking_days))
    header_cols[0].markdown("**Week**")
    for i, day in enumerate(cooking_days):
        header_cols[i + 1].markdown(f"**{day[:3]}**")

    # Roster grid
    for week in weeks:
        cols = st.columns([1.2] + [1.5] * len(cooking_days))
        week_start = week["start"]
        cols[0].markdown(f"**{week['label']}**")
        cols[0].caption(format_date_dutch(week_start))

        for i, day in enumerate(cooking_days):
            slot_key = f"{week['key']}-{day}"
            slot = dm.data["rooster"].get(slot_key, {})
            member_id = slot.get("member_id", "")
            gerecht = slot.get("gerecht", "")
            status = slot.get("status", "")

            with cols[i + 1]:
                if member_id:
                    name = dm.get_member_display(member_id)
                    if status == "completed":
                        icon = "✅"
                    else:
                        icon = ""

                    if view == "Compact":
                        st.markdown(f"""
                        <div class="roster-cell assigned">
                            <div class="chef-name">{icon} {name}</div>
                            <div class="dish-name">{gerecht if gerecht else '...'}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div class="roster-cell assigned">
                            <div class="chef-name">{icon} {name}</div>
                            <div class="dish-name">{gerecht if gerecht else 'Menu onbekend'}</div>
                            <div style="font-size:0.7rem;color:rgba(255,255,255,0.4);margin-top:0.3rem;">
                                {len(slot.get('attendees', []))} personen
                                {'| ' + '★' * int(slot.get('rating_avg', 0)) if slot.get('rating_avg', 0) > 0 else ''}
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.markdown(roster_cell_html(), unsafe_allow_html=True)

    # Auto-fill button
    st.markdown("")
    col1, col2, _ = st.columns([1, 1, 2])
    with col1:
        if st.button("🤖 Auto-invullen (Eerlijk)", type="primary"):
            dm.auto_fill_roster()
            st.rerun()
    with col2:
        empty_count = dm.get_total_slots() - len(dm.data["rooster"])
        st.caption(f"{empty_count} open plekken")


# ═══════════════════════════════════════════════════════════════════════
# TAB: SIGN UP
# ═══════════════════════════════════════════════════════════════════════
with tab_signup:
    st.markdown("### Inschrijven voor Kookbeurten")

    member_names = [m["name"] for m in members]
    selected_name = st.selectbox("Wie ben je?", [""] + member_names, key="signup_member")

    if selected_name:
        member_id = dm.member_id_by_name(selected_name)
        member = dm.data["members"][member_id]

        st.markdown(f"Klik op een vrij vak om **{member['avatar']} {member['name']}** in te schrijven.")
        st.markdown("")

        counts = dm.count_cooking_times()
        my_count = counts.get(member_id, 0)
        target = dm.get_total_slots() / len(members) if members else 0
        st.info(f"Je hebt **{my_count}** kookbeurten (streefaantal: ~{target:.0f})")

        for week in weeks:
            st.markdown(f"**{week['label']}** ({format_date_dutch(week['start'])})")
            cols = st.columns(len(cooking_days))

            for i, day in enumerate(cooking_days):
                slot_key = f"{week['key']}-{day}"
                slot = dm.data["rooster"].get(slot_key, {})
                current_member = slot.get("member_id", "")
                is_absent = dm.is_absent(member_id, slot_key)

                with cols[i]:
                    if current_member == member_id:
                        st.success(f"✅ {day[:3]}")
                        if slot.get("gerecht"):
                            st.caption(f"🍽️ {slot['gerecht']}")
                        if st.button("Afmelden", key=f"rem_{slot_key}", type="secondary"):
                            dm.remove_signup(slot_key)
                            st.rerun()
                    elif current_member:
                        other_name = dm.get_member_display(current_member)
                        st.markdown(f"🔒 **{day[:3]}**")
                        st.caption(other_name[:15])
                    elif is_absent:
                        st.markdown(f"🚫 **{day[:3]}**")
                        st.caption("Afwezig")
                    else:
                        st.markdown(f"⬜ **{day[:3]}**")
                        # Show suggestion
                        suggestion = dm.suggest_fair_assignment(slot_key)
                        if suggestion == member_id:
                            st.caption("Aanbevolen!")
                        if st.button("Inschrijven", key=f"add_{slot_key}"):
                            dm.sign_up(slot_key, member_id)
                            st.rerun()

            st.markdown("")


# ═══════════════════════════════════════════════════════════════════════
# TAB: MENU PLANNING
# ═══════════════════════════════════════════════════════════════════════
with tab_menu:
    st.markdown("### Menu Plannen")
    st.markdown("Vul in wat je gaat koken!")

    member_names = [m["name"] for m in members]
    selected_name = st.selectbox("Wie ben je?", [""] + member_names, key="menu_member")

    if selected_name:
        member_id = dm.member_id_by_name(selected_name)

        # Collect this member's slots
        my_slots = []
        for week in weeks:
            for day in cooking_days:
                slot_key = f"{week['key']}-{day}"
                slot = dm.data["rooster"].get(slot_key, {})
                if slot.get("member_id") == member_id:
                    day_idx = ALL_DAYS.index(day) if day in ALL_DAYS else 0
                    my_slots.append({
                        "slot_key": slot_key,
                        "week": week["label"],
                        "day": day,
                        "date": week["start"] + timedelta(days=day_idx),
                        "gerecht": slot.get("gerecht", ""),
                        "status": slot.get("status", "planned"),
                    })

        if not my_slots:
            st.info("Je hebt nog geen kookdagen. Ga naar **Inschrijven** om je in te schrijven!")
        else:
            used_gerechten = dm.get_all_gerechten()

            # Link recipes
            recipe_names = ["(geen recept)"] + [r["name"] for r in dm.data["recipes"].values()]

            st.markdown(f"**Jouw kookdagen ({len(my_slots)}):**")

            for slot in my_slots:
                col1, col2, col3 = st.columns([1, 2, 1])

                with col1:
                    status_icon = "✅" if slot["status"] == "completed" else "📅"
                    st.markdown(f"{status_icon} **{slot['day']}**")
                    st.caption(f"{slot['week']} - {format_date_dutch(slot['date'])}")

                with col2:
                    gerecht = st.text_input(
                        "Wat ga je koken?",
                        value=slot["gerecht"],
                        placeholder="bijv. Pasta carbonara",
                        key=f"gerecht_{slot['slot_key']}",
                    )

                    if gerecht and gerecht.lower().strip() in used_gerechten:
                        if gerecht.lower().strip() != slot["gerecht"].lower().strip():
                            st.warning("Dit gerecht staat al op het menu!")

                    if gerecht != slot["gerecht"]:
                        dm.set_gerecht(slot["slot_key"], gerecht)

                with col3:
                    # Link to recipe
                    selected_recipe = st.selectbox(
                        "Koppel recept",
                        recipe_names,
                        key=f"recipe_link_{slot['slot_key']}",
                        label_visibility="collapsed",
                    )
                    if selected_recipe != "(geen recept)":
                        for rid, r in dm.data["recipes"].items():
                            if r["name"] == selected_recipe:
                                if dm.data["rooster"][slot["slot_key"]].get("gerecht_id") != rid:
                                    dm.data["rooster"][slot["slot_key"]]["gerecht_id"] = rid
                                    dm.data["rooster"][slot["slot_key"]]["gerecht"] = r["name"]
                                    dm.save()
                                break

                    # Mark as completed
                    if slot["status"] != "completed":
                        if st.button("Afvinken", key=f"complete_{slot['slot_key']}"):
                            dm.complete_slot(slot["slot_key"])
                            st.rerun()

                st.divider()

            # Show others' menus
            with st.expander("🍴 Wat anderen koken"):
                for week in weeks:
                    for day in cooking_days:
                        slot_key = f"{week['key']}-{day}"
                        slot = dm.data["rooster"].get(slot_key, {})
                        if slot.get("gerecht") and slot.get("member_id") != member_id:
                            other = dm.get_member_display(slot["member_id"])
                            st.markdown(f"**{slot['gerecht']}** - {other} ({week['label']}, {day})")


# ═══════════════════════════════════════════════════════════════════════
# TAB: SWAP
# ═══════════════════════════════════════════════════════════════════════
with tab_swap:
    st.markdown("### Kookbeurten Ruilen")
    st.markdown("Wil je een kookbeurt ruilen met iemand anders? Stuur een ruilverzoek!")

    member_names = [m["name"] for m in members]
    selected_name = st.selectbox("Wie ben je?", [""] + member_names, key="swap_member")

    if selected_name:
        member_id = dm.member_id_by_name(selected_name)

        # Show pending swap requests for this member
        pending = dm.get_pending_swaps(member_id)
        if pending:
            st.markdown("#### Binnenkomende Ruilverzoeken")
            for swap in pending:
                from_name = dm.get_member_display(swap["from_member"])
                st.markdown(f"""
                <div class="swap-card">
                    <strong>{from_name}</strong> wil ruilen voor <strong>{swap['slot_key']}</strong>
                </div>
                """, unsafe_allow_html=True)

                col1, col2, _ = st.columns([1, 1, 3])
                with col1:
                    if st.button("Goedkeuren", key=f"approve_{swap['id']}", type="primary"):
                        dm.handle_swap(swap["id"], True)
                        st.rerun()
                with col2:
                    if st.button("Afwijzen", key=f"reject_{swap['id']}"):
                        dm.handle_swap(swap["id"], False)
                        st.rerun()

        # Create new swap request
        st.markdown("#### Nieuw Ruilverzoek")

        # My slots
        my_slot_keys = [
            sk for sk, s in dm.data["rooster"].items()
            if s.get("member_id") == member_id and s.get("status") != "completed"
        ]

        if not my_slot_keys:
            st.info("Je hebt geen kookbeurten om te ruilen.")
        else:
            swap_slot = st.selectbox("Welke kookbeurt wil je ruilen?", my_slot_keys, key="swap_slot")
            other_members = [m for m in members if m["id"] != member_id]
            swap_to = st.selectbox(
                "Met wie wil je ruilen?",
                [f"{m['avatar']} {m['name']}" for m in other_members],
                key="swap_to",
            )

            if st.button("Ruilverzoek Sturen", type="primary"):
                to_name = swap_to.split(" ", 1)[1] if " " in swap_to else swap_to
                to_id = dm.member_id_by_name(to_name)
                if to_id:
                    dm.request_swap(member_id, to_id, swap_slot)
                    st.success("Ruilverzoek verstuurd!")
                    st.rerun()

        # Swap history
        with st.expander("Ruilgeschiedenis"):
            all_swaps = [
                s for s in dm.data["swap_requests"]
                if s["from_member"] == member_id or s["to_member"] == member_id
            ]
            if all_swaps:
                for swap in reversed(all_swaps[-10:]):
                    status_icon = {"pending": "⏳", "approved": "✅", "rejected": "❌"}.get(swap["status"], "?")
                    from_name = dm.get_member_name(swap["from_member"])
                    to_name = dm.get_member_name(swap["to_member"])
                    st.markdown(f"{status_icon} {from_name} ↔ {to_name} - {swap['slot_key']}")
            else:
                st.caption("Geen ruilverzoeken.")


# ═══════════════════════════════════════════════════════════════════════
# TAB: ABSENCE
# ═══════════════════════════════════════════════════════════════════════
with tab_absence:
    st.markdown("### Afwezigheid Melden")
    st.markdown("Geef aan wanneer je er niet bent. Het rooster past zich automatisch aan.")

    member_names = [m["name"] for m in members]
    selected_name = st.selectbox("Wie ben je?", [""] + member_names, key="absence_member")

    if selected_name:
        member_id = dm.member_id_by_name(selected_name)
        absences = dm.data["absences"].get(member_id, [])

        st.info(f"Je bent afwezig gemeld voor **{len(absences)}** dag(en)")

        for week in weeks:
            st.markdown(f"**{week['label']}** ({format_date_dutch(week['start'])})")
            cols = st.columns(len(cooking_days))

            for i, day in enumerate(cooking_days):
                slot_key = f"{week['key']}-{day}"
                is_absent = dm.is_absent(member_id, slot_key)

                with cols[i]:
                    has_slot = slot_key in dm.data["rooster"] and dm.data["rooster"][slot_key].get("member_id") == member_id

                    if has_slot:
                        st.markdown(f"📅 **{day[:3]}** (kook)")
                    elif is_absent:
                        st.markdown(f"🚫 **{day[:3]}**")
                    else:
                        st.markdown(f"**{day[:3]}**")

                    new_absent = st.checkbox(
                        "Afwezig",
                        value=is_absent,
                        key=f"abs_{member_id}_{slot_key}",
                        label_visibility="collapsed",
                    )
                    if new_absent != is_absent:
                        dm.set_absence(member_id, slot_key, new_absent)
                        if new_absent and has_slot:
                            dm.remove_signup(slot_key)
                        st.rerun()

            st.markdown("")