import pandas as pd
import mysql.connector
import os
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import time

def geocode_address(address, city, state, zip_code):
    """
    Geocode address to get latitude and longitude.
    """
    geolocator = Nominatim(user_agent="hospital_analytics")
    full_address = f"{address}, {city}, {state} {zip_code}"
    try:
        location = geolocator.geocode(full_address, timeout=10)
        if location:
            return location.latitude, location.longitude
        else:
            return None, None
    except (GeocoderTimedOut, GeocoderServiceError):
        return None, None

def create_tables(conn):
    """
    Create tables from schema.sql
    """
    schema_path = 'sql/schema.sql'
    if os.path.exists(schema_path):
        with open(schema_path, 'r') as f:
            sql = f.read()
        cursor = conn.cursor()
        # Split SQL into individual statements
        statements = sql.split(';')
        for statement in statements:
            if statement.strip():
                cursor.execute(statement)
        conn.commit()
        cursor.close()
        print("Tables created.")
    else:
        print("Schema file not found.")

def populate_hospitals(conn, df):
    """
    Populate hospitals table with data from DataFrame, including geocoding for lat/lon.
    """
    cursor = conn.cursor()
    for _, row in df.iterrows():
        lat, lon = geocode_address(
            row.get('Address', ''),
            row.get('City', ''),
            row.get('State', ''),
            str(row.get('ZIP Code', ''))
        )
        cursor.execute('''
            INSERT INTO hospitals (hospital_name, address, city, state, zip_code, county_name, phone_number, hospital_type, hospital_ownership, latitude, longitude)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ''', (
            row.get('Hospital Name', 'Unknown'),
            row.get('Address', 'Unknown'),
            row.get('City', 'Unknown'),
            row.get('State', 'Unknown'),
            str(row.get('ZIP Code', 'Unknown')),
            row.get('County Name', 'Unknown'),
            row.get('Phone Number', 'Unknown'),
            row.get('Hospital Type', 'Unknown'),
            row.get('Hospital Ownership', 'Unknown'),
            lat,
            lon
        ))
        time.sleep(1)  # Rate limiting for geocoding
    conn.commit()
    print(f"Inserted {len(df)} hospital records with geocoding.")

def populate_login_activity(conn, num_records):
    """
    Populate login_activity table with dummy data.
    """
    import random
    cursor = conn.cursor()
    # Get hospital_ids
    cursor.execute('SELECT hospital_id FROM hospitals')
    hospital_ids = [row[0] for row in cursor.fetchall()]
    for _ in range(num_records):
        hospital_id = random.choice(hospital_ids) if hospital_ids else 1
        login_count = random.randint(0, 100)
        signin_provider_id = random.randint(1, 5)
        cursor.execute('''
            INSERT INTO login_activity (hospital_id, login_count, signin_provider_id)
            VALUES (%s, %s, %s)
        ''', (hospital_id, login_count, signin_provider_id))
    conn.commit()
    print(f"Inserted {num_records} login activity records.")

if __name__ == "__main__":
    # Load cleaned data
    df = pd.read_csv('data/hospital_data_cleaned.csv')
    # Connect to DB
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='123456',
        database='hospital_db'
    )
    # Create tables
    create_tables(conn)
    # Populate hospitals
    populate_hospitals(conn, df)
    # Populate login activity with dummy data
    populate_login_activity(conn, len(df))  # Same number as hospitals
    conn.close()
    print("Database populated.")