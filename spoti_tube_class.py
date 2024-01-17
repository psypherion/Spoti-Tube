# Import necessary libraries
from dotenv import load_dotenv
import os
import base64
import requests
import json
import urllib.request
import re
import sys
import yt_dlp
from pydub import AudioSegment
import time

# Load environment variables from a .env file
load_dotenv()

class SpotifyDownloader:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = self.get_token()

    def get_token(self):
        auth_string = f"{self.client_id}:{self.client_secret}"
        auth_encode = auth_string.encode("utf-8")
        auth_based64 = str(base64.b64encode(auth_encode), "utf-8")

        url = 'https://accounts.spotify.com/api/token'
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": "Basic " + auth_based64
        }
        data = {"grant_type": "client_credentials"}

        result = requests.post(url, headers=headers, data=data)
        json_data = json.loads(result.content)
        return json_data["access_token"]

class PlaylistDownloader:
    def __init__(self, token, playlist_link, resolution="144p"):
        self.token = token
        self.playlist_link = playlist_link
        self.resolution = resolution

    def get_playlist_id(self):
        id_si = self.playlist_link.split('playlist/')
        if '?si' in id_si[1]:
            return id_si[1].split('?')[0]
        else:
            return id_si[1]

    def get_playlist_details(self):
        playlist_id = self.get_playlist_id()
        base_url = "https://api.spotify.com/v1/playlists/"
        playlist_url = base_url + playlist_id
        headers = {"Authorization": f"Bearer {self.token}"}
        result = requests.get(playlist_url, headers=headers)
        return json.loads(result.content)

    def extract_song_artist_name(self, playlist_dict):
        count_num = 0
        arr = []
        num = 0
        name_parent = []
        artist_name = []
        song_name = []

        for item in playlist_dict["tracks"]:
            count_num += 1
            arr.append(playlist_dict["tracks"][item])
            if count_num > 1:
                for i in range(0, len(arr[1])):
                    for keys in arr[1][i]["track"]:
                        if arr[1][i]["track"]["name"] not in song_name:
                            song_name.append(arr[1][i]["track"]["name"])
                            for album_items in arr[1][i]["track"]["album"]:
                                name_parent.append(arr[1][i]["track"]["album"][album_items])

        for item in name_parent:
            if isinstance(item, list) and item and "name" in item[0]:
                artist_name.append(item[0]["name"])
        return song_name, artist_name

    def generate_youtube_queries(self, song_name, artist_name):
        search_query = [f"{song_name[i]} by {artist_name[i]}" for i in range(len(artist_name))]
        search_queries = [query.replace(" ", "+") for query in search_query]

        youtube_queries = []
        for query in search_queries:
            try:
                html = urllib.request.urlopen("https://www.youtube.com/results?search_query="+query)
                video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
                youtube_queries.append("https://www.youtube.com/watch?v=" + video_ids[0])
            except Exception:
                pass

        return youtube_queries

class AudioDownloader:
    def __init__(self, output_directory='downloads', desired_bitrate="192k", resolution="144p"):
        self.output_directory = output_directory
        self.desired_bitrate = desired_bitrate
        self.resolution = resolution
        self.total_time = 0
    def sanitize_filename(self, title):
        return title.replace("/", "_")

    def download_audio(self, video_urls, song_name, artist_name, playlist_name):
        count = 0
        song_name = song_name
        artist_name = artist_name
        playlist_name = playlist_name
        output_directory = self.output_directory + "/" + playlist_name
        playlist_details_file = os.path.join(output_directory, f"{playlist_name}.txt")
        with open(playlist_details_file, "a", encoding="utf-8") as playlist_name_file:
            playlist_name_file.write(f"Playlist Name: {playlist_name}\n\n")
        for song in song_name:
            with open(playlist_details_file, "a", encoding="utf-8") as song_details_file:
                song_details_file.write(f"Title: {song_name[count]}\nArtist: {artist_name[count]}\n\n")
            count += 1
        print(f"\nPlaylist Details:\nSong Name: {song_name}\nArtist Name: {artist_name}\n")
        for url in video_urls:
            try:
                start_time = time.time()
                ydl_opts = {
                    'format': f'bestvideo[height={self.resolution}]+bestaudio/best',
                    'outtmpl': f'{output_directory}/%(title)s.%(ext)s',
                    'quiet': True,
                    'extractor_args': {
                        'youtube': {
                            'quiet': True,
                            'nocheckcertificate': True,
                            'source_address': '0.0.0.0',
                        },
                        'youtube:info': {
                            'skip': ['ios', 'android', 'm3u8'],
                        },
                    },
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info_dict = ydl.extract_info(url, download=True)
                    video_title = info_dict.get('title', 'video')
                    sanitized_title = self.sanitize_filename(video_title)
                    audio_file_path = ydl.prepare_filename(info_dict)

                    audio = AudioSegment.from_file(audio_file_path)

                    if not os.path.exists(output_directory):
                        os.makedirs(output_directory)

                    output_mp3 = os.path.join(output_directory, f"{sanitized_title}.mp3")

                    audio.export(output_mp3, format="mp3", bitrate=self.desired_bitrate)
                    count += 1
                    end_time = time.time()
                    elapsed_time = end_time - start_time
                    self.total_time += elapsed_time

                    print(f"Video '{video_title}' converted to MP3 and saved as '{output_mp3}'")
                    print(f"Time taken: {elapsed_time} seconds\n")

            except yt_dlp.utils.DownloadError as e:
                if 'Video unavailable' in str(e):
                    print(f"Warning: Video '{url}' is unavailable due to copyright restrictions.")
                else:
                    print(f"Error: {e}")

    def delete_video_files(self, folder_path):
        files = os.listdir(folder_path)
        for file in files:
            if file.endswith(".mp4"):
                file_path = os.path.join(folder_path, file)
                try:
                    os.remove(file_path)
                    print(f"File '{file}' deleted successfully.")
                except Exception as e:
                    print(f"Error deleting file '{file}': {e}")

class SpotifyPlaylistProcessor:
    def __init__(self, client_id, client_secret, playlist_link, resolution="144p"):
        self.spotify_downloader = SpotifyDownloader(client_id, client_secret)
        self.playlist_downloader = PlaylistDownloader(self.spotify_downloader.token, playlist_link, resolution)
        self.audio_downloader = AudioDownloader()

    def process_playlist(self):
        # Get playlist details
        playlist_dict = self.playlist_downloader.get_playlist_details()

        # Extract playlist name, song names, and artist names
        playlist_name = playlist_dict["name"]
        song_name, artist_name = self.playlist_downloader.extract_song_artist_name(playlist_dict)

        # Generate YouTube search queries
        youtube_queries = self.playlist_downloader.generate_youtube_queries(song_name, artist_name)

        # Define output directory path
        output_directory_path = f'{self.audio_downloader.output_directory}/{playlist_name}'

        # Create the output directory if it doesn't exist
        if output_directory_path not in os.listdir():
            os.mkdir(output_directory_path)

        # Download audio from YouTube
        self.audio_downloader.download_audio(
            youtube_queries,
            song_name=song_name,
            artist_name=artist_name,
            playlist_name=playlist_name
        )
        self.audio_downloader.delete_video_files(output_directory_path)

# Example usage:
# client_id and client_secret are your Spotify API credentials
# Spotify API credentials
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
playlist_link = sys.argv[1]
# Create a SpotifyPlaylistProcessor instance
processor = SpotifyPlaylistProcessor(client_id, client_secret, playlist_link)

# Process the playlist
processor.process_playlist()
