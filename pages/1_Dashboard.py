import streamlit as st
import pandas as pd
from modules.data_manager import fetch_accidents
from modules.analysis import prepare_data, group_counts
from visualizations.charts import bar_chart, line_chart

st.title("📊 Accident Dashboard")
raw = fetch_accidents()
df = prepare_data(raw)
if df.empty:
    st.warning("No accident records yet. Import the sample CSV from Accident Records.")
    st.stop()

c1, c2, c3 = st.columns(3)
c1.metric("Total records", f"{len(df):,}")
c2.metric("Regions", f"{df['region'].nunique():,}")
c3.metric("Fatal records", f"{(df['severity'] == 'Fatal').sum():,}")

monthly = group_counts(df, "year_month").sort_values("year_month")
st.pyplot(line_chart(monthly, "year_month", "accident_count", "Recorded accidents by month"))
left, right = st.columns(2)
with left:
    st.pyplot(bar_chart(group_counts(df, "severity"), "severity", "accident_count", "Severity distribution"))
with right:
    st.pyplot(bar_chart(group_counts(df, "time_period"), "time_period", "accident_count", "Accidents by time of day"))
st.caption("These are recorded counts, not population-adjusted risk estimates or evidence of causation.")
