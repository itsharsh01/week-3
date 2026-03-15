"""
Day 16 PM: Data visualization utilities.
Part C Q2: plot_numerical_eda(df) — 1×3 panel (histogram, box plot, QQ plot) per numeric column; saves eda_numerics.png.
"""
from pathlib import Path
from typing import Optional

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats

OUT_DIR = Path(__file__).resolve().parent


def plot_numerical_eda(
    df: pd.DataFrame,
    output_path: Optional[Path] = None,
) -> None:
    """
    For every numerical column: 1×3 panel (histogram, box plot, QQ plot).
    Uses Matplotlib OO API. Saves to output_path or eda_numerics.png in script dir.
    """
    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if not num_cols:
        raise ValueError("DataFrame has no numeric columns")

    output_path = output_path or OUT_DIR / "eda_numerics.png"
    n_cols = len(num_cols)
    fig, axes = plt.subplots(n_cols, 3, figsize=(12, 4 * n_cols))
    if n_cols == 1:
        axes = axes.reshape(1, -1)

    for i, col in enumerate(num_cols):
        data = df[col].dropna()
        # Histogram
        ax_hist = axes[i, 0]
        ax_hist.hist(data, bins=min(40, max(10, len(data) // 20)), edgecolor="black", alpha=0.7)
        ax_hist.set_title(f"{col} — Histogram")
        ax_hist.set_xlabel(col)
        ax_hist.set_ylabel("Count")
        # Box plot
        ax_box = axes[i, 1]
        ax_box.boxplot(data, vert=True)
        ax_box.set_title(f"{col} — Box plot")
        ax_box.set_ylabel(col)
        # QQ plot
        ax_qq = axes[i, 2]
        stats.probplot(data, dist="norm", plot=ax_qq)
        ax_qq.set_title(f"{col} — Q-Q plot")
        ax_qq.get_lines()[0].set_markerfacecolor("steelblue")
        ax_qq.get_lines()[0].set_alpha(0.6)
    plt.tight_layout()
    plt.savefig(output_path, dpi=120, bbox_inches="tight")
    plt.close()
    print("Saved", output_path)
