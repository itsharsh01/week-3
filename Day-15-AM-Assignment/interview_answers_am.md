# Day 15 AM Part C — Interview Ready

## Q1 — Base rate fallacy (medical test)

**Setup:** Disease prevalence 1 in 10,000 (base rate = 0.0001). Test is 99% accurate (sensitivity and specificity ≈ 99%).

- **True positives:** 0.0001 × 0.99 ≈ 0.000099  
- **False positives:** (1 − 0.0001) × 0.01 ≈ 0.009999  
- So among positive results, false positives vastly outnumber true positives. P(disease | positive) = true positives / (true + false positives) ≈ 0.000099 / (0.000099 + 0.009999) ≈ 0.01 (about 1%).

**Why:** The base rate is so low that the 1% false-positive rate applied to the huge healthy population produces many more positive results than the 99% sensitivity applied to the tiny diseased population. So a "99% accurate" test still gives mostly false positives when the disease is rare. That’s the base rate fallacy: ignoring the prior (prevalence) and over-weighting the test result.

---

## Q2 — simulate_clt()

Implemented in `probability_assignment.py`: `simulate_clt(distribution, params, n_samples, n_simulations)` takes any scipy.stats distribution (e.g. `stats.expon`, `params={"scale": 2}`), draws `n_samples` per simulation, computes the sample mean, repeats `n_simulations` times, and returns the array of sample means plus theoretical normal mean and std (μ, σ/√n). The notebook overlays the histogram of sample means with the theoretical normal curve.

---

## Q3 — Exponential mean and what to show instead

**Why mean is misleading:** For an exponential distribution, the mean equals the scale parameter; a few very large purchases can dominate the mean. The distribution is right-skewed, so the mean is pulled above the "typical" purchase; many customers spend less than the mean. Reporting only the mean can overstate what a typical customer spends and hide the high variance and skew.

**What to show instead:** Report median (more robust), percentiles (e.g. 25th, 50th, 75th, 90th), or the full distribution. For investors, revenue or total spend might be more relevant than "average purchase"; also show distribution of spend per customer (histogram or CDF) and possibly segment by cohort or product.
