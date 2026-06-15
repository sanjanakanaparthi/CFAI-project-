"""
main.py
Smart Health Risk Analysis System — command-line interface.

Run:
    python main.py

Requires only the Python standard library.
"""

from health_analyzer import calculate_bmi, bmi_category, risk_score, recommendations
from user_manager    import register_user, user_exists, save_result, get_history
from report          import print_report, print_history, print_comparison


# ─────────────────────────────────────────────────────────────
#  Input helpers
# ─────────────────────────────────────────────────────────────

def ask_float(prompt: str, lo: float = 0.0, hi: float = 9999.0) -> float:
    """Prompt for a float within [lo, hi]. Loops until valid."""
    while True:
        try:
            val = float(input(f"  {prompt}: ").strip())
            if lo <= val <= hi:
                return val
            print(f"  ✗ Please enter a value between {lo} and {hi}.")
        except ValueError:
            print("  ✗ That doesn't look like a number. Try again.")


def ask_int(prompt: str, lo: int = 0, hi: int = 9999) -> int:
    """Prompt for an integer within [lo, hi]."""
    return int(ask_float(prompt, lo, hi))


def ask_bool(prompt: str) -> bool:
    """Prompt for a yes/no answer. Returns True for yes."""
    while True:
        ans = input(f"  {prompt} (y/n): ").strip().lower()
        if ans in ("y", "yes"):
            return True
        if ans in ("n", "no"):
            return False
        print("  ✗ Please type  y  or  n.")


def ask_choice(prompt: str, options: list) -> str:
    """
    Show a numbered menu and return the chosen option string.
    'options' is a list of human-readable strings.
    """
    while True:
        for i, opt in enumerate(options, 1):
            print(f"    {i}. {opt}")
        raw = input(f"  {prompt}: ").strip()
        if raw.isdigit() and 1 <= int(raw) <= len(options):
            return options[int(raw) - 1]
        print(f"  ✗ Enter a number from 1 to {len(options)}.")


def ask_family_history() -> list:
    """Let the user pick zero or more family-history conditions."""
    options = ["Diabetes", "Hypertension", "Heart Disease", "Obesity"]
    print("\n  Family history — enter numbers separated by commas, or press Enter for none:")
    for i, opt in enumerate(options, 1):
        print(f"    {i}. {opt}")
    raw = input("  Your choices: ").strip()
    selected = []
    if raw:
        for ch in raw.split(","):
            ch = ch.strip()
            if ch.isdigit() and 1 <= int(ch) <= len(options):
                item = options[int(ch) - 1].lower()
                if item not in selected:
                    selected.append(item)
    return selected


# ─────────────────────────────────────────────────────────────
#  Authentication
# ─────────────────────────────────────────────────────────────

def login_or_register() -> str:
    """Handle login / registration flow and return the active username."""
    print("\n  ── Welcome ──────────────────────────────────────────")
    action = ask_choice("Choose an option", ["Login", "Register", "Exit"])

    if action == "Exit":
        print("\n  Goodbye!\n")
        raise SystemExit

    username = input("  Username: ").strip()
    if not username:
        print("  ✗ Username cannot be empty.")
        return login_or_register()

    if action == "Register":
        if register_user(username):
            print(f"  ✓ Account created. Welcome, {username}!")
            return username
        else:
            print(f"  ✗ Username '{username}' is already taken.")
            return login_or_register()
    else:  # Login
        if user_exists(username):
            print(f"  ✓ Welcome back, {username}!")
            return username
        else:
            print(f"  ✗ User '{username}' not found. Please register first.")
            return login_or_register()


# ─────────────────────────────────────────────────────────────
#  Health parameter collection
# ─────────────────────────────────────────────────────────────

def collect_params() -> dict:
    """Interactively collect health parameters from the user."""
    print("\n  ── Enter Your Health Parameters ─────────────────────")
    age         = ask_int("Age (years)", 1, 120)
    weight      = ask_float("Weight (kg)", 20, 300)
    height      = ask_float("Height (cm)", 50, 250)
    systolic_bp = ask_int("Systolic Blood Pressure (mmHg)", 70, 220)
    blood_sugar = ask_int("Fasting Blood Sugar (mg/dL)", 50, 600)
    activity    = ask_int("Physical activity (days per week)", 0, 7)
    smoker      = ask_bool("Do you smoke?")
    family_hist = ask_family_history()

    bmi = calculate_bmi(weight, height)
    print(f"\n  Calculated BMI: {bmi}  ({bmi_category(bmi)})")

    return {
        "age":            age,
        "weight":         weight,
        "height":         height,
        "bmi":            bmi,
        "bmi_category":   bmi_category(bmi),
        "systolic_bp":    systolic_bp,
        "blood_sugar":    blood_sugar,
        "activity_days":  activity,
        "smoker":         smoker,
        "family_history": family_hist,
    }


# ─────────────────────────────────────────────────────────────
#  Main menu
# ─────────────────────────────────────────────────────────────

def main_menu(username: str) -> None:
    """Display the main menu and dispatch user choices."""
    menu_items = [
        "Run Health Risk Analysis",
        "View My History",
        "View Risk Trend (first vs latest)",
        "Logout",
    ]

    while True:
        print(f"\n  ── Main Menu  [{username}] ──────────────────────────")
        action = ask_choice("Choose an option", menu_items)

        if action == "Run Health Risk Analysis":
            params = collect_params()
            scores = risk_score(params)
            tips   = recommendations(params, scores)
            print_report(username, params, scores, tips)
            save_result(username, params, scores)
            print("  ✓ Result saved to your history.")

        elif action == "View My History":
            history = get_history(username)
            print_history(history)

        elif action == "View Risk Trend (first vs latest)":
            history = get_history(username)
            print_comparison(history)

        elif action == "Logout":
            print(f"\n  Goodbye, {username}!\n")
            break


# ─────────────────────────────────────────────────────────────
#  Entry point
# ─────────────────────────────────────────────────────────────

def main() -> None:
    print("\n" + "=" * 60)
    print("      SMART HEALTH RISK ANALYSIS SYSTEM")
    print("=" * 60)
    print("  Assess your risk for Diabetes, Hypertension,")
    print("  Cardiovascular Disease, and Obesity.")
    print("=" * 60)

    username = login_or_register()
    main_menu(username)


if __name__ == "__main__":
    main()
