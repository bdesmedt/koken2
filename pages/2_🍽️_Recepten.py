import streamlit as st
from utils.data_manager import get_data_manager, CUISINE_TAGS, MEAL_TAGS, DIETARY_OPTIONS, DIFFICULTY_LEVELS
from utils.styles import inject_custom_css, stars_html, tag_html, badge_html
from utils.helpers import (
    star_rating, difficulty_display, format_duration, QUICK_RECIPES,
    INGREDIENT_SUBSTITUTIONS,
)

st.set_page_config(page_title="Recepten - Kookrooster", page_icon="🍽️", layout="wide")
inject_custom_css()
dm = get_data_manager()

st.markdown("## 🍽️ Receptenbibliotheek")

members = dm.get_members_list()
recipes = dm.data["recipes"]

tab_browse, tab_add, tab_inspiration = st.tabs(["Bladeren", "Nieuw Recept", "Inspiratie"])

# ═══════════════════════════════════════════════════════════════════════
# TAB: BROWSE RECIPES
# ═══════════════════════════════════════════════════════════════════════
with tab_browse:
    if not recipes:
        st.info("Nog geen recepten. Voeg je eerste recept toe!")
    else:
        # Filters
        col_filter1, col_filter2, col_filter3, col_filter4 = st.columns(4)
        with col_filter1:
            search = st.text_input("Zoeken", placeholder="Zoek recept...", key="recipe_search")
        with col_filter2:
            filter_tags = st.multiselect("Tags", CUISINE_TAGS + MEAL_TAGS, key="recipe_tags")
        with col_filter3:
            filter_dietary = st.multiselect("Dieet", DIETARY_OPTIONS, key="recipe_dietary")
        with col_filter4:
            filter_diff = st.selectbox("Moeilijkheid", ["Alle"] + [d["label"] for d in DIFFICULTY_LEVELS.values()],
                                       key="recipe_diff")
            sort_by = st.selectbox("Sorteren", ["Nieuwste", "Best beoordeeld", "Meest gekookt", "Naam"],
                                   key="recipe_sort")

        # Apply filters
        filtered = []
        for rid, recipe in recipes.items():
            if search and search.lower() not in recipe["name"].lower():
                continue
            if filter_tags and not any(t in recipe.get("tags", []) for t in filter_tags):
                continue
            if filter_dietary and not any(d in recipe.get("dietary", []) for d in filter_dietary):
                continue
            if filter_diff != "Alle":
                diff_key = {v["label"]: k for k, v in DIFFICULTY_LEVELS.items()}.get(filter_diff)
                if diff_key and recipe.get("difficulty") != diff_key:
                    continue
            filtered.append((rid, recipe))

        # Sort
        if sort_by == "Nieuwste":
            filtered.sort(key=lambda x: x[1].get("created_at", ""), reverse=True)
        elif sort_by == "Best beoordeeld":
            filtered.sort(key=lambda x: x[1].get("avg_rating", 0), reverse=True)
        elif sort_by == "Meest gekookt":
            filtered.sort(key=lambda x: x[1].get("times_cooked", 0), reverse=True)
        elif sort_by == "Naam":
            filtered.sort(key=lambda x: x[1]["name"])

        st.caption(f"{len(filtered)} recepten gevonden")

        # Display recipes
        for rid, recipe in filtered:
            with st.expander(
                f"{'⭐ ' if recipe.get('avg_rating', 0) >= 4 else ''}"
                f"{recipe['name']} - {difficulty_display(recipe.get('difficulty', 'medium'))} "
                f"| {format_duration(recipe.get('prep_time', 0) + recipe.get('cook_time', 0))}"
            ):
                col1, col2 = st.columns([2, 1])

                with col1:
                    if recipe.get("description"):
                        st.markdown(recipe["description"])

                    # Tags
                    tags_html = " ".join(tag_html(t) for t in recipe.get("tags", []))
                    dietary_html = " ".join(tag_html(d, dietary=True) for d in recipe.get("dietary", []))
                    if tags_html or dietary_html:
                        st.markdown(f"{tags_html} {dietary_html}", unsafe_allow_html=True)

                    # Ingredients
                    if recipe.get("ingredients"):
                        st.markdown("**Ingredienten:**")
                        for ing in recipe["ingredients"]:
                            if isinstance(ing, dict):
                                amount = f"{ing.get('amount', '')} {ing.get('unit', '')}".strip()
                                st.markdown(f"- {amount} {ing.get('name', '')}")
                            else:
                                st.markdown(f"- {ing}")

                    # Instructions
                    if recipe.get("instructions"):
                        st.markdown("**Bereiding:**")
                        for i, step in enumerate(recipe["instructions"], 1):
                            st.markdown(f"{i}. {step}")

                with col2:
                    # Rating
                    st.markdown(stars_html(recipe.get("avg_rating", 0)), unsafe_allow_html=True)
                    ratings_count = len(recipe.get("ratings", {}))
                    st.caption(f"{ratings_count} beoordeling{'en' if ratings_count != 1 else ''}")

                    # Meta info
                    st.markdown(f"**Porties:** {recipe.get('servings', 4)}")
                    st.markdown(f"**Voorbereiden:** {format_duration(recipe.get('prep_time', 0))}")
                    st.markdown(f"**Koken:** {format_duration(recipe.get('cook_time', 0))}")
                    st.markdown(f"**Gekookt:** {recipe.get('times_cooked', 0)}x")

                    creator = dm.get_member_display(recipe.get("created_by", ""))
                    st.caption(f"Toegevoegd door {creator}")

                    # Favorites
                    fav_count = len(recipe.get("favorite_by", []))
                    st.markdown(f"❤️ {fav_count} favoriet{'en' if fav_count != 1 else ''}")

                    # Rate this recipe (if logged in)
                    if "current_member" in st.session_state:
                        mid = st.session_state["current_member"]
                        current_rating = recipe.get("ratings", {}).get(mid, 0)
                        new_rating = st.slider(
                            "Jouw beoordeling",
                            0, 5, current_rating,
                            key=f"rate_{rid}",
                        )
                        if new_rating != current_rating and new_rating > 0:
                            dm.rate_recipe(rid, mid, new_rating)
                            st.rerun()

                        # Favorite toggle
                        is_fav = mid in recipe.get("favorite_by", [])
                        fav_label = "Verwijder uit favorieten" if is_fav else "Voeg toe aan favorieten"
                        if st.button(f"{'💔' if is_fav else '❤️'} {fav_label}", key=f"fav_{rid}"):
                            dm.toggle_favorite(rid, mid)
                            st.rerun()


