# Day 16 AM Part A — Hypothesis Test Design

## Business question (one sentence)

Does the new checkout page (treatment) increase average session duration compared to the old page (control)?

## Hypotheses and test setup

- **H₀:** μ_control = μ_treatment (no difference in mean session duration).
- **H₁:** μ_treatment > μ_control (one-tailed: new page has longer sessions).
- **One-tailed vs two-tailed:** One-tailed — we care only if the new page *increases* duration; we are not testing for a decrease.
- **α = 0.05.** Justification: Standard for business A/B tests; balances false positives (shipping a non-improvement) with false negatives (missing a real improvement). 5% is widely accepted in industry.

## Test selection and justification

- **Test:** Two-sample independent-samples t-test.
- **Justification:** We compare means of two independent groups (control vs treatment). Session duration is continuous. Sample sizes are large enough (n > 30 per group) for the t-test to be robust even if normality is only approximate. We assume roughly equal variance (pooled standard error); if needed, Welch’s t-test can be used.

## Data

Simulated data: control ~ N(4.2, 1.5²), treatment ~ N(4.8, 1.5²), n_control = 120, n_treatment = 115. (Alternatively, use a Kaggle dataset and replace the simulated arrays in the script.)

## Results (run script or notebook)

- Test statistic, p-value, decision (reject/fail to reject H₀).
- 95% confidence interval for (μ_treatment − μ_control).
- Effect size: Cohen’s d.
- **Stakeholder interpretation (5 sentences):** See script output or notebook narrative — we summarize the question, the observed difference, statistical significance, effect size, and a recommendation (e.g. ship new page but monitor conversion/bounce).

All computations are in `hypothesis_test_assignment.py` (function `part_a_business_test()`) and in `hypothesis_test_notebook.ipynb`.
