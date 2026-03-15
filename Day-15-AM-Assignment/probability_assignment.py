"""
Day 15 AM Part A: Five real-world scenarios — identify distribution, justify, compute with scipy.stats.
Part B: Beta distribution plots and posterior simulation.
Part C Q2: simulate_clt().
"""

from pathlib import Path

import numpy as np
from scipy import stats

OUT_DIR = Path(__file__).resolve().parent


# ---------- Part A: 5 scenarios ----------

def scenario_1_website_traffic():
    """Website: 200 requests/min on average. P(more than 220 in a minute)?
    Distribution: Poisson (count of events in fixed interval, rate λ=200).
    Reasons: (1) discrete count in fixed time, (2) rate is given, events typically independent.
    """
    lam = 200
    # P(X > 220) = 1 - P(X <= 220)
    p = 1 - stats.poisson.cdf(220, lam)
    print("1. Website traffic (Poisson): P(X > 220) =", round(p, 4))
    return p


def scenario_2_quality_control():
    """Quality: 2% defective, batch of 50. P(exactly 3 defective)?
    Distribution: Binomial(n=50, p=0.02) — fixed trials, constant p, count successes.
    Reasons: (1) fixed number of trials (50), (2) each bolt independent, same p.
    """
    n, p_def = 50, 0.02
    p = stats.binom.pmf(3, n, p_def)
    print("2. Quality control (Binomial): P(X = 3) =", round(p, 4))
    return p


def scenario_3_delivery():
    """Delivery: N(45 min, 8²). P(>60)? P(40 to 50)?
    Distribution: Normal — continuous, symmetric, given as Normal.
    Reasons: (1) explicitly given Normal, (2) delivery times often approximately normal.
    """
    mu, sigma = 45, 8
    p_gt_60 = 1 - stats.norm.cdf(60, mu, sigma)
    p_40_50 = stats.norm.cdf(50, mu, sigma) - stats.norm.cdf(40, mu, sigma)
    print("3. Delivery (Normal): P(X > 60) =", round(p_gt_60, 4), ", P(40 < X < 50) =", round(p_40_50, 4))
    return p_gt_60, p_40_50


def scenario_4_customer_arrivals():
    """Customer arrivals: 10/hour. P(no customers in next 6 minutes)?
    Distribution: Poisson — events in fixed interval. Rate for 6 min = 10*(6/60) = 1.
    Reasons: (1) count in fixed interval, (2) rate proportional to time.
    """
    lam_6min = 10 * (6 / 60)  # 1
    p = stats.poisson.pmf(0, lam_6min)
    print("4. Customer arrivals (Poisson): P(0 in 6 min) =", round(p, 4))
    return p


def scenario_5_clt_class_average():
    """Class of 35 students. Using CLT, approximate distribution of class average score.
    If individual scores have mean μ and variance σ², sample mean of n=35 is approx N(μ, σ²/35).
    We don't have μ, σ from problem — assume e.g. μ=70, σ=10 for illustration.
    """
    n = 35
    mu_score, sigma_score = 70, 10  # assumed
    mean_avg = mu_score
    std_avg = sigma_score / np.sqrt(n)
    print("5. CLT class average: X̄ ~ N(μ, σ²/n) ≈ N({}, {})".format(mean_avg, round(std_avg**2, 2)))
    return mean_avg, std_avg


# ---------- Part B: Beta distribution ----------

def beta_plots_and_posterior():
    """Beta(2,5), (5,5), (0.5,0.5) PDFs; posterior after 7 heads in 10 flips from Beta(1,1)."""
    x = np.linspace(0.001, 0.999, 200)
    for a, b in [(2, 5), (5, 5), (0.5, 0.5)]:
        _ = stats.beta.pdf(x, a, b)  # PDFs; plot in notebook
    # Posterior: Beta(1,1) prior + 7 heads, 3 tails → Beta(1+7, 1+3) = Beta(8, 4)
    prior_a, prior_b = 1, 1
    heads, tails = 7, 3
    post_a, post_b = prior_a + heads, prior_b + tails
    posterior_mean = post_a / (post_a + post_b)
    print("Part B: Posterior after 7H,3T from Beta(1,1): Beta(8,4), mean =", round(posterior_mean, 4))
    return post_a, post_b


# ---------- Part C Q2: simulate_clt ----------

def simulate_clt(distribution, params, n_samples, n_simulations):
    """
    Simulate CLT: for the given scipy.stats distribution, repeatedly draw n_samples
    and compute sample mean; do this n_simulations times. Return sample_means and
    overlay theoretical normal (mean = dist.mean(), std = dist.std()/sqrt(n_samples)).
    """
    dist = distribution(**params)
    sample_means = []
    for _ in range(n_simulations):
        sample = dist.rvs(size=n_samples)
        sample_means.append(np.mean(sample))
    sample_means = np.array(sample_means)
    theo_mean = dist.mean()
    theo_std = dist.std() / np.sqrt(n_samples) if hasattr(dist, "std") else np.sqrt(dist.var() / n_samples)
    return sample_means, theo_mean, theo_std


def main():
    print("=== Part A ===\n")
    scenario_1_website_traffic()
    scenario_2_quality_control()
    scenario_3_delivery()
    scenario_4_customer_arrivals()
    scenario_5_clt_class_average()
    print("\n=== Part B ===\n")
    beta_plots_and_posterior()
    print("\n=== Part C Q2: simulate_clt demo ===\n")
    means, m, s = simulate_clt(stats.expon, {"scale": 2.0}, n_samples=30, n_simulations=5000)
    print("Exponential(scale=2): sample means mean =", round(np.mean(means), 4), ", theoretical N mean =", m, ", std =", round(s, 4))


if __name__ == "__main__":
    main()
