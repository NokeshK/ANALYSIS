import pandas as pd
import os

def load_and_clean_data(input_path, output_path):
    """
    Load dataset from CSV, handle missing values, convert ZIP to string, and save cleaned data.
    """
    if not os.path.exists(input_path):
        print(f"Input file {input_path} not found.")
        return

    df = pd.read_csv(input_path)

    # Check for null values and fill with "Unknown"
    df.fillna("Unknown", inplace=True)

    # Convert ZIP codes to string
    if 'zip_code' in df.columns:
        df['zip_code'] = df['zip_code'].astype(str)

    # Save cleaned dataset
    df.to_csv(output_path, index=False)
    print(f"Cleaned data saved to {output_path}")

if __name__ == "__main__":
    # Default paths for standalone run
    input_path = '/Users/nokeshkothagundla/Desktop/HospInfo.csv'
    output_path = 'data/hospital_data_cleaned.csv'
    load_and_clean_data(input_path, output_path)