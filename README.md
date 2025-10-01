# Hospital Management Analytics

A comprehensive Python project for analyzing hospital data, featuring data preprocessing, database storage, exploratory data analysis, and an interactive dashboard.

## Project Overview

This project processes hospital data from a CSV file, cleans it, stores it in both relational (MySQL) and JSON formats, and provides analytics through scripts and a Streamlit dashboard.

## Features

- **Automated Data Pipeline**: One-click data processing from CSV to dashboard.
- **Data Preprocessing**: Load CSV, handle missing values, convert to JSON.
- **Database Storage**: Store data in MySQL tables (structured and JSON).
- **Interactive Dashboard**: Streamlit app with KPIs, charts, filters, and sorting.
- **KPIs**: Total hospitals, top states, ownership distribution, ratings.
- **Charts**: Bar charts, pie charts, heatmaps for analysis.
- **Interactive Map**: Folium map with hospital markers, color-coded by ownership, popups with names.
- **Filters**: By state, hospital type, ownership (applies to all visualizations).
- **Sorting**: Sortable tables and charts.

## Workflow Diagram

```
CSV File (HospInfo.csv)
    ↓
Data Cleaning & Preprocessing
    ↓
Cleaned CSV + JSON Files
    ↓
MySQL Database (Structured Tables + JSON Table)
    ↓
Streamlit Dashboard with Interactive Charts & Filters
```

## Data Flow

1. **CSV → Cleaned CSV & JSON**: `scripts/master_pipeline.py` (automated)
2. **Populate MySQL**: Structured tables and JSON table
3. **Dashboard**: Load from JSON, display KPIs, charts, filters
4. **Update Data**: One-click button in dashboard to rerun pipeline

## Installation

1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Set up MySQL database 'hospital_db' with user 'root' and password '123456'.
4. Run data processing scripts in order.

## Usage

### Local Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Set up MySQL database 'hospital_db' with user 'root' and password '123456'.
3. Place HospInfo.csv in the project root or update paths in scripts.
4. Run full pipeline: `cd hospital_analytics && python scripts/master_pipeline.py`
5. Launch dashboard: `cd hospital_analytics && streamlit run dashboard.py`

### Dashboard Features

- View KPIs and charts
- Use filters in sidebar
- Sort data tables and charts
- Click "Update Data" to refresh from source

## Deployment

### Streamlit Cloud

1. Push code to GitHub repository.
2. Go to [share.streamlit.io](https://share.streamlit.io), connect GitHub.
3. Select repository, set main file as `dashboard.py`.
4. For database, use cloud MySQL (e.g., PlanetScale, AWS RDS) and update db_config in scripts.
5. Upload data file or use API for data source.

### Alternative Deployments

- **Heroku**: Use Heroku Postgres or MySQL add-on.
- **AWS/GCP**: Deploy on EC2/GCE with MySQL instance.
- Ensure database is accessible from cloud environment.

## Screenshots

### Dashboard Overview
![Dashboard KPIs](screenshots/dashboard_kpis.png)
*KPIs showing total hospitals, top states, ownership distribution.*

### Charts and Filters
![Charts](screenshots/dashboard_charts.png)
*Interactive charts with filters for states, types, and ownership.*

### Data Table
![Data Table](screenshots/data_table.png)
*Sortable data table with hospital details.*

*Note: Add actual screenshots by taking images of the running dashboard and placing in `screenshots/` folder.*

## Technologies

- Python, Pandas, MySQL, Streamlit, Plotly, Seaborn, Matplotlib

## Future Enhancements

- Predictive analytics: Forecast hospital growth by state using ML models.
- Historical trends: Add time-series data for trend analysis.
- API layer: Expose data via REST API for external access.