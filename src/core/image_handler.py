"""
Image handling for clipboard paste functionality.
Manages image capture from clipboard and hotkey registration.
"""
import os
import keyboard
from PIL import ImageGrab, Image
from colorama import Fore, Style


class ImageHandler:
    """Handles image pasting from clipboard with hotkey support."""
    
    def __init__(self):
        """Initialize the image handler and register hotkey."""
        self.current_image_path = None
        # Register the hotkey (Ctrl+V)
        keyboard.add_hotkey('ctrl+v', lambda: self.on_image_paste())
    
    def on_image_paste(self):
        """Handles the Ctrl+V hotkey to paste an image from the clipboard.
        Returns the path of the saved image."""
        try:
            image = ImageGrab.grabclipboard()
            path = os.path.join(os.getcwd(), "pasted_image.png")
            if image is not None:
                print(Fore.GREEN + "[ ./pasted_image.png ]" + Style.RESET_ALL)
                image.save(path, "PNG")
                self.current_image_path = path
            else:
                self.current_image_path = None
        except Exception as e:
            print(Fore.RED + f"Error pasting image: {e}" + Style.RESET_ALL)
            self.current_image_path = None

    def get_current_image_path(self):
        """Returns the path of the currently pasted image, if any."""
        if self.current_image_path and os.path.exists(self.current_image_path):
            return self.current_image_path
        return None
    
    def cleanup_image(self, image_path):
        """Clean up the pasted image after processing."""
        if image_path and os.path.exists(image_path):
            try:
                os.remove(image_path)
            except Exception as e:
                print(Fore.RED + f"Error removing pasted image: {e}" + Style.RESET_ALL)