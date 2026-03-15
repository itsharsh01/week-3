# Day 16 AM Part C — Interview Ready

## Q1 — P-value vs confidence interval (for a product manager)

- **P-value:** “If there were truly no difference between the two variants, the probability of seeing a difference at least as large as the one we observed is p.” So a small p (e.g. &lt; 0.05) suggests the data are inconsistent with “no difference.” It answers: *Is the effect statistically significant?*
- **Confidence interval (e.g. 95% CI):** A range of plausible values for the true difference (e.g. difference in means). If the interval excludes 0, we reject “no difference” at that level. The interval also shows *how big* the effect might be (upper and lower bounds). It answers: *What is the size of the effect and its uncertainty?*
- **When each is more useful:** Use the **p-value** when the main question is a yes/no “should we call this a win?” (e.g. ship or not). Use the **confidence interval** when you need to communicate magnitude and uncertainty (e.g. “we expect a lift between 2% and 8%”) or when you care about clinical/business significance, not just statistical significance.

---

## Q2 — ab_test(control, treatment, alpha=0.05)

See **hypothesis_test_assignment.py**: function `ab_test(control, treatment, alpha=0.05)`.

- **(a) Normality:** Shapiro–Wilk on each group; if both groups are normal (p &gt; 0.05) and sample sizes are adequate, use the t-test; otherwise use Mann–Whitney U.
- **(b) Test selection:** Parametric (two-sample t-test) vs non-parametric (Mann–Whitney U) based on the normality check and sample size.
- **(c) Return:** `{'statistic', 'p_value', 'reject_H0', 'effect_size', 'ci_95'}` (plus `test_used`, `normal_control`, `normal_treatment` for transparency).

---

## Q3 — p = 0.04, effect size 0.02 (very small); manager says “ship it.” Three questions to ask before agreeing

1. **“What is the minimum effect size we need for this change to be worth the cost (e.g. engineering, risk)?”** If 0.02 is below that threshold, we may not want to ship despite p &lt; 0.05.
2. **“Is the confidence interval for the effect entirely above that minimum?”** If the CI includes zero or only tiny effects, we might be underpowered or the true effect could be negligible.
3. **“Can we run the experiment longer or increase sample size to narrow the CI and confirm the effect?”** With a very small effect, we want to reduce the chance we’re chasing noise (p-hacking / regression to the mean) and ensure the result is replicable.

These separate *statistical* significance (p) from *practical* significance (effect size and business impact).
