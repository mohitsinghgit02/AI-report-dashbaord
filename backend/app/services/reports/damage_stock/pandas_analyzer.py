import pandas as pd
import numpy as np
import random


MAX_SAMPLE = 5000


def safe_score(value):
    if value is None or not np.isfinite(value) or value <= 0:
        return 0.1
    return float(value)


def analyze_data(df: pd.DataFrame):

    if len(df) < 5:
        return {"error": "Data is not sufficient for analysis"}

    # sample for heavy charts
    if len(df) > MAX_SAMPLE:
        df_sample = df.sample(MAX_SAMPLE, random_state=1)
    else:
        df_sample = df.copy()

    insights = {
        "overview": {"rows": int(len(df)), "columns": int(len(df.columns))},
        "kpis": [],
        "charts": [],
        "statistics": {},
        "correlations": [],
    }

    chart_candidates = []

    # -------------------------
    # NUMERIC ANALYSIS
    # -------------------------

    num_cols = df.select_dtypes(include="number").columns

    for col in num_cols:

        series = df[col].dropna()

        if len(series) == 0:
            continue

        total = float(series.sum())
        avg = float(series.mean())
        max_val = float(series.max())
        min_val = float(series.min())

        insights["kpis"].append(
            {"metric": col, "total": total, "avg": avg, "max": max_val, "min": min_val}
        )

        std_val = series.std()
        median_val = series.median()

        insights["statistics"][col] = {
            "std": float(std_val) if np.isfinite(std_val) else 0,
            "median": float(median_val),
        }

        # Histogram candidate
        std_val = safe_score(std_val)

        chart_candidates.append(
            {
                "score": std_val,
                "chart": {
                    "type": "histogram",
                    "title": f"{col} Distribution",
                    "labels": df_sample[col].round(2).tolist(),
                    "values": df_sample[col].tolist(),
                },
            }
        )

        # Boxplot candidate
        chart_candidates.append(
            {
                "score": std_val * 0.8,
                "chart": {
                    "type": "box",
                    "title": f"{col} Spread",
                    "labels": [col],
                    "values": df_sample[col].tolist(),
                },
            }
        )

    # -------------------------
    # CORRELATION ANALYSIS
    # -------------------------

    if len(num_cols) > 1:

        corr = df[num_cols].corr()

        for i in range(len(corr.columns)):
            for j in range(i + 1, len(corr.columns)):

                val = corr.iloc[i, j]

                if not np.isfinite(val):
                    continue

                if abs(val) > 0.5:

                    col1 = corr.columns[i]
                    col2 = corr.columns[j]

                    insights["correlations"].append(
                        {"metric_1": col1, "metric_2": col2, "correlation": float(val)}
                    )

                    chart_candidates.append(
                        {
                            "score": abs(val) * 10,
                            "chart": {
                                "type": "scatter",
                                "title": f"{col1} vs {col2}",
                                "labels": df_sample[col1].tolist(),
                                "values": df_sample[col2].tolist(),
                            },
                        }
                    )

    # -------------------------
    # CATEGORICAL ANALYSIS
    # -------------------------

    cat_cols = df.select_dtypes(include="object").columns

    for col in cat_cols:

        unique_count = df[col].nunique()

        if unique_count > 25:
            continue

        counts = df[col].value_counts().head(8)

        if len(counts) == 0:
            continue

        importance = counts.iloc[0] / counts.sum()

        chart_type = random.choice(["bar", "pie", "donut"])

        chart_candidates.append(
            {
                "score": safe_score(importance * 6),
                "chart": {
                    "type": chart_type,
                    "title": f"{col} Distribution",
                    "labels": counts.index.tolist(),
                    "values": counts.values.tolist(),
                },
            }
        )

    # -------------------------
    # DATE TREND ANALYSIS
    # -------------------------

    date_cols = df.select_dtypes(include="datetime").columns

    if len(date_cols) > 0 and len(num_cols) > 0:

        date_col = date_cols[0]
        metric = random.choice(num_cols)

        trend = df.groupby(df[date_col].dt.to_period("M"))[metric].sum()

        if len(trend) > 1:

            chart_candidates.append(
                {
                    "score": 9,
                    "chart": {
                        "type": random.choice(["line", "area"]),
                        "title": f"{metric} Monthly Trend",
                        "labels": trend.index.astype(str).tolist(),
                        "values": trend.values.tolist(),
                    },
                }
            )

    # -------------------------
    # TOP CONTRIBUTOR
    # -------------------------

    if len(num_cols) > 0 and len(cat_cols) > 0:

        metric = random.choice(num_cols)
        category = random.choice(cat_cols)

        grouped = (
            df.groupby(category)[metric].sum().sort_values(ascending=False).head(8)
        )

        if len(grouped) > 0:

            chart_candidates.append(
                {
                    "score": 8,
                    "chart": {
                        "type": "bar",
                        "title": f"Top {category} by {metric}",
                        "labels": grouped.index.tolist(),
                        "values": grouped.values.tolist(),
                    },
                }
            )

    # -------------------------
    # CHART SELECTION
    # -------------------------

    chart_candidates = sorted(
        chart_candidates, key=lambda x: safe_score(x["score"]), reverse=True
    )

    selected = []
    used_types = set()

    # pass 1 → ensure diversity
    for c in chart_candidates:

        chart_type = c["chart"]["type"]

        if chart_type not in used_types:

            selected.append(c["chart"])
            used_types.add(chart_type)

        if len(selected) >= 5:
            break

    # pass 2 → fill remaining with weighted random
    remaining = chart_candidates[len(selected) :]

    if len(selected) < 5 and len(remaining) > 0:

        weights = [safe_score(c["score"]) for c in remaining]

        extra = random.choices(
            remaining, weights=weights, k=min(5 - len(selected), len(remaining))
        )

        for e in extra:
            selected.append(e["chart"])

    insights["charts"] = selected[:5]

    return insights
