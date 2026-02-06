import streamlit as st
from datetime import datetime
from utils.data_manager import get_data_manager, AVATARS, DIETARY_OPTIONS, DEFAULT_DAYS
from utils.styles import inject_custom_css, metric_card
from utils.helpers import ALL_DAYS

st.set_page_config(page_title="Beheer - Kookrooster", page_icon="⚙️", layout="wide")
inject_custom_css()
dm = get_data_manager()

st.markdown("## ⚙️ Beheer & Instellingen")

tab_members, tab_group, tab_profiles, tab_data = st.tabs([
    "Leden", "Groep Instellingen", "Profielen", "Data & Export"
])

# ═══════════════════════════════════════════════════════════════════════
# TAB: MEMBER MANAGEMENT
# ═══════════════════════════════════════════════════════════════════════
with tab_members:
    st.markdown("### Leden Beheer")

    members = dm.get_members_list()

    # Add new member
    st.markdown("#### Nieuw Lid Toevoegen")
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        new_name = st.text_input("Naam", placeholder="bijv. Jan & Marie", key="new_member_name")
    with col2:
        new_avatar = st.selectbox("Avatar", AVATARS, key="new_member_avatar")
    with col3:
        new_role = st.selectbox("Rol", ["member", "admin"], key="new_member_role")

    if st.button("Lid Toevoegen", type="primary"):
        if new_name:
            existing_names = [m["name"] for m in members]
            if new_name in existing_names:
                st.error("Dit lid bestaat al!")
            else:
                dm.add_member(new_name, new_avatar, new_role)
                st.success(f"{new_avatar} {new_name} toegevoegd!")
                st.rerun()
        else:
            st.error("Vul een naam in!")

    # List current members
    st.markdown("---")
    st.markdown("#### Huidige Leden")

    if members:
        st.markdown(f"**{len(members)} leden**")
        for member in members:
            col1, col2, col3, col4, col5 = st.columns([3, 1, 1, 1, 1])
            with col1:
                st.markdown(f"**{member['avatar']} {member['name']}**")
                st.caption(f"Lid sinds {member.get('joined_date', '?')[:10]}")
            with col2:
                role_display = "Admin" if member.get("role") == "admin" else "Lid"
                st.markdown(f"`{role_display}`")
            with col3:
                points = member.get("points", 0)
                st.markdown(f"**{points}** pts")
            with col4:
                ach_count = len(member.get("achievements", []))
                st.markdown(f"**{ach_count}** badges")
            with col5:
                if st.button("Verwijderen", key=f"remove_{member['id']}", type="secondary"):
                    dm.remove_member(member["id"])
                    st.rerun()
            st.divider()
    else:
        st.info("Nog geen leden. Voeg hierboven je eerste lid toe!")

    # Invite link placeholder
    st.markdown("---")
    st.markdown("#### Leden Uitnodigen")
    st.markdown("Deel deze app-link met je vrienden om ze uit te nodigen.")
    st.code("https://jouw-kookrooster-app.streamlit.app", language=None)


