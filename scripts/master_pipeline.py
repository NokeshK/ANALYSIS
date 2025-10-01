"""
Master pipeline script to automate the entire data processing workflow.
Combines load_data.py, convert_to_json.py, populate_db.py, populate_json_db.py
"""

import os
import sys

# Add scripts directory to path
sys.path.append(os.path.dirname(__file__))

from load_data import load_and_clean_data
from convert_to_json import load_clean_and_convert_to_json
from populate_db import create_tables, populate_hospitals, populate_login_activity
from populate_json_db import create_json_table, populate_json_data
import pandas as pd
import mysql.connector

def run_pipeline(input_csv_path, output_csv_path, output_json_path, db_config):
    """
    Run the complete data pipeline.

    Args:
        input_csv_path (str): Path to input CSV file
        output_csv_path (str): Path to save cleaned CSV
        output_json_path (str): Path to save JSON
        db_config (dict): Database configuration
    """
    print("Starting data pipeline...")

    # Step 1: Load and clean data to CSV
    print("Step 1: Loading and cleaning data...")
    load_and_clean_data(input_csv_path, output_csv_path)

    # Step 2: Convert to JSON
    print("Step 2: Converting to JSON...")
    load_clean_and_convert_to_json(input_csv_path, output_json_path)

    # Step 3: Populate MySQL database
    print("Step 3: Populating MySQL database...")
    conn = mysql.connector.connect(**db_config)
    create_tables(conn)
    df = pd.read_csv(output_csv_path)
    populate_hospitals(conn, df)
    populate_login_activity(conn, len(df))
    conn.close()

    # Step 4: Populate JSON database
    print("Step 4: Populating JSON database...")
    conn = mysql.connector.connect(**db_config)
    create_json_table(conn)
    populate_json_data(conn, output_json_path)
    conn.close()

    print("Pipeline completed successfully!")

if __name__ == "__main__":
    # Configuration
    input_csv = '/Users/nokeshkothagundla/Desktop/HospInfo.csv'  # Update this path
    output_csv = 'data/hospital_data_cleaned.csv'
    output_json = 'data/hospital_data_cleaned.json'
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '123456',
        'database': 'hospital_db'
    }

    run_pipeline(input_csv, output_csv, output_json, db_config)