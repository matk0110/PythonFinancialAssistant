from pathlib import Path
from typing import List, Tuple

try:
    import pytesseract  # type: ignore
    from PIL import Image  # type: ignore
except ImportError:  # allow running without OCR deps installed yet
    pytesseract = None
    Image = None


def extract_lines(image_path: str) -> List[str]:
    """Return raw text lines from a receipt image. Graceful if OCR libs missing."""
    if pytesseract is None or Image is None:
        raise RuntimeError("OCR dependencies not installed. Install pillow and pytesseract.")
    img = Image.open(Path(image_path))
    text = pytesseract.image_to_string(img)
    return [l.strip() for l in text.splitlines() if l.strip()]


def simple_amount_parser(lines: List[str]) -> List[Tuple[str, float]]:
    """Very naive parser: find lines with pattern <name> <amount> (last token numeric)."""
    results: List[Tuple[str, float]] = []
    for line in lines:
        parts = line.rsplit(" ", 1)
        if len(parts) == 2:
            name, last = parts
            last = last.replace('$', '').replace(',', '')
            try:
                value = float(last)
                results.append((name.strip(), value))
            except ValueError:
                continue
    return results
