#Command: media play music
#Command: media pause
#Command: media unmute
#Command: media mute
#Command: media set volume [volume level]

import os
from utils.windows_media import get_volume, set_volume, mute_volume, unmute_volume

def control_media(command):
    if "play music" in command:
        os.system("start spotify")  # Adjust this for the media player you use
        print("Playing music.")
    elif "pause" in command:
        os.system("pause")
        print("Music paused.")
    elif "unmute" in command:
        unmute_volume()
        print("Volume unmuted.")
    elif "mute" in command:
        mute_volume()
        print("Volume muted.")
    elif "set volume" in command:
        # Extract the volume level from the command
        words = command.split()
        index = words.index("volume")
        level = float(words[index + 1])
        #if level is not in the command, dont do anything
        if level is None:
            return
        # Set volume (0.0 is max, -65.25 is min)
        if level > 0:
            level = 0
        elif level < -65.25:
            level = -65.25
        set_volume(level)
        print(f"Volume set to {level}.")
    else:
        print("Media command not recognized.")
