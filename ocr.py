"""
ocr.py  —  Reads receipt image and extracts grocery items
"""

import re
import pytesseract
from PIL import Image
import os

# ── Tell Python exactly where Tesseract is installed on Windows ──
# If you installed Tesseract in a different folder, update this path.
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\70086497\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"


def extract_items_from_image(uploaded_file) -> list:
    """Takes a Streamlit uploaded image and returns a list of grocery items."""
    try:
        image = Image.open(uploaded_file)
        raw_text = pytesseract.image_to_string(image)
        return parse_items(raw_text)
    except Exception as e:
        return [f"Error reading image: {str(e)}"]


def parse_items(raw_text: str) -> list:
    """Cleans raw OCR text — removes prices, totals, store info, etc."""
    items = []

    skip_words = [
        "total", "subtotal", "tax", "change", "cash", "card",
        "thank", "welcome", "receipt", "invoice", "bill",
        "amount", "balance", "vat", "gst", "discount",
        "store", "address", "phone", "date", "time",
        "visa", "mastercard", "upi", "paid", "save"
    ]

    for line in raw_text.split("\n"):
        line = line.strip()
        if len(line) < 3:
            continue
        if re.match(r"^[\d\s\.\,\:\/\-]+$", line):
            continue
        if any(word in line.lower() for word in skip_words):
            continue

        # Remove trailing prices like 45.00 or Rs.45
        cleaned = re.sub(r"\s+[\d]+[\.\,][\d]{2}\s*$", "", line)
        cleaned = re.sub(r"\s+Rs\.?[\d\.\,]+\s*$", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\s+\d+\s*$", "", cleaned).strip()

        if re.search(r"[a-zA-Z]", cleaned) and len(cleaned) > 2:
            items.append(cleaned)

    # Remove duplicates, keep order
    seen = set()
    result = []
    for item in items:
        if item.lower() not in seen:
            seen.add(item.lower())
            result.append(item)
    return result
