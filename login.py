import requests
from flask import Flask, request, jsonify, redirect, session, render_template
import os
import urllib.parse
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)
app.secret_key = os.urandom(24)
client_id = '4d883b68243a4c37aed440eb6228bab3'
client_secret = '2b5bf4c12d864fe3b868af0a537c9e02'

AUTH_URL = "https://accounts.spotify.com/authorize"
TOKEN_URL = "https://accounts.spotify.com/api/token"
API_BASE_URL = "https://api.spotify.com/v1/"
REDIRECT_URI = "http://127.0.0.1:5000/callback"


@app.route('/')
def index():
    return "Welcome to my Spotify user Data Showing App : <br><br><a href='/login'>Login with Spotify</a>"

@app.route('/login')
def login():
    SPOTIFY_SCOPES = 'user-top-read'
    
    params = {
        "client_id": client_id,
        "response_type": 'code',
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
        session['expires_at'] = datetime.now().timestamp() + 10
        
        return redirect('/top_genres')

@app.route('/playlists')
def get_playlists():
    if "access_token" not in session:
        return redirect('/login')
    
    if datetime.now().timestamp() > session['expires_at']:
        print("refreshing token")
        return redirect('/refresh_token')
    
    headers = {
        "Authorization": f"Bearer {session['access_token']}"
    }
    
    response = requests.get(API_BASE_URL + "me/playlists", headers=headers)
    playlists = response.json()
    print(response)
    
    return jsonify(playlists)


@app.route('/refresh_token')
def refresh_token():
    if "refresh_token" not in session:
        return redirect('/login')
    
    if datetime.now().timestamp() > session['expires_at']:
        print("refreshing token")
        req_body = {
            "grant_type" : "refresh_token",
            "refresh_token" : session['refresh_token'],
            "client_id" : client_id,
            "client_secret" : client_secret
        }
    
        response = requests.post(TOKEN_URL, data=req_body)
        new_token_info = response.json()
        
        session['access_token']= new_token_info['access_token']
        session['expires_at'] = datetime.now().timestamp() + 10
    
        return redirect('/playlists')


@app.route('/top_tracks')
def get_tracks():
    if "access_token" not in session:
        return redirect('/login')
    
    if datetime.now().timestamp() > session['expires_at']:
        print("refreshing token")
        return redirect('/refresh_token')
    
    headers = {
        "Authorization": f"Bearer {session['access_token']}"
    }
    
    # Get available genre seeds
    response_genres_seeds = requests.get(API_BASE_URL + "me/top/tracks", headers=headers)
    available_genres = response_genres_seeds.json()
    print(available_genres["items"][0]["name"])
    top_songs = available_genres["items"]
    top = []
    for i in range(0, 19):
        print(top_songs[i]["name"])
        top.append(top_songs[i]["name"])
    
    return top

@app.route('/top_artists')
def top_artists():
    if "access_token" not in session:
        return redirect('/login')
    
    if datetime.now().timestamp() > session['expires_at']:
        print("refreshing token")
        return redirect('/refresh_token')
    
    headers = {
        "Authorization": f"Bearer {session['access_token']}"
    }

    response_top_artists = requests.get(API_BASE_URL + "me/top/artists", headers=headers)
    top_artists = response_top_artists.json()

    artists = top_artists["items"]
    top = []
    for i in range(0, 19):
        print(artists[i]["name"])
        top.append(artists[i]["name"])
    
    return top

@app.route('/top_genres')
def top_genres():
    if "access_token" not in session:
        return redirect('/login')
    
    if datetime.now().timestamp() > session['expires_at']:
        print("refreshing token")
        refresh_token_url = f"{API_BASE_URL}me/top/artists?access_token={session['access_token']}"
        response_top_genres = requests.get(refresh_token_url)
    else:
        headers = {
            "Authorization": f"Bearer {session['access_token']}"
        }

        response_top_genres = requests.get(API_BASE_URL + "me/top/artists"
                                           , headers=headers)
        
        response_top_tracks = requests.get(API_BASE_URL + "me/top/tracks"
                                           , headers=headers)
        
    
    if response_top_genres.status_code == 200:
        top_genres_data = response_top_genres.json()
        top_tracks_data = response_top_tracks.json()
        items = top_genres_data["items"]
        top_songs = top_tracks_data["items"]
        top_genres = []
        top_artists = []
        top_tracks = []
        image_urls = []  # Initialize image_urls here
        test = top_genres_data
        for i in range(0, 19):
            print(items[i]["genres"])
            top_genres.append(items[i]["genres"])
        
        genres = [item for sublist in top_genres for item in sublist]
        
        for i in range(0, 19):
            print(items[i]["name"])
            top_artists.append(items[i]["name"])
        
        for i in range(0, 19):
            print(top_songs[i]["name"])
            top_tracks.append(top_songs[i]["name"])
            
        # genre counts :
        genre_counts = {}
        for genre in genres:
            if genre in genre_counts:
                genre_counts[genre] += 1
            else:
                genre_counts[genre] = 1
        
        # genre counts sorted 
        sorted_genres = sorted(genre_counts.items(), key=lambda x: x[1], reverse=True)
        
        # first ten genres percentage
        total_count = sum([count for genre, count in sorted_genres[:10]])
        first_ten_percentage = [(genre, round(count/total_count*100)) for genre, count in sorted_genres[:10]]
        labels = [genre[0] for genre in first_ten_percentage]
        values = [genre[1] for genre in first_ten_percentage]
        
        print(values)
        print(labels)
        # Creating the pie chart
        fig, ax = plt.subplots()
        ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle

        # Saving the plot to a BytesIO object
        img_buf = io.BytesIO()
        plt.savefig(img_buf, format='png')
        img_buf.seek(0)

        # Encoding the image as base64 for embedding in HTML
        img_base64 = base64.b64encode(img_buf.getvalue()).decode('utf-8')

        for item in top_genres_data.get("items", []):
            images = item.get("images", [])
            if images and len(images) > 2:  # Check if there are images and at least 3 images are available
                image_urls.append(images[2]["url"])

        # Print the list of image URLs
        print("Image URLs:")
        for url in image_urls:
            print(url)
        
        artists_urls = [item['external_urls']['spotify'] for item in top_genres_data['items']]
        track_urls = [item['external_urls']['spotify'] for item in top_tracks_data['items']]

        # Print the extracted Spotify URLs
        for url in artists_urls:
            print(url)
            # Pass image_urls when rendering the template
        return render_template('top_genres.html', img_base64=img_base64, top_artists=top_artists, top_tracks=top_tracks, top_genres=top_genres, image_urls=image_urls, artists_urls=artists_urls, track_urls=track_urls)
        # return track_urls
    else:
        return jsonify({"error": "Failed to fetch top genres", "status_code": response_top_genres.status_code})

if __name__ == '__main__':
    app.run(debug=True)