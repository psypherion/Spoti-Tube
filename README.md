# Spoti-Tube

Spoti-Tube is a Python script that allows you to download songs from a given Spotify playlist. By leveraging the Spotify API for playlist information and the pytube library for YouTube integration, Spoti-Tube seamlessly converts your favorite Spotify playlist into a local collection of MP3 files.

## Features

- **Easy Setup:** Quickly set up Spoti-Tube by installing the required dependencies and configuring your Spotify API credentials in the `.env` file.

- **Playlist Conversion:** Input your Spotify playlist link, and Spoti-Tube will retrieve the list of songs and search for corresponding MP3s on YouTube.

- **Automatic Download:** The script automatically downloads the identified songs in MP3 format to the `music` directory, organized by playlist name.

- **Error Handling:** Spoti-Tube gracefully handles errors during the download process, ensuring a smooth experience even in the face of occasional issues.


**GitHub Repository:** [Spoti-Tube on GitHub](https://github.com/yourusername/spoti-tube)

Enjoy your seamless journey from Spotify playlists to local MP3s with Spoti-Tube!
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

2. Enter the Spotify playlist link when prompted, and let Spoti-Tube handle the rest.

3. Spoti-Tube will then fetch the playlist information and search for corresponding songs on YouTube.

4. The script will start downloading the songs in MP3 format to the `music` directory, & create a directory using the playlist name.

## Notes

- Spoti-Tube uses the [pytube](https://github.com/pytube/pytube) library to interact with YouTube and download videos.

- The downloaded songs will be saved in the `music` directory with the playlist name as a subdirectory.

- If an error occurs during the download, the script will continue with the next song.

## Disclaimer

Spoti-Tube is intended for personal use and educational purposes only. Ensure compliance with the terms of service of the platforms involved and adhere to local copyright laws.

Please be aware that downloading copyrighted material without permission may violate the terms of service of certain platforms and local copyright laws. Use this script responsibly and only for legal purposes.


---

Feel free to contribute to the project or report any issues on the [GitHub repository](https://github.com/ky13-troj/spoti-tube).
