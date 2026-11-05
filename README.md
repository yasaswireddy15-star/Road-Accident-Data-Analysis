# Road Accident Data Analysis System

A Python/Streamlit application for managing and analyzing public, synthetic, or properly anonymized road accident records.

## Features
- Add and browse accident records
- Import CSV files with validation feedback
- Store locations and accidents in a relational database
- Filter by date, region, vehicle type and severity
- Analyze trends by month, hour, location and severity
- View Matplotlib charts and download CSV summaries

**Important:** Counts describe the records available in the dataset. They do not prove why accidents occurred. Document the dataset source, coverage and location granularity. Do not upload names, phone numbers, registration numbers or other personal identifiers.

## 1. Requirements
- Python 3.10 or newer
- pip
- MySQL Server (optional if using the default SQLite demo mode)

## 2. Create and activate a virtual environment

Windows:
```bash
python -m venv .venv
.venv\Scripts\activate
```

macOS/Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 3. Install dependencies
```bash
pip install -r requirements.txt
```

## 4. Configure the database

Copy `.env.example` to `.env`.

For a quick local run, keep:
```env
DATABASE_URL=sqlite:///road_accidents.db
```

For MySQL, first create the database:
```sql
CREATE DATABASE road_accident_db;
```
Then set `.env` (replace credentials):
```env
DATABASE_URL=mysql+pymysql://YOUR_USERNAME:YOUR_PASSWORD@localhost:3306/road_accident_db
```
If your password contains special URL characters, URL-encode them.

## 5. Create database tables
```bash
python -m database.setup_db
```

## 6. Run the application
```bash
streamlit run app.py
```
Streamlit prints a local URL, usually `http://localhost:8501`.

## 7. Load sample data
Open **Accident Records** in the sidebar, upload `data/sample_accidents.csv`, review validation feedback, and import valid rows. The sample data is synthetic and intended only for demonstration.

## CSV format
Required columns:
- `accident_datetime` (example: `2025-01-15 08:30:00`)
- `region`
- `road_name` (may be blank)
- `vehicle_type`
- `severity` (`Minor`, `Moderate`, `Severe`, or `Fatal`)

Optional:
- `weather`

The app also accepts `location` as an alias for `region`.

## Project structure
```text
database/       Database connection, ORM models and setup
modules/        Validation, record management and analysis
visualizations/ Matplotlib charts
pages/          Streamlit application pages
data/           Synthetic example CSV and upload folder
reports/        Download/export workspace
```

## Troubleshooting
- **MySQL connection error:** verify MySQL is running, database exists, and `.env` credentials are correct.
- **Module not found:** activate `.venv` and run `pip install -r requirements.txt`.
- **Port already in use:** run `streamlit run app.py --server.port 8502`.

## GitHub
```bash
git init
git add .
git commit -m "Initial commit: Road Accident Data Analysis System"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/Road-Accident-Data-Analysis.git
git push -u origin main
```
Create an empty GitHub repository first. Do not commit `.env`, database files or personal data.
