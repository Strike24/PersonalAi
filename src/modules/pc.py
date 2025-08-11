#Command: pc open [application_name]
#Command: pc open_website [website_url]
#Command: pc sleep
#Command: pc restart
#Command: pc shutdown
#Command: pc lock
#Command: pc screenshot [path]

import os
import subprocess
import webbrowser
import shutil
from pathlib import Path


def find_application(app_name):
    """Find application executable by name or path."""
    # If it's already a full path and exists, return it
    if os.path.isfile(app_name):
        return app_name
    
    # Check if it's a simple executable name
    if shutil.which(app_name):
        return shutil.which(app_name)
    
    # Common application locations on Windows
    common_paths = [
        f"C:\\Program Files\\{app_name}",
        f"C:\\Program Files (x86)\\{app_name}", 
        f"C:\\Users\\{os.getenv('USERNAME')}\\AppData\\Local\\Programs\\{app_name}",
        f"C:\\Users\\{os.getenv('USERNAME')}\\AppData\\Roaming\\{app_name}",
    ]
    
    # Common executable extensions
    extensions = ['.exe', '.bat', '.cmd', '.com']
    
    # Search in common paths
    for base_path in common_paths:
        if os.path.isdir(base_path):
            # Look for executable files in the directory
            for root, dirs, files in os.walk(base_path):
                for file in files:
                    name, ext = os.path.splitext(file)
                    if ext.lower() in extensions and app_name.lower() in name.lower():
                        return os.path.join(root, file)
    
    # Try adding .exe extension if not present
    if not any(app_name.lower().endswith(ext) for ext in extensions):
        return find_application(app_name + '.exe')
    
    return None


def take_screenshot(save_path=None):
    """Take a screenshot and save it to the specified path."""
    try:
        import PIL.ImageGrab as ImageGrab
        
        # Take screenshot
        screenshot = ImageGrab.grab()
        
        # Generate default path if none provided
        if save_path is None:
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            save_path = f"screenshot_{timestamp}.png"
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        # Save screenshot
        screenshot.save(save_path)
        return f"Screenshot saved to: {save_path}"
        
    except ImportError:
        return "Error: PIL (Pillow) library not installed. Please install it with: pip install Pillow"
    except Exception as e:
        return f"Error taking screenshot: {str(e)}"


def safe_system_command(command, description):
    """Safely execute system commands using subprocess."""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            return f"{description} command executed successfully."
        else:
            return f"Error executing {description.lower()}: {result.stderr}"
    except subprocess.TimeoutExpired:
        return f"{description} command timed out."
    except Exception as e:
        return f"Error executing {description.lower()}: {str(e)}"

def execute(args):
    if args is None or len(args) == 0:
        return "No command provided."
    
    action = args.get("action", "").lower()

    if "open_website" in action:
        website_url = args.get("website_url", None)
        if website_url is None:
            return "No website URL provided."
        
        try:
            # Ensure URL has protocol
            if not website_url.startswith(('http://', 'https://', 'ftp://')):
                website_url = 'https://' + website_url
            
            webbrowser.open(website_url)
            return f"Opening website: {website_url}"
        except Exception as e:
            return f"Error opening website: {str(e)}"

    elif "open" in action:
        app_name = args.get("application_name", None)
        if app_name is None:
            return "No application name provided."
        
        # Find the application
        app_path = find_application(app_name)
        if app_path is None:
            return f"Could not find application: {app_name}. Please provide the full path or ensure the application is installed."
        
        try:
            # Use subprocess instead of os.system for better control
            subprocess.Popen([app_path], shell=True)
            return f"Opening {app_name} from: {app_path}"
        except Exception as e:
            return f"Error opening {app_name}: {str(e)}"

    elif "screenshot" in action:
        save_path = args.get("path", None)
        return take_screenshot(save_path)

    elif "sleep" in action:
        return safe_system_command("shutdown /h", "Sleep")

    elif "restart" in action:
        return safe_system_command("shutdown /r /t 0", "Restart")

    elif "shutdown" in action:
        return safe_system_command("shutdown /s /t 0", "Shutdown")

    elif "lock" in action:
        return safe_system_command("rundll32.exe user32.dll,LockWorkStation", "Lock screen")

    else:
        available_commands = ["open", "open_website", "sleep", "restart", "shutdown", "lock", "screenshot"]
        return f"PC command not recognized. Available commands: {', '.join(available_commands)}"
