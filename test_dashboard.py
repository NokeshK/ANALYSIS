import pandas as pd
import json

# Test loading data
try:
    with open('data/hospital_data_cleaned.json', 'r') as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    print(f"Data loaded successfully. Shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    print(f"Sample data:\n{df.head()}")
    print("Dashboard data verification: PASSED")
except Exception as e:
    print(f"Error loading data: {e}")
    print("Dashboard data verification: FAILED")