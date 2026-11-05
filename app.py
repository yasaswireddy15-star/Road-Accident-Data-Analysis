import streamlit as st
from database.connection import init_db
from database.models import Accident
from database.connection import SessionLocal
from sqlalchemy import func

st.set_page_config(page_title="Road Accident Analysis", page_icon="🚦", layout="wide")
init_db()

st.title("🚦 Road Accident Data Analysis System")
st.subheader("Understand accident patterns through data")
st.write(
    "Explore recorded accident counts by time, location, vehicle type and severity. "
    "These summaries show associations in the available data; they do not establish causation."
)

with SessionLocal() as session:
    total = session.query(func.count(Accident.accident_id)).scalar() or 0
    locations = session.query(func.count(func.distinct(Accident.location_id))).scalar() or 0
    severe = session.query(func.count(Accident.accident_id)).filter(
        Accident.severity.in_(["Severe", "Fatal"])
    ).scalar() or 0

c1, c2, c3 = st.columns(3)
c1.metric("Accident records", f"{total:,}")
c2.metric("Locations represented", f"{locations:,}")
c3.metric("Severe / fatal records", f"{severe:,}")

st.info("Use the pages in the sidebar to manage records, explore analysis and download reports.")
st.markdown("""
### Getting started
1. Configure your database in `.env`.
2. Run `python -m database.setup_db`.
3. Start the app with `streamlit run app.py`.
4. Import `data/sample_accidents.csv` from **Accident Records** to explore the sample data.
""")
