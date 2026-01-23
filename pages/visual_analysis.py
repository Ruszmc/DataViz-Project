import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Visual Analysis", page_icon="📈", layout="wide")

if 'data' not in st.session_state:
    st.error('Please open the main page first to load the data.')
    st.stop()

df = st.session_state.data

st.header("📈 Visual Data Analysis")
st.markdown("""
Use the options below to visualize different aspects of the dataset. 
Select a metric to see its distribution across the top songs.
""")

st.divider()

# --- Visualization Section ---
col1, col2 = st.columns([1, 3])

numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
# Remove unhelpful numeric columns if they exist
unwanted = ['Key', 'Duration_ms']
options = [c for c in numeric_cols if c not in unwanted]

with col1:
    st.subheader("Settings")
    selected_metric = st.selectbox(
        "Select metric for the chart",
        options=options,
        index=options.index('Stream') if 'Stream' in options else 0
    )
    
    chart_type = st.radio(
        "Select chart type",
        ["Histogram", "Bar Chart"]
    )
    
    color_by = st.selectbox(
        "Color by (Optional)",
        ["None", "Album_type", "Licensed", "official_video"]
    )

with col2:
    st.subheader(f"{selected_metric} Distribution")
    
    color_param = None if color_by == "None" else color_by
    
    if chart_type == "Histogram":
        fig = px.histogram(df, x=selected_metric, color=color_param, 
                           marginal="rug", hover_data=df.columns,
                           title=f"Histogram of {selected_metric}",
                           template="plotly_white")
    elif chart_type == "Bar Chart":
        fig = px.bar(df, y=selected_metric, x=color_param, color=color_param,
                     orientation='h', title=f"Box plot of {selected_metric}",
                     template="plotly_white")
    
    st.plotly_chart(fig, width="stretch")

st.divider()

# --- Insight Section ---
st.subheader("💡 Key Takeaways")
st.info(f"""
- **{selected_metric} Mean:** {df[selected_metric].mean():,.2f}
- **{selected_metric} Median:** {df[selected_metric].median():,.2f}
- **{selected_metric} Max:** {df[selected_metric].max():,.2f}
""")