# ═══════════════════════════════════════════════════════════════════════
# TAB: ADD RECIPE
# ═══════════════════════════════════════════════════════════════════════
with tab_add:
    st.markdown("### Nieuw Recept Toevoegen")

    if not members:
        st.warning("Voeg eerst leden toe via Beheer.")
    else:
        with st.form("new_recipe_form"):
            name = st.text_input("Naam van het gerecht *", placeholder="bijv. Pasta Carbonara")
            description = st.text_area("Beschrijving", placeholder="Een korte beschrijving...")

            col1, col2, col3 = st.columns(3)
            with col1:
                difficulty = st.selectbox("Moeilijkheid", list(DIFFICULTY_LEVELS.keys()),
                                          format_func=lambda x: DIFFICULTY_LEVELS[x]["label"])
                servings = st.number_input("Porties", min_value=1, max_value=20, value=4)
            with col2:
                prep_time = st.number_input("Voorbereidingstijd (min)", min_value=0, max_value=300, value=15)
                cook_time = st.number_input("Kooktijd (min)", min_value=0, max_value=300, value=30)
            with col3:
                tags = st.multiselect("Tags", CUISINE_TAGS + MEAL_TAGS)
                dietary = st.multiselect("Dieet labels", DIETARY_OPTIONS)

            # Ingredients
            st.markdown("**Ingredienten** (een per regel, bijv. '500g spaghetti')")
            ingredients_text = st.text_area("Ingredienten", placeholder="500g spaghetti\n200g spek\n4 eieren\n100g parmezaan",
                                            label_visibility="collapsed")

            # Instructions
            st.markdown("**Bereidingsstappen** (een per regel)")
            instructions_text = st.text_area("Bereiding", placeholder="Kook de pasta al dente\nBak het spek krokant\nMix eieren met kaas",
                                              label_visibility="collapsed")

            member_names = [m["name"] for m in members]
            created_by_name = st.selectbox("Toegevoegd door", member_names)

            submitted = st.form_submit_button("Recept Opslaan", type="primary")

            if submitted:
                if not name:
                    st.error("Geef het gerecht een naam!")
                else:
                    ingredients = [ing.strip() for ing in ingredients_text.strip().split("\n") if ing.strip()] if ingredients_text else []
                    instructions = [step.strip() for step in instructions_text.strip().split("\n") if step.strip()] if instructions_text else []
                    created_by = dm.member_id_by_name(created_by_name)

                    dm.add_recipe(
                        name=name,
                        created_by=created_by,
                        description=description,
                        ingredients=ingredients,
                        instructions=instructions,
                        prep_time=prep_time,
                        cook_time=cook_time,
                        difficulty=difficulty,
                        tags=tags,
                        dietary=dietary,
                        servings=servings,
                    )
                    st.success(f"Recept '{name}' opgeslagen!")
                    st.rerun()


