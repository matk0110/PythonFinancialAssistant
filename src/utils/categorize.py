from __future__ import annotations

from difflib import get_close_matches
from typing import Dict, List, Optional, Sequence, Set, Tuple

# Built-in keyword groups for common budgeting categories
BUILTIN_GROUPS: Dict[str, Set[str]] = {
    "food": {
        "food",
        "groceries",
        "grocery",
        "supermarket",
        "restaurant",
        "dining",
        "lunch",
        "dinner",
        "breakfast",
        "snack",
        "coffee",
        "cafe",
        "tea",
        "pizza",
        "burger",
        "drink",
    },
    "transport": {
        "transport",
        "transportation",
        "uber",
        "lyft",
        "taxi",
        "bus",
        "train",
        "metro",
        "subway",
        "fuel",
        "gas",
        "diesel",
        "parking",
        "toll",
        "carshare",
        "ride",
    },
    "housing": {"rent", "mortgage", "lease"},
    "utilities": {
        "utilities",
        "electric",
        "electricity",
        "power",
        "water",
        "gas",
        "internet",
        "wifi",
        "phone",
        "mobile",
        "cell",
        "trash",
        "sewer",
    },
    "health": {
        "health",
        "medical",
        "pharmacy",
        "drugstore",
        "doctor",
        "dentist",
        "hospital",
        "copay",
        "fitness",
        "gym",
    },
    "entertainment": {
        "entertainment",
        "movie",
        "cinema",
        "game",
        "concert",
        "music",
        "theater",
        "sports",
        "ticket",
        "netflix",
        "spotify",
        "hulu",
    },
    "shopping": {"shopping", "amazon", "target", "walmart", "clothes", "apparel"},
    "travel": {"flight", "hotel", "airbnb", "travel", "trip", "uber", "lyft"},
    "education": {"school", "tuition", "books", "course", "class", "udemy", "coursera"},
    "subscriptions": {"subscription", "subscribe", "membership", "prime", "icloud"},
}


def _tokens(text: str) -> List[str]:
    cleaned = "".join(ch.lower() if ch.isalnum() else " " for ch in text)
    return [t for t in cleaned.split() if t]


def _category_group_for_name(name: str) -> Optional[str]:
    """Map a category name to a built-in group if obvious."""
    n = name.lower()
    for group, kws in BUILTIN_GROUPS.items():
        if group in n:
            return group
        for kw in kws:
            if kw in n:
                return group
    return None


def infer_category(text: str, categories: Sequence[str]) -> Optional[str]:
    """Infer the best matching category from free text and a list of user categories.

    Returns the chosen category name if confidence is high enough, else None.
    """
    if not categories:
        return None

    toks = _tokens(text)
    if not toks:
        return None

    lower_to_orig = {c.lower(): c for c in categories}
    q = " ".join(toks)
    for low, orig in lower_to_orig.items():
        if low in q:
            return orig

    close = get_close_matches(q, list(lower_to_orig.keys()), n=1, cutoff=0.85)
    if close:
        return lower_to_orig[close[0]]

    cat_groups: Dict[str, Optional[str]] = {c: _category_group_for_name(c) for c in categories}

    def score_for(cat: str) -> int:
        score = 0
        cat_low = cat.lower()
        for t in toks:
            if t in cat_low:
                score += 2
        group = cat_groups.get(cat)
        if group and group in BUILTIN_GROUPS:
            kws = BUILTIN_GROUPS[group]
            for t in toks:
                if t in kws:
                    score += 2
        for group, kws in BUILTIN_GROUPS.items():
            if any(t in kws for t in toks) and group in cat_low:
                score += 1
        return score

    scored: List[Tuple[int, str]] = [(score_for(c), c) for c in categories]
    scored.sort(reverse=True)
    best_score, best_cat = scored[0]

    return best_cat if best_score >= 2 else None
