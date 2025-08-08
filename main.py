from src.budget.model import Budget
from src.spending.tracker import SpendingTracker
from src.receipts import parser
from src.persistence.storage import load_budget, save_budget
from src.utils.formatting import format_usd, parse_currency


def interactive_cli():
    print("Free Spending Budget Agent")
    # Load existing budget if present
    budget = load_budget()
    if budget.categories:
        print(f"Loaded {len(budget.categories)} categories from previous session.")

    # Setup categories
    if not budget.categories:
        while True:
            cat = input("Add category name (or blank to finish): ").strip()
            if not cat:
                break
            amt_raw = input(f"Budget amount for {cat}: ").strip()
            try:
                amt = parse_currency(amt_raw)
            except ValueError:
                print("Invalid amount, try again.")
                continue
            budget.set_category(cat, amt)
        save_budget(budget)

    tracker = SpendingTracker(budget)

    while True:
        print("\nMenu: 1) Add expense 2) Show summary 3) Parse receipt 4) Save 5) Quit")
        choice = input("Choose: ").strip()
        if choice == '1':
            cat = input("Category: ").strip()
            amt_raw = input("Amount: ").strip()
            try:
                amt = parse_currency(amt_raw)
                tracker.record_expense(cat, amt)
                save_budget(budget)
            except Exception as e:  # broad for early prototype
                print(f"Error: {e}")
        elif choice == '2':
            for cat, info in budget.summary().items():
                spent = format_usd(info['spent'])
                budget_amt = format_usd(info['budget'])
                remaining = format_usd(info['remaining'])
                # crude progress bar
                used_pct = 0.0
                if info['budget']:
                    used_pct = max(0.0, min(100.0, (info['spent'] / info['budget']) * 100))
                bar_len = 20
                filled = int(bar_len * used_pct / 100)
                bar = "█" * filled + "-" * (bar_len - filled)
                print(f"{cat}: [{bar}] {used_pct:.0f}% | spent {spent} / {budget_amt} | remaining {remaining}")
        elif choice == '3':
            path = input("Receipt image path: ").strip()
            try:
                lines = parser.extract_lines(path)
                items = parser.simple_amount_parser(lines)
                for name, value in items:
                    # naive: attribute to first matching category name substring
                    matched = None
                    for cat in budget.categories:
                        if cat.lower() in name.lower():
                            matched = cat
                            break
                    if matched:
                        tracker.record_expense(matched, value)
                        print(f"Added {format_usd(value)} to {matched} from line '{name}'")
                save_budget(budget)
                print("Receipt parsing done.")
            except Exception as e:
                print(f"Receipt parse failed: {e}")
        elif choice == '4':
            save_budget(budget)
            print("Saved.")
        elif choice == '5':
            save_budget(budget)
            print("Goodbye.")
            break
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    interactive_cli()
