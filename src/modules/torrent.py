# Torrent module for managing torrents via qBittorrent
# Command: torrent search [query]
# Command: torrent add [magnet_link]
# Command: torrent list

import qbittorrentapi
import os

# Configuration - create torrent_config.py to override these settings
try:
    from . import torrent_config as config
except ImportError:
    # Default configuration
    class Config:
        QBITTORRENT_HOST = 'localhost'
        QBITTORRENT_PORT = 8080
        QBITTORRENT_USERNAME = 'admin'
        QBITTORRENT_PASSWORD = 'adminpass'  # CHANGE THIS!
        MAX_SEARCH_RESULTS = 5
        REQUEST_TIMEOUT = 10
        ENABLE_SEARCH = False  # Disabled by default for safety
    
    config = Config()


def execute(args):
    """
    Execute torrent-related commands.
    
    Args:
        args (dict): Arguments containing action and other parameters
    
    Returns:
        str: Result message
    """
    if args is None or len(args) == 0:
        return "No command provided."
    
    action = args.get("action", "").lower()
    
    if action == "search":
        query = args.get("query", "")
        if not query:
            return "No search query provided."
        return search_torrents(query)
    
    elif action == "add":
        magnet_link = args.get("magnet_link", "")
        if not magnet_link:
            return "No magnet link provided."
        return add_magnet_to_qbittorrent(magnet_link)
    
    elif action == "list":
        return list_active_torrents()
    
    else:
        return "Torrent command not recognized. Available actions: search, add, list"


# Torrent module for managing torrents via qBittorrent
# Command: torrent search [query]
# Command: torrent add [magnet_link]
# Command: torrent list

import qbittorrentapi
import requests
import urllib.parse
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import re
import time
import os

# Configuration - create torrent_config.py to override these settings
try:
    from . import torrent_config as config
except ImportError:
    # Default configuration
    class Config:
        QBITTORRENT_HOST = 'localhost'
        QBITTORRENT_PORT = 8080
        QBITTORRENT_USERNAME = 'admin'
        QBITTORRENT_PASSWORD = 'adminpass'  # CHANGE THIS!
        MAX_SEARCH_RESULTS = 5
        REQUEST_TIMEOUT = 10
        ENABLE_SEARCH = False  # Disabled by default for safety
        
        # Legal content keywords for filtering
        LEGAL_KEYWORDS = [
            'linux', 'ubuntu', 'debian', 'fedora', 'centos', 'opensuse',
            'creative commons', 'public domain', 'open source', 'foss',
            'free software', 'educational', 'documentary', 'lecture'
        ]
        
        # Blocked keywords for copyright protection
        BLOCKED_KEYWORDS = [
            'movie', 'film', 'dvd', 'bluray', 'tv show', 'series', 'episode',
            'music album', 'song', 'mp3', 'game', 'software', 'windows',
            'office', 'adobe', 'crack', 'keygen', 'patch'
        ]
    
    config = Config()


def execute(args):
    """
    Execute torrent-related commands.
    
    Args:
        args (dict): Arguments containing action and other parameters
    
    Returns:
        str: Result message
    """
    if args is None or len(args) == 0:
        return "No command provided."
    
    action = args.get("action", "").lower()
    
    if action == "search":
        query = args.get("query", "")
        if not query:
            return "No search query provided."
        return search_torrents(query)
    
    elif action == "add":
        magnet_link = args.get("magnet_link", "")
        if not magnet_link:
            return "No magnet link provided."
        return add_magnet_to_qbittorrent(magnet_link)
    
    elif action == "list":
        return list_active_torrents()
    
    else:
        return "Torrent command not recognized. Available actions: search, add, list"


def is_legal_content(query, title=""):
    """
    Check if the search query or title appears to be for legal content.
    
    Args:
        query (str): Search query
        title (str): Torrent title (optional)
    
    Returns:
        bool: True if appears to be legal content
    """
    combined_text = f"{query} {title}".lower()
    
    # Check for blocked keywords first
    for keyword in config.BLOCKED_KEYWORDS:
        if keyword in combined_text:
            return False
    
    # Check for legal keywords
    for keyword in config.LEGAL_KEYWORDS:
        if keyword in combined_text:
            return True
    
    # If no legal keywords found, consider it potentially copyrighted
    return False


# Torrent module for managing torrents via qBittorrent
# Command: torrent search [query]
# Command: torrent add [magnet_link]
# Command: torrent list

