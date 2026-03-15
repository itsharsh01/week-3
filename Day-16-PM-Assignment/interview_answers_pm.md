# Day 16 PM Part C — Interview Ready

## Q1 — Violin plot vs box plot

**When to use a violin plot instead of a box plot:** Use a violin plot when you want to show the **full shape of the distribution** (e.g. bimodal, skewed, or multi-peaked) across groups. A box plot only shows quartiles, median, and sometimes outliers, so it hides the actual density.

**What the violin adds:** The violin plot shows a kernel density estimate (KDE) of the distribution—width at a given value represents the proportion of data there. So you can see multiple modes, symmetry vs skew, and where the mass of the data lies, not just the five-number summary. This is especially useful when comparing distributions across categories that might have different shapes (e.g. one category bimodal, another unimodal).

---

## Q2 — plot_numerical_eda(df)

See **visualization_utils.py**: `plot_numerical_eda(df, output_path=None)`. For every numerical column it creates a 1×3 panel (histogram, box plot, QQ plot) using the Matplotlib OO API (subplots, axes), and saves to `eda_numerics.png` (or the given path). It uses `scipy.stats.probplot` for the QQ plot and filters to numeric columns with `df.select_dtypes(include=[np.number])`.

---

## Q3 — Chart critique

**(a) 3D pie chart with 12 segments for market share**  
**Problem:** 3D distorts proportions; 12 segments are hard to compare; pie charts are poor for comparing many values.  
**Alternative:** Horizontal bar chart (sorted by share) or a single treemap so segment sizes are comparable.

**(b) Line chart for survey scores across 5 unordered categories**  
**Problem:** A line implies continuity/order between categories; the reader may infer a trend that doesn’t exist.  
**Alternative:** Bar chart (or column chart) so each category is independent and comparison is by length.

**(c) Scatter plot with 500k points and no transparency**  
**Problem:** Overplotting—points stack so you can’t see density or structure; the plot looks like a solid blob.  
**Alternative:** Use alpha (e.g. 0.1–0.3) or hexbin / 2D histogram / density contour to show density; or sample/subset for a scatter and note the sample size.
