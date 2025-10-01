import mysql.connector

def connect_db():
    """
    Connect to the MySQL database.
    """
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='123456',
        database='hospital_db'
    )

def insert_hospital(conn, hospital_data):
    """
    Insert a hospital record into the database.
    hospital_data: dict with keys: hospital_name, address, city, state, zip_code, county_name, phone_number, hospital_type, hospital_ownership
    """
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO hospitals (hospital_name, address, city, state, zip_code, county_name, phone_number, hospital_type, hospital_ownership)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    ''', (
        hospital_data['hospital_name'],
        hospital_data['address'],
        hospital_data['city'],
        hospital_data['state'],
        hospital_data['zip_code'],
        hospital_data['county_name'],
        hospital_data['phone_number'],
        hospital_data['hospital_type'],
        hospital_data['hospital_ownership']
    ))
    conn.commit()

def fetch_top_10_hospitals(conn):
    """
    Fetch the top 10 hospitals from the database.
    """
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM hospitals LIMIT 10')
    return cursor.fetchall()

def fetch_all_hospitals(conn):
    """
    Fetch all hospitals from the database.
    """
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM hospitals')
    return cursor.fetchall()