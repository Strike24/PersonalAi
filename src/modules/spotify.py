# This module is used to control Spotify playback using the Spotipy library.
#Command: spotify play
#Command: spotify play [song name]
#Command: spotify pause
#Command: spotify next
#Command: spotify previous
#Command: spotify volume [volume level]


import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

# --- Environment Setup ---
load_dotenv()
client_id = os.getenv('SPOTIFY_CLIENT_ID')
client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(client_id=client_id,
                              client_secret=client_secret,
                              redirect_uri='http://localhost:8888/callback',
                              scope='user-read-playback-state,user-modify-playback-state'))

def execute(args):
    if args is None or len(args) == 0:
        return ("No command provided.")
    
    command = args.get("action", None).lower()  # Convert command to lowercase for case-insensitive matching

    if "play" in command:
        # check if second argument
        song_name = args.get("song_name", None)

        if song_name:
            results = sp.search(q=song_name, limit=1)
            song_uri = results['tracks']['items'][0]['uri']
            # play the song
            sp.start_playback(uris=[song_uri])
            return f"Playing {song_name}."
        else:
            sp.start_playback()
            return "Resuming music."
        
    elif "pause" in command:
        sp.pause_playback()
        return "music paused."
    elif "next" in command:
        sp.next_track()
        return "Skipped to next track."
    elif "previous" in command:
        sp.previous_track()
        print("Previous track.")
    elif "volume" in command:
        # Extract the volume level from the command
        level = args.get("level", None)
        if (level is None) or (not level.isdigit()):
            return "No volume level provided."  
        else:
            level = int(level)
        # Set volume (0 is max, 100 is min)
        if level > 100:
            level = 100
        elif level < 0:
            level = 0
        sp.volume(level)
        return (f"Volume set to {level}.")
    else:
        return ("Spotify command not recognized.")

    