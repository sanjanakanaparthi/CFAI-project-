"""
report.py
Generates text reports and ASCII bar charts for health risk analysis.
Uses only Python standard library.
"""

from health_analyzer import risk_level, overall_risk

# Colour codes for terminals that support ANSI
_COLOURS = {
    "Low":       "\033[92m",   # green
    "Moderate":  "\033[93m",   # yellow
    "High":      "\033[91m",   # red
    "Very High": "\033[95m",   # magenta
    "reset":     "\033[0m",
}

_LINE = "=" * 60


def _coloured(text: str, level: str) -> str:
    col = _COLOURS.get(level, "")
    rst = _COLOURS["reset"]
    return f"{col}{text}{rst}"


def _bar(score: int, width: int = 28) -> str:
    """Return an ASCII progress bar with percentage."""
    filled = round(score / 100 * width)
    bar    = "█" * filled + "░" * (width - filled)
    return f"[{bar}] {score:>3}%"


# ─────────────────────────────────────────────────────────────
#  Main report
# ─────────────────────────────────────────────────────────────

def print_report(username: str, params: dict, scores: dict, tips: list) -> None:
    """Print the full health-risk report to stdout."""
    print(f"\n{_LINE}")
    print(f"  HEALTH RISK REPORT  —  {username.upper()}")
    print(_LINE)

    # ── Health parameters ─────────────────────────────────────
    print("\n  ── Your Health Parameters ──────────────────────────")
    print(f"  Age              : {params['age']} years")
    print(f"  Weight / Height  : {params['weight']} kg / {params['height']} cm")
    print(f"  BMI              : {params['bmi']}  ({params['bmi_category']})")
    print(f"  Systolic BP      : {params['systolic_bp']} mmHg")
    print(f"  Fasting Sugar    : {params['blood_sugar']} mg/dL")
    print(f"  Activity         : {params['activity_days']} day(s)/week")
    print(f"  Smoker           : {'Yes' if params['smoker'] else 'No'}")

    fh = params.get("family_history", [])
    print(f"  Family History   : {', '.join(fh).title() if fh else 'None'}")

    # ── Disease risk scores ───────────────────────────────────
    print("\n  ── Disease Risk Scores ─────────────────────────────")
    for disease, score in scores.items():
        level  = risk_level(score)
        label  = f"{disease:<26}"
        colour = _coloured(f"{level:<10}", level)
        print(f"  {label} {colour} {_bar(score)}")

    # ── Overall risk ──────────────────────────────────────────
    overall = overall_risk(scores)
    print(f"\n  Overall Risk Level : {_coloured(overall, overall)}")

    # ── Recommendations ───────────────────────────────────────
    print("\n  ── Personalised Recommendations ────────────────────")
    for i, tip in enumerate(tips, 1):
        # Wrap long tips at ~56 chars
        words, line, lines = tip.split(), "", []
        for w in words:
            if len(line) + len(w) + 1 > 54:
                lines.append(line)
                line = w
            else:
                line = (line + " " + w).strip()
        if line:
            lines.append(line)
        prefix = f"  {i}. "
        indent = "     "
        print(prefix + lines[0])
        for l in lines[1:]:
            print(indent + l)

    print(f"\n{_LINE}\n")


# ─────────────────────────────────────────────────────────────
#  History table
# ─────────────────────────────────────────────────────────────

def print_history(history: list) -> None:
    """Print a summary table of all past analyses."""
    if not history:
        print("\n  No history found.\n")
        return

    header = f"  {'#':<4} {'Date':<18} {'Diabetes':>9} {'Hypertension':>13} {'CVD':>5} {'Obesity':>8}"
    print(f"\n{header}")
    print("  " + "─" * 62)

    for idx, entry in enumerate(history, 1):
        s = entry["scores"]
        d  = s.get("Diabetes", 0)
        h  = s.get("Hypertension", 0)
        cv = s.get("Cardiovascular Disease", 0)
        ob = s.get("Obesity", 0)
        print(
            f"  {idx:<4} {entry['date']:<18}"
            f" {d:>9} {h:>13} {cv:>5} {ob:>8}"
        )
    print()


def print_comparison(history: list) -> None:
    """Print a side-by-side risk trend between first and latest entry."""
    if len(history) < 2:
        print("\n  Need at least 2 entries for a trend comparison.\n")
        return

    first  = history[0]
    latest = history[-1]

    print(f"\n  ── Risk Trend: First vs Latest ─────────────────────")
    print(f"  {'Disease':<26} {'First':>8}  {'Latest':>8}  {'Change':>8}")
    print("  " + "─" * 56)

    for disease in first["scores"]:
        f_val = first["scores"].get(disease, 0)
        l_val = latest["scores"].get(disease, 0)
        diff  = l_val - f_val
        arrow = ("▲" if diff > 0 else ("▼" if diff < 0 else "─"))
        sign  = "+" if diff > 0 else ""
        print(f"  {disease:<26} {f_val:>8}  {l_val:>8}  {sign}{diff:>6} {arrow}")

    print(f"\n  First check : {first['date']}")
    print(f"  Latest check: {latest['date']}\n")
