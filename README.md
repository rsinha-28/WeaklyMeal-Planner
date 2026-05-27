# 🛒 Grocery Receipt → Meal Planner
### Powered by Google Gemini (Free) · No credit card needed

---

## ⚡ Quick Start — 4 steps

### Step 1 — Paste your API key

Open the `.env` file in this folder.
Replace `paste-your-key-here` with your actual Gemini key:

```
GEMINI_API_KEY=AIzaSy...your-actual-key-here
```

Get a free key at 👉 https://aistudio.google.com → "Get API Key"
No credit card needed. 1,500 free calls per day.

---

### Step 2 — Install Tesseract OCR (one-time)

Tesseract reads text from your receipt photo.
It is NOT a pip package — install it separately:

**Windows:**
- Download from: https://github.com/UB-Mannheim/tesseract/wiki
- Run the `.exe` installer — keep all default settings
- Restart VS Code / terminal after install

**Mac:**
```
brew install tesseract
```

**Linux:**
```
sudo apt install tesseract-ocr
```

---

### Step 3 — Install Python packages

Open a terminal in this folder and run:

```
pip install -r requirements.txt
```

---

### Step 4 — Run the app

```
streamlit run app.py
```

Your browser opens at **http://localhost:8501** ✅

---

## 📁 What each file does

```
grocery-gemini/
│
├── app.py              ← Main app — run this
├── ocr.py              ← Reads receipt photo → item list
├── llm.py              ← Sends items to Gemini → meal plan
├── tracker.py          ← Saves items to CSV (for Power BI)
│
├── .env                ← YOUR API KEY GOES HERE (never share)
├── requirements.txt    ← pip install -r requirements.txt
├── .gitignore          ← keeps .env off GitHub
│
├── receipts/           ← put test photos here
└── data/               ← spending_log.csv saved here
```

---

## 🔧 Troubleshooting

| Problem | Fix |
|---|---|
| `pytesseract is not installed or not in PATH` | Install Tesseract OCR (Step 2 above) |
| `Gemini API key not found` | Open `.env` and paste your key correctly |
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` again |
| Bad OCR — wrong items detected | Edit items in the text box before generating |
| Receipt photo not working | Use a flat, well-lit photo; try increasing brightness |

---

## 🔒 Keep your API key safe

- Key goes ONLY in the `.env` file
- Never paste it in chat, email, or code
- Never upload `.env` to GitHub (the `.gitignore` file prevents this)
- If you accidentally share it — delete it immediately at aistudio.google.com and create a new one
