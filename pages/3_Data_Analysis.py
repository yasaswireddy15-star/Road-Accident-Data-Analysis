import streamlit as st
import pandas as pd
from modules.data_manager import fetch_accidents
from modules.analysis import prepare_data, group_counts
from visualizations.charts import bar_chart, line_chart

st.title("🔎 Data Analysis")
df = prepare_data(fetch_accidents())
if df.empty:
    st.info("Add or import records to begin analysis.")
    st.stop()

with st.sidebar:
    st.header("Analysis filters")
    regions = sorted(df["region"].dropna().unique().tolist())
    chosen_regions = st.multiselect("Region", regions, default=regions)
    severities = sorted(df["severity"].dropna().unique().tolist())
    chosen_severity = st.multiselect("Severity", severities, default=severities)
    vehicles = sorted(df["vehicle_type"].dropna().unique().tolist())
    chosen_vehicles = st.multiselect("Vehicle type", vehicles, default=vehicles)

filtered = df[
    df["region"].isin(chosen_regions) &
    df["severity"].isin(chosen_severity) &
    df["vehicle_type"].isin(chosen_vehicles)
]
st.write(f"Showing **{len(filtered)}** of **{len(df)}** records.")
if filtered.empty:
    st.warning("No records match these filters.")
    st.stop()

a, b = st.columns(2)
with a:
    st.pyplot(line_chart(group_counts(filtered, "year_month").sort_values("year_month"),
                         "year_month", "accident_count", "Monthly accident trend"))
with b:
    st.pyplot(bar_chart(group_counts(filtered, "region").head(10),
                        "region", "accident_count", "Top 10 regions by recorded count"))
a, b = st.columns(2)
with a:
    st.pyplot(bar_chart(group_counts(filtered, "vehicle_type"),
                        "vehicle_type", "accident_count", "Records by vehicle type"))
with b:
    st.pyplot(bar_chart(group_counts(filtered, "time_period"),
                        "time_period", "accident_count", "Records by time of day"))
st.subheader("Severity summary")
st.dataframe(group_counts(filtered, "severity"), use_container_width=True, hide_index=True)
st.caption("A higher count may reflect more traffic, longer observation periods, reporting differences or other factors. It is not by itself a measure of risk.")
