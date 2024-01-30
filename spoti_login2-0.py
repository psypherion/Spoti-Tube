from flask import Flask, redirect, request, session, url_for, jsonify
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv
import json

from IPython.display import display

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Spotify API credentials
SPOTIPY_CLIENT_ID = "2b1ee99056b14d68b294dcdb36e60eb4"
SPOTIPY_CLIENT_SECRET = "daa293bbae3245f881e860ff32fbeabe"
SPOTIPY_REDIRECT_URI = "http://127.0.0.1:5000/callback" 
SPOTIFY_SCOPES = 'user-read-private user-read-email playlist-read-private'

# Spotify OAuth configuration
sp_oauth = SpotifyOAuth(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, scope=SPOTIFY_SCOPES)

@app.route('/')
def index():
    return 'Welcome to My Spotify App! <a href="/login">Login with Spotify</a>'

@app.route('/login')
def login():
    return redirect(sp_oauth.get_authorize_url())

@app.route('/callback')
def callback():
    token_info = sp_oauth.get_access_token(request.args['code'])
    session['token_info'] = token_info
    return "logged in"

@app.route('/get_user_id')
def get_user_id():
    # if 'token_info' not in session:
    #     return redirect(url_for('login'))

    print(session)
    print(session['token_info']['access_token'])
    sp = Spotify(auth=session['token_info']['access_token'])
    display(dir(sp))
    try:
        print(sp.current_user())
    except Exception as e:
        print(e)
    # print(sp.current_user())
    # user_info = sp.current_user()
    # user_id = user_info['id']
    # user = sp.user(user_id)
    
@app.route('/get_user_info')
def get_user_info():
    if 'token_info' not in session:
        return redirect(url_for('login'))

    try:
        sp = Spotify(auth=session['token_info']['access_token'])
        user_info = sp.current_user()
        return json.dumps(user_info)
    except Exception as e:
        return jsonify({'error': str(e)})

    return f'{sp}'

if __name__ == '__main__':
    app.run(debug=True)
