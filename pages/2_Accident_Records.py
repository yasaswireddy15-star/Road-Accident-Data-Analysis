import streamlit as st
import pandas as pd
from datetime import datetime
from modules.data_manager import add_accident, import_accidents, fetch_accidents
from modules.data_validation import validate_accident_dataframe, VALID_SEVERITIES

st.title("📝 Accident Records")
tab1, tab2, tab3 = st.tabs(["Add record", "Import CSV", "Browse records"])

with tab1:
    with st.form("add_accident_form"):
        accident_date = st.date_input("Accident date")
        accident_time = st.time_input("Accident time")
        region = st.text_input("Region / area")
        road = st.text_input("Road name (optional)")
        vehicle = st.selectbox("Vehicle type", ["Car", "Motorcycle", "Bus", "Truck", "Bicycle", "Pedestrian", "Other"])
        severity = st.selectbox("Recorded severity", VALID_SEVERITIES)
        weather = st.selectbox("Weather (optional)", ["", "Clear", "Rain", "Fog", "Cloudy", "Other"])
        submitted = st.form_submit_button("Save accident")
    if submitted:
        if not region.strip():
            st.error("Region is required.")
        else:
            dt = datetime.combine(accident_date, accident_time)
            add_accident(dt, region, road, vehicle, severity, weather)
            st.success("Accident record saved.")

with tab2:
    st.write("Expected columns: accident_datetime, region (or location), vehicle_type, severity. road_name and weather are optional.")
    uploaded = st.file_uploader("Choose a CSV file", type=["csv"])
    if uploaded is not None:
        try:
            source = pd.read_csv(uploaded)
            valid, issues = validate_accident_dataframe(source)
            st.write(f"Rows in file: **{len(source)}** | Valid: **{len(valid)}** | Rows with issues: **{len(issues)}**")
            if not issues.empty:
                st.warning("Rows with validation issues will not be imported.")
                st.dataframe(issues, use_container_width=True)
            if not valid.empty and st.button("Import valid rows"):
                added = import_accidents(valid)
                st.success(f"Imported {added} records.")
        except Exception as exc:
            st.error(f"Could not read this CSV: {exc}")

with tab3:
    records = fetch_accidents()
    st.dataframe(records, use_container_width=True, hide_index=True)
    if not records.empty:
        st.download_button("Download records as CSV", records.to_csv(index=False), "accident_records.csv", "text/csv")
