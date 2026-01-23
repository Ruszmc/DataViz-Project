import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    df = pd.read_csv('data_set.csv', index_col=0)
    df.columns = df.columns.str.strip()

    # Fix for Arrow serialization issues with newer NumPy/Pandas
    # Ensure all float columns are standard numpy float64 (not nullable Float64)
    # and all object columns are clean.
    for col in df.columns:
        if pd.api.types.is_float_dtype(df[col]):
            df[col] = df[col].astype('float64')
        elif pd.api.types.is_integer_dtype(df[col]):
            df[col] = df[col].astype('int64')
        elif pd.api.types.is_object_dtype(df[col]):
            # Ensure object columns don't contain mixed types that confuse Arrow
            # Forcing to string if they are mostly strings
            df[col] = df[col].astype(str)

    return df

st.set_page_config(page_title="Spotify & YouTube Analytics", page_icon="📊", layout="wide")
if 'data' not in st.session_state:
    st.session_state.data = load_data()
df = st.session_state.data

dataset_description = {
    "Track": "Name of the song, as visible on the Spotify platform.",
    "Artist": "Name of the artist.",
    "Url_spotify": "The URL of the artist.",
    "Album": "The album in which the song is contained on Spotify.",
    "Album_type": "Indicates if the song is released on Spotify as a single or contained in an album.",
    "Uri": "A Spotify link used to find the song through the API.",
    "Danceability": "Describes how suitable a track is for dancing based on a combination of musical elements including tempo, rhythm stability, beat strength, and overall regularity. A value of 0.0 is least danceable and 1.0 is most danceable.",
    "Energy": "A measure from 0.0 to 1.0 and represents a perceptual measure of intensity and activity. Typically, energetic tracks feel fast, loud, and noisy. For example, death metal has high energy, while a Bach prelude scores low on the scale.",
    "Key": "The key the track is in. Integers map to pitches using standard Pitch Class notation. E.g. 0 = C, 1 = C♯/D♭, 2 = D, and so on. If no key was detected, the value is -1.",
    "Loudness": "The overall loudness of a track in decibels (dB). Loudness values are averaged across the entire track.",
    "Speechiness": "Detects the presence of spoken words in a track. The more exclusively speech-like the recording, the closer to 1.0 the attribute value.",
    "Acousticness": "A confidence measure from 0.0 to 1.0 of whether the track is acoustic. 1.0 represents high confidence the track is acoustic.",
    "Instrumentalness": 'Predicts whether a track contains no vocals. The closer the instrumentalness value is to 1.0, the greater likelihood the track contains no vocal content.',
    'Liveness': 'Detects the presence of an audience in the recording. Higher liveness values represent an increased probability that the track was performed live.',
    'Valence': 'A measure from 0.0 to 1.0 describing the musical positiveness conveyed by a track.',
    'Tempo': 'The overall estimated tempo of a track in beats per minute (BPM).',
    'Duration_ms': 'The total duration of the track in milliseconds.',
    'Stream': 'Number of Streams of the song on Spotify.',
    'Url_youtube': 'URL of the video linked to the song on YouTube, if it has any.',
    'Title': 'Title of the videoclip on YouTube.',
    'Channel': 'Name of the channel that published the video.',
    'Views': 'Number of views.',
    'Likes': 'Number of likes.',
    'Comments': 'Number of comments.',
    'Licensed': 'Indicates whether the video represents licensed content.',
    'official_video': 'Boolean value that indicates if the video found is the official video of the song.',
    'Description': 'Statistics for the Top 10 songs of various Spotify artists and their YouTube videos.'
}


def welcome():
    st.title('🎵 Spotify & YouTube Data Insights')
    st.markdown("""
    Welcome to this Data Analysis Project. We explore a dataset containing the top songs from various artists on Spotify 
    and their corresponding performance on YouTube.
    
    This overview provides a quick glimpse into the key metrics of our dataset. For detailed analysis, please visit the **Find your Song** page.
    """)

    st.divider()

    st.subheader("Data Set Overview")
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Total Songs", f"{len(df):,}")
    with m2:
        st.metric("Avg Energy", f"{df['Energy'].mean():.2f}")
    with m3:
        st.metric("Avg Danceability", f"{df['Danceability'].mean():.2f}")
    with m4:
        st.metric("Avg BPM", f"{df['Tempo'].mean():.2f}")

    st.divider()

    st.subheader("Explore the Data")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.info("📊 **In-depth Analysis**\n\nCheck out the 'Dataset Details' for comprehensive stats.")
    with c2:
        st.info("📈 **Visual Insights**\n\nVisualize distributions in 'Visual Analysis'.")
    with c3:
        st.info("🔗 **Correlations**\n\nFind relationships between metrics in 'Correlation Analysis'.")

    st.divider()
    
    st.subheader("Random Sample")
    st.dataframe(df.sample(10), width="stretch", hide_index=True)

    st.page_link("pages/dataset_details.py")


with st.sidebar:
    st.header("Dictionary")
    sel_var = st.selectbox("Select a Variable to see its description", df.columns.tolist())
    description = dataset_description.get(sel_var)

    st.info(f"**{sel_var}:** {description}")
    
    st.divider()
    st.markdown("### About")
    st.write("This dashboard analyzes the intersection of music streaming on Spotify and video engagement on YouTube.")


pages = {
    'Overview': [
        st.Page(welcome, title='Home', icon="🏠"),
        st.Page('pages/dataset_details.py', title='Dataset Details', icon='📋')
    ],

    'Analysis': [
        st.Page('pages/visual_analysis.py', title='Visual Analysis', icon='📈'),
        st.Page('pages/correlation_analysis.py', title='Correlation Analysis', icon='🔗'),
        st.Page('pages/find_your_song.py', title='Find your Song', icon='🎵'),
    ]
}


pg = st.navigation(pages)
pg.run()