# Python Financial Assistant (Chat Budget Agent)

A simple, chat-based budgeting agent that helps you set category budgets, track spending, and see how much you have left—kept lightweight and fully terminal-driven.

## Features
- Natural-language chat commands (set budgets, add expenses, summary, list, save/quit)
- USD formatting with 2 decimals
- JSON persistence to `data/budget_state.json` (auto-created)
- Optional receipt OCR parser (install Pillow + Tesseract OCR to enable)

## Quickstart (Windows, PowerShell)
```powershell
# From repo root
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
pip install -r requirements.dev.txt  # optional: tests & dev tools

# Run tests (optional)
pytest -q

# Start chat agent
python .\chat.py
```

Try commands:
- set Food to $200
- spent $12.50 on Food
- add 5 to Fun
- show summary
- list categories
- save | quit

## Data
- Budget is saved to `data/budget_state.json` automatically on save/quit and some actions.
- The `data/` folder is ignored by Git.

## Optional: Receipt OCR
- The function `src/receipts/parser.py` supports OCR via Pillow and pytesseract.
- You also need to install Tesseract OCR locally and ensure it’s on PATH.
- If OCR deps are missing, calling `extract_lines()` will raise a helpful error.

## Notes
- A legacy `streamlit_app.py` prototype is included but not required. If you want to try it, install Streamlit separately.
- This repo is intentionally minimal for a great terminal experience.

## License
MIT
