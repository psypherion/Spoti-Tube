# Spoti-Tube

Spoti-Tube is a Python script that allows you to download songs from a given Spotify playlist. It leverages the Spotify API to retrieve information about the songs in the playlist and then uses YouTube to find and download the corresponding songs in MP3 format.

## Setup

Before using Spoti-Tube, you need to set up your environment by following these steps:

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/spoti-tube.git
   cd spoti-tube
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root directory and add your Spotify API credentials:

   ```env
   CLIENT_ID="your_spotify_client_id"
   CLIENT_SECRET="your_spotify_client_secret"
   ```

   Replace `your_spotify_client_id` and `your_spotify_client_secret` with your actual Spotify API credentials.

## Usage

1. Run the Spoti-Tube script:

   ```bash
   python spoti-tube.py
   ```

2. Enter the Spotify playlist link when prompted.

3. Spoti-Tube will then fetch the playlist information and search for corresponding songs on YouTube.

4. The script will start downloading the songs in MP3 format to the `music` directory.

## Notes

- Spoti-Tube uses the [pytube](https://github.com/pytube/pytube) library to interact with YouTube and download videos.

- The downloaded songs will be saved in the `music` directory with the playlist name as a subdirectory.

- If an error occurs during the download, the script will continue with the next song.

## Disclaimer

Please be aware that downloading copyrighted material without permission may violate the terms of service of certain platforms and local copyright laws. Use this script responsibly and only for legal purposes.

---

Feel free to contribute to the project or report any issues on the [GitHub repository](https://github.com/ky13-troj/spoti-tube).
