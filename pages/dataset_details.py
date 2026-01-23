import streamlit as st
import pandas as pd

st.set_page_config(page_title="Dataset Details", page_icon="📋", layout="wide")

if 'data' not in st.session_state:
    st.error('Please open the main page first to load the data.')
    st.stop()

df = st.session_state.data

st.header("📋 Detailed Dataset Insights")
st.markdown("""
This page provides a deeper dive into the structure and statistics of our Spotify & YouTube dataset.
Explore distributions, missing values, and high-level summaries.
""")

st.divider()

# --- Section 1: Data Summary ---
st.subheader("📊 Statistical Summary")
col1, col2 = st.columns([1, 2])

with col1:
    st.write("**Dataset Shape**")
    st.write(f"- Total Rows: {df.shape[0]:,}")
    st.write(f"- Total Columns: {df.shape[1]}")
    
    st.write("**Data Types Count**")
    st.write(df.dtypes.value_counts())

with col2:
    st.write("**Numerical Summary**")
    st.dataframe(df.describe().T, width="stretch")

st.divider()

# --- Section 2: Missing Values & Uniqueness ---
st.subheader("🔍 Data Quality & Uniqueness")
q1, q2 = st.columns(2)

with q1:
    st.write("**Missing Values per Column**")
    missing_data = df.isnull().sum()
    st.dataframe(missing_data[missing_data > 0].to_frame(name="Missing Count"), width="stretch")

with q2:
    st.write("**Unique Values per Category**")
    cat_cols = ['Artist', 'Album', 'Album_type', 'Channel', 'Licensed', 'official_video']
    unique_counts = {col: df[col].nunique() for col in cat_cols if col in df.columns}
    st.dataframe(pd.Series(unique_counts).to_frame(name="Unique Values"), width="stretch")

st.divider()

# --- Section 3: Detailed Data View ---
st.subheader("📑 Full Data Explorer")
st.write("Browse the entire dataset below. Use the filters in the sidebar or search directly in the table.")

# Simple filtering for the explorer
artist_filter = st.multiselect("Filter by Artist", options=sorted(df['Artist'].unique()[:100])) # Limit to 100 for performance in selectbox

explorer_df = df.copy()
if artist_filter:
    explorer_df = explorer_df[explorer_df['Artist'].isin(artist_filter)]

st.dataframe(explorer_df, width="stretch", hide_index=True)
