"""
tracker.py  —  Logs grocery items to CSV for Power BI dashboard
"""

import csv
import os
from datetime import datetime

LOG_FILE = "data/spending_log.csv"


def log_receipt(items: list):
    """Appends items to spending_log.csv (creates file if it doesn't exist)."""
    os.makedirs("data", exist_ok=True)
    file_exists = os.path.isfile(LOG_FILE)

    with open(LOG_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["date", "item", "category"])
        for item in items:
            writer.writerow([datetime.now().strftime("%Y-%m-%d"), item, categorize(item)])


def categorize(item: str) -> str:
    """Simple keyword-based category tagger."""
    w = item.lower()
    if any(x in w for x in ["milk", "curd", "yogurt", "cheese", "paneer", "butter", "ghee"]):
        return "Dairy"
    if any(x in w for x in ["chicken", "mutton", "fish", "egg", "prawn", "meat"]):
        return "Protein"
    if any(x in w for x in ["apple", "banana", "tomato", "onion", "potato", "carrot",
                              "spinach", "mango", "orange", "lemon", "capsicum", "brinjal"]):
        return "Fruits & Vegetables"
    if any(x in w for x in ["rice", "wheat", "bread", "atta", "pasta", "dal", "lentil", "oats"]):
        return "Grains & Pulses"
    if any(x in w for x in ["oil", "salt", "sugar", "masala", "spice", "turmeric", "chilli"]):
        return "Spices & Condiments"
    if any(x in w for x in ["biscuit", "chocolate", "chips", "juice", "cola", "snack"]):
        return "Snacks & Beverages"
    return "Other"


def get_summary() -> dict:
    """Returns item count per category from the log."""
    if not os.path.isfile(LOG_FILE):
        return {}
    summary = {}
    with open(LOG_FILE, "r", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            cat = row.get("category", "Other")
            summary[cat] = summary.get(cat, 0) + 1
    return summary
