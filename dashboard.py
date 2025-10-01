import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import sys
import os
import folium
from streamlit_folium import st_folium
import mysql.connector

# Add scripts to path
sys.path.append('scripts')

from master_pipeline import run_pipeline

# Load cleaned JSON data
@st.cache_data
def load_data():
    with open('data/hospital_data_cleaned.json', 'r') as f:
        data = json.load(f)
    return pd.DataFrame(data)

# Load hospital data from MySQL with lat/lon
@st.cache_data
def load_hospital_data_from_db():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='123456',
        database='hospital_db'
    )
    query = "SELECT * FROM hospitals"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

df = load_data()

st.title("🏥 Hospital Management Analytics Dashboard")
st.markdown("Interactive dashboard for analyzing hospital data from cleaned JSON.")

# Update Data Button
if st.button("🔄 Update Data from Source"):
    with st.spinner("Updating data pipeline... This may take a few minutes."):
        try:
            input_csv = '/Users/nokeshkothagundla/Desktop/HospInfo.csv'
            output_csv = 'data/hospital_data_cleaned.csv'
            output_json = 'data/hospital_data_cleaned.json'
            db_config = {
                'host': 'localhost',
                'user': 'root',
                'password': '123456',
                'database': 'hospital_db'
            }
            run_pipeline(input_csv, output_csv, output_json, db_config)
            load_data.clear()  # Clear cache to reload new data
            st.success("Data updated successfully! Refreshing dashboard...")
            st.rerun()
        except Exception as e:
            st.error(f"Error updating data: {e}")

# KPIs
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Hospitals", len(df))
with col2:
    top_state = df['State'].value_counts().idxmax()
    st.metric("Top State", top_state)
with col3:
    common_ownership = df['Hospital Ownership'].value_counts().idxmax()
    st.metric("Most Common Ownership", common_ownership)
with col4:
    ratings = pd.to_numeric(df['Hospital overall rating'], errors='coerce').dropna()
    avg_rating = ratings.mean() if not ratings.empty else 0
    st.metric("Avg Rating", f"{avg_rating:.1f}")

# Additional KPIs
col5, col6, col7 = st.columns(3)
with col5:
    top_5_states = df['State'].value_counts().head(5).index.tolist()
    st.metric("Top 5 States", ", ".join(top_5_states))
with col6:
    # Government vs Private
    ownership_counts = df['Hospital Ownership'].value_counts()
    government_types = [own for own in ownership_counts.index if 'Government' in own]
    private_types = [own for own in ownership_counts.index if 'Proprietary' in own or 'Private' in own]
    gov_count = sum(ownership_counts.get(typ, 0) for typ in government_types)
    priv_count = sum(ownership_counts.get(typ, 0) for typ in private_types)
    total = len(df)
    gov_pct = (gov_count / total * 100) if total > 0 else 0
    st.metric("Government Hospitals %", f"{gov_pct:.1f}%")
with col7:
    priv_pct = (priv_count / total * 100) if total > 0 else 0
    st.metric("Private Hospitals %", f"{priv_pct:.1f}%")

# Filters
st.sidebar.header("Filters")
selected_states = st.sidebar.multiselect("Select States", options=df['State'].unique(), default=df['State'].unique()[:5])
selected_types = st.sidebar.multiselect("Select Hospital Types", options=df['Hospital Type'].unique(), default=df['Hospital Type'].unique())
selected_ownership = st.sidebar.multiselect("Select Ownership Types", options=df['Hospital Ownership'].unique(), default=df['Hospital Ownership'].unique())

filtered_df = df[df['State'].isin(selected_states) & df['Hospital Type'].isin(selected_types) & df['Hospital Ownership'].isin(selected_ownership)]

st.header("📊 Data Overview")
st.dataframe(filtered_df, use_container_width=True)

# Bar chart for hospital types
st.header("🏥 Hospital Types Distribution")
fig1 = px.bar(filtered_df['Hospital Type'].value_counts(), title="Hospital Types Count")
st.plotly_chart(fig1)

# Pie chart for hospital ownership
st.header("🏢 Hospital Ownership Distribution")
ownership_counts = filtered_df['Hospital Ownership'].value_counts()
fig2 = px.pie(values=ownership_counts.values, names=ownership_counts.index, title="Ownership Distribution")
st.plotly_chart(fig2)

# Bar chart for top states
st.header("📍 Top States with Most Hospitals")
sort_option = st.selectbox("Sort States By", ["Count Descending", "Count Ascending", "Alphabetical"])
top_states = filtered_df['State'].value_counts()
if sort_option == "Count Descending":
    top_states = top_states.head(10)
elif sort_option == "Count Ascending":
    top_states = top_states.tail(10).sort_values()
elif sort_option == "Alphabetical":
    top_states = top_states.sort_index().head(10)
fig3 = go.Figure(data=[go.Bar(x=top_states.index, y=top_states.values)])
fig3.update_layout(title=f"Top 10 States ({sort_option})", xaxis_title="State", yaxis_title="Number of Hospitals")
st.plotly_chart(fig3)

# Cross-tab: Ownership vs Type
st.header("🔄 Ownership vs Type Analysis")
crosstab = pd.crosstab(filtered_df['Hospital Ownership'], filtered_df['Hospital Type'])
fig4 = px.imshow(crosstab, text_auto=True, title="Ownership vs Type Heatmap")
st.plotly_chart(fig4)

# Alerts: States with fewer hospitals than average
st.header("🚨 Alerts: States with Low Hospital Count")
state_counts = df['State'].value_counts()
avg_hospitals = state_counts.mean()
low_states = state_counts[state_counts < avg_hospitals]
if not low_states.empty:
    st.warning(f"States with fewer hospitals than average ({avg_hospitals:.1f}):")
    st.dataframe(low_states.to_frame(name="Hospital Count"))
else:
    st.success("All states have at least average hospital count.")

# Interactive Map
st.header("🗺️ Hospital Locations Map")

# Load data with lat/lon from DB
hospital_df = load_hospital_data_from_db()

# Filter for map (use same filters as above)
map_filtered_df = hospital_df[
    (hospital_df['state'].isin(selected_states)) &
    (hospital_df['hospital_type'].isin(selected_types)) &
    (hospital_df['hospital_ownership'].isin(selected_ownership))
].dropna(subset=['latitude', 'longitude'])

if not map_filtered_df.empty:
    # Calculate average coordinates for centering
    avg_lat = map_filtered_df['latitude'].mean()
    avg_lon = map_filtered_df['longitude'].mean()

    # Create folium map
    m = folium.Map(location=[avg_lat, avg_lon], zoom_start=6)

    # Color coding based on ownership
    def get_color(ownership):
        if 'Government' in ownership:
            return 'blue'
        else:
            return 'red'

    # Add markers
    for _, row in map_filtered_df.iterrows():
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=row['hospital_name'],
            icon=folium.Icon(color=get_color(row['hospital_ownership']))
        ).add_to(m)

    # Display map
    st_folium(m, width=700, height=500)
else:
    st.write("No location data available for the selected filters.")