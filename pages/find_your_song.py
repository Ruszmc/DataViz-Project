import streamlit as st

st.set_page_config(page_title="Find Your Song", page_icon="🎵", layout="wide")

st.header('🎵 Your personal Song recommendations')

if 'data' not in st.session_state:
    st.error('Please open the main page first to load the data.')
    st.stop()

df = st.session_state.data

st.markdown('''
Don't know what to listen to right now? 
Adjust the filters below to match your mood, and we'll find the perfect tracks for you!
''')

st.divider()

# --- FILTER SECTION ---
with st.expander("🛠️ Filter Options", expanded=True):
    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader('Mood & Energy')
        dance_mood = st.select_slider(
            'How much do you want to dance?',
            options=['Not at all', 'A little', 'Doesn´t matter', 'Let´s party!'],
            value='Doesn´t matter'
        )

        energy_mood = st.select_slider(
            'What is your energy level?',
            options=['Low / Relaxed', 'Medium / Normal', 'High / Energetic'],
            value='Medium / Normal'
        )

        happy_mood = st.radio(
            'Should the music be happy?',
            ['Sad / Melancholic', 'Neutral', 'Happy / Cheerful'],
            index=1
        )

    with col2:
        st.subheader('Popularity')
        # Stream filter
        max_streams = int(df['Stream'].max())
        min_streams = int(df['Stream'].min())
        
        streams_range = st.slider(
            'Filter by Spotify Streams (in Millions)',
            min_value=0,
            max_value=int(max_streams / 1_000_000),
            value=(0, int(max_streams / 1_000_000)),
            step=10
        )

    with col3:
        st.subheader('Additional Filters')
        instrumental = st.checkbox('Prefer instrumental music?', value=False)
        live = st.checkbox('Prefer live recordings?', value=False)
        
        st.write("---")
        limit = st.number_input('Show top X results', min_value=1, max_value=100, value=20)

# --- FILTERING LOGIC ---

filtered_df = df.copy()

# Danceability mapping
if dance_mood == 'Not at all':
    filtered_df = filtered_df[filtered_df['Danceability'] < 0.4]
elif dance_mood == 'A little':
    filtered_df = filtered_df[(filtered_df['Danceability'] >= 0.4) & (filtered_df['Danceability'] < 0.6)]
elif dance_mood == 'Let´s party!':
    filtered_df = filtered_df[filtered_df['Danceability'] >= 0.7]

# Energy mapping
if energy_mood == 'Low / Relaxed':
    filtered_df = filtered_df[filtered_df['Energy'] < 0.4]
elif energy_mood == 'Medium / Normal':
    filtered_df = filtered_df[(filtered_df['Energy'] >= 0.4) & (filtered_df['Energy'] < 0.7)]
elif energy_mood == 'High / Energetic':
    filtered_df = filtered_df[filtered_df['Energy'] >= 0.7]

# Happiness (Valence) mapping
if happy_mood == 'Sad / Melancholic':
    filtered_df = filtered_df[filtered_df['Valence'] < 0.4]
elif happy_mood == 'Happy / Cheerful':
    filtered_df = filtered_df[filtered_df['Valence'] > 0.6]

# Stream filter application
filtered_df = filtered_df[
    (filtered_df['Stream'] >= streams_range[0] * 1_000_000) & 
    (filtered_df['Stream'] <= streams_range[1] * 1_000_000)
]

# Instrumentalness
if instrumental:
    filtered_df = filtered_df[filtered_df['Instrumentalness'] > 0.5]

# Liveness
if live:
    filtered_df = filtered_df[filtered_df['Liveness'] > 0.5]

# --- DISPLAY RESULTS ---

st.divider()
st.subheader(f'Found {len(filtered_df)} matching songs')

if not filtered_df.empty:
    # Sort by streams by default
    display_df = filtered_df.sort_values(by='Stream', ascending=False).head(limit)
    
    # Select columns for better display
    display_cols = ['Track', 'Artist', 'Album', 'Stream', 'Danceability', 'Energy', 'Valence']
    
    # Format Stream column for display
    display_df_styled = display_df[display_cols].copy()
    display_df_styled['Stream'] = display_df_styled['Stream'].apply(lambda x: f"{x:,.0f}")
    
    st.dataframe(display_df_styled, width="stretch", hide_index=True)
    
    # Add a success message if many songs found
    if len(filtered_df) > 0:
        st.success(f"Successfully found {len(filtered_df)} songs! Here are the top {min(limit, len(filtered_df))}.")
else:
    st.warning("No songs found with the current filters. Try to loosen them a bit!")