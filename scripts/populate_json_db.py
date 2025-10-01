import mysql.connector
import json
import os

def create_json_table(conn):
    """
    Create table for JSON data.
    """
    schema_path = 'sql/json_schema.sql'
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
        print("JSON table created.")
    else:
        print("JSON schema file not found.")

def populate_json_data(conn, json_path):
    """
    Populate JSON data into the database.
    """
    if not os.path.exists(json_path):
        print(f"JSON file {json_path} not found.")
        return

    with open(json_path, 'r') as f:
        data = json.load(f)

    cursor = conn.cursor()
    for record in data:
        cursor.execute('INSERT INTO hospital_json (data) VALUES (%s)', (json.dumps(record),))
    conn.commit()
    cursor.close()
    print(f"Inserted {len(data)} JSON records.")

if __name__ == "__main__":
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='123456',
        database='hospital_db'
    )
    create_json_table(conn)
    populate_json_data(conn, 'data/hospital_data_cleaned.json')
    conn.close()
    print("JSON database populated.")