import qbittorrentapi
import requests
import urllib.parse
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import re
import time
import os

# Configuration - create torrent_config.py to override these settings
try:
    from . import torrent_config as config
except ImportError:
    # Default configuration
    class Config:
        QBITTORRENT_HOST = 'localhost'
        QBITTORRENT_PORT = 8080
        QBITTORRENT_USERNAME = 'admin'
        QBITTORRENT_PASSWORD = 'adminpass'  # CHANGE THIS!
        MAX_SEARCH_RESULTS = 5
        REQUEST_TIMEOUT = 10
        ENABLE_SEARCH = False  # Disabled by default for safety
    
    config = Config()


def execute(args):
    """
    Execute torrent-related commands.
    
    Args:
        args (dict): Arguments containing action and other parameters
    
    Returns:
        str: Result message
    """
    if args is None or len(args) == 0:
        return "No command provided."
    
    action = args.get("action", "").lower()
    
    if action == "search":
        query = args.get("query", "")
        if not query:
            return "No search query provided."
        return search_torrents(query)
    
    elif action == "add":
        magnet_link = args.get("magnet_link", "")
        if not magnet_link:
            return "No magnet link provided."
        return add_magnet_to_qbittorrent(magnet_link)
    
    elif action == "list":
        return list_active_torrents()
    
    else:
        return "Torrent command not recognized. Available actions: search, add, list"


def search_torrents(query):
    """
    Search for torrents on The Pirate Bay and 1337x.
    
    Args:
        query (str): Search query
    
    Returns:
        str: Search results or message
    """
    if not config.ENABLE_SEARCH:
        return ("Torrent search is currently disabled.\n"
                "To enable, edit torrent_config.py and set ENABLE_SEARCH = True.")
    
    try:
        results = []
        
        # Search The Pirate Bay
        try:
            tpb_results = search_tpb(query)
            results.extend(tpb_results)
        except Exception as e:
            pass
        
        # Try alternative search if no results
        if not results:
            try:
                alt_results = search_alternative(query)
                results.extend(alt_results)
            except Exception as e:
                pass
        
        if not results:
            return f"No torrents found for '{query}'. This might be due to:\n- Sites being blocked/down\n- Network issues\n- Anti-bot protection"
        
        # Sort by seeders (descending)
        results.sort(key=lambda x: int(x['seeders']) if x['seeders'].replace(',', '').isdigit() else 0, reverse=True)
        
        # Limit results
        results = results[:config.MAX_SEARCH_RESULTS]
        
        response = f"Found {len(results)} torrents for '{query}':\n\n"
        for i, torrent in enumerate(results, 1):
            response += f"{i}. {torrent['name']}\n"
            response += f"   Size: {torrent['size']}\n"
            response += f"   Seeders: {torrent['seeders']}\n"
            response += f"   Source: {torrent['source']}\n"
            response += f"   Magnet: {torrent['magnet'][:80]}...\n\n"
        
        return response
        
    except Exception as e:
        return f"Error searching for torrents: {str(e)}"


