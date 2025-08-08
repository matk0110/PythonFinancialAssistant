from src.utils.formatting import parse_currency


def test_parse_currency_variants():
    assert parse_currency("$1,234.5") == 1234.50
    assert parse_currency("  99.9 ") == 99.90
    assert parse_currency(10) == 10.00
