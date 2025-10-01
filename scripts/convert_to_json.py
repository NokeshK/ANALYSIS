import pandas as pd
import json
import os

def load_clean_and_convert_to_json(input_path, output_path):
    """
    Load CSV, clean data, and save as JSON.
    """
    if not os.path.exists(input_path):
        print(f"Input file {input_path} not found.")
        return

    df = pd.read_csv(input_path)

    # Clean data: fill nulls with "Unknown", convert ZIP to string
    df.fillna("Unknown", inplace=True)
    if 'ZIP Code' in df.columns:
        df['ZIP Code'] = df['ZIP Code'].astype(str)

    # Convert to JSON
    json_data = df.to_dict(orient='records')

    with open(output_path, 'w') as f:
        json.dump(json_data, f, indent=4)

    print(f"Cleaned data saved as JSON to {output_path}")

if __name__ == "__main__":
    
    input_path = '/Users/nokeshkothagundla/Desktop/HospInfo.csv'
    output_path = 'data/hospital_data_cleaned.json'
    load_clean_and_convert_to_json(input_path, output_path)