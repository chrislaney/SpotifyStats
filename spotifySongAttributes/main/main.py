import os
from utils import load_genre_cache, parse_playlist, parse_tracks  
from flask import Flask, session, url_for, request, jsonify, Response, render_template
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import FlaskSessionCacheHandler
from werkzeug.utils import redirect
from user import User
print("Flask is running THIS file:", __file__)
# Create the Flask app
app = Flask(__name__)

#change in prod 
app.config['SECRET_KEY'] = os.urandom(64)

#these are got when you create a spotify developer app on spotify.com
client_id = '104ec8795164430c814e8b4e98a6d781'
client_secret = 'e1dbca47ea984b6a8256631b4bbcfab8'
redirect_uri = 'http://localhost:5000/callback'

#need all the scopes listed to fetch data wanted
scope = 'user-library-read, user-top-read, playlist-read-private' #to add more scopes you just seperate them within the string with a comma

# OAuth handler
cache_handler = FlaskSessionCacheHandler(session)
sp_oauth = SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope=scope,
    cache_handler=cache_handler,
    show_dialog=True
)

# ensure valid token and refresh if needed
def ensure_token():
    token_info = session.get("token_info", None)

    if not token_info:
        raise Exception("No token found. User must log in.")

    if sp_oauth.is_token_expired(token_info):
        print("Token expired, refreshing...")
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
        session['token_info'] = token_info  # Save updated token

    return token_info

# ensure token or redirect to login
def ensure_token_or_redirect():
    try:
        return ensure_token()
    except Exception:
        return redirect(sp_oauth.get_authorize_url())

# Home route - Checks login and redirects
@app.route('/')
def home():
    if 'token_info' not in session:
        return redirect(sp_oauth.get_authorize_url())
    return redirect(url_for('get_user'))

# Callback for Spotify OAuth, stores token info in flask session
@app.route('/callback')
def callback():
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session['token_info'] = token_info  # Save token in session
    return redirect(url_for('get_user'))

# Get user data and genre distributions
@app.route('/get_user')
def get_user():
    token_info = ensure_token_or_redirect()
    if isinstance(token_info, dict):
        try:
            sp = Spotify(auth=token_info['access_token'])
            genre_cache = load_genre_cache()
            user = User.from_spotify(sp, genre_cache)
            #print(user)
            return jsonify({"user": user.__dict__})
        except Exception as e:
            #traceback.print_exc()  # prints full error to terminal and webpage for debugging 
            return jsonify({'error': str(e)})

# Get playlist data
@app.route('/get_playlist/<playlist_id>')
def get_playlist_data(playlist_id):
    token_info = ensure_token_or_redirect()
    if isinstance(token_info, dict):
        try:
            sp = Spotify(auth=token_info['access_token'])
            genre_cache = load_genre_cache()

            playlist_data = parse_playlist(sp, playlist_id)

            parsed_tracks, subgenre_distro, supergenre_distro = parse_tracks(
                sp, playlist_data['tracks'], genre_cache
            )

            response = {
                "playlist_metadata": {
                    "id": playlist_data['id'],
                    "name": playlist_data['name'],
                    # "description": playlist_data['description'],
                    # "owner": playlist_data['owner'],
                    # "image_url": playlist_data['image_url'],
                    "track_count": playlist_data['track_count']
                },
                "subgenre_distribution": subgenre_distro,
                "supergenre_distribution": supergenre_distro
               #"parsed_tracks": parsed_tracks
            }

            #print(" Final response:", response)
            return jsonify(response)

        except Exception as e:
            #traceback.print_exc()
            return jsonify({'error': str(e)})
    else:
        return token_info  # Redirect response

# Logout route
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)


