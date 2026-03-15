# Day 16 PM Part B — Plotly Express: interactive vs static

## Task

Recreate 3 of the Matplotlib/Seaborn charts as interactive Plotly charts; save as HTML; identify 2 types of insights easier to see in interactive vs static charts.

## Implementation

- **visualization_plotly.py** (or cells in the notebook): Uses `plotly.express` to create (1) histogram with KDE equivalent (e.g. px.histogram or density), (2) scatter with trend line (px.scatter with trendline="ols"), (3) box plot (px.box). Each figure is saved with `fig.write_html("plotly_histogram.html")` etc.

## Two types of insights easier in interactive charts

1. **Drill-down and exact values:** Hovering reveals exact counts, values, or percentages for any bar/point. In static charts you only see approximate values from axis labels. So “which category has the highest median?” or “what is the value at this point?” is answered immediately without reading off axes or adding annotations for every element.

2. **Zoom, pan, and subsetting:** For dense scatter plots or time series, zooming into a region or filtering (e.g. by category in a Plotly dropdown or legend toggle) lets you explore local patterns and outliers without creating multiple static views. So “what happens in Q3 only?” or “how do these two segments compare?” is easier without pre-defining many static panels.
