import importlib
import os
from utils.prompt import get_prompt
from utils.memory import save_to_memory, load_memory
from colorama import Fore, Style
from google import genai
from google.genai import types
from dotenv import load_dotenv
load_dotenv()  # Load environment variables from .env file

# Initialize the Google Gemini model
api_key = os.getenv('GEMINI_API_KEY')
client = genai.Client(api_key=api_key)
# add memory to the chat
chat = client.chats.create(model="gemini-2.5-flash")
chat.send_message(str(load_memory()))

media_functions = {
    "name": "media",
    "description": "Control media playback and volume settings on the computer.",
    "parameters": {
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
                "enum": ["play", "pause", "mute", "unmute", "set_volume"],
                "description": "The action to perform on media playback, such as play, pause, mute, unmute, or set volume.",
            },
            "volume_level": {
                "type": "number",
                "description": "The volume level to set when setting volume, where 0.0 is maximum volume and -65.25 is minimum volume.",
            }
        },
        "required": ["action"],
    },
}

pc_functions = {
    "name": "pc",
    "description": "Control the personal computer, including opening applications, sleeping, restarting",
    "parameters": {
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
                "enum": ["open", "sleep", "restart"],
                "description": "The action to perform on the personal computer, such as opening an application, sleeping, or restarting.",
            },
            "application_name": {
                "type": "string",
                "description": "The name of the application to open when the action is 'open'. (include the full path to the application)",
            }
        },
        "required": ["action"],
    },
}
#Command: files createDir [path\directory name]
#Command: files create [path\file name]
#Command: files write [path\file name] [content]
#Command: files read [path\file name]
#Command: files delete [path\file name]
#Command: files copy [source path] [destination path]
#Command: files move [source path] [destination path]
#Command: files rename [path] [old name] [new name]
#Command: files list [path]
#Command: files search [path] [file name]

files_functions = {
    "name": "files",
    "description": "Manage files and directories on the computer, including creating, writing, reading, deleting, copying, moving, renaming, listing, searching or creating a directory.",
    "parameters": {
        "type": "object",
        "properties": {
            "action": {
                "type": "string",
                "enum": ["create", "write", "read", "delete", "copy", "move", "rename", "list", "search", "createDir"],
                "description": "The action to perform on files or directories, such as creating, writing, reading, deleting, copying, moving, renaming, listing, searching or creating a directory.",
            },
            "path": {
                "type": "string",
                "description": "The path of the file or directory to perform the action on inclding the name of the file or directory. (when searching include only the path without the file name)",
            },
            "content": {
                "type": "string",
                "description": "The content to write to the file when the action is 'write'.",
            },
            "source_path": {
                "type": "string",
                "description": "The source path for copying, moving files.",
            },
            "destination_path": {
                "type": "string",
                "description": "The destination path for copying or moving files.",
            },
            "new_name": {
                "type": "string",
                "description": "The new name for the file or directory when renaming.",
            },
            "file_name": {
                "type": "string",
                "description": "The name of the file to search for when the action is 'search'.",
            }

        },
        "required": ["action", "path"]
    },
}

memory_functions = {
    "name": "memory",
    "description": "Manage (SAVE) memory topics and information.",
    "parameters": {
        "type": "object",
        "properties": {
            "topic": {
                "type": "string",
                "description": "The topic to save or retrieve information from memory.",
            },
            "info": {
                "type": "string",
                "description": "The information to save under the specified topic.",
            }
        },
        "required": ["topic", "info"]
    },
}

# Enable google search tool
grounding_tool = types.Tool(
    google_search=types.GoogleSearch(),
    function_declarations=[media_functions, pc_functions, files_functions, memory_functions],
)
config = types.GenerateContentConfig(
    tools=[grounding_tool],
    automatic_function_calling=types.AutomaticFunctionCallingConfig(
        disable=False
    ),
    tool_config=types.ToolConfig(
             function_calling_config=types.FunctionCallingConfig(mode='auto')
    ),
)



# Helper function to dynamically load a module
def load_module(module_name):
    try:
        module = importlib.import_module(f'modules.{module_name}')
        return module
    except ModuleNotFoundError:
        print(f"Module {module_name} not found!")
        return None


response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Who attacked iran?",
    config =  types.GenerateContentConfig(
        tools=[grounding_tool],
        
        tool_config=types.ToolConfig(
            function_calling_config=types.FunctionCallingConfig(mode='auto')
        )
    )
)

print(response.candidates[0].content.parts[0].text)

if __name__ == "__main__":
    while True:
        user_input =  input(Fore.YELLOW + 'Command: ' + Style.RESET_ALL)  # Prompt the user for input
        if user_input.lower() == 'exit':
            print(Fore.RED + "Goodbye!")
            print(Style.RESET_ALL)
            break  # Exit the loop if the user types 'exit'
        elif user_input.lower() == 'clear':
            os.system('cls' if os.name == 'nt' else 'clear')
            print(Fore.YELLOW + "Cleared the screen.") 
            print(Style.RESET_ALL)
            continue  # Skip the rest of the loop
        elif user_input.strip() == '':
            print(Fore.RED + "Please enter a command.")
            print(Style.RESET_ALL)
            continue

        # Send conversation history to the model
        response = chat.send_message(message=user_input, config=config)
        
        if response.candidates[0].content.parts[0].function_call:
            function_calls = response.candidates[0].content.parts
            for fn in function_calls:
                fn = fn.function_call
                function_name = fn.name
                function_args = fn.args
                print(Fore.GREEN + f"Function call detected: {function_name} with arguments {function_args}" + Style.RESET_ALL)


                if (function_name == "memory"):
                    # Handle memory function calls
                    topic = function_args.get("topic")
                    info = function_args.get("info")
                    if topic and info:
                        save_to_memory(topic, info)
                        print(Fore.GREEN + f"Saved information under topic '{topic}'." + Style.RESET_ALL)
                    elif topic:
                        memory = load_memory()
                        if topic in memory:
                            print(Fore.GREEN + f"Memory for topic '{topic}': {memory[topic]}" + Style.RESET_ALL)
                        else:
                            print(Fore.RED + f"No information found for topic '{topic}'." + Style.RESET_ALL)
                    else:
                        print(Fore.RED + "Invalid memory function call." + Style.RESET_ALL)
                    continue
                module = load_module(function_name)
                # call function based on the function name dynamically without calling specific functions
                if module:
                    if hasattr(module, 'execute'):
                        # Call the execute function in the module
                        res = module.execute(function_args)
                        if res is None:
                            print(Fore.RED + "No response from the function." + Style.RESET_ALL)
                            continue
                        
                        function_response_part = types.Part.from_function_response(
                            name=function_name,
                            response={"result": res})

                        
                        # Add the function response part to the chat
                        if   function_response_part is None:
                            print(Fore.RED + "No response from the function." + Style.RESET_ALL)
                            continue
                        res = chat.send_message(function_response_part)

                        print(Style.DIM + Fore.WHITE + res.text + Style.RESET_ALL)
                
                
            
        else:
            print(Style.DIM + Fore.WHITE + response.candidates[0].content.parts[0].text + Style.RESET_ALL)
            print(Fore.RED + "\nNo function call found in the response.")
        print(Style.RESET_ALL)
