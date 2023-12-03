from dotenv import load_dotenv
import os
import base64
import requests
import json
import urllib.request
import re
import pytube
import sys
load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

def get_token():
    auth_string = client_id+":"+client_secret
    auth_encode = auth_string.encode("utf-8")
    auth_based64 = str(base64.b64encode(auth_encode), "utf-8")
    
    url = 'https://accounts.spotify.com/api/token'
    headers = {
        "Content-Type" : "application/x-www-form-urlencoded",
        "Authorization" : "Basic " + auth_based64
    }
    # print(headers["Authorization"])
    data ={
        "grant_type" : "client_credentials"
    }
    
    result = requests.post(url, headers=headers, data=data)
    json_data = json.loads(result.content)
    token = json_data["access_token"]
    return token

def get_playlist(token, playlist_id):
    base_url = "https://api.spotify.com/v1/playlists/"
    id = playlist_id
    playlist_url = base_url+id
    # print(playlist_url)
    token=token
    headers = {
        "Authorization": f"Bearer {token}"
    }
    # print(headers)

    result = requests.get(playlist_url, headers=headers)
    json_data = json.loads(result.content)
    # data_json = json.dumps(json_data)
    return json_data

def list_id(playlist_link):
    id_si = playlist_link.split('playlist/')
    if '?si' in id_si[1]:
        playlist_id = id_si[1].split('?')[0]
    else :
        playlist_id = id_si
    return str(playlist_id)

def queries(playlist_dict):
    count_num = 0
    arr = []
    num = 0
    name_parent = []
    artist_name = []
    song_name = []
    for item in playlist_dict["tracks"]:
        count_num += 1
        arr.append(playlist_dict["tracks"][item])
        if count_num > 1 :
            for i in range(0, len(arr[1])):
                for keys in arr[1][i]["track"]:
                    if arr[1][i]["track"]["name"] not in song_name:
                        song_name.append(arr[1][i]["track"]["name"]) 
                        for album_items in arr[1][i]["track"]["album"]:
                            name_parent.append(arr[1][i]["track"]["album"][album_items])

    for dict in name_parent:
        if isinstance(dict, type(name_parent[1])):
            if "name" in dict[0]:
                artist_name.append(dict[0]["name"])


    search_query = []
    for i in range(0, len(artist_name)):
        search_query.append(f"{song_name[i]} by {artist_name[i]}")
        

    search_queries = []
    for queries in search_query:
        queries = queries.replace(" ", "+")
        search_queries.append(queries)
        
    youtube_queries = []
    
    for query in search_queries:
        try : 
            html = urllib.request.urlopen("https://www.youtube.com/results?search_query="+query)
            video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
            youtube_queries.append("https://www.youtube.com/watch?v=" + video_ids[0])
        except Exception:
            pass
        
    return youtube_queries
    
def Download(link):
    youtubeObject = pytube.YouTube(link,
                                   use_oauth=True,
                                   allow_oauth_cache=True)
    youtubeObject = youtubeObject.streams.filter(only_audio=True).first()
    try:
        print(f"\nYour song : {youtubeObject.title} has started.")
        youtubeObject.download(output_path=f"music/{playlist_name}",filename=f"{youtubeObject.title}.mp3")
    except:
        print("An error has occurred")
    
    
if __name__ == "__main__":
    token = get_token()
    playlist_link = sys.argv[1]
    playlist_id = list_id(playlist_link)
    playlist_dict = get_playlist(token, playlist_id=playlist_id)
    playlist_name = playlist_dict["name"]
    youtube_queries = queries(playlist_dict)

    for links in youtube_queries : 
        Download(links)
