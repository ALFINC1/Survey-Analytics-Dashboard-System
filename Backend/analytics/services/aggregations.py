import pandas as pd


def build_summary(df: pd.DataFrame) -> dict:
    return {
        "total_responses": int(len(df)),
        "total_columns": int(df.shape[1]),
        "columns": list(df.columns),
    }


def is_categorical(series: pd.Series) -> bool:
    # Heuristic: treat as categorical if unique values are small
    unique = series.dropna().nunique()
    return 1 <= unique <= 20


def build_charts(df: pd.DataFrame) -> list:
    charts = []

    for col in df.columns:
        s = df[col]
        if not is_categorical(s):
            continue

        counts = s.value_counts(dropna=True).to_dict()
        labels = [str(k) for k in counts.keys()]
        values = [int(v) for v in counts.values()]

        charts.append({
            "column": str(col),
            "type": "bar",
            "labels": labels,
            "values": values,
        })

    return charts