# ═══════════════════════════════════════════════════════════════════════
# TAB: GROUP SETTINGS
# ═══════════════════════════════════════════════════════════════════════
with tab_group:
    st.markdown("### Groep Instellingen")

    group = dm.data["group"]

    with st.form("group_settings"):
        group_name = st.text_input("Groepsnaam", value=group["name"])
        group_avatar = st.selectbox(
            "Groep Emoji",
            ["🍳", "🍕", "🍔", "🌮", "🍣", "🥘", "🍝", "🥗"],
            index=["🍳", "🍕", "🍔", "🌮", "🍣", "🥘", "🍝", "🥗"].index(group.get("avatar", "🍳"))
            if group.get("avatar", "🍳") in ["🍳", "🍕", "🍔", "🌮", "🍣", "🥘", "🍝", "🥗"] else 0,
        )

        st.markdown("---")
        st.markdown("#### Kookdagen")
        cooking_days = st.multiselect(
            "Op welke dagen wordt er gekookt?",
            ALL_DAYS,
            default=group.get("cooking_days", DEFAULT_DAYS),
        )

        st.markdown("#### Planning")
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input(
                "Startdatum rooster",
                value=datetime.strptime(group["start_date"], "%Y-%m-%d"),
            )
            num_weeks = st.number_input(
                "Aantal weken",
                min_value=1, max_value=52,
                value=group.get("num_weeks", 12),
            )
        with col2:
            default_portions = st.number_input(
                "Standaard porties",
                min_value=1, max_value=30,
                value=group.get("default_portions", 4),
            )
            rsvp_deadline = st.number_input(
                "RSVP deadline (uren voor maaltijd)",
                min_value=1, max_value=72,
                value=group.get("rsvp_deadline_hours", 24),
            )

        st.markdown("#### Regels")
        swap_approval = st.checkbox(
            "Ruilverzoeken vereisen goedkeuring",
            value=group.get("swap_approval_required", True),
        )
        max_budget = st.number_input(
            "Maximum budget per maaltijd (0 = geen limiet)",
            min_value=0.0, step=5.0,
            value=float(group.get("max_budget", 0)),
            format="%.2f",
        )

        if st.form_submit_button("Instellingen Opslaan", type="primary"):
            dm.data["group"].update({
                "name": group_name,
                "avatar": group_avatar,
                "cooking_days": cooking_days,
                "start_date": start_date.strftime("%Y-%m-%d"),
                "num_weeks": num_weeks,
                "default_portions": default_portions,
                "rsvp_deadline_hours": rsvp_deadline,
                "swap_approval_required": swap_approval,
                "max_budget": max_budget,
            })
            dm.save()
            st.success("Instellingen opgeslagen!")
            st.rerun()


# ═══════════════════════════════════════════════════════════════════════
# TAB: MEMBER PROFILES
# ═══════════════════════════════════════════════════════════════════════
with tab_profiles:
    st.markdown("### Profiel Bewerken")

    members = dm.get_members_list()
    if not members:
        st.info("Nog geen leden.")
    else:
        member_names = [m["name"] for m in members]
        selected_name = st.selectbox("Selecteer lid", member_names, key="profile_member")
        member_id = dm.member_id_by_name(selected_name)
        member = dm.data["members"].get(member_id, {})

        with st.form("edit_profile"):
            col1, col2 = st.columns(2)

            with col1:
                edit_name = st.text_input("Naam", value=member.get("name", ""))
                edit_avatar = st.selectbox(
                    "Avatar",
                    AVATARS,
                    index=AVATARS.index(member.get("avatar", "👨‍🍳"))
                    if member.get("avatar", "👨‍🍳") in AVATARS else 0,
                )
                edit_role = st.selectbox(
                    "Rol",
                    ["member", "admin"],
                    index=0 if member.get("role") == "member" else 1,
                )
                edit_bio = st.text_area("Bio", value=member.get("bio", ""),
                                        placeholder="Vertel iets over jezelf...")

            with col2:
                edit_dietary = st.multiselect(
                    "Dieet restricties",
                    DIETARY_OPTIONS,
                    default=member.get("dietary_restrictions", []),
                )
                edit_allergies = st.text_input(
                    "Allergieen (komma-gescheiden)",
                    value=", ".join(member.get("allergies", [])),
                )
                edit_fav_cuisine = st.selectbox(
                    "Favoriete keuken",
                    [""] + list(set([
                        "Italiaans", "Aziatisch", "Mexicaans", "Nederlands",
                        "Frans", "Indiaas", "Grieks", "Japans", "Thais",
                    ])),
                    index=0,
                )

            if st.form_submit_button("Profiel Opslaan", type="primary"):
                dm.data["members"][member_id].update({
                    "name": edit_name,
                    "avatar": edit_avatar,
                    "role": edit_role,
                    "bio": edit_bio,
                    "dietary_restrictions": edit_dietary,
                    "allergies": [a.strip() for a in edit_allergies.split(",") if a.strip()],
                    "favorite_cuisine": edit_fav_cuisine,
                })
                dm.save()
                st.success("Profiel opgeslagen!")
                st.rerun()

        # Current profile overview
        st.markdown("---")
        st.markdown("#### Huidig Profiel")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**{member.get('avatar', '👤')} {member.get('name', '')}**")
            st.caption(f"Rol: {member.get('role', 'member').title()}")
            if member.get("bio"):
                st.markdown(f"*{member['bio']}*")
        with col2:
            if member.get("dietary_restrictions"):
                st.markdown(f"**Dieet:** {', '.join(member['dietary_restrictions'])}")
            if member.get("allergies"):
                st.markdown(f"**Allergieen:** {', '.join(member['allergies'])}")
            if member.get("favorite_cuisine"):
                st.markdown(f"**Favoriete keuken:** {member['favorite_cuisine']}")


