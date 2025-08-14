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
import webbrowser

# --- Environment Setup ---
load_dotenv()
client_id = os.getenv('SPOTIFY_CLIENT_ID')
client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
spotify_premium = int(os.getenv('SPOTIFY_PREMIUM', 0))  # Default to 0 (free)

# For premium users, we need full scope access
# For free users, we only need search functionality (no scope required)
scope = 'user-read-playback-state,user-modify-playback-state' if spotify_premium else None

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(client_id=client_id,
                              client_secret=client_secret,
                              redirect_uri='http://localhost:8888/callback',
                              scope=scope))

def execute(args):
    if args is None or len(args) == 0:
        return ("No command provided.")
    
    command = args.get("action", None).lower()  # Convert command to lowercase for case-insensitive matching

    if "play" in command:
        # check if second argument
        song_name = args.get("song_name", None)

        if song_name:
            # Clean and improve the search query
            search_query = song_name.strip()
            
            # If the query contains "by", treat it as "track artist" format
            if " by " in search_query.lower():
                parts = search_query.lower().split(" by ")
                if len(parts) == 2:
                    track_part = parts[0].strip()
                    artist_part = parts[1].strip()
                    search_query = f'track:"{track_part}" artist:"{artist_part}"'
            
            # Improve search by getting more results and filtering for best match
            results = sp.search(q=search_query, limit=10, type='track')
            if not results['tracks']['items']:
                # Fallback to simple search if structured search fails
                results = sp.search(q=song_name, limit=10, type='track')
                if not results['tracks']['items']:
                    return f"No results found for '{song_name}'."
            
            # Find the best match by looking for exact or close matches
            tracks = results['tracks']['items']
            best_track = None
            
            # First, try to find an exact match (case insensitive)
            search_lower = song_name.lower()
            for track in tracks:
                track_full = f"{track['name']} {track['artists'][0]['name']}".lower()
                if search_lower in track_full or track_full in search_lower:
                    # Prefer tracks that are not karaoke, instrumental, or cover versions
                    track_name_lower = track['name'].lower()
                    if not any(word in track_name_lower for word in ['karaoke', 'instrumental', 'cover', 'originally performed', 'tribute', 'remix']):
                        best_track = track
                        break
            
            # If no good match found, fall back to first result
            if not best_track:
                best_track = tracks[0]
            
            song_uri = best_track['uri']
            track_id = best_track['id']
            track_name = best_track['name']
            artist_name = best_track['artists'][0]['name']
            
            if spotify_premium:
                # Premium users: use API to control playback
                sp.start_playback(uris=[song_uri])
                return f"Playing {track_name} by {artist_name}."
            else:
                # Free users: open Spotify URL in browser
                spotify_url = f"spotify:track:{track_id}"
                webbrowser.open(spotify_url)
                return f"Opening {track_name} by {artist_name} in Spotify (free version - opens in browser/app)."
        else:
            if spotify_premium:
                sp.start_playback()
                return "Resuming music."
            else:
                return "Cannot resume playback with free Spotify. Please specify a song to play."
        
    elif "pause" in command:
        if spotify_premium:
            sp.pause_playback()
            return "Music paused."
        else:
            return "Cannot pause playback with free Spotify. Please use the Spotify app directly."
            
    elif "next" in command:
        if spotify_premium:
            sp.next_track()
            return "Skipped to next track."
        else:
            return "Cannot skip tracks with free Spotify. Please use the Spotify app directly."
            
    elif "previous" in command:
        if spotify_premium:
            sp.previous_track()
            return "Previous track."
        else:
            return "Cannot go to previous track with free Spotify. Please use the Spotify app directly."
            
    elif "volume" in command:
        if spotify_premium:
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
            return "Cannot control volume with free Spotify. Please use the Spotify app directly."
    else:
        return ("Spotify command not recognized.")

    