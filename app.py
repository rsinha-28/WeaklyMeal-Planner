"""
app.py  —  Grocery Receipt → Meal Planner  (Google Gemini free version)

HOW TO RUN:
  1. Open .env file and paste your Gemini API key
  2. Open terminal in this folder
  3. Run:  pip install -r requirements.txt
  4. Run:  streamlit run app.py
  5. Browser opens at http://localhost:8501
"""

import streamlit as st
from ocr import extract_items_from_image
from llm import generate_meal_plan, generate_quick_recipe
from tracker import log_receipt, get_summary


# ── Page setup ────────────────────────────────────────────────
st.set_page_config(
    page_title="Grocery → Meal Planner",
    page_icon="🛒",
    layout="centered"
)

# ── Header ────────────────────────────────────────────────────
st.title("🛒 Grocery Receipt → Meal Planner")
st.caption("Upload your grocery receipt · Get a free AI-powered 5-day meal plan · Powered by Google Gemini")
st.divider()


# ── Step 1: Upload ────────────────────────────────────────────
st.subheader("Step 1 — Upload your receipt photo")
st.caption("Tip: Take a clear, flat photo in good lighting for best results.")

uploaded_file = st.file_uploader(
    "Upload receipt image",
    type=["jpg", "jpeg", "png"],
    label_visibility="collapsed"
)

if uploaded_file:

    col1, col2 = st.columns([1, 2])
    with col1:
        st.image(uploaded_file, caption="Your receipt", use_container_width=True)
    with col2:
        with st.spinner("Reading receipt with OCR..."):
            items = extract_items_from_image(uploaded_file)

        if not items:
            st.error("Could not read items. Please try a clearer photo.")
            st.stop()

        st.success(f"✅ Found {len(items)} items!")
        st.caption("Scroll down to review and edit them.")

    st.divider()

    # ── Step 2: Review & edit items ───────────────────────────
    st.subheader("Step 2 — Review items (edit if needed)")
    st.caption("OCR sometimes makes mistakes. Fix any wrong names below before generating.")

    edited_text = st.text_area(
        "Detected items (one per line):",
        value="\n".join(items),
        height=180
    )

    final_items = [line.strip() for line in edited_text.split("\n") if line.strip()]
    st.caption(f"{len(final_items)} items ready for meal planning.")

    st.divider()

    # ── Step 3: Preferences ───────────────────────────────────
    st.subheader("Step 3 — Dietary preferences (optional)")

    preferences = st.text_input(
        "Any preferences?",
        placeholder="e.g.  vegetarian · low carb · Indian food · no onion garlic · diabetic friendly"
    )

    st.divider()

    # ── Step 4: Generate ──────────────────────────────────────
    st.subheader("Step 4 — Generate your meal plan")

    if st.button("✨ Generate Meal Plan", type="primary", use_container_width=True):

        if not final_items:
            st.error("Please add at least one grocery item above.")
        else:
            with st.spinner("Gemini is creating your personalised meal plan... (5–10 seconds)"):
                try:
                    meal_plan = generate_meal_plan(final_items, preferences)
                    log_receipt(final_items)   # save to CSV for Power BI

                    st.success("Your meal plan is ready! 🎉")
                    st.divider()
                    st.markdown(meal_plan)

                    # ── Bonus: quick recipe for one item ──────
                    st.divider()
                    st.subheader("🍳 Want a quick recipe for one item?")

                    selected = st.selectbox(
                        "Pick an ingredient:",
                        options=final_items
                    )

                    if st.button("Get Quick Recipe", use_container_width=True):
                        with st.spinner("Generating recipe..."):
                            recipe = generate_quick_recipe(selected, final_items)
                        st.markdown(recipe)

                except ValueError as e:
                    # API key missing
                    st.error(str(e))
                    st.info("👉 Open the **.env** file in this folder and paste your Gemini API key.")

                except Exception as e:
                    st.error(f"Something went wrong: {str(e)}")
                    st.info("Check that your API key in .env is correct and try again.")

    st.divider()

    # ── Spending summary ──────────────────────────────────────
    summary = get_summary()
    if summary:
        st.subheader("📊 Your grocery categories (all receipts)")
        st.caption("Full log saved to  data/spending_log.csv  — open it in Power BI for a dashboard.")
        for cat, count in sorted(summary.items(), key=lambda x: -x[1]):
            st.write(f"**{cat}** — {count} items")

else:
    # Show instructions when no file is uploaded yet
    st.info("👆 Upload a receipt photo above to get started.")

    with st.expander("Don't have a receipt handy? Try this test list instead."):
        st.markdown("""
You can skip the upload and type items directly.
Here's a sample grocery list to test with:

```
Tomatoes
Onions
Chicken breast
Basmati rice
Spinach
Milk
Eggs
Bread
Olive oil
Garlic
Lemon
Yogurt
```

Just paste this into the items box after uploading any image,
or ask me to add a manual entry mode to the app.
""")


# ── Sidebar ───────────────────────────────────────────────────
with st.sidebar:
    st.header("📋 How to use")
    st.markdown("""
1. **Upload** a grocery receipt photo
2. **Check** the detected items — fix any OCR mistakes
3. **Add** dietary preferences (optional)
4. **Click** Generate Meal Plan
5. **Enjoy** your 5-day plan + 2 recipes!
""")
    st.divider()

    st.header("⚙️ Setup checklist")
    st.markdown("""
- [ ] API key pasted in `.env` file
- [ ] Ran `pip install -r requirements.txt`
- [ ] Tesseract OCR installed (see README)
- [ ] Running with `streamlit run app.py`
""")
    st.divider()

    st.header("🔑 API key")
    st.markdown("""
Get your **free** Gemini key at:
[aistudio.google.com](https://aistudio.google.com)

Free tier: **1,500 calls/day**
No credit card needed.
""")
    st.divider()
    st.caption("Built with Python · Streamlit · Google Gemini · pytesseract")