# ═══════════════════════════════════════════════════════════════════════
# TAB: DATA & EXPORT
# ═══════════════════════════════════════════════════════════════════════
with tab_data:
    st.markdown("### Data & Export")

    # Data overview
    st.markdown("#### Data Overzicht")
    import json

    data = dm.data
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(metric_card("Leden", str(len(data.get("members", {})))), unsafe_allow_html=True)
    with col2:
        st.markdown(metric_card("Rooster Items", str(len(data.get("rooster", {})))), unsafe_allow_html=True)
    with col3:
        st.markdown(metric_card("Recepten", str(len(data.get("recipes", {})))), unsafe_allow_html=True)
    with col4:
        st.markdown(metric_card("Berichten", str(len(data.get("messages", [])))), unsafe_allow_html=True)

    st.markdown("---")

    # Export
    st.markdown("#### Export")
    col1, col2 = st.columns(2)

    with col1:
        # JSON export
        json_data = json.dumps(data, indent=2, ensure_ascii=False)
        st.download_button(
            "Download als JSON",
            json_data,
            file_name="kookrooster_backup.json",
            mime="application/json",
        )

    with col2:
        # CSV export of roster
        csv_lines = ["Week,Dag,Kok,Gerecht,Status,Rating"]
        for slot_key, slot in sorted(data.get("rooster", {}).items()):
            parts = slot_key.split("-")
            week = f"{parts[0]}-{parts[1]}" if len(parts) >= 2 else slot_key
            day = parts[2] if len(parts) >= 3 else ""
            cook = dm.get_member_name(slot.get("member_id", ""))
            gerecht = slot.get("gerecht", "")
            status = slot.get("status", "planned")
            rating = str(slot.get("rating_avg", ""))
            csv_lines.append(f"{week},{day},{cook},{gerecht},{status},{rating}")

        csv_data = "\n".join(csv_lines)
        st.download_button(
            "Download Rooster als CSV",
            csv_data,
            file_name="kookrooster_rooster.csv",
            mime="text/csv",
        )

    # Import
    st.markdown("---")
    st.markdown("#### Import")
    uploaded_file = st.file_uploader("Upload JSON backup", type=["json"], key="import_data")
    if uploaded_file:
        try:
            import_data = json.loads(uploaded_file.read())
            st.json(import_data)
            if st.button("Import Data", type="primary"):
                dm._data = import_data
                dm.save()
                st.success("Data geimporteerd!")
                st.rerun()
        except json.JSONDecodeError:
            st.error("Ongeldig JSON bestand!")

    # Reset
    st.markdown("---")
    st.markdown("#### Reset")
    st.warning("**Let op:** Dit verwijdert alle data permanent!")
    confirm_text = st.text_input("Typ 'RESET' om te bevestigen", key="reset_confirm")
    if st.button("Alle Data Wissen", type="secondary"):
        if confirm_text == "RESET":
            dm._data = dm._default_data()
            dm.save()
            st.success("Alle data gewist!")
            st.rerun()
        else:
            st.error("Typ 'RESET' om te bevestigen.")

    # Activity log
    st.markdown("---")
    st.markdown("#### Activiteiten Log")
    activities = data.get("activity_log", [])
    if activities:
        for act in reversed(activities[-30:]):
            member_name = dm.get_member_name(act.get("member_id", "")) if act.get("member_id") else "Systeem"
            st.caption(f"[{act.get('timestamp', '?')[:16]}] {member_name}: {act.get('details', '')}")
    else:
        st.caption("Geen activiteiten.")