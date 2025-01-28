import json
from collections import Counter
from io import BytesIO
import base64

import spotipy


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

def get_top_100(sp):
    top_tracks = []
    limit = 50  # Spotify API max limit for top tracks per request
    time_range = 'medium_term'  # Approx. last 6 months (includes this year)

    try:
        # Fetch first 50 tracks
        response = sp.current_user_top_tracks(limit=limit, offset=0, time_range=time_range)
        top_tracks.extend(response['items'])

        # Fetch next 50 tracks if available
        if len(response['items']) == limit:
            response = sp.current_user_top_tracks(limit=limit, offset=50, time_range=time_range)
            top_tracks.extend(response['items'])

        # Return raw track data
        return top_tracks

    except spotipy.exceptions.SpotifyException as e:
        print(f"Error fetching top tracks: {e}")
        return []

# gets users top tracks for time range. DEFAULT: num_tracks=100, time_range='medium_term' 
# long_term  last ~1 year, medium_term last ~6 months,short_term last ~4 weeks
def fetch_top_tracks(sp, num_tracks=100, time_range='medium_term'):
    top_tracks = []
    limit = 50  # Spotify API max limit for top tracks per request
    VALID_TIME_RANGES = ['short_term', 'medium_term', 'long_term']
    
     # Validate
    if time_range not in VALID_TIME_RANGES:
        raise ValueError(f"Invalid time_range: {time_range}. Must be one of {VALID_TIME_RANGES}.")
    if num_tracks <= 0:
        raise ValueError("num_tracks must be a positive integer.")

   
    offset = 0
    try:
        # Fetch first num_tracks%50 tracks to ensure spotify API max limit for top tracks per request is followed 
        if num_tracks % limit != 0:
            response = sp.current_user_top_tracks(limit=num_tracks % limit, offset=offset, time_range=time_range)
            offset += num_tracks % limit
            top_tracks.extend(response['items'])

        # Fetch next 50 tracks till num_tracks is met 
        for _ in range(num_tracks // limit):
            response = sp.current_user_top_tracks(limit=limit, offset=offset, time_range=time_range)
            offset += limit
            top_tracks.extend(response['items'])

        # Return raw track data
        return top_tracks

    except spotipy.exceptions.SpotifyException as e:
        print(f"Error fetching top tracks: {e}")
        return []

    #  fetch audio features for a given list of track URIs.
def fetch_audio_features(sp, track_uris):
    audio_features = {}  # dict to store the track's URI and corresponding audio features
    BATCH_SIZE = 100  # Spotify API limit for audio features per request
    try:
        for i in range(0, len(track_uris), BATCH_SIZE):  # Iterate over track_uris in batches of 100
            batch = track_uris[i:i + BATCH_SIZE]  # Get the current batch of URIs
            response = sp.audio_features(batch)  # Fetch audio features for the batch

            if response: 
                for features in response:  # Iterate over each track's audio features
                    if features:  # Ensure features are valid (not None)
                        audio_features[features["uri"]] = {
                            "danceability": features.get("danceability"),
                            "energy": features.get("energy"),
                            "tempo": features.get("tempo"),
                            "valence": features.get("valence"),
                            "acousticness": features.get("acousticness"),
                            "instrumentalness": features.get("instrumentalness"),
                        }
    except Exception as e:
        print(f"Error fetching audio features: {e}")

    print(audio_features)
    return audio_features


def parse_saved_tracks(sp, raw_tracks, genre_cache):
    parsed_tracks = []
    unknown_artist_ids = set()
    track_uris = []

    for track in raw_tracks:  # raw_tracks is now a flat list of tracks
        artist_id = track['artists'][0]['id']  # grabbing artist_id
        if artist_id not in genre_cache:  # checking if in genre cache
            unknown_artist_ids.add(artist_id)  # adding to unknown set if not in

        track_uris.append(track['uri']) #grabbing all track URIs and putting them in a dict for attribute population

        parsed_tracks.append({
            "track_name": track['name'],
            "artist_names": [artist['name'] for artist in track['artists']],
            "artist_id": track['artists'][0]['id'],
            "album_name": track['album']['name'],
            "uri": track['uri'],
            "url": track["external_urls"]['spotify'],
            "album_cover": track['album']['images'][0]['url'],
        })

    audio_features = fetch_audio_features(sp, track_uris)

    for track in parsed_tracks:
        track['audio_features'] = audio_features.get(track['uri'], {})


    # Fetching unknown artist genres and adding to our genre_cache
    if unknown_artist_ids:
        fetched_genres = fetch_unknown_artist_genres(sp, list(unknown_artist_ids))
        genre_cache.update(fetched_genres)

    # Adding all genres to parsed tracks
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