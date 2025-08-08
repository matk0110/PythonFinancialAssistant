from dataclasses import dataclass
from typing import List, Dict

from src.persistence.storage import load_budget, save_budget
from src.budget.model import Budget
from src.spending.tracker import SpendingTracker
from src.utils.formatting import format_usd, parse_currency


@dataclass
class Message:
    role: str
    content: str


class BudgetChatAgent:
    """A simple rule-based chat agent for budgeting.

    Supported intents:
    - set budget: "set Food to $200"
    - add expense: "spent $12.50 on food" or "add 12.5 to Food"
    - show summary: "show summary" / "status"
    - list categories: "list categories"
    - help
    - save / quit
    """

    def __init__(self):
        self.budget: Budget = load_budget()
        self.tracker = SpendingTracker(self.budget)
        self.history: List[Message] = []

    def handle(self, text: str) -> str:
        t = text.strip()
        self.history.append(Message("user", t))
        lower = t.lower()

        if lower in {"help", "?"}:
            return self._help()
        if lower in {"status", "summary", "show summary"}:
            return self._summary()
        if lower in {"list categories", "categories"}:
            return self._list_categories()
        if lower in {"save", "persist"}:
            save_budget(self.budget)
            return "Saved."
        if lower in {"quit", "exit"}:
            save_budget(self.budget)
            return "Goodbye."

        # Set budget intent: "set Food to $200" / "Food = 200"
        if any(k in lower for k in ["set ", " = ", " to "]):
            try:
                # naive parse: split around ' to ' or '='
                if " to " in lower:
                    name_part, amt_part = t.split(" to ", 1)
                    name = name_part.replace("set", "").strip()
                elif "=" in t:
                    name, amt_part = t.split("=", 1)
                    name = name.strip()
                else:
                    raise ValueError
                amount = parse_currency(amt_part)
                if not name:
                    raise ValueError
                self.budget.set_category(name, amount)
                save_budget(self.budget)
                return f"Set {name} to {format_usd(amount)}."
            except Exception:
                return "I couldn't parse that. Try: set Food to $200"

        # Add expense intent: "spent $12 on food" / "add 12 to Food"
        if any(k in lower for k in ["spent", "add "]):
            try:
                # try pattern: spent <amt> on <cat>
                if "spent" in lower and " on " in lower:
                    before_on, after_on = t.lower().split(" on ", 1)
                    amt_text = before_on.replace("spent", "").strip()
                    amount = parse_currency(amt_text)
                    # use original case from t to get category substring
                    cat = t[-len(after_on):].strip()
                else:
                    # pattern: add <amt> to <cat>
                    _, rest = lower.split("add ", 1)
                    if " to " in rest:
                        amt_text, cat = rest.split(" to ", 1)
                        # get slices from original
                        start = t.lower().find(amt_text)
                        end = start + len(amt_text)
                        amt_text_orig = t[start:end]
                        amount = parse_currency(amt_text_orig)
                        cat = t.lower().split(" to ", 1)[1].strip()
                    else:
                        raise ValueError
                # map category by case-insensitive match
                matched = None
                for c in self.budget.categories:
                    if c.lower() == cat.lower():
                        matched = c
                        break
                if not matched:
                    return "Unknown category. Say 'list categories' or create it with 'set <name> to <amount>'."
                self.tracker.record_expense(matched, amount)
                save_budget(self.budget)
                return f"Added {format_usd(amount)} to {matched}."
            except Exception:
                return "I couldn't parse that. Try: spent $12 on Food"

        return "I didn't understand. Type 'help' for commands."

    def _summary(self) -> str:
        lines: List[str] = []
        for cat, info in self.budget.summary().items():
            spent = format_usd(info["spent"])
            budget_amt = format_usd(info["budget"])
            remaining = format_usd(info["remaining"])
            used_pct = 0.0
            if info["budget"]:
                used_pct = max(0.0, min(100.0, (info["spent"] / info["budget"]) * 100))
            lines.append(f"- {cat}: {used_pct:.0f}% | {spent} / {budget_amt} | left {remaining}")
        if not lines:
            return "No categories yet. Try: set Food to $200"
        return "\n".join(lines)

    def _list_categories(self) -> str:
        if not self.budget.categories:
            return "No categories yet. Try: set Food to $200"
        cats = ", ".join(sorted(self.budget.categories.keys()))
        return f"Categories: {cats}"

    def _help(self) -> str:
        return (
            "Commands:\n"
            "- set Food to $200\n"
            "- spent $12.50 on Food\n"
            "- add 5 to Fun\n"
            "- show summary\n"
            "- list categories\n"
            "- save | quit\n"
        )
