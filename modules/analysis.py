import pandas as pd
import numpy as np

def prepare_data(df):
    if df.empty:
        return df.copy()
    result = df.copy()
    result["accident_datetime"] = pd.to_datetime(result["accident_datetime"], errors="coerce")
    result = result.dropna(subset=["accident_datetime"])
    result["date"] = result["accident_datetime"].dt.date
    result["year_month"] = result["accident_datetime"].dt.to_period("M").astype(str)
    result["hour"] = result["accident_datetime"].dt.hour
    result["time_period"] = pd.cut(
        result["hour"], bins=[-1, 5, 11, 17, 23],
        labels=["Night (00-05)", "Morning (06-11)", "Afternoon (12-17)", "Evening (18-23)"]
    )
    return result

def summary_statistics(df):
    if df.empty:
        return {"total": 0, "average_per_day": 0.0, "unique_locations": 0}
    days = max(df["date"].nunique(), 1)
    return {
        "total": int(len(df)),
        "average_per_day": round(float(np.mean([len(df) / days])), 2),
        "unique_locations": int(df["region"].nunique())
    }

def group_counts(df, column):
    if df.empty or column not in df.columns:
        return pd.DataFrame(columns=[column, "accident_count"])
    return df.groupby(column, observed=False).size().reset_index(name="accident_count").sort_values(
        "accident_count", ascending=False
    )
