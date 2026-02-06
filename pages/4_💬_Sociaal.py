import streamlit as st
from utils.data_manager import get_data_manager
from utils.styles import (
    inject_custom_css, chat_message_html, stars_html,
    leaderboard_row_html, card,
)
from utils.helpers import time_ago, star_rating

st.set_page_config(page_title="Sociaal - Kookrooster", page_icon="💬", layout="wide")
inject_custom_css()
dm = get_data_manager()

st.markdown("## 💬 Sociaal")

members = dm.get_members_list()

tab_chat, tab_reactions, tab_hof, tab_wall = st.tabs([
    "Groepschat", "Reacties & Comments", "Hall of Fame", "Foto Wall"
])

# ═══════════════════════════════════════════════════════════════════════
# TAB: GROUP CHAT
# ═══════════════════════════════════════════════════════════════════════
with tab_chat:
    st.markdown("### Groepschat")

    if not members:
        st.warning("Voeg eerst leden toe.")
    else:
        # Chat display
        messages = dm.get_messages(slot_key=None, limit=50)

        chat_container = st.container()
        with chat_container:
            if messages:
                for msg in messages:
                    author = dm.get_member_display(msg.get("member_id", ""))
                    ts = time_ago(msg.get("timestamp", ""))
                    st.markdown(
                        chat_message_html(author, msg["text"], ts),
                        unsafe_allow_html=True,
                    )
            else:
                st.caption("Nog geen berichten. Begin het gesprek!")

        # Send message
        st.markdown("")
        col1, col2 = st.columns([1, 4])
        with col1:
            sender_name = st.selectbox("Als", [m["name"] for m in members], key="chat_sender",
                                       label_visibility="collapsed")
        with col2:
            message_text = st.text_input("Bericht", placeholder="Typ een bericht...",
                                         key="chat_input", label_visibility="collapsed")

        if st.button("Verstuur", type="primary", key="send_chat"):
            if message_text:
                sender_id = dm.member_id_by_name(sender_name)
                dm.send_message(sender_id, message_text)
                st.rerun()

        # Meal-specific chat
        st.markdown("---")
        st.markdown("#### Praat over een Specifieke Maaltijd")

        meal_slots = {
            f"{sk}: {s.get('gerecht', '?')} ({dm.get_member_name(s['member_id'])})": sk
            for sk, s in dm.data["rooster"].items()
            if s.get("gerecht")
        }

        if meal_slots:
            selected_meal = st.selectbox("Selecteer maaltijd", list(meal_slots.keys()))
            meal_key = meal_slots[selected_meal]

            meal_messages = dm.get_messages(slot_key=meal_key, limit=20)
            if meal_messages:
                for msg in meal_messages:
                    author = dm.get_member_display(msg.get("member_id", ""))
                    ts = time_ago(msg.get("timestamp", ""))
                    st.markdown(
                        chat_message_html(author, msg["text"], ts),
                        unsafe_allow_html=True,
                    )

            col1, col2 = st.columns([1, 4])
            with col1:
                meal_sender = st.selectbox("Als", [m["name"] for m in members], key="meal_chat_sender",
                                           label_visibility="collapsed")
            with col2:
                meal_msg = st.text_input("Bericht over deze maaltijd", key="meal_chat_input",
                                         label_visibility="collapsed")

            if st.button("Verstuur", type="primary", key="send_meal_chat"):
                if meal_msg:
                    sender_id = dm.member_id_by_name(meal_sender)
                    dm.send_message(sender_id, meal_msg, slot_key=meal_key)
                    st.rerun()


