def format_usd(value: float) -> str:
    try:
        return f"${value:,.2f}"
    except Exception:
        # Fallback to simple two-decimal formatting if value isn't numeric
        return f"${value}"


def parse_currency(text: str) -> float:
    """Parse common currency text like "$1,234.5" into a float rounded to 2 decimals.

    Accepts commas, optional leading/trailing spaces, optional $.
    Raises ValueError if not parseable.
    """
    if isinstance(text, (int, float)):
        return round(float(text), 2)
    cleaned = (
        str(text)
        .strip()
        .replace("$", "")
        .replace(",", "")
    )
    value = float(cleaned)
    return round(value, 2)
