import pandas as pd

VALID_SEVERITIES = ["Minor", "Moderate", "Severe", "Fatal"]
REQUIRED = ["accident_datetime", "region", "vehicle_type", "severity"]

def validate_accident_dataframe(dataframe):
    """Return (valid_rows, issue_rows). Issues include CSV row numbers starting at 2."""
    df = dataframe.copy()
    df["accident_datetime"] = df["accident_datetime"].astype(object)
    df.columns = [str(c).strip().lower() for c in df.columns]
    if "location" in df.columns and "region" not in df.columns:
        df = df.rename(columns={"location": "region"})
    for col in REQUIRED:
        if col not in df.columns:
            return pd.DataFrame(), pd.DataFrame([{
                "row": "-", "issue": f"Missing required column: {col}"
            }])

    if "road_name" not in df.columns:
        df["road_name"] = None
    if "weather" not in df.columns:
        df["weather"] = None

    issues, valid_indices = [], []
    for idx, row in df.iterrows():
        row_number = idx + 2 if isinstance(idx, int) else str(idx)
        problems = []
        dt = pd.to_datetime(row["accident_datetime"], errors="coerce")
        if pd.isna(dt):
            problems.append("Invalid or missing date/time")
        for col in ["region", "vehicle_type", "severity"]:
            if pd.isna(row[col]) or not str(row[col]).strip():
                problems.append(f"Missing {col}")
        severity = str(row["severity"]).strip().title() if pd.notna(row["severity"]) else ""
        if severity and severity not in VALID_SEVERITIES:
            problems.append("Severity must be Minor, Moderate, Severe or Fatal")
        if problems:
            issues.append({"row": row_number, "issue": "; ".join(problems)})
        else:
            df.at[idx, "accident_datetime"] = dt.to_pydatetime()
            df.at[idx, "severity"] = severity
            for col in ["region", "vehicle_type"]:
                df.at[idx, col] = str(row[col]).strip()
            valid_indices.append(idx)

    valid = df.loc[valid_indices, REQUIRED + ["road_name", "weather"]].copy()
    return valid, pd.DataFrame(issues, columns=["row", "issue"])