# ═══════════════════════════════════════════════════════════════════════
# TAB: REACTIONS & COMMENTS
# ═══════════════════════════════════════════════════════════════════════
with tab_reactions:
    st.markdown("### Reacties op Maaltijden")

    REACTION_EMOJIS = ["🔥", "😍", "🤤", "👏", "❤️", "😋", "💪", "🎉"]

    if not members:
        st.warning("Voeg eerst leden toe.")
    else:
        member_names = [m["name"] for m in members]
        reactor_name = st.selectbox("Reageer als", member_names, key="reactor")
        reactor_id = dm.member_id_by_name(reactor_name)

        st.markdown("")

        # Show meals that can be reacted to
        for slot_key, slot in sorted(dm.data["rooster"].items(), reverse=True):
            if not slot.get("gerecht"):
                continue

            cook_name = dm.get_member_display(slot["member_id"])
            reactions = slot.get("reactions", {})
            comments = slot.get("comments", [])

            st.markdown(f"""
            <div class="card">
                <div style="display:flex;justify-content:space-between;">
                    <div>
                        <div style="font-weight:700;">{slot['gerecht']}</div>
                        <div style="color:rgba(255,255,255,0.5);font-size:0.85rem;">
                            {cook_name} | {slot_key}
                        </div>
                    </div>
                    <div>{stars_html(slot.get('rating_avg', 0), small=True)}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Existing reactions
            if reactions:
                reaction_display = " ".join(
                    f"{emoji}" for emoji in reactions.values()
                )
                st.markdown(f"Reacties: {reaction_display}")

            # Add reaction
            react_cols = st.columns(len(REACTION_EMOJIS) + 1)
            for i, emoji in enumerate(REACTION_EMOJIS):
                with react_cols[i]:
                    if st.button(emoji, key=f"react_{slot_key}_{emoji}_{reactor_id}"):
                        dm.add_reaction(slot_key, reactor_id, emoji)
                        st.rerun()

            # Rate
            with react_cols[-1]:
                current_rating = slot.get("ratings", {}).get(reactor_id, 0)
                new_rating = st.selectbox(
                    "Score",
                    [0, 1, 2, 3, 4, 5],
                    index=current_rating,
                    key=f"slot_rate_{slot_key}_{reactor_id}",
                    label_visibility="collapsed",
                )
                if new_rating != current_rating and new_rating > 0:
                    dm.rate_slot(slot_key, reactor_id, new_rating)
                    st.rerun()

            # Comments
            if comments:
                for comment in comments[-3:]:
                    author = dm.get_member_display(comment["member_id"])
                    ts = time_ago(comment.get("timestamp", ""))
                    st.caption(f"💬 {author}: {comment['text']} ({ts})")

            # Add comment
            comment_text = st.text_input(
                "Reactie toevoegen",
                key=f"comment_{slot_key}",
                placeholder="Zeg iets over dit gerecht...",
                label_visibility="collapsed",
            )
            if comment_text and st.button("Plaats", key=f"post_comment_{slot_key}"):
                dm.add_comment(slot_key, reactor_id, comment_text)
                st.rerun()

            st.markdown("---")


# ═══════════════════════════════════════════════════════════════════════
# TAB: HALL OF FAME
# ═══════════════════════════════════════════════════════════════════════
with tab_hof:
    st.markdown("### Hall of Fame")

    if not members:
        st.info("Voeg leden toe om de Hall of Fame te zien.")
    else:
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### Meeste Kookbeurten")
            counts = dm.count_cooking_times()
            sorted_cooks = sorted(counts.items(), key=lambda x: x[1], reverse=True)
            for rank, (mid, count) in enumerate(sorted_cooks, 1):
                if count == 0:
                    continue
                name = dm.get_member_name(mid)
                avatar = dm.get_member_avatar(mid)
                st.markdown(
                    leaderboard_row_html(rank, name, avatar, str(count), f"{count} keer gekookt"),
                    unsafe_allow_html=True,
                )

        with col2:
            st.markdown("#### Beste Gemiddelde Rating")
            member_ratings = {}
            for slot in dm.data["rooster"].values():
                mid = slot.get("member_id", "")
                if slot.get("rating_avg", 0) > 0:
                    if mid not in member_ratings:
                        member_ratings[mid] = []
                    member_ratings[mid].append(slot["rating_avg"])

            avg_ratings = {
                mid: sum(ratings) / len(ratings)
                for mid, ratings in member_ratings.items()
            }
            sorted_ratings = sorted(avg_ratings.items(), key=lambda x: x[1], reverse=True)

            if sorted_ratings:
                for rank, (mid, avg) in enumerate(sorted_ratings, 1):
                    name = dm.get_member_name(mid)
                    avatar = dm.get_member_avatar(mid)
                    st.markdown(
                        leaderboard_row_html(rank, name, avatar, f"{avg:.1f}", star_rating(avg)),
                        unsafe_allow_html=True,
                    )
            else:
                st.caption("Nog geen ratings.")

        # Best dishes
        st.markdown("---")
        st.markdown("#### Beste Gerechten Ooit")

        rated_dishes = [
            (sk, s) for sk, s in dm.data["rooster"].items()
            if s.get("rating_avg", 0) > 0 and s.get("gerecht")
        ]
        rated_dishes.sort(key=lambda x: x[1]["rating_avg"], reverse=True)

        if rated_dishes:
            for i, (sk, slot) in enumerate(rated_dishes[:10], 1):
                cook = dm.get_member_display(slot["member_id"])
                rating = star_rating(slot["rating_avg"])
                st.markdown(f"**{i}.** {slot['gerecht']} - {cook} | {rating} ({slot['rating_avg']:.1f})")
        else:
            st.caption("Nog geen beoordeelde gerechten.")

        # Most points
        st.markdown("---")
        st.markdown("#### Meeste Punten")
        sorted_points = sorted(
            members,
            key=lambda m: dm.data["members"].get(m["id"], {}).get("points", 0),
            reverse=True,
        )
        for rank, member in enumerate(sorted_points, 1):
            points = dm.data["members"].get(member["id"], {}).get("points", 0)
            if points > 0:
                st.markdown(
                    leaderboard_row_html(rank, member["name"], member["avatar"],
                                         f"{points} pts", "punten"),
                    unsafe_allow_html=True,
                )


# ═══════════════════════════════════════════════════════════════════════
# TAB: PHOTO WALL
# ═══════════════════════════════════════════════════════════════════════
with tab_wall:
    st.markdown("### Foto Wall")
    st.caption("Deel foto's van jullie maaltijden!")

    if not members:
        st.warning("Voeg eerst leden toe.")
    else:
        # Upload photo
        member_names = [m["name"] for m in members]
        uploader_name = st.selectbox("Upload als", member_names, key="photo_uploader")

        meal_options = [
            f"{sk}: {s.get('gerecht', '?')}"
            for sk, s in dm.data["rooster"].items()
            if s.get("gerecht")
        ]

        if meal_options:
            selected_meal = st.selectbox("Voor welke maaltijd?", meal_options, key="photo_meal")
            uploaded_file = st.file_uploader("Upload foto", type=["jpg", "jpeg", "png"], key="photo_upload")

            if uploaded_file:
                st.image(uploaded_file, caption="Preview", width=300)
                st.info("Foto upload is beschikbaar wanneer de app op een server draait met opslag.")

        # Display existing photos placeholder
        st.markdown("---")
        st.markdown("#### Galerij")

        photos_found = False
        for sk, slot in dm.data["rooster"].items():
            if slot.get("photos"):
                photos_found = True
                st.markdown(f"**{slot.get('gerecht', '?')}** - {dm.get_member_display(slot['member_id'])}")
                for photo_url in slot["photos"]:
                    st.image(photo_url, width=200)

        if not photos_found:
            st.markdown("""
            <div class="card" style="text-align:center;padding:3rem;">
                <div style="font-size:3rem;margin-bottom:1rem;">📸</div>
                <div style="font-weight:600;">Nog geen foto's</div>
                <div style="color:rgba(255,255,255,0.5);margin-top:0.5rem;">
                    Upload foto's van jullie maaltijden om ze hier te tonen!
                </div>
            </div>
            """, unsafe_allow_html=True)