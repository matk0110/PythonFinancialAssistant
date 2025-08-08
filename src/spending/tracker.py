from typing import Optional
from ..budget.model import Budget

class SpendingTracker:
    def __init__(self, budget: Budget):
        self.budget = budget

    def record_expense(self, category: str, amount: float, note: Optional[str] = None) -> None:
        self.budget.add_spend(category, amount)
        # Placeholder for persistence / logging

    def category_status(self, category: str) -> dict:
        remaining = self.budget.remaining(category)
        allocated = self.budget.categories[category]
        percent = (allocated - remaining) / allocated * 100 if allocated else 0
        return {
            "category": category,
            "allocated": round(allocated, 2),
            "remaining": round(remaining, 2),
            "percent_used": round(percent, 2),
        }
