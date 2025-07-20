# Torrent Module Setup Guide

## Overview

The torrent module allows you to interact with qBittorrent to manage torrent downloads through your AI assistant.

## Features

- Add magnet links to qBittorrent
- List active torrents and their status
- Search functionality (placeholder for legal implementation)

## Prerequisites

### 1. Install qBittorrent

Download and install qBittorrent from: https://www.qbittorrent.org/

### 2. Enable Web UI in qBittorrent

1. Open qBittorrent
2. Go to **Tools** > **Options** (or **Preferences** on Mac)
3. Click on **Web UI** in the left sidebar
4. Check **Enable the Web User Interface (Remote control)**
5. Set the port (default is 8080)
6. Set username and password (default username is 'admin')
7. Click **OK** to save

### 3. Install Python Dependencies

The required packages should already be installed, but if needed:

```bash
pip install qbittorrent-api beautifulsoup4 requests lxml
```

## Configuration

### Create Configuration File

1. Copy `torrent_config_example.py` to `torrent_config.py`
2. Edit the settings in `torrent_config.py`:

```python
# qBittorrent Web UI settings
QBITTORRENT_HOST = 'localhost'
QBITTORRENT_PORT = 8080
QBITTORRENT_USERNAME = 'admin'
QBITTORRENT_PASSWORD = 'your_actual_password'  # Set your qBittorrent password

# Search settings (for future implementation)
MAX_SEARCH_RESULTS = 10
REQUEST_TIMEOUT = 15

# Safety settings
ENABLE_SEARCH = False  # Set to True when you implement search functionality
```

## Usage

### Add Magnet Link

```
torrent add magnet:?xt=urn:btih:...
```

### List Active Torrents

```
torrent list
```

### Search (when implemented)

```
torrent search "your search query"
```

## Important Legal Notice

⚠️ **LEGAL DISCLAIMER** ⚠️

This module is provided for educational purposes and to interact with legally obtained torrent files. Users are responsible for:

1. Ensuring all downloads comply with local copyright laws
2. Only downloading content they have legal rights to access
3. Respecting the terms of service of any torrent sites
4. Following all applicable laws and regulations

The search functionality is intentionally disabled by default and requires manual implementation to ensure legal compliance.

## Troubleshooting

### "Failed to login to qBittorrent"

1. Make sure qBittorrent is running
2. Verify Web UI is enabled in qBittorrent settings
3. Check that the credentials in `torrent_config.py` match your qBittorrent settings
4. Ensure the port number is correct

### "Cannot connect to qBittorrent"

1. Check if qBittorrent is running
2. Verify the host and port settings
3. Make sure no firewall is blocking the connection
4. Try accessing the Web UI directly at `http://localhost:8080` (or your configured port)

### "Search is disabled"

This is intentional for safety. To enable search:

1. Create your own legal torrent search implementation
2. Set `ENABLE_SEARCH = True` in `torrent_config.py`
3. Ensure your implementation only searches legal content

## Security Notes

- Keep your qBittorrent credentials secure
- Only allow connections from localhost unless specifically needed
- Be cautious when downloading files from unknown sources
- Regularly update qBittorrent for security patches

## Extending the Module

To add search functionality:

1. Research legal torrent APIs or RSS feeds
2. Implement search in the `search_torrents()` function
3. Ensure compliance with all terms of service
4. Test thoroughly before enabling
