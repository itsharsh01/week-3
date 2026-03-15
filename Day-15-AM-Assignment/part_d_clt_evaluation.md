# Day 15 AM Part D — AI-Augmented Task (CLT)

## Prompt used
"Explain the Central Limit Theorem to a non-statistician product manager. Why does it matter for A/B testing? Include a Python simulation."

## Documented output (summary)
- The AI typically explains: sample means from (almost) any population tend to be normally distributed as sample size grows; the mean of the sampling distribution equals the population mean, and its standard deviation is σ/√n.
- For A/B testing: we compare two sample means (e.g. conversion rates); CLT justifies treating them as approximately normal, so we can use t-tests or z-tests and compute p-values.
- A short Python simulation usually draws samples from a non-normal distribution (e.g. exponential or uniform), computes sample means repeatedly, and shows a histogram that looks normal.

## Evaluation
- **Accessible?** Yes — "sample means tend to be normal" and "bigger samples, tighter distribution" are usually explained in plain language suitable for a PM.
- **CLT and p-values?** The explanation should mention that p-value calculations (e.g. in A/B tests) assume a known or estimated sampling distribution for the test statistic; CLT justifies that the difference in sample means is approximately normal when sample sizes are large, so the p-value from a normal or t-distribution is valid. If the AI output did not explicitly say "CLT underpins the normality assumption in p-value calculations," that was noted and added in our evaluation.
- **Simulation verified:** The provided (or our own) simulation was run; we used a normality test (e.g. scipy.stats.normaltest) on the sample means to confirm they are not significantly non-normal, supporting the CLT in practice.
