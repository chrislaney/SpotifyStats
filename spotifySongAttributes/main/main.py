import os
from utils import load_genre_cache
from flask import Flask, session, url_for, request, jsonify, Response, render_template
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import FlaskSessionCacheHandler
from werkzeug.utils import redirect
from user import User

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

# Token management
def ensure_token():
    token_info = sp_oauth.get_cached_token()
    if not token_info:
        raise Exception("No token found. User must log in.")
    if sp_oauth.is_token_expired(token_info):
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
    return token_info

# Home route - Checks login and redirects
@app.route('/')
def home():
    if not sp_oauth.get_cached_token():
        return redirect(sp_oauth.get_authorize_url())
    return redirect(url_for('get_data'))

# Callback for Spotify OAuth
@app.route('/callback')
def callback():
    sp_oauth.get_access_token(request.args['code'])
    return redirect(url_for('get_data'))

# Get user data and genre distributions
@app.route('/get_data')
def get_data():
    try:
        token_info = ensure_token()
        sp = Spotify(auth=token_info['access_token'])

        genre_cache = load_genre_cache()
        user = User.from_spotify(sp, genre_cache)
        print(user)

        return jsonify({"user": user.__dict__})
    except Exception as e:
        if "No token found" in str(e):
            return redirect(sp_oauth.get_authorize_url())
        return jsonify({'error': str(e)})

# Logout route
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
