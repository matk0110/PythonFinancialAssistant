from src.utils.formatting import format_usd


def test_format_usd_basic():
    assert format_usd(0) == "$0.00"
    assert format_usd(12.3) == "$12.30"
    assert format_usd(1234.567) == "$1,234.57"
