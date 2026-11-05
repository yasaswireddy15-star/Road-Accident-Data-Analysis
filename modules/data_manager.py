import pandas as pd
from database.connection import SessionLocal
from database.models import Accident, Location

def add_accident(accident_datetime, region, road_name, vehicle_type, severity, weather=None):
    with SessionLocal() as session:
        location = session.query(Location).filter_by(
            region=region.strip(), road_name=(road_name.strip() if road_name else None)
        ).first()
        if location is None:
            location = Location(region=region.strip(), road_name=road_name.strip() if road_name else None)
            session.add(location)
            session.flush()
        record = Accident(
            accident_datetime=accident_datetime, location_id=location.location_id,
            vehicle_type=vehicle_type.strip(), severity=severity,
            weather=weather.strip() if weather else None
        )
        session.add(record)
        session.commit()

def import_accidents(dataframe):
    count = 0
    with SessionLocal() as session:
        for _, row in dataframe.iterrows():
            road = None if pd.isna(row["road_name"]) or not str(row["road_name"]).strip() else str(row["road_name"]).strip()
            region = str(row["region"]).strip()
            location = session.query(Location).filter_by(region=region, road_name=road).first()
            if location is None:
                location = Location(region=region, road_name=road)
                session.add(location)
                session.flush()
            dt = pd.to_datetime(row["accident_datetime"]).to_pydatetime()
            weather = None if pd.isna(row["weather"]) or not str(row["weather"]).strip() else str(row["weather"]).strip()
            session.add(Accident(
                accident_datetime=dt, location_id=location.location_id,
                vehicle_type=str(row["vehicle_type"]).strip(),
                severity=str(row["severity"]).strip(), weather=weather
            ))
            count += 1
        session.commit()
    return count

def fetch_accidents():
    with SessionLocal() as session:
        rows = session.query(Accident, Location).join(
            Location, Accident.location_id == Location.location_id
        ).order_by(Accident.accident_datetime.desc()).all()
        records = [{
            "accident_id": a.accident_id, "accident_datetime": a.accident_datetime,
            "region": loc.region, "road_name": loc.road_name,
            "vehicle_type": a.vehicle_type, "severity": a.severity, "weather": a.weather
        } for a, loc in rows]
    return pd.DataFrame(records, columns=[
        "accident_id", "accident_datetime", "region", "road_name",
        "vehicle_type", "severity", "weather"
    ])
