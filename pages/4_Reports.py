import streamlit as st
from modules.data_manager import fetch_accidents
from modules.analysis import prepare_data, group_counts, summary_statistics

st.title("📄 Reports")
df = prepare_data(fetch_accidents())
if df.empty:
    st.info("No data available. Add or import accident records first.")
    st.stop()

stats = summary_statistics(df)
st.subheader("Accident trend report")
st.write(f"- Total recorded accidents: **{stats['total']}**")
st.write(f"- Regions represented: **{stats['unique_locations']}**")
st.write(f"- Average recorded accidents per represented day: **{stats['average_per_day']}**")

st.subheader("Location summary")
locations = group_counts(df, "region")
st.dataframe(locations, use_container_width=True, hide_index=True)
st.subheader("Severity summary")
severity = group_counts(df, "severity")
st.dataframe(severity, use_container_width=True, hide_index=True)

st.download_button("Download location summary", locations.to_csv(index=False),
                   "location_summary.csv", "text/csv")
st.download_button("Download severity summary", severity.to_csv(index=False),
                   "severity_summary.csv", "text/csv")
st.download_button("Download filtered source records", df.to_csv(index=False),
                   "accident_analysis_data.csv", "text/csv")
st.caption("Report source and coverage should be documented separately when using a real dataset.")
