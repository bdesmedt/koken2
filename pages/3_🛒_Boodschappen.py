import streamlit as st
from utils.data_manager import get_data_manager
from utils.styles import inject_custom_css, metric_card, card
from utils.helpers import format_date_dutch

st.set_page_config(page_title="Boodschappen & Kosten - Kookrooster", page_icon="🛒", layout="wide")
inject_custom_css()
dm = get_data_manager()

st.markdown("## 🛒 Boodschappen & Kosten")

members = dm.get_members_list()

tab_shopping, tab_expenses, tab_balances = st.tabs(["Boodschappenlijst", "Uitgaven", "Afrekenen"])

# ═══════════════════════════════════════════════════════════════════════
# TAB: SHOPPING LIST
# ═══════════════════════════════════════════════════════════════════════
with tab_shopping:
    st.markdown("### Automatische Boodschappenlijst")

    if not dm.data["rooster"]:
        st.info("Plan eerst maaltijden in het rooster om een boodschappenlijst te genereren.")
    else:
        # Select which meals to generate shopping list for
        weeks = dm.get_weeks()
        cooking_days = dm.get_cooking_days()

        upcoming_slots = []
        for week in weeks:
            for day in cooking_days:
                slot_key = f"{week['key']}-{day}"
                slot = dm.data["rooster"].get(slot_key)
                if slot and slot.get("status") != "completed" and slot.get("gerecht_id"):
                    upcoming_slots.append({
                        "slot_key": slot_key,
                        "label": f"{week['label']} {day} - {slot.get('gerecht', '?')}",
                        "gerecht_id": slot["gerecht_id"],
                        "portions": slot.get("portions", 4),
                    })

        if not upcoming_slots:
            st.info("Koppel recepten aan je kookbeurten om automatisch een boodschappenlijst te genereren.")
            st.markdown("**Tip:** Ga naar het Rooster > Menu Plannen en koppel een recept aan je kookbeurt.")
        else:
            selected_meals = st.multiselect(
                "Selecteer maaltijden",
                [s["label"] for s in upcoming_slots],
                default=[s["label"] for s in upcoming_slots[:3]],
            )

            if selected_meals:
                all_ingredients = []
                for slot in upcoming_slots:
                    if slot["label"] in selected_meals:
                        recipe = dm.data["recipes"].get(slot["gerecht_id"], {})
                        portions_ratio = slot["portions"] / recipe.get("servings", 4) if recipe.get("servings") else 1
                        for ing in recipe.get("ingredients", []):
                            if isinstance(ing, dict):
                                all_ingredients.append(f"{ing.get('amount', '')} {ing.get('unit', '')} {ing.get('name', '')}".strip())
                            else:
                                all_ingredients.append(str(ing))

                if all_ingredients:
                    st.markdown("### Boodschappenlijst")
                    for ing in all_ingredients:
                        st.checkbox(ing, key=f"shop_{ing}")

                    st.markdown("")
                    # Export as text
                    shopping_text = "\n".join(f"- {ing}" for ing in all_ingredients)
                    st.download_button(
                        "Download als tekst",
                        shopping_text,
                        file_name="boodschappenlijst.txt",
                        mime="text/plain",
                    )
                else:
                    st.info("De geselecteerde recepten hebben geen ingredienten.")

        # Manual shopping list
        st.markdown("---")
        st.markdown("### Handmatige Boodschappenlijst")
        manual_items = st.text_area(
            "Voeg items toe (een per regel)",
            placeholder="Melk\nBrood\nEieren\nKaas",
            key="manual_shopping",
        )

        # Budget mode
        st.markdown("---")
        st.markdown("### Budget Mode")
        max_budget = dm.data["group"].get("max_budget", 0)
        if max_budget > 0:
            st.info(f"Maximum budget per maaltijd: **€{max_budget:.2f}**")
        else:
            st.caption("Geen budget limiet ingesteld. Stel dit in via Beheer.")


