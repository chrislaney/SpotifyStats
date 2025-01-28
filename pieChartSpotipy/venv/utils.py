import json
from collections import Counter
import matplotlib.pyplot as plt
from io import BytesIO
import base64
import plotly.express as px


def plot_genre_pie_chart(genre_frequencies):
    genres = list(genre_frequencies.keys())
    counts = list(genre_frequencies.values())

    # Create the plot
    plt.figure(figsize=(10, 7))
    plt.pie(counts, labels=genres, startangle=140)
    plt.title('Distribution of Genres in Liked Songs')
    plt.axis('equal')  # Equal aspect ratio ensures the pie is circular.

    # Add a legend below the chart
    plt.legend(genres, title="Genres", loc="center left", bbox_to_anchor=(1, 0.5))

    # Save the plot to a BytesIO object
    img = BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    # Encode the image as a base64 string
    img_b64 = base64.b64encode(img.getvalue()).decode('utf-8')

    return img_b64



def plot_interactive_pie_chart(genre_frequencies):
    genres = list(genre_frequencies.keys())
    counts = list(genre_frequencies.values())

    fig = px.pie(
        names=genres, values=counts, title='Distribution of Genres in Liked Songs'
    )
    fig.update_layout(
        width=1500,  # Set chart width
        height=1000,  # Set chart height
        title_font_size=24,  # Increase title font size
        legend_font_size=16,  # Increase legend font size
        legend_title_font_size=18,  # Increase legend title font size
        margin=dict(l=20, r=20, t=50, b=20),  # Adjust margins

        legend=dict(
            orientation="h",  # Horizontal legend
            yanchor="bottom",
            y=-5,  # Position the legend below the chart
            xanchor="center",
            x=0.5
        )

    )
    fig.update_traces(
        textinfo='none',  # Show both label and percent
        textfont_size=18,  # Increase font size inside pie
        hoverinfo='label+percent',
        hole=0,  # If you want a donut, set this to a value like 0.3
    )

    return fig.to_html(full_html=False)



def get_genre_frequencies(parsed_tracks):
    # Flatten the list of genres from all tracks
    all_genres = []
    for track in parsed_tracks:
        all_genres.extend(track['genres'])

    # Count occurrences of each genre
    genre_frequencies = Counter(all_genres)

    # Group smaller genres
    #genre_frequencies = group_genres_below_max_threshold(genre_frequencies)

    return genre_frequencies

#max threshold for admittance to piechart
def group_smaller_genres(genre_frequencies, threshold=5):
    """
    Group genres with count less than 'threshold' into an 'Other' category.
    """
    grouped = {}
    other_count = 0

    # Iterate over the genres and their counts
    for genre, count in genre_frequencies.items():
        if count < threshold:
            other_count += count  # Add to 'Other' if the genre is too small
        else:
            grouped[genre] = count  # Keep larger genres as they are

    # Add 'Other' if there are genres below the threshold
    if other_count > 0:
        grouped['Other'] = other_count

    return grouped

# min threshold for admittance to pie chart
def group_genres_below_max_threshold(genre_frequencies, threshold=10):
    """
    Keep genres with counts above 'threshold' and group the rest into 'Other'.
    """
    grouped = {}
    other_count = 0

    for genre, count in genre_frequencies.items():
        if count > threshold:
            grouped[genre] = count  # Keep genres above the threshold
        else:
            other_count += count  # Group genres below or equal to the threshold

    # Add 'Other' category if there are grouped genres
    if other_count > 0:
        grouped['Other'] = other_count

    return grouped


# Load JSON file into a dictionary
def load_genre_cache(file_path='genre_cache.json'):
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # If file doesn't exist, create an empty JSON file
        with open(file_path, 'w') as f:
            json.dump({}, f, indent=4)  # Create an empty JSON object
        return {}  # Return an empty dictionary


#saves genre_cache dict to file_path - THIS MIGHT BE SLOWER BC I AM REWRITING ALL GENRE CACHE
def save_genre_cache(genre_cache, file_path='genre_cache.json'):
    with open(file_path, 'w') as f:
        json.dump(genre_cache, f, indent=4)




#This should get all songs that a spotify user as liked and put them
def get_liked_songs(sp):

    raw_results = sp.current_user_saved_tracks(limit=50)
    tracks = raw_results['items']

    while raw_results['next']:
        raw_results = sp.next(raw_results)
        tracks.extend(raw_results['items'])

    return [item['track'] for item in tracks]



def parse_saved_tracks(sp, raw_tracks, genre_cache):
    parsed_tracks = []
    unknown_artist_ids = set()

    for track in raw_tracks:  # raw_tracks is now a flat list of tracks
        artist_id = track['artists'][0]['id'] #grabbing artist_id
        if artist_id not in genre_cache: #checking if in genre cache
            unknown_artist_ids.add(artist_id) #adding to unknown set if not in

        parsed_tracks.append({
            "track_name": track['name'],
            "artist_names": [artist['name'] for artist in track['artists']],
            "artist_id": track['artists'][0]['id'],
            "album_name": track['album']['name'],
            "uri": track['uri'],
            "url": track["external_urls"]['spotify'],
            "album_cover": track['album']['images'][0]['url'],
        })

    #fetching unknown artist genres and adding to our genre_cache
    if unknown_artist_ids:
        fetched_genres = fetch_unknown_artist_genres(sp, list(unknown_artist_ids))
        genre_cache.update(fetched_genres)


    #adding all genres to parsed tracks
    for track in parsed_tracks:
        track['genres'] = genre_cache.get(track['artist_id'], [])

    save_genre_cache(genre_cache)
    return parsed_tracks


def fetch_unknown_artist_genres(sp, unknown_artist_genres):
    genres = {} #dict to store artist_id and genre
    try:
        for i in range(0, len(unknown_artist_genres), 50): #iterates over unknown_genre_list in sequences of 50
            response = sp.artists(unknown_artist_genres[i:i + 50]) #fetches in batches of 50
            for artist in response['artists']: #this iterates over our artist information
                genres[artist['id']] = artist.get('genres',[]) #this gets the genre from each and adds it to the dict
    except Exception as e:
        print(f"Error fetching genres: {e}")
    return genres

