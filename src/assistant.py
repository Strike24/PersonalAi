import importlib
import os
import json
from utils.memory import save_to_memory, load_memory
from colorama import Fore, Style
from google import genai
from google.genai import types
from dotenv import load_dotenv

# --- Environment Setup ---
load_dotenv()
api_key = os.getenv('GEMINI_API_KEY')
client = genai.Client(api_key=api_key)

HISTORY_FILE = "history.json"
MAX_HISTORY = 100
MEMORY_FILE = "memory.json"
PROMPT_FILE = "prompt.txt"

# --- Conversation History Management ---

def load_history():
    """Load conversation history from a JSON file."""
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except Exception:
                return []
    return []

def save_history(history):
    """Save conversation history to a JSON file."""
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history[-MAX_HISTORY:], f, ensure_ascii=False, indent=2)

def add_to_history(history, role, content):
    """Add a message to the history and trim to the last MAX_HISTORY messages."""
    history.append({"role": role, "content": content})
    if len(history) > MAX_HISTORY:
        history = history[-MAX_HISTORY:]
    save_history(history)
    return history

def load_memory_content():
    """Load memory.json as a string for context injection."""
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            try:
                memory = json.load(f)
                return json.dumps(memory, ensure_ascii=False, indent=2)
            except Exception:
                return ""
    return ""

def load_system_prompt():
    """Load the system prompt from prompt.txt."""
    if os.path.exists(PROMPT_FILE):
        with open(PROMPT_FILE, "r", encoding="utf-8") as f:
            return f.read()
    
    print(Fore.RED + "System prompt file not found! Using default prompt.\nCreate a prompt.txt file for customized instructions." + Style.RESET_ALL)
    return "You are a helpful AI assistant."

# --- Function Declarations for AI API ---

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
        "description": "Control the PC: open files, sleep, or restart.",
        "parameters": {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "enum": ["open", "sleep", "restart"],
                    "description": "PC action: open an application, sleep, or restart.",
                },
                "application_name": {
                    "type": "string",
                    "description": "Full path of the file to open (for 'open' action).",
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

# --- AI Tool Configuration ---

def get_grounding_tool():
    """Returns the AI tool configuration with all function declarations."""
    return types.Tool(
        google_search=types.GoogleSearch(),
        function_declarations=[
            get_media_functions(),
            get_pc_functions(),
            get_files_functions(),
            get_memory_functions(),
            get_commandline_functions()
        ],
    )


def get_content_config():
    """Returns the content generation configuration for the AI model."""
    return types.GenerateContentConfig(
        tools=[get_grounding_tool()],
        system_instruction=load_system_prompt(),
        thinking_config=types.ThinkingConfig(thinking_budget=1024),
        tool_config=types.ToolConfig(
            function_calling_config=types.FunctionCallingConfig(
                mode='AUTO')
        ),
    )

# --- Helper Functions ---

def load_module(module_name):
    """Dynamically loads a module from the 'modules' package."""
    try:
        return importlib.import_module(f'modules.{module_name}')
    except ModuleNotFoundError:
        print(f"Module {module_name} not found!")
        return None

def handle_memory_function(function_args):
    """Handles memory function calls: save or retrieve information."""
    topic = function_args.get("topic")
    info = function_args.get("info")
    if topic and info:
        save_to_memory(topic, info)
        print(Fore.GREEN + f"Saved information under topic '{topic}'." + Style.RESET_ALL)
    else:
        print(Fore.RED + "Invalid memory function call." + Style.RESET_ALL)

def handle_function_call(function_name, function_args, history):
    """Handles dynamic function calls by loading and executing the appropriate module.
    Adds the function response to history so the AI remembers."""
    if function_name == "memory":
        handle_memory_function(function_args)
        return history

    module = load_module(function_name)
    if module and hasattr(module, 'execute'):
        res = module.execute(function_args)
        if res is None:
            print(Fore.RED + "No response from the function." + Style.RESET_ALL)
            return history
        print(Style.DIM + Fore.WHITE + str(res) + Style.RESET_ALL)
        # Add function response to history as assistant message
        history = add_to_history(history, "assistant", str(res))
        return history
    else:
        print(Fore.RED + f"No executable module found for '{function_name}'." + Style.RESET_ALL)
        return history

def print_ai_response(response):
    """Prints the AI's text response."""
    print(Style.DIM + Fore.WHITE + response + Style.RESET_ALL)

def build_gemini_messages(history):
    """Convert history to Gemini API message format, with memory context at the start."""
    messages = []
    # Add memory context as the second message
    memory_context = load_memory_content()
    if memory_context.strip():
        messages.append(types.Content(role="user", parts=[types.Part(text=f"Here is my memory context, remember this about me and use it for all future responses:\n{memory_context}")]))
    # Add conversation history
    for msg in history:
        if msg["role"] == "user":
            messages.append(types.Content(role="user", parts=[types.Part(text=msg["content"])]))
        else:
            messages.append(types.Content(role="model", parts=[types.Part(text=msg["content"])]))
    return messages

def process_user_input(user_input, history, config):
    """Processes user input, sends it to Gemini, handles function calls, and lets the AI answer after function calls."""
    history = add_to_history(history, "user", user_input)
    messages = build_gemini_messages(history)
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=config
    )
    parts = response.candidates[0].content.parts
    function_called = False
    if hasattr(parts[0], "function_call") and parts[0].function_call:
        for fn in parts:
            fn = fn.function_call
            function_name = fn.name
            function_args = fn.args
            print(Fore.LIGHTRED_EX + f"Function call detected: {function_name} with arguments {function_args}" + Style.RESET_ALL + "\n------------------------------------------------------------")
            history = handle_function_call(function_name, function_args, history)
            function_called = True

    # After function call(s), let the AI respond with the updated history
    if function_called:
        messages = build_gemini_messages(history)
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=config
        )
        parts = response.candidates[0].content.parts
        ai_text = parts[0].text
        print_ai_response("RESPONSE :"+ ai_text)
        history = add_to_history(history, "assistant", ai_text)
    elif parts and hasattr(parts[0], "text"):
        ai_text = parts[0].text
        print_ai_response(ai_text)
        history = add_to_history(history, "assistant", ai_text)
    return history

def clear_history():
    """Clear the conversation history (both in memory and on disk)."""
    if os.path.exists(HISTORY_FILE):
        os.remove(HISTORY_FILE)
    print(Fore.YELLOW + "Conversation history cleared." + Style.RESET_ALL)
    return []

def main():
    """Main loop for the assistant."""
    history = load_history()
    config = get_content_config()

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
        history = process_user_input(user_input, history, config)

if __name__ == "__main__":
    main()
