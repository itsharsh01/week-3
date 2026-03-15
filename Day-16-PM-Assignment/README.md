# Day 16 PM — Data Visualization (Matplotlib & Seaborn)

- **Data:** Use `eda_assignment_data.csv` (sample included; real file **eda_assignment_data.csv** is on LMS — 1200 rows, 10 mixed-type columns). To regenerate the sample: `python create_sample_eda_data.py`.
- **Part A:** Open `eda_report_notebook.ipynb` and run all cells for the full EDA (3 hist+KDE, 2 regplot, 1 heatmap, 1 box plot). Export the notebook and save a dashboard PNG if required.
- **Part B:** Run `python visualization_plotly.py` (requires `pip install plotly`) to create `plotly_histogram.html`, `plotly_scatter_regression.html`, `plotly_box.html`. See `part_b_plotly_insights.md` for interactive vs static insights.
- **Part C:** `plot_numerical_eda(df)` is in `visualization_utils.py`; it saves `eda_numerics.png`. Run: `python -c "import pandas as pd; from visualization_utils import plot_numerical_eda; plot_numerical_eda(pd.read_csv('eda_assignment_data.csv'))"`. Interview answers in `interview_answers_pm.md`.
- **Part D:** See `part_d_ai_eda_evaluation.md` for prompt, run note, and evaluation.
- **Dependencies:** `pip install -r requirements.txt` (pandas, matplotlib, seaborn, scipy, plotly, jupyter).
