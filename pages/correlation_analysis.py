import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Correlation Analysis", page_icon="🔗", layout="wide")

if 'data' not in st.session_state:
    st.error('Please open the main page first to load the data.')
    st.stop()

df = st.session_state.data

st.header("🔗 Correlation & Relationship Analysis")
st.markdown("""
Explore how different musical features and performance metrics relate to each other.
Select two variables to see their correlation and scatter plot.
""")

st.divider()

# --- Selection Section ---
col1, col2 = st.columns(2)

numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
# Filter out non-insightful columns
filtered_cols = [c for c in numeric_cols if c not in ['Key']]

with col1:
    var_x = st.selectbox("Select X-axis Variable", options=filtered_cols, index=filtered_cols.index('Danceability') if 'Danceability' in filtered_cols else 0)

with col2:
    var_y = st.selectbox("Select Y-axis Variable", options=filtered_cols, index=filtered_cols.index('Valence') if 'Valence' in filtered_cols else 1)

st.divider()

if var_x == var_y:
    st.error("X-axis and Y-axis variables cannot be the same.")
    st.stop()

# --- Scatter Plot Section ---
c1, c2 = st.columns([3, 1])

with c1:
    st.subheader(f"Relationship: {var_x} vs {var_y}")
    
    # Sampling for performance if dataset is huge, but here it's ~20k rows which Plotly handles okay
    # but we can add a trendline
    fig = px.scatter(df, x=var_x, y=var_y, 
                     color='Stream',
                     hover_data=['Track', 'Artist'],
                     trendline="ols",
                     title=f"Scatter plot of {var_x} and {var_y}",
                     template="plotly_white")
    st.plotly_chart(fig, width="stretch")

with c2:
    st.subheader("Stats")
    correlation = df[[var_x, var_y]].corr().iloc[0, 1]
    st.metric("Pearson Correlation", f"{correlation:.3f}")
    
    st.write("""
    **Interpretation:**
    - Close to **1.0**: Strong positive relationship.
    - Close to **-1.0**: Strong negative relationship.
    - Close to **0**: No linear relationship.
    """)
    
    if abs(correlation) > 0.7:
        st.success("Strong Correlation detected!")
    elif abs(correlation) > 0.4:
        st.info("Moderate Correlation detected.")
    else:
        st.warning("Weak or no linear correlation.")

st.divider()

# --- Heatmap Section ---
st.subheader("🌡️ Overall Correlation Heatmap")
if st.checkbox("Show Heatmap for all features"):
    corr_matrix = df[filtered_cols].corr()
    fig_heat = px.imshow(corr_matrix, 
                         text_auto=".2f", 
                         aspect="auto",
                         color_continuous_scale='RdBu_r',
                         title="Correlation Heatmap",
                         template="plotly_white")
    st.plotly_chart(fig_heat, width="stretch")
