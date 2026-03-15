"""
Day 16 AM: Hypothesis Testing & Confidence Intervals.
Part A: Business hypothesis test (design, run, CI, effect size, interpretation).
Part B: Multiple comparison simulation + Bonferroni.
Part C Q2: ab_test(control, treatment, alpha=0.05).
"""

from pathlib import Path
from typing import Any

import numpy as np
from scipy import stats

OUT_DIR = Path(__file__).resolve().parent


# ---------- Part A: Business hypothesis test ----------

def part_a_business_test() -> dict[str, Any]:
    """
    Business question: Does the new checkout page (treatment) increase
    average session duration (minutes) compared to the old page (control)?

    H0: μ_control = μ_treatment  (no difference)
    H1: μ_treatment > μ_control  (one-tailed: new page has longer sessions)
    α = 0.05 (standard for business decisions; 5% false positive rate).
    Test: Two-sample t-test (comparing means of two independent groups).
    """
    np.random.seed(42)
    # Simulated session durations (minutes): control ~ N(4.2, 1.5^2), treatment ~ N(4.8, 1.5^2)
    control = np.random.normal(4.2, 1.5, 120)
    treatment = np.random.normal(4.8, 1.5, 115)

    # Two-sample t-test (one-tailed: treatment > control)
    result = stats.ttest_ind(treatment, control, alternative="greater")
    t_stat = result.statistic
    p_value = result.pvalue

    # 95% CI for difference in means (treatment - control)
    n1, n2 = len(treatment), len(control)
    diff = treatment.mean() - control.mean()
    pooled_std = np.sqrt(
        ((treatment.std() ** 2) * (n1 - 1) + (control.std() ** 2) * (n2 - 1))
        / (n1 + n2 - 2)
    )
    se_diff = pooled_std * np.sqrt(1 / n1 + 1 / n2)
    df = n1 + n2 - 2
    t_crit = stats.t.ppf(0.975, df)
    ci_low = diff - t_crit * se_diff
    ci_high = diff + t_crit * se_diff

    # Cohen's d
    cohens_d = diff / pooled_std

    reject_H0 = p_value < 0.05

    report = {
        "business_question": "Does the new checkout page increase average session duration?",
        "H0": "μ_control = μ_treatment",
        "H1": "μ_treatment > μ_control (one-tailed)",
        "alpha": 0.05,
        "test": "Two-sample t-test (independent samples, one-tailed)",
        "test_statistic": float(t_stat),
        "p_value": float(p_value),
        "reject_H0": reject_H0,
        "decision": "Reject H0" if reject_H0 else "Fail to reject H0",
        "ci_95": (float(ci_low), float(ci_high)),
        "effect_size_cohens_d": float(cohens_d),
        "control_mean": float(control.mean()),
        "treatment_mean": float(treatment.mean()),
        "stakeholder_interpretation": (
            "We tested whether the new checkout page leads to longer session times. "
            "On average, users on the new page stayed about {:.2f} minutes longer than on the old page. "
            "This difference is statistically significant (p = {:.4f}), meaning it is unlikely due to chance. "
            "The effect size (Cohen's d = {:.2f}) suggests a small-to-moderate practical effect. "
            "We recommend shipping the new page, but monitor conversion and bounce rates to confirm overall impact."
        ).format(diff, p_value, cohens_d),
    }
    return report


# ---------- Part B: Multiple comparison (p-hacking) ----------

def p_at_least_one_false_positive(n_tests: int = 20, alpha: float = 0.05) -> float:
    """P(at least one false positive) = 1 - (1 - α)^n when all nulls are true."""
    return 1 - (1 - alpha) ** n_tests


