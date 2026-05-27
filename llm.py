"""
llm.py  —  Sends grocery items to Google Gemini and gets back a meal plan.
Uses the FREE tier of Gemini API (no credit card needed, 1500 calls/day free).
"""

import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()


def setup_gemini():
    """Reads API key from .env and sets up Gemini."""
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key or api_key == "paste-your-key-here":
        raise ValueError(
            "Gemini API key not found!\n"
            "Open the .env file and replace 'paste-your-key-here' with your actual key."
        )

    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-2.5-flash")  # free model


def generate_meal_plan(items: list, preferences: str = "") -> str:
    """
    Sends grocery items to Gemini and returns a 5-day meal plan.

    items       : list of grocery items from OCR
    preferences : e.g. "vegetarian", "low carb", "Indian food"
    """
    model = setup_gemini()

    items_text = "\n".join(f"- {item}" for item in items)
    pref_line  = f"\nDietary preferences: {preferences}" if preferences.strip() else ""

    prompt = f"""You are a friendly meal planning assistant.

The user just bought these groceries:
{items_text}
{pref_line}

Please create the following:

1. **5-Day Meal Plan**
   Breakfast, lunch, and dinner for each day.
   Use ONLY the ingredients listed above. Be realistic and practical.

2. **2 Easy Recipes**
   Pick 2 meals from the plan and give step-by-step cooking instructions.

3. **Nutrition Highlights**
   Briefly mention key nutrients in these groceries (protein, fibre, vitamins).

4. **Shopping Tip**
   Mention 2-3 ingredients that are missing and would make this grocery haul more balanced.

Keep your response friendly, clear, and easy to read.
"""

    response = model.generate_content(prompt)
    return response.text


def generate_quick_recipe(item_name: str, all_items: list) -> str:
    """Generates one quick recipe for a selected ingredient."""
    model = setup_gemini()

    prompt = f"""Give me one simple quick recipe featuring "{item_name}".

Available ingredients: {', '.join(all_items)}

Format:
- **Recipe name**
- **Ingredients** (only from the list above)
- **Steps** (5 simple steps)
- **Cook time**

Be concise and friendly.
"""

    response = model.generate_content(prompt)
    return response.text
