import json
from pathlib import Path
from typing import Any, Dict
import csv
from ..budget.model import Budget

DEFAULT_DATA_FILE = Path("data/budget_state.json")


def ensure_data_dir(path: Path = DEFAULT_DATA_FILE) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def save_budget(budget: Budget, path: Path | None = None) -> None:
    if path is None:
        path = DEFAULT_DATA_FILE
    ensure_data_dir(path)
    data = {
        "categories": budget.categories,
        "spent": budget.spent,
    }
    path.write_text(json.dumps(data, indent=2))


def load_budget(path: Path | None = None) -> Budget:
    if path is None:
        path = DEFAULT_DATA_FILE
    if not path.exists():
        return Budget()
    raw: Dict[str, Any] = json.loads(path.read_text())
    b = Budget()
    for k, v in raw.get("categories", {}).items():
        b.set_category(k, float(v))
    for k, v in raw.get("spent", {}).items():
        b.spent[k] = float(v)
    return b


def export_summary_csv(budget: Budget, out_path: Path = Path("data/summary.csv")) -> Path:
    """Export budget summary to CSV and return file path."""
    ensure_data_dir(out_path)
    summary = budget.summary()
    with out_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Category", "Budget", "Spent", "Remaining"])
        for cat, info in summary.items():
            writer.writerow([cat, round(info["budget"], 2), round(info["spent"], 2), round(info["remaining"], 2)])
    return out_path