def simulate_multiple_comparisons(
    n_tests: int = 20,
    alpha: float = 0.05,
    n_simulations: int = 10_000,
    sample_size: int = 50,
) -> dict[str, Any]:
    """Simulate n_tests independent tests under H0; count proportion of runs with ≥1 rejection."""
    np.random.seed(123)
    rejections_per_run = []
    for _ in range(n_simulations):
        count = 0
        for _ in range(n_tests):
            # Under H0: two groups from same distribution
            g1 = np.random.normal(0, 1, sample_size)
            g2 = np.random.normal(0, 1, sample_size)
            _, p = stats.ttest_ind(g1, g2)
            if p < alpha:
                count += 1
        rejections_per_run.append(count)
    at_least_one = sum(1 for c in rejections_per_run if c >= 1) / n_simulations
    return {
        "theoretical_P_at_least_one_FP": p_at_least_one_false_positive(n_tests, alpha),
        "simulated_P_at_least_one_FP": at_least_one,
        "bonferroni_alpha": alpha / n_tests,
        "n_tests": n_tests,
        "alpha": alpha,
    }


# ---------- Part C: ab_test() ----------

def ab_test(
    control: np.ndarray,
    treatment: np.ndarray,
    alpha: float = 0.05,
) -> dict[str, Any]:
    """
    A/B test: check normality, select test (t-test or Mann-Whitney U),
    return statistic, p_value, reject_H0, effect_size, ci_95.
    """
    # Normality check (Shapiro-Wilk; use for small samples; for n>50 often use t-test anyway)
    _, p_control = stats.shapiro(control)
    _, p_treatment = stats.shapiro(treatment)
    normal_control = p_control > 0.05
    normal_treatment = p_treatment > 0.05
    use_parametric = normal_control and normal_treatment and len(control) >= 20 and len(treatment) >= 20

    if use_parametric:
        result = stats.ttest_ind(treatment, control, alternative="two-sided")
        stat = float(result.statistic)
        p_value = float(result.pvalue)
        n1, n2 = len(treatment), len(control)
        diff = treatment.mean() - control.mean()
        pooled_std = np.sqrt(
            ((treatment.std() ** 2) * (n1 - 1) + (control.std() ** 2) * (n2 - 1))
            / (n1 + n2 - 2)
        )
        se_diff = pooled_std * np.sqrt(1 / n1 + 1 / n2)
        df = n1 + n2 - 2
        t_crit = stats.t.ppf(1 - alpha / 2, df)
        ci_95 = (float(diff - t_crit * se_diff), float(diff + t_crit * se_diff))
        effect_size = float(diff / pooled_std) if pooled_std > 0 else 0.0
    else:
        result = stats.mannwhitneyu(treatment, control, alternative="two-sided")
        stat = float(result.statistic)
        p_value = float(result.pvalue)
        # Bootstrap-style CI for difference in medians (simplified: use percentile on differences)
        diffs = np.array([np.median(np.random.choice(treatment, len(treatment))) -
                          np.median(np.random.choice(control, len(control)))
                          for _ in range(1000)])
        ci_95 = (float(np.percentile(diffs, alpha / 2 * 100)),
                 float(np.percentile(diffs, (1 - alpha / 2) * 100)))
        # Effect size: rank-biserial approx or (median_t - median_c) / pooled_mad
        med_t, med_c = np.median(treatment), np.median(control)
        mad = np.median(np.abs(np.concatenate([treatment, control]) - np.median(np.concatenate([treatment, control]))))
        effect_size = float((med_t - med_c) / mad) if mad > 0 else 0.0

    return {
        "statistic": stat,
        "p_value": p_value,
        "reject_H0": p_value < alpha,
        "effect_size": effect_size,
        "ci_95": ci_95,
        "test_used": "ttest_ind" if use_parametric else "mannwhitneyu",
        "normal_control": normal_control,
        "normal_treatment": normal_treatment,
    }


def main() -> None:
    print("=== Part A: Business hypothesis test ===\n")
    report_a = part_a_business_test()
    for k, v in report_a.items():
        print(f"{k}: {v}")

    print("\n=== Part B: Multiple comparison ===\n")
    report_b = simulate_multiple_comparisons()
    for k, v in report_b.items():
        print(f"{k}: {v}")

    print("\n=== Part C: ab_test() demo ===\n")
    np.random.seed(99)
    c = np.random.normal(10, 2, 60)
    t = np.random.normal(10.5, 2, 55)
    result = ab_test(c, t)
    for k, v in result.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
