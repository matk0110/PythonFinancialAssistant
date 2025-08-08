import streamlit as st
from src.persistence.storage import load_budget, save_budget, export_summary_csv
from src.utils.formatting import format_usd
from src.budget.model import Budget
from src.spending.tracker import SpendingTracker

st.set_page_config(page_title="Free Spending Budget", page_icon="💰", layout="centered")

budget = load_budget()
tracker = SpendingTracker(budget)

st.title("Free Spending Budget Agent")

with st.expander("Setup / Add Categories", expanded=not bool(budget.categories)):
    name = st.text_input("Category name")
    amount = st.number_input("Budget amount", min_value=0.0, step=10.0)
    if st.button("Add / Update Category") and name:
        budget.set_category(name, amount)
        save_budget(budget)
        st.success(f"Category '{name}' saved.")

st.header("Add Expense")
col1, col2 = st.columns(2)
with col1:
    cat = st.selectbox("Category", options=list(budget.categories.keys()) or ["-- none --"])
with col2:
    amt = st.number_input("Amount", min_value=0.0, step=1.0)

note = st.text_input("Note (optional)")
if st.button("Record Expense"):
    if cat in budget.categories:
        tracker.record_expense(cat, amt, note=note)
        save_budget(budget)
        st.success("Expense recorded.")
    else:
        st.error("Select a valid category.")

st.header("Summary")
if budget.categories:
    rows = []
    for c, info in budget.summary().items():
        rows.append(
            {
                "Category": c,
                "Budget": format_usd(info['budget']),
                "Spent": format_usd(info['spent']),
                "Remaining": format_usd(info['remaining']),
            }
        )
    st.table(rows)

    st.subheader("Progress by Category")
    for c, info in budget.summary().items():
        used_pct = 0.0
        if info['budget']:
            used_pct = max(0.0, min(100.0, (info['spent'] / info['budget']) * 100))
        st.write(f"{c}: {used_pct:.0f}% used")
        st.progress(int(used_pct))

    if st.button("Export CSV"):
        path = export_summary_csv(budget)
        st.success(f"Exported to {path}")
else:
    st.info("No categories defined yet.")

st.caption("Prototype UI – data stored locally in data/budget_state.json")
