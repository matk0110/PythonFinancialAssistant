from dataclasses import dataclass, field
from typing import Dict

@dataclass
class Budget:
    categories: Dict[str, float] = field(default_factory=dict)
    spent: Dict[str, float] = field(default_factory=dict)

    def set_category(self, name: str, amount: float) -> None:
        self.categories[name] = amount
        self.spent.setdefault(name, 0.0)

    def add_spend(self, name: str, amount: float) -> None:
        if name not in self.categories:
            raise ValueError(f"Unknown category: {name}")
        self.spent[name] = self.spent.get(name, 0.0) + amount

    def remaining(self, name: str) -> float:
        if name not in self.categories:
            raise ValueError(f"Unknown category: {name}")
        return self.categories[name] - self.spent.get(name, 0.0)

    def summary(self) -> Dict[str, Dict[str, float]]:
        return {
            cat: {
                "budget": self.categories[cat],
                "spent": self.spent.get(cat, 0.0),
                "remaining": self.remaining(cat)
            } for cat in self.categories
        }
