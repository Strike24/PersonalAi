# This module is used to control Spotify playback using the Spotipy library.
#Command: spotify play
#Command: spotify play [song name]
#Command: spotify pause
#Command: spotify next
#Command: spotify previous
#Command: spotify volume [volume level]


import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(client_id='0a9b212550a34cadabbd8350d4e403d7',
                              client_secret='4b88b3a871ab4b6a9412f3a7a4b1a4ee',
                              redirect_uri='http://localhost:8888/callback',
                              scope='user-read-playback-state,user-modify-playback-state'))

def control_spotify(command):
    if "play" in command:
        # check if second argument
        words = command.split()
        if len(words) > 1:
            index = words.index("play")
            song_name = " ".join(words[index + 1:])
            # search for the song
            results = sp.search(q=song_name, limit=1)
            song_uri = results['tracks']['items'][0]['uri']
            # play the song
            sp.start_playback(uris=[song_uri])
            print(f"Playing {song_name}.")
        else:
            sp.start_playback()
            print("Playing music.")
    elif "pause" in command:
        sp.pause_playback()
        print("Music paused.")
    elif "next" in command:
        sp.next_track()
        print("Next track.")
    elif "previous" in command:
        sp.previous_track()
        print("Previous track.")
    elif "volume" in command:
        # Extract the volume level from the command
        words = command.split()
        index = words.index("volume")
        level = int(words[index + 1])
        # Set volume (0 is max, 100 is min)
        if level > 100:
            level = 100
        elif level < 0:
            level = 0
        sp.volume(level)
        print(f"Volume set to {level}.")
    else:
        print("Spotify command not recognized.")

    