def search_tpb(query):
    """
    Search The Pirate Bay for torrents.
    
    Args:
        query (str): Search query
    
    Returns:
        list: List of torrent dictionaries
    """
    results = []
    ua = UserAgent()
    headers = {
        'User-Agent': ua.random,
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive'
    }
    
    try:
        # The Pirate Bay search URLs (TPB now requires JavaScript for search results)
        tpb_mirrors = [
            'https://thepiratebay.org',
            'https://tpb.party',
            'https://piratebay.live',
            'https://thehiddenbay.com',
            'https://piratebay.ink'
        ]
        
        encoded_query = urllib.parse.quote(query)
        
        for mirror in tpb_mirrors:
            try:
                # Try both old and new URL formats
                search_urls = [
                    f"{mirror}/search/{encoded_query}/1/99/0",  # New format
                    f"{mirror}/search.php?q={encoded_query}&all=on&search=Pirate+Search&page=0&orderby=",  # Old format
                    f"{mirror}/s/?q={encoded_query}",  # Alternative format
                ]
                
                for search_url in search_urls:
                    response = requests.get(search_url, headers=headers, timeout=config.REQUEST_TIMEOUT)
                    
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, 'html.parser')
                        
                        # Check for JavaScript requirement
                        page_text = soup.get_text().lower()
                        if 'enable js' in page_text or 'javascript' in page_text:
                            continue  # Try next URL/mirror
                            
                        # Try different parsing methods
                        result_count = 0
                        
                        # Method 1: Look for traditional table structure
                        for i, row in enumerate(soup.find_all('tr')[1:6]):
                            try:
                                cells = row.find_all('td')
                                if len(cells) >= 4:
                                    # Get torrent name
                                    name_cell = cells[1]
                                    name_links = name_cell.find_all('a')
                                    
                                    if len(name_links) >= 1:
                                        name = name_links[0].get_text(strip=True)
                                        
                                        # Get magnet link
                                        magnet_links = name_cell.find_all('a', href=lambda x: x and x.startswith('magnet:'))
                                        if not magnet_links:
                                            # Check other cells for magnet link
                                            for cell in cells:
                                                magnet_links = cell.find_all('a', href=lambda x: x and x.startswith('magnet:'))
                                                if magnet_links:
                                                    break
                                        
                                        if magnet_links:
                                            magnet = magnet_links[0]['href']
                                            
                                            # Get size from cell 4 (based on debug output)
                                            size = "Unknown"
                                            if len(cells) > 4:
                                                size = cells[4].get_text(strip=True)
                                            
                                            # Get seeders from cell 5 (based on debug output)
                                            seeders = "Unknown"
                                            if len(cells) > 5:
                                                seeders_text = cells[5].get_text(strip=True)
                                                if seeders_text.replace(',', '').isdigit():
                                                    seeders = seeders_text
                                            
                                            results.append({
                                                'name': name,
                                                'size': size,
                                                'seeders': seeders,
                                                'magnet': magnet,
                                                'source': 'TPB'
                                            })
                                            result_count += 1
                            except Exception as e:
                                continue
                        
                        # Method 2: Look for div-based structure
                        if result_count == 0:
                            divs = soup.find_all('div', class_=['list-item', 'torrent-item', 'result'])
                            
                        # Method 3: Look for any links that contain magnet
                        if result_count == 0:
                            magnet_links = soup.find_all('a', href=lambda x: x and 'magnet:' in x)
                            
                            # Debug: let's see the page structure
                            if magnet_links:
                                first_link = magnet_links[0]
                                row = first_link.find_parent('tr')
                                if row:
                                    cells = row.find_all('td')
                                    for idx, cell in enumerate(cells):
                                        pass
                                else:
                                    pass
                            
                            for i, link in enumerate(magnet_links[:5]):
                                try:
                                    magnet = link['href']
                                    
                                    # Try to find the torrent info in the row structure
                                    row = link.find_parent('tr')
                                    if row:
                                        cells = row.find_all('td')
                                        if len(cells) >= 4:
                                            # Get name from first cell or link
                                            name_cell = cells[1] if len(cells) > 1 else cells[0]
                                            name_links = name_cell.find_all('a')
                                            name = name_links[0].get_text(strip=True) if name_links else f"Torrent {i+1}"
                                            
                                            # Get seeders (usually in column 2 or 3)
                                            seeders = "Unknown"
                                            if len(cells) >= 3:
                                                seeders_text = cells[2].get_text(strip=True)
                                                if seeders_text.isdigit():
                                                    seeders = seeders_text
                                            
                                            # Get size from description in name cell
                                            size = "Unknown"
                                            size_font = name_cell.find('font', class_='detDesc')
                                            if size_font:
                                                size_text = size_font.get_text()
                                                size_match = re.search(r'Size ([^,]+)', size_text)
                                                if size_match:
                                                    size = size_match.group(1)
                                        else:
                                            # Fallback: try to find name nearby
                                            parent = link.parent
                                            name_elem = parent.find_previous('a') or parent.find_next('a') or parent
                                            name = name_elem.get_text(strip=True) if name_elem else f"Torrent {i+1}"
                                            seeders = "Unknown"
                                            size = "Unknown"
                                    else:
                                        # Not in a table row, try other methods
                                        parent = link.parent
                                        name_elem = parent.find_previous('a') or parent.find_next('a') or parent
                                        name = name_elem.get_text(strip=True) if name_elem else f"Torrent {i+1}"
                                        seeders = "Unknown"
                                        size = "Unknown"
                                    
                                    results.append({
                                        'name': name[:100],  # Limit name length
                                        'size': size,
                                        'seeders': seeders,
                                        'magnet': magnet,
                                        'source': 'TPB'
                                    })
                                    result_count += 1
                                except Exception as e:
                                    continue
                        
                        if result_count > 0:
                            return results  # Success, return immediately
                    
            except Exception as e:
                continue  # Try next mirror
        
        return results
        
    except Exception as e:
        return []