# ═══════════════════════════════════════════════════════════════════════
# TAB: INSPIRATION
# ═══════════════════════════════════════════════════════════════════════
with tab_inspiration:
    st.markdown("### Inspiratie")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Aanbevolen voor jouw groep")
        suggestions = dm.get_recipe_suggestions()
        if suggestions:
            for rid, recipe in suggestions:
                st.markdown(f"""
                <div class="recipe-card">
                    <div class="recipe-title">{recipe['name']}</div>
                    <div class="recipe-meta">
                        {stars_html(recipe.get('avg_rating', 0), small=True)}
                        <span>{difficulty_display(recipe.get('difficulty', 'medium'))}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.caption("Voeg recepten toe om suggesties te krijgen!")

    with col2:
        st.markdown("#### Snelle Recepten om te Proberen")
        for qr in QUICK_RECIPES:
            with st.expander(f"{qr['name']} ({qr['time']} min)"):
                st.markdown(f"**Moeilijkheid:** {difficulty_display(qr['difficulty'])}")
                tags_html_str = " ".join(tag_html(t) for t in qr.get("tags", []))
                st.markdown(tags_html_str, unsafe_allow_html=True)
                st.markdown("**Ingredienten:**")
                for ing in qr["ingredients"]:
                    st.markdown(f"- {ing}")
                st.markdown("**Bereiding:**")
                for i, step in enumerate(qr["instructions"], 1):
                    st.markdown(f"{i}. {step}")

                # Quick add to recipe library
                if members and st.button(f"Voeg toe aan bibliotheek", key=f"quick_add_{qr['name']}"):
                    first_member = members[0]["id"]
                    dm.add_recipe(
                        name=qr["name"],
                        created_by=first_member,
                        ingredients=qr["ingredients"],
                        instructions=qr["instructions"],
                        prep_time=qr["time"] // 2,
                        cook_time=qr["time"] // 2,
                        difficulty=qr["difficulty"],
                        tags=qr.get("tags", []),
                        servings=4,
                    )
                    st.success(f"'{qr['name']}' toegevoegd!")
                    st.rerun()

    # Favorite recipes
    if recipes:
        st.markdown("---")
        st.markdown("#### Favoriete Recepten")
        favorites = [
            (rid, r) for rid, r in recipes.items()
            if len(r.get("favorite_by", [])) > 0
        ]
        favorites.sort(key=lambda x: len(x[1]["favorite_by"]), reverse=True)

        if favorites:
            for rid, recipe in favorites[:5]:
                fav_count = len(recipe["favorite_by"])
                st.markdown(f"❤️ **{recipe['name']}** - {fav_count} favoriet{'en' if fav_count != 1 else ''} | "
                            f"{star_rating(recipe.get('avg_rating', 0))}")
        else:
            st.caption("Nog geen favorieten. Markeer recepten als favoriet!")