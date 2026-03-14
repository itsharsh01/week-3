"""
Day 13 PM Part B: Automated Data Profiler.
Takes any DataFrame; returns nested dict profile and prints formatted summary.
Per column: dtype, unique count, null count/%, top 5 values; numeric: min, max, mean, median, std, skew; string: lengths, patterns; issues: single-value, high-cardinality, outliers.
"""

from typing import Any

import pandas as pd

try:
    from scipy.stats import skew as _skew
except ImportError:
    def _skew(x):  # noqa: ARG001
        return None


def profile_dataframe(df: pd.DataFrame) -> dict[str, Any]:
    """
    Generate complete profile for any DataFrame. Returns nested dict and prints summary.
    """
    if df.empty:
        print("(Empty DataFrame)")
        return {"shape": (0, 0), "columns": {}}

    profile = {
        "shape": df.shape,
        "memory_mb": round(df.memory_usage(deep=True).sum() / (1024 * 1024), 4),
        "columns": {},
        "issues": [],
    }

    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()

    for col in df.columns:
        ser = df[col]
        null_count = int(ser.isnull().sum())
        null_pct = round(null_count / len(df) * 100, 2) if len(df) else 0
        unique_count = int(ser.nunique())
        top5 = ser.value_counts(dropna=False).head(5)
        top5_values = [{"value": str(k), "count": int(v)} for k, v in top5.items()]

        col_profile: dict[str, Any] = {
            "dtype": str(ser.dtype),
            "unique_count": unique_count,
            "null_count": null_count,
            "null_pct": null_pct,
            "top5_values": top5_values,
        }

        if col in numeric_cols:
            clean = ser.dropna()
            if len(clean) > 0:
                col_profile["min"] = float(clean.min())
                col_profile["max"] = float(clean.max())
                col_profile["mean"] = round(float(clean.mean()), 4)
                col_profile["median"] = float(clean.median())
                col_profile["std"] = round(float(clean.std()), 4) if len(clean) > 1 else 0.0
                s = _skew(clean) if len(clean) > 2 else None
                col_profile["skewness"] = round(float(s), 4) if s is not None else None
                # Outliers: > 3 std from mean
                mean_, std_ = clean.mean(), clean.std()
                if std_ > 0:
                    outliers = ((ser - mean_).abs() > 3 * std_).sum()
                    if outliers > 0:
                        profile["issues"].append(f"{col}: {int(outliers)} value(s) >3 std from mean")
            else:
                col_profile["min"] = col_profile["max"] = col_profile["mean"] = col_profile["median"] = None
                col_profile["std"] = col_profile["skewness"] = None
        else:
            # String-like: avg length, min/max length
            str_ser = ser.astype(str)
            lengths = str_ser.str.len()
            col_profile["avg_length"] = round(float(lengths.mean()), 2)
            col_profile["min_length"] = int(lengths.min())
            col_profile["max_length"] = int(lengths.max())
            # Simple "common pattern": sample of unique values
            col_profile["sample_values"] = ser.dropna().head(5).tolist()
            if unique_count == 1:
                profile["issues"].append(f"{col}: single-value column")
            if unique_count > len(df) * 0.9 and ser.dtype == object:
                profile["issues"].append(f"{col}: high-cardinality string ({unique_count} unique)")

        profile["columns"][col] = col_profile

    # Print formatted summary
    print("=" * 60)
    print("DATA PROFILE")
    print("=" * 60)
    print(f"Shape: {profile['shape'][0]} rows × {profile['shape'][1]} columns")
    print(f"Memory: {profile['memory_mb']} MB\n")
    for col, cp in profile["columns"].items():
        print(f"--- {col} ({cp['dtype']}) ---")
        print(f"  Unique: {cp['unique_count']}, Null: {cp['null_count']} ({cp['null_pct']}%)")
        print(f"  Top 5: {cp['top5_values'][:3]}...")
        if "mean" in cp and cp.get("mean") is not None:
            print(f"  Numeric: min={cp['min']}, max={cp['max']}, mean={cp['mean']}, std={cp['std']}, skew={cp.get('skewness')}")
        if "avg_length" in cp:
            print(f"  String: avg_len={cp['avg_length']}, min_len={cp['min_length']}, max_len={cp['max_length']}")
        print()
    if profile["issues"]:
        print("Potential issues:", profile["issues"])
    print("=" * 60)

    return profile


if __name__ == "__main__":
    from pathlib import Path
    # Test on cleaned survey
    cleaned_path = Path(__file__).resolve().parent / "cleaned_survey.csv"
    if cleaned_path.is_file():
        df = pd.read_csv(cleaned_path)
        profile_dataframe(df)
    else:
        # Fallback: small demo
        df = pd.DataFrame({"a": [1, 2, 3, 4, 5], "b": ["x", "y", "x", "y", "x"]})
        profile_dataframe(df)
