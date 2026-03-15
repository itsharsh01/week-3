# Day 16 AM Part B — Multiple comparison (p-hacking) and Bonferroni

## Problem

If we run **20 independent** A/B tests, each at **α = 0.05**, and in truth **all null hypotheses are true**, what is the probability of **at least one false positive**?

## Theoretical answer

- P(no false positive in one test) = 1 − α = 0.95.
- For 20 independent tests under the null: P(no FP in any) = (0.95)^20 ≈ **0.358**.
- So **P(at least one false positive) = 1 − (0.95)^20 ≈ 0.642** (about 64%).

So we have a high chance of “finding” at least one “significant” result by chance when we run many tests.

## Simulation

The script `hypothesis_test_assignment.py` runs `simulate_multiple_comparisons(n_tests=20, alpha=0.05, n_simulations=10_000)`. For each simulation it runs 20 independent two-sample t-tests (both groups from the same distribution, so H₀ true). It counts the proportion of simulation runs where at least one test rejects. This proportion should be close to **1 − (0.95)^20 ≈ 0.642**.

## Bonferroni correction

- **Corrected α:** α_corrected = α / n = 0.05 / 20 = **0.0025**.
- Reject H₀ only when p &lt; 0.0025 for that test. Then the **family-wise error rate** (P(at least one false positive) when all nulls are true) is at most 0.05.
- **Compare to original:** Original α = 0.05 per test → ~64% chance of at least one false positive across 20 tests. Bonferroni α = 0.0025 per test → at most 5% chance of at least one false positive. So we make it much harder to reject each individual test, which reduces false discoveries but can reduce power (more false negatives).
