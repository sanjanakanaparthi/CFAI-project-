"""
test_health_analyzer.py
Unit tests for health_analyzer.py using only the standard library (unittest).

Run:
    python -m unittest test_health_analyzer -v
"""

import unittest
from health_analyzer import (
    calculate_bmi,
    bmi_category,
    risk_score,
    risk_level,
    overall_risk,
    recommendations,
)


class TestCalculateBMI(unittest.TestCase):
    def test_normal_bmi(self):
        bmi = calculate_bmi(70, 175)
        self.assertAlmostEqual(bmi, 22.86, places=1)

    def test_obese_bmi(self):
        bmi = calculate_bmi(100, 170)
        self.assertGreater(bmi, 30)

    def test_zero_height_raises(self):
        with self.assertRaises((ValueError, ZeroDivisionError)):
            calculate_bmi(70, 0)

    def test_rounding(self):
        bmi = calculate_bmi(80, 180)
        # result should be a float with ≤ 2 decimal places
        self.assertEqual(bmi, round(bmi, 2))


class TestBMICategory(unittest.TestCase):
    def test_underweight(self):
        self.assertEqual(bmi_category(17.0), "Underweight")

    def test_normal(self):
        self.assertEqual(bmi_category(22.5), "Normal")

    def test_overweight(self):
        self.assertEqual(bmi_category(27.0), "Overweight")

    def test_obese(self):
        self.assertEqual(bmi_category(32.0), "Obese")

    def test_boundary_normal_to_overweight(self):
        self.assertEqual(bmi_category(25.0), "Overweight")

    def test_boundary_underweight_to_normal(self):
        self.assertEqual(bmi_category(18.5), "Normal")


class TestRiskScore(unittest.TestCase):
    def _base_params(self, **overrides):
        params = {
            "age":            30,
            "bmi":            22.0,
            "systolic_bp":    115,
            "blood_sugar":    90,
            "activity_days":  5,
            "smoker":         False,
            "family_history": [],
        }
        params.update(overrides)
        return params

    def test_healthy_person_low_scores(self):
        scores = risk_score(self._base_params())
        for v in scores.values():
            self.assertLess(v, 25, msg=f"Expected low score, got {v}")

    def test_high_blood_sugar_raises_diabetes(self):
        scores = risk_score(self._base_params(blood_sugar=130))
        self.assertGreaterEqual(scores["Diabetes"], 40)

    def test_high_bp_raises_hypertension(self):
        scores = risk_score(self._base_params(systolic_bp=145))
        self.assertGreaterEqual(scores["Hypertension"], 40)

    def test_smoker_raises_cvd(self):
        scores_smoke = risk_score(self._base_params(smoker=True))
        scores_clean = risk_score(self._base_params(smoker=False))
        self.assertGreater(
            scores_smoke["Cardiovascular Disease"],
            scores_clean["Cardiovascular Disease"],
        )

    def test_obese_bmi_raises_obesity(self):
        scores = risk_score(self._base_params(bmi=36.0))
        self.assertGreaterEqual(scores["Obesity"], 50)

    def test_family_history_diabetes_increases_score(self):
        with_fh    = risk_score(self._base_params(family_history=["diabetes"]))
        without_fh = risk_score(self._base_params())
        self.assertGreater(with_fh["Diabetes"], without_fh["Diabetes"])

    def test_scores_capped_at_100(self):
        # Throw every risk factor at once
        worst = self._base_params(
            age=70, bmi=40, systolic_bp=180, blood_sugar=200,
            activity_days=0, smoker=True,
            family_history=["diabetes", "hypertension", "heart disease", "obesity"],
        )
        scores = risk_score(worst)
        for k, v in scores.items():
            self.assertLessEqual(v, 100, msg=f"{k} score exceeded 100: {v}")

    def test_scores_are_non_negative(self):
        scores = risk_score(self._base_params())
        for k, v in scores.items():
            self.assertGreaterEqual(v, 0, msg=f"{k} score is negative: {v}")


class TestRiskLevel(unittest.TestCase):
    def test_low(self):
        self.assertEqual(risk_level(10), "Low")

    def test_moderate(self):
        self.assertEqual(risk_level(40), "Moderate")

    def test_high(self):
        self.assertEqual(risk_level(60), "High")

    def test_very_high(self):
        self.assertEqual(risk_level(80), "Very High")

    def test_boundary_low_moderate(self):
        self.assertEqual(risk_level(25), "Moderate")

    def test_boundary_moderate_high(self):
        self.assertEqual(risk_level(55), "High")

    def test_boundary_high_very_high(self):
        self.assertEqual(risk_level(75), "Very High")


class TestOverallRisk(unittest.TestCase):
    def test_returns_worst_level(self):
        scores = {
            "Diabetes": 10,
            "Hypertension": 80,
            "Cardiovascular Disease": 30,
            "Obesity": 55,
        }
        self.assertEqual(overall_risk(scores), "Very High")

    def test_all_low(self):
        scores = {"Diabetes": 5, "Hypertension": 10, "Cardiovascular Disease": 5, "Obesity": 0}
        self.assertEqual(overall_risk(scores), "Low")


class TestRecommendations(unittest.TestCase):
    def _base(self, **overrides):
        p = {
            "bmi": 22.0,
            "activity_days": 5,
            "smoker": False,
            "blood_sugar": 90,
            "systolic_bp": 115,
        }
        p.update(overrides)
        s = {"Cardiovascular Disease": 10}
        return p, s

    def test_healthy_gets_positive_tip(self):
        params, scores = self._base()
        tips = recommendations(params, scores)
        self.assertTrue(any("Excellent" in t or "Great" in t or "healthy" in t for t in tips))

    def test_high_bmi_tip(self):
        params, scores = self._base(bmi=32.0)
        tips = recommendations(params, scores)
        self.assertTrue(any("BMI" in t or "weight" in t.lower() or "obesity" in t.lower() for t in tips))

    def test_smoker_tip(self):
        params, scores = self._base(smoker=True)
        tips = recommendations(params, scores)
        self.assertTrue(any("smok" in t.lower() for t in tips))

    def test_high_sugar_tip(self):
        params, scores = self._base(blood_sugar=130)
        tips = recommendations(params, scores)
        self.assertTrue(any("sugar" in t.lower() or "diabet" in t.lower() or "blood" in t.lower() for t in tips))

    def test_always_returns_list(self):
        params, scores = self._base()
        tips = recommendations(params, scores)
        self.assertIsInstance(tips, list)
        self.assertGreater(len(tips), 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
