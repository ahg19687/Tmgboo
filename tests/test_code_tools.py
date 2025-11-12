# tests/test_code_tools.py

from telegram_bot.utils.code_tools import generate_code, create_bulk_codes

def test_generate_code():
    c = generate_code()
    assert len(c) == 6

def test_bulk_codes():
    out = create_bulk_codes(3, typ="test", duration_days=1, issued_by=1)
    assert len(out) == 3
