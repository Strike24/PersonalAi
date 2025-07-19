"""
Function declarations for Gemini API function calling.

This module contains all the function schemas that the AI can call to interact
with the system. Each function declaration defines:
- Function name and description
- Required and optional parameters
- Parameter types and validation rules

Functions include:
- Media control (play, pause, volume)
- PC operations (open files, sleep, restart)
- File management (create, read, write, delete)
- Memory operations (save/retrieve information)
- Command line execution
- Spotify integration (if premium)

Extracted from assistant.py to improve code organization and maintainability.
"""
import os


def get_media_functions():
    """Returns the function declaration for controlling media playback and volume."""
    return {
        "name": "media",
        "description": "Control media playback and volume on the computer.",
        "parameters": {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": ["play", "pause", "mute", "unmute", "set_volume"],
                    "description": "Media action: play, pause, mute, unmute, or set volume.",
                },
                "volume_level": {
                    "type": "number",
                    "description": "Volume level for 'set_volume' (0.0 = max, -65.25 = min).",
                }
            },
            "required": ["action"],
        },
    }


def get_pc_functions():
    """Returns the function declaration for controlling PC actions."""
    return {
        "name": "pc",
        "description": "Control the PC: open files, open websites, sleep, or restart.",
        "parameters": {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": ["open", "sleep", "restart", "open_website"],
                    "description": "PC action: open an application, open a website, sleep, or restart.",
                },
                "application_name": {
                    "type": "string",
                    "description": "Full path of the file to open (for 'open' action).",
                },
                "website_url": {
                    "type": "string",
                    "description": "URL of the website to open (for 'open_website' action).",
                }
            },
            "required": ["action"],
        },
    }


def get_files_functions():
    """Returns the function declaration for managing files and directories."""
    return {
        "name": "files",
        "description": "Manage files and directories: create, write, read, delete, copy, move, rename, list, search, or create a directory.",
        "parameters": {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": [
                        "create", "write", "read", "delete", "copy", "move",
                        "rename", "list", "search", "createDir"
                    ],
                    "description": "File/directory action.",
                },
                "path": {
                    "type": "string",
                    "description": "Path of the file/directory (include name). For 'search', only the directory path.",
                },
                "content": {
                    "type": "string",
                    "description": "Content to write (for 'write' action).",
                },
                "source_path": {
                    "type": "string",
                    "description": "Source path (for copy/move).",
                },
                "destination_path": {
                    "type": "string",
                    "description": "Destination path (for copy/move).",
                },
                "new_name": {
                    "type": "string",
                    "description": "New name (for 'rename').",
                },
                "file_name": {
                    "type": "string",
                    "description": "File name to search (for 'search').",
                }
            },
            "required": ["action", "path"]
        },
    }


def get_memory_functions():
    """Returns the function declaration for managing memory topics and information."""
    return {
        "name": "memory",
        "description": "Save information under a memory topic.",
        "parameters": {
            "type": "object",
            "properties": {
                "topic": {
                    "type": "string",
                    "description": "Topic to save or retrieve information.",
                },
                "info": {
                    "type": "string",
                    "description": "Information to save under the topic.",
                }
            },
            "required": ["topic", "info"]
        },
    }


def get_commandline_functions():
    """Returns the function declaration for executing command line commands."""
    return {
        "name": "commandline",
        "description": "Execute a command in the system command line and return the output.",
        "parameters": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "The command to execute in the system shell.",
                    },
                    "path": {
                        "type": "string",
                        "description": "The working directory for the command execution.",
                    }
                },
                "required": ["command", "path"]
            },
        }


def get_spotify_functions():
    """Returns the function declaration for controlling Spotify playback."""
    spotify_premium = os.getenv('SPOTIFY_PREMIUM', '0') == '1'
    
    if not spotify_premium:  # If not premium, return empty. api will not work
        return {}
    else:
        return {
            "name": "spotify",
            "description": "Control Spotify playback: play, pause, next, previous, or set volume.",
            "parameters": {
                "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": ["play", "pause", "next", "previous", "volume"],
                    "description": "Spotify action: play, pause, next track, previous track, or set volume.",
                },
                "song_name": {
                    "type": "string",
                    "description": "Name of the song to play (for 'play' action). if no name, just resuming playback",
                },
                "volume_level": {
                    "type": "number",
                    "description": "Volume level for 'volume'.",
                }
            },
            "required": ["action"],
        },
    }


def get_all_function_declarations():
    """Returns a list of all available function declarations."""
    return [
        get_media_functions(),
        get_pc_functions(),
        get_files_functions(),
        get_memory_functions(),
        get_commandline_functions()
    ]