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
        ["Histogram", "Box Plot", "Violin Plot", "Bar Chart (Top 20)"]
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
    elif chart_type == "Box Plot":
        fig = px.box(df, y=selected_metric, x=color_param, color=color_param,
                     title=f"Box Plot of {selected_metric}",
                     template="plotly_white")
    elif chart_type == "Violin Plot":
        fig = px.violin(df, y=selected_metric, x=color_param, color=color_param, 
                        box=True, points="all",
                        title=f"Violin Plot of {selected_metric}",
                        template="plotly_white")
    elif chart_type == "Bar Chart (Top 20)":
        # Bar charts for large datasets need aggregation, otherwise they are extremely slow and can fail.
        # Here we'll show a bar chart of the metric grouped by the 'color_by' selection if provided.
        if color_param:
            df_agg = df.groupby(color_param)[selected_metric].mean().reset_index()
            fig = px.bar(df_agg, x=color_param, y=selected_metric, color=color_param,
                         title=f"Average {selected_metric} by {color_param}",
                         template="plotly_white")
        else:
            # If no grouping, a bar chart of ~20k rows is probably not what the user wants, 
            # but we can show the top 20 tracks by that metric as a fallback.
            df_top = df.sort_values(selected_metric, ascending=False).head(50)
            fig = px.bar(df_top, x='Track', y=selected_metric, 
                         title=f"Top 20 Tracks by {selected_metric}",
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
