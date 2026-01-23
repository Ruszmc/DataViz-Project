import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Visual Analysis", page_icon="📈", layout="wide")

if 'data' not in st.session_state:
    st.error('Please open the main page first to load the data.')
    st.stop()

df = st.session_state.data

st.header("📈 Visuelle Datenanalyse")
st.markdown("""
Verwenden Sie die untenstehenden Optionen, um verschiedene Aspekte des Datensatzes zu visualisieren. 
Wählen Sie eine Metrik aus, um deren Verteilung über die Top-Songs zu sehen.
""")

st.divider()

# --- Visualization Section ---
col1, col2 = st.columns([1, 3])

numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
# Remove unhelpful numeric columns if they exist
unwanted = ['Key', 'Duration_ms']
options = [c for c in numeric_cols if c not in unwanted]

with col1:
    st.subheader("Einstellungen")
    selected_metric = st.selectbox(
        "Wählen Sie eine Metrik für das Diagramm",
        options=options,
        index=options.index('Stream') if 'Stream' in options else 0
    )
    
    chart_type = st.radio(
        "Wählen Sie den Diagrammtyp",
        ["Histogramm", "Box-Plot", "Violin-Plot", "Balkendiagramm (Top 50)"]
    )
    
    color_by = st.selectbox(
        "Farbe nach (Optional)",
        ["Keine", "Album_type", "Licensed", "official_video"]
    )

with col2:
    st.subheader(f"{selected_metric} Verteilung")
    
    color_param = None if color_by == "Keine" else color_by
    
    # Random sample for the first three charts
    df_sample = df.sample(n=min(500, len(df)), random_state=42) if chart_type in ["Histogramm", "Box-Plot", "Violin-Plot"] else df
    
    if chart_type == "Histogramm":
        fig = px.histogram(df_sample, x=selected_metric, color=color_param, 
                           marginal="rug", hover_data=df_sample.columns,
                           title=f"Histogramm von {selected_metric} (Stichprobe von 500)",
                           template="plotly_white")
    elif chart_type == "Box-Plot":
        fig = px.box(df_sample, y=selected_metric, x=color_param, color=color_param,
                     title=f"Box-Plot von {selected_metric} (Stichprobe von 500)",
                     template="plotly_white")
    elif chart_type == "Violin-Plot":
        fig = px.violin(df_sample, y=selected_metric, x=color_param, color=color_param, 
                        box=True, points="all",
                        title=f"Violin-Plot von {selected_metric} (Stichprobe von 500)",
                        template="plotly_white")
    elif chart_type == "Balkendiagramm (Top 50)":
        # Bar charts for large datasets need aggregation, otherwise they are extremely slow and can fail.
        # Here we'll show a bar chart of the metric grouped by the 'color_by' selection if provided.
        if color_param:
            df_agg = df.groupby(color_param)[selected_metric].mean().reset_index()
            fig = px.bar(df_agg, x=color_param, y=selected_metric, color=color_param,
                         title=f"Durchschnittliche {selected_metric} nach {color_param}",
                         template="plotly_white")
        else:
            # If no grouping, a bar chart of ~20k rows is probably not what the user wants, 
            # but we can show the top 50 tracks by that metric as a fallback.
            df_top = df.sort_values(selected_metric, ascending=False).head(50)
            fig = px.bar(df_top, x='Track', y=selected_metric, 
                         title=f"Top 50 Tracks nach {selected_metric}",
                         template="plotly_white")
    
    st.plotly_chart(fig, width="stretch")

st.divider()

# --- Insight Section ---
st.subheader("💡 Wichtige Erkenntnisse")
st.info(f"""
- **{selected_metric} Durchschnitt:** {df[selected_metric].mean():,.2f}
- **{selected_metric} Median:** {df[selected_metric].median():,.2f}
- **{selected_metric} Maximum:** {df[selected_metric].max():,.2f}
""")
