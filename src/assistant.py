"""
Personal AI Assistant - Main Entry Point

This module serves as the main entry point for the Personal AI Assistant.
It coordinates between different modules to provide a clean, organized codebase.

The assistant can:
- Control media playback and system functions
- Manage files and directories  
- Execute command line operations
- Remember information across sessions
- Process images from clipboard
- Integrate with Spotify (if premium)
"""
import os
from colorama import Fore, Style

# Import our refactored modules
from gemini.client import GeminiClient, load_system_prompt
from core.history_manager import load_history, clear_history
from core.image_handler import ImageHandler
from core.message_processor import process_user_input

def main():
    """Main loop for the assistant."""
    # Initialize components
    gemini_client = GeminiClient()
    image_handler = ImageHandler()
    
    # Load system configuration
    system_prompt = load_system_prompt()
    config = gemini_client.get_content_config(system_prompt)
    
    # Load conversation history
    history = load_history()

    while True:
        user_input = input(Fore.YELLOW + 'Command: ' + Style.RESET_ALL)
        if user_input.lower() == 'exit':
            print(Fore.RED + "Goodbye!" + Style.RESET_ALL)
            break
        elif user_input.lower() == 'clear':
            os.system('cls' if os.name == 'nt' else 'clear')
            print(Fore.YELLOW + "Cleared the screen." + Style.RESET_ALL)
            continue
        elif user_input.lower() == 'clear history':
            history = clear_history()
            continue
        elif user_input.strip() == '':
            print(Fore.RED + "Please enter a command." + Style.RESET_ALL)
            continue
        
        # Process user input using the message processor
        history = process_user_input(user_input, history, gemini_client, config, image_handler)


def get_landing_text():
    """Returns the colorful landing text for the application."""
    return Fore.MAGENTA + Style.BRIGHT + r"""

                                                                                          
                                                                                          
""" + Fore.LIGHTRED_EX + r"""    ██████╗ ███████╗██████╗ ███████╗ ██████╗ ███╗   ██╗ █████╗ ██╗          █████╗ ██╗    
    ██╔══██╗██╔════╝██╔══██╗██╔════╝██╔═══██╗████╗  ██║██╔══██╗██║         ██╔══██╗██║    
    ██████╔╝█████╗  ██████╔╝███████╗██║   ██║██╔██╗ ██║███████║██║         ███████║██║    
    ██╔═══╝ ██╔══╝  ██╔══██╗╚════██║██║   ██║██║╚██╗██║██╔══██║██║         ██╔══██║██║    
    ██║     ███████╗██║  ██║███████║╚██████╔╝██║ ╚████║██║  ██║███████╗    ██║  ██║██║    
    ╚═╝     ╚══════╝╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝    ╚═╝  ╚═╝╚═╝    
""" + Fore.MAGENTA + r"""                                                                                          
                                                                                          
                                                                                          
"""


if __name__ == "__main__":
    try:
        print(get_landing_text())
        main()
    except KeyboardInterrupt:
        print(Fore.RED + "\nProgram interrupted." + Style.RESET_ALL)
        exit(0)

