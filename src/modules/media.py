#Command: media play music
#Command: media pause
#Command: media unmute
#Command: media mute
#Command: media set volume [volume level]

import os
from utils.windows_media import get_volume, set_volume, mute_volume, unmute_volume

def execute(args):
    if args is None or len(args) == 0:
        return("No command provided.")
        return
    
    command = args.get("action", None).lower()  # Convert command to lowercase for case-insensitive matching
    volume_level = args.get("volume_level", None)  # Get volume level if provided

    if "play" in command:
        os.system("play")
        return("Playing music.")
    elif "pause" in command:
        os.system("pause")
        return("Music paused.")
    elif "unmute" in command:
        unmute_volume()
        return("Volume unmuted.")
    elif "mute" in command:
        mute_volume()
        return("Volume muted.")
    elif "set_volume" in command:
        # Extract the volume level from the command
        if volume_level is None:
            return("No volume level specified.")
            return
        level = float(volume_level)
        #if level is not in the command, dont do anything
        if level is None:
            return
        # Set volume (0.0 is max, -65.25 is min)
        if level > 0:
            level = 0
        elif level < -65.25:
            level = -65.25
        set_volume(level)
        return(f"Volume set to {level}.")
    else:
        return("Media command not recognized.")