# ═══════════════════════════════════════════════════════════════════════
# TAB: EXPENSES
# ═══════════════════════════════════════════════════════════════════════
with tab_expenses:
    st.markdown("### Uitgaven Bijhouden")

    if not members:
        st.warning("Voeg eerst leden toe via Beheer.")
    else:
        # Add new expense
        with st.form("add_expense"):
            st.markdown("#### Nieuwe Uitgave")

            col1, col2 = st.columns(2)
            with col1:
                amount = st.number_input("Bedrag (€)", min_value=0.0, step=0.50, format="%.2f")
                paid_by_name = st.selectbox("Betaald door", [m["name"] for m in members])
            with col2:
                description = st.text_input("Omschrijving", placeholder="bijv. Boodschappen Albert Heijn")
                # Link to a meal slot
                slot_options = ["(geen koppeling)"] + [
                    f"{sk}: {s.get('gerecht', '?')}"
                    for sk, s in dm.data["rooster"].items()
                    if s.get("status") != "completed"
                ]
                linked_slot = st.selectbox("Gekoppeld aan maaltijd", slot_options)

            split_names = st.multiselect(
                "Verdeel tussen",
                [m["name"] for m in members],
                default=[m["name"] for m in members],
            )

            submitted = st.form_submit_button("Uitgave Toevoegen", type="primary")
            if submitted and amount > 0:
                paid_by_id = dm.member_id_by_name(paid_by_name)
                split_ids = [dm.member_id_by_name(n) for n in split_names]
                split_ids = [sid for sid in split_ids if sid]
                slot_key = linked_slot.split(":")[0] if linked_slot != "(geen koppeling)" else ""

                dm.add_expense(
                    slot_key=slot_key,
                    amount=amount,
                    paid_by=paid_by_id,
                    description=description,
                    split_between=split_ids,
                )
                st.success(f"Uitgave van €{amount:.2f} toegevoegd!")
                st.rerun()

        # Expense history
        st.markdown("---")
        st.markdown("#### Uitgaven Geschiedenis")

        expenses = dm.data.get("expenses", [])
        if expenses:
            total_spent = sum(e["amount"] for e in expenses)
            unsettled = sum(e["amount"] for e in expenses if not e.get("settled"))

            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(metric_card("Totaal Uitgegeven", f"€{total_spent:.2f}"), unsafe_allow_html=True)
            with col2:
                st.markdown(metric_card("Openstaand", f"€{unsettled:.2f}"), unsafe_allow_html=True)
            with col3:
                avg = total_spent / len(expenses) if expenses else 0
                st.markdown(metric_card("Gem. per Maaltijd", f"€{avg:.2f}"), unsafe_allow_html=True)

            st.markdown("")
            for exp in reversed(expenses[-20:]):
                paid_name = dm.get_member_display(exp.get("paid_by", ""))
                split_count = len(exp.get("split_between", []))
                per_person = exp["amount"] / split_count if split_count else exp["amount"]
                settled_icon = "✅" if exp.get("settled") else "⏳"

                col1, col2, col3, col4 = st.columns([3, 2, 1, 1])
                with col1:
                    st.markdown(f"{settled_icon} **{exp.get('description', 'Uitgave')}**")
                    st.caption(f"Betaald door {paid_name}")
                with col2:
                    st.markdown(f"**€{exp['amount']:.2f}**")
                    st.caption(f"€{per_person:.2f} p.p. ({split_count} pers.)")
                with col3:
                    if not exp.get("settled"):
                        if st.button("Afrekenen", key=f"settle_{exp['id']}"):
                            dm.settle_expense(exp["id"])
                            st.rerun()
                with col4:
                    if exp.get("slot_key"):
                        st.caption(f"📅 {exp['slot_key']}")
        else:
            st.info("Nog geen uitgaven geregistreerd.")


# ═══════════════════════════════════════════════════════════════════════
# TAB: BALANCES
# ═══════════════════════════════════════════════════════════════════════
with tab_balances:
    st.markdown("### Afrekenen")

    if not dm.data.get("expenses"):
        st.info("Geen uitgaven om af te rekenen.")
    else:
        balances = dm.calculate_balances()

        st.markdown("#### Saldo per Persoon")
        st.caption("Positief = je hebt meer betaald dan je deel. Negatief = je bent nog schuldig.")

        for mid, balance in sorted(balances.items(), key=lambda x: x[1], reverse=True):
            name = dm.get_member_display(mid)
            if balance > 0.01:
                st.markdown(f"""
                <div class="card-success">
                    <strong>{name}</strong>: <span style="color:#2ecc71;font-weight:700;">+€{balance:.2f}</span>
                    <br><small>Krijgt nog geld terug</small>
                </div>
                """, unsafe_allow_html=True)
            elif balance < -0.01:
                st.markdown(f"""
                <div class="card-warning">
                    <strong>{name}</strong>: <span style="color:#e74c3c;font-weight:700;">-€{abs(balance):.2f}</span>
                    <br><small>Moet nog betalen</small>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="card">
                    <strong>{name}</strong>: <span style="color:rgba(255,255,255,0.5);">€0.00</span>
                    <br><small>Quitte</small>
                </div>
                """, unsafe_allow_html=True)

        # Simplified settlement suggestions
        st.markdown("---")
        st.markdown("#### Aanbevolen Betalingen")

        debtors = [(mid, -bal) for mid, bal in balances.items() if bal < -0.01]
        creditors = [(mid, bal) for mid, bal in balances.items() if bal > 0.01]

        debtors.sort(key=lambda x: x[1], reverse=True)
        creditors.sort(key=lambda x: x[1], reverse=True)

        settlements = []
        d_idx, c_idx = 0, 0
        d_remaining = dict(debtors)
        c_remaining = dict(creditors)

        for d_mid, d_amount in debtors:
            while d_remaining[d_mid] > 0.01 and c_idx < len(creditors):
                c_mid = creditors[c_idx][0]
                transfer = min(d_remaining[d_mid], c_remaining[c_mid])
                if transfer > 0.01:
                    settlements.append((d_mid, c_mid, transfer))
                    d_remaining[d_mid] -= transfer
                    c_remaining[c_mid] -= transfer
                if c_remaining[c_mid] <= 0.01:
                    c_idx += 1

        if settlements:
            for from_mid, to_mid, amount in settlements:
                from_name = dm.get_member_display(from_mid)
                to_name = dm.get_member_display(to_mid)
                st.markdown(f"""
                <div class="card-accent">
                    <strong>{from_name}</strong> betaalt <strong>€{amount:.2f}</strong> aan <strong>{to_name}</strong>
                </div>
                """, unsafe_allow_html=True)

            st.markdown("")
            st.markdown("**Betaal direct via:**")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown("[Tikkie](https://tikkie.me)")
            with col2:
                st.markdown("[PayPal](https://paypal.me)")
            with col3:
                st.markdown("[Venmo](https://venmo.com)")
        else:
            st.success("Iedereen staat quitte!")