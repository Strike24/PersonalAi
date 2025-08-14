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
        "description": "Control the PC: open applications, open websites, sleep, restart, shutdown, lock screen, or take screenshots.",
        "parameters": {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": ["open", "open_website", "sleep", "restart", "shutdown", "lock", "screenshot"],
                    "description": "PC action: open an application, open a website, sleep, restart, shutdown, lock screen, or take a screenshot.",
                },
                "application_name": {
                    "type": "string",
                    "description": "Name or path of the application to open (for 'open' action). Can be a simple name like 'notepad' or full path.",
                },
                "website_url": {
                    "type": "string",
                    "description": "URL of the website to open (for 'open_website' action). Protocol (http/https) is optional.",
                },
                "path": {
                    "type": "string",
                    "description": "File path where to save the screenshot (for 'screenshot' action). If not provided, saves with timestamp in current directory.",
                }
            },
            "required": ["action"],
        },
    }


def get_files_functions():
    """Returns the function declaration for managing files and directories."""
    return {
        "name": "files",
        "description": "Manage files and directories: create, write, read, delete, copy, move, rename, list, search, create a directory, create PDF files, or create various document types.",
        "parameters": {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": [
                        "create", "write", "read", "delete", "copy", "move",
                        "rename", "list", "search", "createDir", "createPdf", "createDoc"
                    ],
                    "description": "File/directory action.",
                },
                "path": {
                    "type": "string",
                    "description": "Path of the file/directory (include name). For 'search', only the directory path.",
                },
                "content": {
                    "type": "string",
                    "description": "Content to write (for 'write', 'createPdf', 'createDoc' actions).",
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
                    "description": "File name to search (for 'search'). Good only for searching by specific file name.",
                },
                "title": {
                    "type": "string",
                    "description": "Title for the document (for 'createPdf' action). Defaults to 'Document'.",
                },
                "doc_type": {
                    "type": "string",
                    "enum": ["pdf", "html", "md", "markdown", "csv", "json", "txt"],
                    "description": "Type of document to create (for 'createDoc' action): pdf, html, md/markdown, csv, json, or txt.",
                },
                "date_filter": {
                    "type": "string",
                    "description": "Filter files by date (for 'list' action). Formats: 'YYYY-MM-DD' (exact date), '>= YYYY-MM-DD' or 'after: YYYY-MM-DD' (on or after), '<= YYYY-MM-DD' or 'before: YYYY-MM-DD' (on or before), 'today', 'yesterday', 'last 7 days', 'last week', 'last month'.",
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
    
    # Always return Spotify functions - the module handles premium vs free logic internally
    description = "Control Spotify playback: play, pause, next, previous, or set volume. IMPORTANT: Only call this function ONCE per user request. The function will find and open the best available match for the requested song."
    if not spotify_premium:
        description += " (Free users: song search and opening in Spotify app/browser. Other controls require premium.)"
    
    return {
        "name": "spotify",
        "description": description,
        "parameters": {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": ["play", "pause", "next", "previous", "volume"],
                    "description": "Spotify action: play, pause, next track, previous track, or set volume. For 'play' action, the system will automatically find the best match for the song.",
                },
                "song_name": {
                    "type": "string",
                    "description": "Name of the song to play (for 'play' action). Include artist name for better results (e.g., 'This Love by Maroon 5'). The system will find the best available match - do not retry if the exact version isn't found.",
                },
                "level": {
                    "type": "string",
                    "description": "Volume level for 'volume' action (0-100). Premium only.",
                }
            },
            "required": ["action"],
        },
    }


def get_torrent_functions():
    """Returns the function declaration for torrent operations."""
    return {
        "name": "torrent",
        "description": "Search for torrents and manage downloads via qBittorrent.",
        "parameters": {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": ["search", "add", "list"],
                    "description": "Torrent action: search for torrents, add magnet link to qBittorrent, or list active torrents.",
                },
                "query": {
                    "type": "string",
                    "description": "Search query for finding torrents (for 'search' action).",
                },
                "magnet_link": {
                    "type": "string",
                    "description": "Magnet link to add to qBittorrent (for 'add' action).",
                },
                "download_path": {
                    "type": "string",
                    "description": "Path where to save the downloaded torrent (for 'add' action). Use only if specified.",
                },
            },
            "required": ["action"],
        },
    }


def get_gmail_functions():
    """Returns the function declaration for Gmail operations."""
    return {
        "name": "gmail",
        "description": "Send emails through Gmail with or without attachments, retrieve recent emails, or fetch a specific email by ID.",
        "parameters": {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": ["send", "send_with_attachment", "get", "get_by_id"],
                    "description": "Gmail action: send regular email, send email with attachment, get recent emails, or get a specific email by ID.",
                },
                "to": {
                    "type": "string",
                    "description": "Recipient email address (required for send actions).",
                },
                "subject": {
                    "type": "string",
                    "description": "Email subject line (for send actions).",
                },
                "body": {
                    "type": "string",
                    "description": "Email body content (for send actions).",
                },
                "attachment_path": {
                    "type": "string",
                    "description": "Full path to the attachment file (for 'send_with_attachment' action).",
                },
                "count": {
                    "type": "integer",
                    "description": "Number of recent emails to retrieve (for 'get' action). Defaults to 10 if not specified.",
                    "minimum": 1,
                    "maximum": 100
                },
                "id": {
                    "type": "string",
                    "description": "Gmail message ID (for 'get_by_id' action).",
                }
            },
            "required": ["action"],
        },
    }


def get_bubble_functions():
    """Returns the function declaration for managing ephemeral working memory bubbles."""
    return {
        "name": "bubble",
        "description": "Manage ephemeral working memory bubbles - temporary information storage that can automatically expire.",
        "parameters": {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": ["create", "update", "get", "delete", "list", "context"],
                    "description": "Bubble action: create new bubble, update existing bubble, get bubble by key, delete bubble, list all bubbles, or get auto-include context.",
                },
                "key": {
                    "type": "string",
                    "description": "Bubble identifier/name (required for create, update, get, delete actions).",
                },
                "value": {
                    "type": "string",
                    "description": "Information to store in the bubble (required for create, optional for update).",
                },
                "lifespan": {
                    "type": "object",
                    "description": "Expiration settings as object. Examples: {\"minutes\": 30}, {\"hours\": 2}, {\"messages\": 10}, {\"minutes\": 15, \"messages\": 5}. Can also be a string like '30 minutes' or '2 hours'.",
                    "properties": {
                        "minutes": {"type": "integer", "minimum": 1},
                        "hours": {"type": "integer", "minimum": 1},
                        "seconds": {"type": "integer", "minimum": 1},
                        "messages": {"type": "integer", "minimum": 1}
                    }
                },
                "on_demand": {
                    "type": "boolean",
                    "description": "If false (default), bubble is automatically included in prompts. If true, bubble is only retrieved when explicitly requested.",
                },
                "include_expired": {
                    "type": "boolean",
                    "description": "For 'list' action: whether to include expired bubbles in the results (default: false).",
                }
            },
            "required": ["action"],
        },
    }


def get_all_function_declarations():
    """Returns a list of all available function declarations."""
    functions = [
        get_media_functions(),
        get_pc_functions(),
        get_files_functions(),
        get_memory_functions(),
        get_commandline_functions(),
        get_spotify_functions(),
        get_bubble_functions(),
        get_torrent_functions(),
        get_gmail_functions()
    ]
    
    # Filter out empty function declarations
    return [func for func in functions if func]