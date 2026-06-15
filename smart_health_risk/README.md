# Smart Health Risk Analysis System

A command-line Python application that assesses an individual's risk for four chronic diseases — **Diabetes**, **Hypertension**, **Cardiovascular Disease**, and **Obesity** — based on simple health parameters.

---

## Features

| Feature | Details |
|---|---|
| Disease risk scoring | Rule-based model; scores 0–100 per disease |
| Risk levels | Low / Moderate / High / Very High |
| Personalised tips | Based on the user's specific readings |
| User accounts | Registration & login stored in `users.json` |
| History tracking | Every result is saved; view past analyses |
| Trend comparison | First vs latest check side-by-side |
| ASCII bar charts | Visual risk bars printed in the terminal |

---

## Requirements

- **Python 3.9+**
- **No external packages** — uses only the standard library (`json`, `os`, `datetime`, `unittest`)

---

## Project Structure

```
smart_health_risk/
├── main.py               # Entry point & CLI menus
├── health_analyzer.py    # BMI, risk scoring, recommendations
├── user_manager.py       # User registration, login, JSON storage
├── report.py             # ASCII reports, history table, trend view
├── test_health_analyzer.py  # Unit tests (unittest)
└── README.md
```

---

## How to Run

```bash
cd smart_health_risk
python main.py
```

Sample session:
```
============================================================
      SMART HEALTH RISK ANALYSIS SYSTEM
============================================================
  Assess your risk for Diabetes, Hypertension,
  Cardiovascular Disease, and Obesity.
============================================================

  ── Welcome ──────────────────────────────────────────
    1. Login
    2. Register
    3. Exit
  Choose an option: 2
  Username: alice
  ✓ Account created. Welcome, alice!
```

---

## Running Tests

```bash
python -m unittest test_health_analyzer -v
```

Tests cover: BMI calculation, BMI categories, risk scoring (including boundary values), risk levels, overall risk, and recommendation generation.

---

## Health Parameters Collected

| Parameter | Range |
|---|---|
| Age | 1 – 120 years |
| Weight | 20 – 300 kg |
| Height | 50 – 250 cm |
| Systolic Blood Pressure | 70 – 220 mmHg |
| Fasting Blood Sugar | 50 – 600 mg/dL |
| Physical Activity | 0 – 7 days/week |
| Smoker | Yes / No |
| Family History | Diabetes, Hypertension, Heart Disease, Obesity |

---

## Risk Score Thresholds

| Level | Score Range |
|---|---|
| Low | 0 – 24 |
| Moderate | 25 – 54 |
| High | 55 – 74 |
| Very High | 75 – 100 |

---

## Data Storage

User data is stored locally in `users.json` (auto-created on first run). No network connection or database required.
