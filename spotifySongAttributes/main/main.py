import os
from utils import parse_saved_tracks, load_genre_cache, get_top_100, fetch_top_tracks, get_normalized_genre_distribution
from flask import Flask, session, url_for, request, jsonify, Response, render_template

from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from spotipy.cache_handler import FlaskSessionCacheHandler
from werkzeug.utils import redirect



#this creates the flask app
app = Flask(__name__)

#this secret key is to secure the flask session so data cannot be tampered with between running and display on webpage
#in a production env you want this to be a fixed string stored in an env variable or in a secure cred store
app.config['SECRET_KEY'] = os.urandom(64)

#these are got when you create a spotify developer app on spotify.com
client_id = '104ec8795164430c814e8b4e98a6d781'
client_secret = 'e1dbca47ea984b6a8256631b4bbcfab8'
redirect_uri = 'http://localhost:5000/callback'

#need all the scopes listed to fetch data wanted
scope = 'user-library-read, user-top-read, playlist-read-private' #to add more scopes you just seperate them within the string with a comma

cache_handler = FlaskSessionCacheHandler(session)
sp_oauth = SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope=scope,
    cache_handler=cache_handler,
    show_dialog=True
)

#token_info = sp_oauth.get_cached_token()  # Retrieve token from cache
#if not token_info:
#    auth_url = sp_oauth.get_authorize_url()
#    print(f"Please log in: {auth_url}")
#    code = input("Enter the authorization code: ")
#    token_info = sp_oauth.get_access

##instance of spotify client, with the oauth credentials
#sp = Spotify(auth_manager=sp_oauth)

#Ensure the token is valid and refresh if necessary
def ensure_token():

    token_info = sp_oauth.get_cached_token()
    if not token_info:
        raise Exception("No token found. User must log in.")
    if sp_oauth.is_token_expired(token_info):
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
    return token_info

    token_info = sp_oauth.get_cached_token()
    if not token_info:
        # If no cached token, redirect user to login
        #notify user? 
        return redirect(sp_oauth.get_authorize_url())
    if sp_oauth.is_token_expired(token_info):
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
    return token_info


#END POINTS -------------------------------

#directs user to homepage, and makes them log in if needed
@app.route('/')
def home():
    #cache_handler.get_cached_token checks to see if user has a prexisting cached token, if not directs them to auth
    if not sp_oauth.get_cached_token():
        #this if not checks if user is not logged in, and directs them to auth_url
        return redirect(sp_oauth.get_authorize_url()) #if user not logged in, directs them to auth
    return redirect(url_for('get_data')) #if user is logged in, fires get_playlists



#auth manager, refreshes token upon expiration. This is what provides a continuous experience and no need to manually fetch token
@app.route('/callback')
def callback():
    sp_oauth.get_access_token(request.args['code'])
    return redirect(url_for('get_data'))



@app.route('/get_data')
def get_data():
   
    try:
        # ensure token is good first 
        token_info = ensure_token()
    
        # authenticate token 
        sp = Spotify(auth=token_info['access_token'])


        genre_distribution = get_normalized_genre_distribution(sp, 4)
        return jsonify(genre_distribution)

        # TO-DO save top 100 song IDS to user object 
        # TO-DO create genre dist to then use in similarity scoring  

    except Exception as e:
        #If no token exists, redirect to Spotify login
        if "No token found" in str(e):
            return redirect(sp_oauth.get_authorize_url())
        # Handle any other exceptions
        return jsonify({'error': str(e)})



@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))


# this runs the flask app - it is created at the top of the file
if __name__ == '__main__':
    app.run(debug=True)
