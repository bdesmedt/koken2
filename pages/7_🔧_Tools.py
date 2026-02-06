import streamlit as st
import time
from utils.data_manager import get_data_manager
from utils.styles import inject_custom_css, metric_card
from utils.helpers import INGREDIENT_SUBSTITUTIONS, UNIT_CONVERSIONS

st.set_page_config(page_title="Tools - Kookrooster", page_icon="🔧", layout="wide")
inject_custom_css()
dm = get_data_manager()

st.markdown("## 🔧 Keukentools")

tab_timer, tab_converter, tab_substitutes, tab_portions, tab_checklist = st.tabs([
    "Timer", "Omrekenen", "Substituties", "Porties", "Checklist"
])

# ═══════════════════════════════════════════════════════════════════════
# TAB: TIMER
# ═══════════════════════════════════════════════════════════════════════
with tab_timer:
    st.markdown("### Kooktimer")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("#### Snelle Timers")
        quick_times = [
            ("1 min", 1), ("3 min", 3), ("5 min", 5),
            ("10 min", 10), ("15 min", 15), ("20 min", 20),
            ("30 min", 30), ("45 min", 45), ("60 min", 60),
        ]

        cols = st.columns(3)
        for i, (label, minutes) in enumerate(quick_times):
            with cols[i % 3]:
                if st.button(label, key=f"quick_timer_{minutes}", use_container_width=True):
                    st.session_state["timer_minutes"] = minutes
                    st.session_state["timer_active"] = True
                    st.session_state["timer_start"] = time.time()

    with col2:
        st.markdown("#### Aangepaste Timer")
        custom_min = st.number_input("Minuten", min_value=1, max_value=300, value=10, key="custom_timer_min")
        if st.button("Start Timer", type="primary", key="start_custom_timer"):
            st.session_state["timer_minutes"] = custom_min
            st.session_state["timer_active"] = True
            st.session_state["timer_start"] = time.time()

    with col3:
        st.markdown("#### Timer Status")
        if st.session_state.get("timer_active"):
            elapsed = time.time() - st.session_state.get("timer_start", time.time())
            total_seconds = st.session_state.get("timer_minutes", 0) * 60
            remaining = max(0, total_seconds - elapsed)

            mins = int(remaining // 60)
            secs = int(remaining % 60)

            st.markdown(f"""
            <div class="timer-display">{mins:02d}:{secs:02d}</div>
            """, unsafe_allow_html=True)

            if remaining <= 0:
                st.balloons()
                st.success("Timer afgelopen!")
                st.session_state["timer_active"] = False
            else:
                progress = elapsed / total_seconds if total_seconds > 0 else 0
                st.progress(min(progress, 1.0))

                if st.button("Stop Timer", key="stop_timer"):
                    st.session_state["timer_active"] = False
        else:
            st.markdown("""
            <div class="timer-display" style="opacity:0.3;">00:00</div>
            """, unsafe_allow_html=True)
            st.caption("Selecteer een timer om te starten")

    # Common cooking timers
    st.markdown("---")
    st.markdown("#### Handige Kooktijden")

    cook_times = {
        "Pasta": [("Al dente", "8-10 min"), ("Zacht", "10-12 min")],
        "Rijst": [("Witte rijst", "12-15 min"), ("Bruine rijst", "25-30 min"), ("Basmati", "10-12 min")],
        "Eieren": [("Zacht gekookt", "6 min"), ("Medium", "8 min"), ("Hard gekookt", "12 min")],
        "Groenten": [("Stomen", "5-8 min"), ("Blancheren", "2-3 min"), ("Roosteren", "20-30 min")],
        "Vlees": [("Biefstuk rare", "2-3 min/kant"), ("Medium", "4-5 min/kant"), ("Well done", "6+ min/kant")],
        "Vis": [("Bakken", "3-4 min/kant"), ("Oven", "15-20 min"), ("Stomen", "8-10 min")],
    }

    cols = st.columns(3)
    for i, (category, times_list) in enumerate(cook_times.items()):
        with cols[i % 3]:
            st.markdown(f"**{category}**")
            for name, duration in times_list:
                st.caption(f"{name}: {duration}")


# ═══════════════════════════════════════════════════════════════════════
# TAB: UNIT CONVERTER
# ═══════════════════════════════════════════════════════════════════════
with tab_converter:
    st.markdown("### Omrekentool")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Gewicht & Volume")

        amount = st.number_input("Hoeveelheid", min_value=0.0, value=1.0, step=0.5, key="convert_amount")
        conversion = st.selectbox("Omrekening", [
            "Cups naar ml",
            "Ounces (oz) naar gram",
            "Pounds (lb) naar kg",
            "Tablespoon naar ml",
            "Teaspoon naar ml",
            "Gallon naar liter",
        ])

        conversion_map = {
            "Cups naar ml": ("cups", "ml", UNIT_CONVERSIONS["cups_to_ml"]),
            "Ounces (oz) naar gram": ("oz", "g", UNIT_CONVERSIONS["oz_to_g"]),
            "Pounds (lb) naar kg": ("lb", "kg", UNIT_CONVERSIONS["lb_to_kg"]),
            "Tablespoon naar ml": ("tbsp", "ml", UNIT_CONVERSIONS["tbsp_to_ml"]),
            "Teaspoon naar ml": ("tsp", "ml", UNIT_CONVERSIONS["tsp_to_ml"]),
            "Gallon naar liter": ("gal", "L", UNIT_CONVERSIONS["gallon_to_l"]),
        }

        from_unit, to_unit, factor = conversion_map[conversion]
        result = amount * factor

        st.markdown(f"""
        <div class="card-accent" style="text-align:center;padding:1.5rem;">
            <div style="font-size:1.5rem;font-weight:700;">{amount} {from_unit} = {result:.2f} {to_unit}</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown("#### Temperatuur")

        temp_direction = st.radio("Richting", ["Fahrenheit naar Celsius", "Celsius naar Fahrenheit"],
                                  key="temp_direction")
        temp_value = st.number_input("Temperatuur", value=350.0 if "Fahrenheit" in temp_direction.split()[0] else 180.0,
                                     key="temp_value")

        if temp_direction == "Fahrenheit naar Celsius":
            converted = (temp_value - 32) * 5 / 9
            st.markdown(f"""
            <div class="card-accent" style="text-align:center;padding:1.5rem;">
                <div style="font-size:1.5rem;font-weight:700;">{temp_value:.0f}°F = {converted:.0f}°C</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            converted = temp_value * 9 / 5 + 32
            st.markdown(f"""
            <div class="card-accent" style="text-align:center;padding:1.5rem;">
                <div style="font-size:1.5rem;font-weight:700;">{temp_value:.0f}°C = {converted:.0f}°F</div>
            </div>
            """, unsafe_allow_html=True)

        # Common oven temperatures
        st.markdown("**Veelgebruikte oventemperaturen:**")
        oven_temps = [
            ("Laag", "150°C / 300°F"),
            ("Matig", "180°C / 350°F"),
            ("Heet", "200°C / 400°F"),
            ("Zeer heet", "220°C / 425°F"),
            ("Grill", "250°C / 475°F"),
        ]
        for name, temp in oven_temps:
            st.caption(f"{name}: {temp}")


# ═══════════════════════════════════════════════════════════════════════
# TAB: SUBSTITUTIONS
# ═══════════════════════════════════════════════════════════════════════
with tab_substitutes:
    st.markdown("### Ingredienten Substituties")
    st.caption("Mis je een ingrediënt? Hier zijn alternatieven!")

    search_ing = st.text_input("Zoek ingrediënt", placeholder="bijv. boter, melk, ei...",
                               key="sub_search")

    if search_ing:
        found = False
        for ingredient, subs in INGREDIENT_SUBSTITUTIONS.items():
            if search_ing.lower() in ingredient.lower():
                found = True
                st.markdown(f"""
                <div class="card-accent">
                    <div style="font-weight:700;font-size:1.1rem;margin-bottom:0.5rem;">
                        Alternatieven voor: {ingredient.title()}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                for sub in subs:
                    st.markdown(f"- {sub}")
                st.markdown("")

        if not found:
            st.info(f"Geen substituties gevonden voor '{search_ing}'.")
    else:
        # Show all
        st.markdown("#### Alle Substituties")
        cols = st.columns(2)
        items = list(INGREDIENT_SUBSTITUTIONS.items())
        half = len(items) // 2 + 1

        for i, (ingredient, subs) in enumerate(items):
            col_idx = 0 if i < half else 1
            with cols[col_idx]:
                with st.expander(f"{ingredient.title()}"):
                    for sub in subs:
                        st.markdown(f"- {sub}")


# ═══════════════════════════════════════════════════════════════════════
# TAB: PORTIONS CALCULATOR
# ═══════════════════════════════════════════════════════════════════════
with tab_portions:
    st.markdown("### Porties Omrekenen")
    st.caption("Pas hoeveelheden aan voor meer of minder personen.")

    col1, col2 = st.columns(2)
    with col1:
        original_portions = st.number_input("Oorspronkelijk aantal porties", min_value=1, max_value=50, value=4,
                                            key="orig_portions")
    with col2:
        new_portions = st.number_input("Gewenst aantal porties", min_value=1, max_value=50, value=6,
                                       key="new_portions")

    ratio = new_portions / original_portions if original_portions > 0 else 1

    st.markdown(f"""
    <div class="card-accent" style="text-align:center;">
        <div style="font-size:1.5rem;font-weight:700;">Factor: {ratio:.2f}x</div>
        <div style="color:rgba(255,255,255,0.5);">Vermenigvuldig alle hoeveelheden met {ratio:.2f}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("#### Reken ingredienten om")
    ingredients_input = st.text_area(
        "Voer ingredienten in (een per regel, bijv. '500g pasta')",
        placeholder="500g pasta\n200ml room\n4 eieren\n100g kaas",
        key="portions_input",
    )

    if ingredients_input:
        st.markdown("**Omgerekende hoeveelheden:**")
        import re
        for line in ingredients_input.strip().split("\n"):
            line = line.strip()
            if not line:
                continue
            # Try to find a number
            match = re.match(r'(\d+\.?\d*)\s*(.*)', line)
            if match:
                amount = float(match.group(1))
                rest = match.group(2)
                new_amount = amount * ratio
                # Format nicely
                if new_amount == int(new_amount):
                    st.markdown(f"- **{int(new_amount)}** {rest}")
                else:
                    st.markdown(f"- **{new_amount:.1f}** {rest}")
            else:
                st.markdown(f"- {line}")

    # Quick link to recipes
    if dm.data["recipes"]:
        st.markdown("---")
        st.markdown("#### Omrekenen vanuit Recept")
        recipe_names = [r["name"] for r in dm.data["recipes"].values()]
        selected_recipe = st.selectbox("Selecteer recept", recipe_names, key="portion_recipe")

        for rid, r in dm.data["recipes"].items():
            if r["name"] == selected_recipe:
                st.info(f"Origineel: {r.get('servings', 4)} porties")
                if r.get("ingredients"):
                    for ing in r["ingredients"]:
                        st.markdown(f"- {ing}")
                break


# ═══════════════════════════════════════════════════════════════════════
# TAB: COOKING CHECKLIST
# ═══════════════════════════════════════════════════════════════════════
with tab_checklist:
    st.markdown("### Kook Checklist")
    st.caption("Houd je voorbereiding en kookproces bij!")

    # Predefined checklist items
    st.markdown("#### Voor het Koken")
    prep_items = [
        "Recept gelezen en begrepen",
        "Alle ingredienten verzameld",
        "Werkplek schoongemaakt",
        "Gereedschap klaargelegd",
        "Voorbereidingswerk gedaan (snijden, marineren, etc.)",
        "Oven/grill voorverwarmd",
    ]
    for item in prep_items:
        st.checkbox(item, key=f"prep_{item}")

    st.markdown("#### Tijdens het Koken")
    cook_items = [
        "Handen gewassen",
        "Timer gezet",
        "Gerecht geproefd en op smaak gebracht",
        "Borden voorverwarmd",
    ]
    for item in cook_items:
        st.checkbox(item, key=f"cook_{item}")

    st.markdown("#### Na het Koken")
    after_items = [
        "Restjes bewaard",
        "Keuken opgeruimd",
        "Afwas gedaan",
        "Foto gemaakt voor de groep!",
        "Kosten geregistreerd",
    ]
    for item in after_items:
        st.checkbox(item, key=f"after_{item}")

    # Custom checklist
    st.markdown("---")
    st.markdown("#### Eigen Notities")
    notes = st.text_area("Persoonlijke kooknotities", placeholder="Notities voor deze kooksessie...",
                         key="cook_notes")