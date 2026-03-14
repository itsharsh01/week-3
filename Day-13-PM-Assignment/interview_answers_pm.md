# Day 13 PM Part C — Interview Ready Answers

## Q1 (Conceptual): 1M rows, 40% of 'income' missing — drop vs fill?

**Decision process:**

1. **Understand impact of dropping:** Dropping 40% (400k rows) would lose a lot of data and might introduce selection bias (e.g. missing income could be correlated with job type or region). So dropping is usually a last resort unless the missingness is clearly random and the analysis can tolerate it.

2. **When to drop:** Drop if (a) the column is not critical for the analysis, (b) the missingness is clearly MCAR (missing completely at random) and we have enough rows left, or (c) we are doing a sensitivity analysis and want a “complete-case” baseline.

3. **When to fill:** Prefer filling when (a) the column is important (e.g. income for segmentation), (b) we have a defensible strategy, and (c) we can document and possibly sensitivity-check the choice.

4. **Fill strategy and why:**  
   - **Median** is a good default for income: robust to outliers and skew, and doesn’t assume normality. Mean would be pulled by high earners.  
   - **Mode** is less ideal for continuous income.  
   - **Imputation by group** (e.g. median income by region/role) can be better if missingness is related to those variables (MAR).  
   - **Model-based imputation** (e.g. regression or MICE) is stronger but more complex.  
   For 40% missing, I’d use median (or group median if we have good predictors) and note in the report that results are conditional on this imputation; optionally run analyses with “income missing” as a category to check sensitivity.
