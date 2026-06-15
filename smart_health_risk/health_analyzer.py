"""
health_analyzer.py
Core logic: BMI calculation, disease risk scoring, and recommendations.
Uses only Python standard library (no external packages).
"""


# ─────────────────────────────────────────────────────────────
#  BMI
# ─────────────────────────────────────────────────────────────

def calculate_bmi(weight_kg: float, height_cm: float) -> float:
    """Return BMI rounded to 2 decimal places."""
    if height_cm <= 0:
        raise ValueError("Height must be greater than zero.")
    height_m = height_cm / 100
    return round(weight_kg / (height_m ** 2), 2)


def bmi_category(bmi: float) -> str:
    """Return a human-readable BMI category string."""
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25.0:
        return "Normal"
    elif bmi < 30.0:
        return "Overweight"
    else:
        return "Obese"


# ─────────────────────────────────────────────────────────────
#  Risk Scoring  (rule-based, 0–100 scale)
# ─────────────────────────────────────────────────────────────

def risk_score(params: dict) -> dict:
    """
    Calculate disease risk scores (0–100) for four conditions.

    Parameters expected in `params`
    --------------------------------
    age           : int   – years
    bmi           : float – kg/m²
    systolic_bp   : int   – mmHg  (e.g. 120)
    blood_sugar   : int   – fasting mg/dL
    activity_days : int   – days/week with ≥30 min moderate exercise
    smoker        : bool
    family_history: list  – subset of ["diabetes","hypertension",
                                        "heart disease","obesity"]
    """
    age    = params["age"]
    bmi    = params["bmi"]
    bp     = params["systolic_bp"]
    sugar  = params["blood_sugar"]
    active = params["activity_days"]
    smoke  = params["smoker"]
    fhist  = [c.lower() for c in params.get("family_history", [])]

    scores = {
        "Diabetes":               0,
        "Hypertension":           0,
        "Cardiovascular Disease": 0,
        "Obesity":                0,
    }

    # ── Diabetes ──────────────────────────────────────────────
    if sugar >= 126:     scores["Diabetes"] += 40
    elif sugar >= 100:   scores["Diabetes"] += 20
    if bmi >= 30:        scores["Diabetes"] += 20
    elif bmi >= 25:      scores["Diabetes"] += 10
    if age >= 45:        scores["Diabetes"] += 15
    if active < 3:       scores["Diabetes"] += 10
    if "diabetes" in fhist:         scores["Diabetes"] += 15

    # ── Hypertension ──────────────────────────────────────────
    if bp >= 140:        scores["Hypertension"] += 40
    elif bp >= 130:      scores["Hypertension"] += 20
    if bmi >= 30:        scores["Hypertension"] += 15
    if age >= 50:        scores["Hypertension"] += 15
    if smoke:            scores["Hypertension"] += 15
    if "hypertension" in fhist:     scores["Hypertension"] += 15

    # ── Cardiovascular Disease ────────────────────────────────
    if age >= 55:        scores["Cardiovascular Disease"] += 20
    if bp >= 140:        scores["Cardiovascular Disease"] += 20
    if smoke:            scores["Cardiovascular Disease"] += 25
    if bmi >= 30:        scores["Cardiovascular Disease"] += 10
    if active < 2:       scores["Cardiovascular Disease"] += 15
    if "heart disease" in fhist:    scores["Cardiovascular Disease"] += 10

    # ── Obesity ───────────────────────────────────────────────
    if bmi >= 35:        scores["Obesity"] += 50
    elif bmi >= 30:      scores["Obesity"] += 30
    elif bmi >= 25:      scores["Obesity"] += 10
    if active < 2:       scores["Obesity"] += 20
    if age >= 40:        scores["Obesity"] += 10
    if "obesity" in fhist:          scores["Obesity"] += 20

    # Cap at 100
    return {k: min(v, 100) for k, v in scores.items()}


def risk_level(score: int) -> str:
    """Convert a numeric risk score to a text category."""
    if score < 25:   return "Low"
    elif score < 55: return "Moderate"
    elif score < 75: return "High"
    else:            return "Very High"


def overall_risk(scores: dict) -> str:
    """Return the highest single-disease risk level as the overall level."""
    max_score = max(scores.values())
    return risk_level(max_score)


# ─────────────────────────────────────────────────────────────
#  Recommendations
# ─────────────────────────────────────────────────────────────

def recommendations(params: dict, scores: dict) -> list:
    """Return a list of personalised health tip strings."""
    tips = []
    bmi    = params["bmi"]
    active = params["activity_days"]
    smoke  = params["smoker"]
    sugar  = params["blood_sugar"]
    bp     = params["systolic_bp"]

    if bmi >= 30:
        tips.append("Your BMI indicates obesity — aim for gradual, sustainable weight loss "
                    "through a calorie-controlled diet and daily movement.")
    elif bmi >= 25:
        tips.append("You are in the overweight range. A balanced diet and regular exercise "
                    "will help you reach a healthier BMI.")
    elif bmi < 18.5:
        tips.append("Your BMI is below the healthy range. Consider consulting a nutritionist "
                    "to increase caloric intake with nutrient-dense foods.")

    if active < 2:
        tips.append("You are largely sedentary. Start with short 20-minute walks daily and "
                    "build up to 150+ minutes of moderate activity per week.")
    elif active < 4:
        tips.append("Aim for at least 4–5 active days per week — brisk walking, cycling, "
                    "or swimming all count.")

    if smoke:
        tips.append("Smoking is a major driver of cardiovascular and hypertension risk. "
                    "Speak to your doctor about a cessation plan.")

    if sugar >= 126:
        tips.append("Your fasting blood sugar is in the diabetic range. Please consult a "
                    "doctor promptly for an HbA1c test and treatment guidance.")
    elif sugar >= 100:
        tips.append("Pre-diabetic blood sugar detected. Reduce refined carbs and sugar; "
                    "increase fibre, and monitor regularly.")

    if bp >= 140:
        tips.append("Your blood pressure is in the hypertensive range. Reduce sodium, manage "
                    "stress, and seek medical advice.")
    elif bp >= 130:
        tips.append("Elevated blood pressure (pre-hypertension). Limit salt, alcohol, and "
                    "try relaxation techniques like deep breathing.")

    if scores.get("Cardiovascular Disease", 0) >= 50:
        tips.append("Your cardiovascular risk is significant — schedule a screening with your "
                    "doctor and consider a lipid profile test.")

    if not tips:
        tips.append("Excellent! Your indicators look healthy. Keep up your good habits and "
                    "attend routine check-ups every 1–2 years.")

    return tips
