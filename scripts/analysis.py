import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def load_cleaned_data(path):
    """
    Load the cleaned hospital dataset.
    """
    return pd.read_csv(path)

def filter_hospitals_by_state(df, state):
    """
    Filter hospitals by state.
    """
    return df[df['state'] == state]

def filter_hospitals_by_type(df, hospital_type):
    """
    Filter hospitals by hospital type.
    """
    return df[df['hospital_type'] == hospital_type]

def plot_ownership_distribution(df):
    """
    Generate bar plot for hospital ownership distribution.
    """
    plt.figure(figsize=(10, 6))
    sns.countplot(data=df, x='hospital_ownership')
    plt.title('Hospital Ownership Distribution')
    plt.xticks(rotation=45)
    plt.savefig('data/ownership_distribution.png')
    print("Ownership distribution plot saved as data/ownership_distribution.png")

def plot_login_activity_distribution(login_counts):
    """
    Generate histogram for login activity distribution.
    login_counts: list or series of login counts.
    """
    plt.figure(figsize=(10, 6))
    sns.histplot(login_counts, bins=20)
    plt.title('Login Activity Distribution')
    plt.xlabel('Login Count')
    plt.ylabel('Frequency')
    plt.show()