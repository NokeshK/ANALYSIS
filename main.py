import pandas as pd
from scripts.db_operations import connect_db, fetch_all_hospitals
from scripts.analysis import filter_hospitals_by_state, plot_ownership_distribution

def main():
    """
    Main function to fetch hospitals from database, filter by state, and display ownership distribution plot.
    """
    # Connect to database
    conn = connect_db()

    # Fetch all hospitals
    hospitals = fetch_all_hospitals(conn)
    conn.close()

    # Convert to DataFrame
    columns = ['hospital_id', 'hospital_name', 'address', 'city', 'state', 'zip_code', 'county_name', 'phone_number', 'hospital_type', 'hospital_ownership']
    df = pd.DataFrame(hospitals, columns=columns)

    print("Fetched hospital details from the database. Displaying the first few hospital entries:")
    print(df.head())

    # Filter by state (e.g., CA)
    filtered_df = filter_hospitals_by_state(df, 'CA')

    print("\nFiltered the dataset by the state of California (CA). Displaying hospital records in tabular format:")
    print(filtered_df[['hospital_id', 'hospital_name', 'city', 'state', 'hospital_type']])

    # Display ownership distribution plot
    plot_ownership_distribution(filtered_df)

    print("\nGenerated visual insights, including the hospital ownership distribution plot.")
    print("The bar chart shows that most hospitals are classified as Voluntary non-profit – Private, followed by Proprietary and other ownership types.")

if __name__ == "__main__":
    main()