import requests
import json
from flask import Flask, render_template, request, jsonify, redirect, url_for, send_file, session
import os
import urllib.parse
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = os.urandom(24)
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

AUTH_URL = "https://accounts.spotify.com/authorize"
TOKEN_URL = "https://accounts.spotify.com/api/token"
API_BASE_URL = "https://api.spotify.com/v1/"
REDIRECT_URI = "http://127.0.0.1:5000/callback"
SPOTIFY_SCOPES = 'user-read-private user-read-email playlist-read-private'

@app.route('/')
def index():
    return "Welcome to my Spotify user Data Showing App : <br><br><a href='/login'>Login with Spotify</a>"

@app.route('/login')
def login():
    params = {
        "client_id": client_id,
        "response_type": "code",
        "redirect_uri": REDIRECT_URI,
        "scope": SPOTIFY_SCOPES,
        "show_dialog": True
    }
    
    auth_url = f"{AUTH_URL}?{urllib.parse.urlencode(params)}"
    return redirect(auth_url)


@app.route('/callback')
def callback():
    if "error" in request.args:
        return jsonify({"error": request.args["error"]})
    
    if "code" in request.args:
        req_body = {
            "code" : request.args["code"],
            "redirect_uri" : REDIRECT_URI,
            "grant_type" : "authorization_code",
            "client_id" : client_id,
            "client_secret" : client_secret
        }
        
        response = requests.post(TOKEN_URL, data=req_body)
        token_info = response.json()
        
        session['access_token']= token_info['access_token']
        session['refresh_token'] = token_info['refresh_token']
        session['expires_at'] = datetime.now().timestamp() + token_info['expires_in']
        
        return redirect('/playlists')

@app.route('/playlists')
def playlists():
    if "access_token" not in session:
        return redirect('/login')
    
    headers = {
        "Authorization": f"Bearer {session['access_token']}"
    }
    
    response = requests.get(API_BASE_URL + "me/playlists", headers=headers)
    # playlists = response.json()
    print(response)
    
    return "0"


@app.route('/refresh_token')
def refresh_token():
    if "refresh_token" not in session:
        return redirect('/login')
    
    req_body = {
        "grant_type" : "refresh_token",
        "refresh_token" : session['refresh_token'],
        "client_id" : client_id,
        "client_secret" : client_secret
    }
    
    response = requests.post(TOKEN_URL, data=req_body)
    new_token_info = response.json()
    
    session['access_token']= new_token_info['access_token']
    session['refresh_token'] = new_token_info['refresh_token']
    session['expires_at'] = datetime.now().timestamp() + new_token_info['expires_in']
    
    return redirect('/playlists')



if __name__ == '__main__':
    app.run(debug=True)