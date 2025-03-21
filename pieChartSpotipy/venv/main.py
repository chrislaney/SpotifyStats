import base64
import os
from utils import parse_saved_tracks, get_liked_songs, load_genre_cache, get_genre_frequencies, plot_genre_pie_chart, plot_interactive_pie_chart
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
scope = 'playlist-read-private, user-library-read' #to add more scopes you just seperate them within the string with a comma

cache_handler = FlaskSessionCacheHandler(session)
sp_oauth = SpotifyOAuth(
    client_id=client_id,
    client_secret=client_secret,
    redirect_uri=redirect_uri,
    scope=scope,
    cache_handler=cache_handler,
    show_dialog=True
)

#instance of spotify client, with the oauth credentials
sp = Spotify(auth_manager=sp_oauth)


#END POINTS -------------------------------

#directs user to homepage, and makes them log in if needed
@app.route('/')
def home():
    #cache_handler.get_cached_token checks to see if user has a prexisting cached token, if not directs them to auth
    if not sp_oauth.validate_token(cache_handler.get_cached_token()):
        #this if not checks if user is not logged in, and directs them to auth_url
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url) #if user not logged in, directs them to auth
    return redirect(url_for('get_data')) #if user is logged in, fires get_playlists


#auth manager, refreshes token upon expiration. This is what provides a continuous experience and no need to manually fetch token
@app.route('/callback')
def callback():
    sp_oauth.get_access_token(request.args['code'])
    return redirect(url_for('get_data'))



@app.route('/get_data')
def get_data():

    if not sp_oauth.validate_token(cache_handler.get_cached_token()): #This token validation could/should be its own method
        auth_url = sp_oauth.get_authorize_url()
        return redirect(auth_url)

    genre_cache = load_genre_cache()
    all_liked_songs_raw = get_liked_songs(sp)
    parsed_tracks = parse_saved_tracks(sp, all_liked_songs_raw, genre_cache)

    # Get parsed_tracks and generate genre frequencies
    genre_frequencies = get_genre_frequencies(parsed_tracks)

    # Generate pie chart as base64 string
    #img_b64 = plot_genre_pie_chart(genre_frequencies)
    #img_data = base64.b64decode(img_b64)

    # Render the HTML template and pass the image

    #return Response(img_data, mimetype='image/png')

    chart_html = plot_interactive_pie_chart(genre_frequencies)

    return render_template('plot.html', chart_html=chart_html)



    #return jsonify(parsed_tracks)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))


# this runs the flask app - it is created at the top of the file
if __name__ == '__main__':
    app.run(debug=True)