def search_alternative(query):
    """
    Alternative search method using different approach or sites.
    """
    results = []
    try:
        # You could add other torrent sites or APIs here
        # For now, this is a placeholder that creates sample results for testing
        
        # Example: You could add searches for other sites like:
        # - RARBG alternatives
        # - YTS for movies
        # - EZTV for TV shows
        # - Torrentz2 meta-search
        
        # Placeholder result for testing
        if query:
            results.append({
                'name': f"Sample result for '{query}' (Alternative search)",
                'size': "Unknown",
                'seeders': "0",
                'magnet': f"magnet:?xt=urn:btih:sample&dn={urllib.parse.quote(query)}",
                'source': 'Alternative'
            })
        
        return results
        
    except Exception as e:
        return []


def add_magnet_to_qbittorrent(magnet_link):
    """
    Add magnet link to qBittorrent.
    
    Args:
        magnet_link (str): Magnet link to add
    
    Returns:
        str: Result message
    """
    try:
        # Validate magnet link
        if not magnet_link.startswith('magnet:'):
            return "Invalid magnet link. Must start with 'magnet:'"
        
        # Connect to qBittorrent
        qbt_client = qbittorrentapi.Client(
            host=config.QBITTORRENT_HOST,
            port=config.QBITTORRENT_PORT,
            username=config.QBITTORRENT_USERNAME,
            password=config.QBITTORRENT_PASSWORD
        )
        
        # Try to log in
        try:
            qbt_client.auth_log_in()
        except qbittorrentapi.LoginFailed:
            return ("Failed to login to qBittorrent. Please check:\n"
                   "1. qBittorrent is running\n"
                   "2. Web UI is enabled (Tools > Options > Web UI)\n"
                   "3. Credentials are correct in torrent_config.py")
        except Exception as e:
            return f"Cannot connect to qBittorrent: {str(e)}"
        
        # Add the magnet link
        qbt_client.torrents_add(urls=magnet_link)
        
        return "Successfully added magnet link to qBittorrent"
        
    except Exception as e:
        return f"Error adding magnet to qBittorrent: {str(e)}"


def list_active_torrents():
    """
    List active torrents in qBittorrent.
    
    Returns:
        str: List of active torrents
    """
    try:
        # Connect to qBittorrent
        qbt_client = qbittorrentapi.Client(
            host=config.QBITTORRENT_HOST,
            port=config.QBITTORRENT_PORT,
            username=config.QBITTORRENT_USERNAME,
            password=config.QBITTORRENT_PASSWORD
        )
        
        # Try to log in
        try:
            qbt_client.auth_log_in()
        except qbittorrentapi.LoginFailed:
            return ("Failed to login to qBittorrent. Please check:\n"
                   "1. qBittorrent is running\n"
                   "2. Web UI is enabled (Tools > Options > Web UI)\n"
                   "3. Credentials are correct in torrent_config.py")
        except Exception as e:
            return f"Cannot connect to qBittorrent: {str(e)}"
        
        # Get torrent list
        torrents = qbt_client.torrents_info()
        
        if not torrents:
            return "No active torrents found in qBittorrent."
        
        response = f"Active torrents ({len(torrents)}):\n\n"
        for torrent in torrents:
            progress = torrent.progress * 100
            response += f"• {torrent.name}\n"
            response += f"  Status: {torrent.state}\n"
            response += f"  Progress: {progress:.1f}%\n"
            response += f"  Size: {format_bytes(torrent.size)}\n"
            response += f"  Speed: ↓{format_bytes(torrent.dlspeed)}/s ↑{format_bytes(torrent.upspeed)}/s\n\n"
        
        return response
        
    except Exception as e:
        return f"Error listing torrents: {str(e)}"


def format_bytes(bytes_value):
    """
    Format bytes into human-readable format.
    
    Args:
        bytes_value (int): Number of bytes
    
    Returns:
        str: Formatted string
    """
    if bytes_value == 0:
        return "0 B"
    
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_value < 1024.0:
            return f"{bytes_value:.1f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.1f} PB"
