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
Use the tools below to explore various trends and distributions within the dataset. 
Discover how metrics like Streams, Danceability, and Energy vary across a representative sample of songs.
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
        "Select Metric",
        options=options,
        index=options.index('Stream') if 'Stream' in options else 0
    )
    
    chart_type = st.radio(
        "Chart Type",
        ["Histogram", "Box Plot", "Violin Plot", "Bar Chart"]
    )
    
    color_by = st.selectbox(
        "Color by (Optional)",
        ["None", "Album_type", "Licensed", "official_video"]
    )

with col2:
    st.subheader(f"{selected_metric} Distribution")
    
    color_param = None if color_by == "None" else color_by

    df_sample = df.sample(n=min(500, len(df)), random_state=42)
    
    if chart_type == "Histogram":
        fig = px.histogram(df_sample, x=selected_metric, color=color_param, 
                           marginal="rug", hover_data=df_sample.columns,
                           title=f"Histogram of {selected_metric} (Sample of 500)",
                           template="plotly_white")
    elif chart_type == "Box Plot":
        fig = px.box(df_sample, y=selected_metric, x=color_param, color=color_param,
                     title=f"Box Plot of {selected_metric} (Sample of 500)",
                     template="plotly_white")
    elif chart_type == "Violin Plot":
        fig = px.violin(df_sample, y=selected_metric, x=color_param, color=color_param, 
                        box=True, points="all",
                        title=f"Violin Plot of {selected_metric} (Sample of 500)",
                        template="plotly_white")
    elif chart_type == "Bar Chart":
        if color_param:
            df_agg = df_sample.groupby(color_param)[selected_metric].mean().reset_index()
            fig = px.bar(df_agg, x=color_param, y=selected_metric, color=color_param,
                         title=f"Average {selected_metric} by {color_param} (Sample of 500)",
                         template="plotly_white")
        else:
            # Show a sample of songs, but hide the X-axis labels as requested
            fig = px.bar(df_sample, x='Track', y=selected_metric, 
                         title=f"Bar Chart of {selected_metric} (Sample of 500)",
                         template="plotly_white")
            fig.update_layout(xaxis={'showticklabels': False})
    
    st.plotly_chart(fig, width="stretch")

st.divider()

# --- Insight Section ---
st.subheader("💡 Key Takeaways")
st.info(f"""
- **{selected_metric} Average:** {df[selected_metric].mean():,.2f}
- **{selected_metric} Median:** {df[selected_metric].median():,.2f}
- **{selected_metric} Maximum:** {df[selected_metric].max():,.2f}
""")
