import ollama
import importlib
import os
from utils.prompt import get_prompt

# Helper function to dynamically load a module
def load_module(module_name):
    try:
        module = importlib.import_module(f'modules.{module_name}')
        return module
    except ModuleNotFoundError:
        print(f"Module {module_name} not found!")
        return None

# Function to handle user commands and trigger the right module
def handle_command(command):
    # Split command to identify module and action
    parts = command.split()
    if len(parts) < 2:
        print("Please provide a module and a command.")
        return
    
    module_name = parts[0]
    action = ' '.join(parts[1:])  # Join the rest as the action

    # Load the specified module
    module = load_module(module_name)
    if module:
        # Check if the module has a function to handle commands
        if hasattr(module, 'control_' + module_name):
            control_function = getattr(module, 'control_' + module_name)
            control_function(action)  # Call the function with the action
        else:
            print(f"""Module '{module_name}' does not have a function to handle the commands,
                  or it isn't named right.""")
    else:
        print("Command not recognized.")

if __name__ == "__main__":
    while True:
        # Get the user's input
        response = ollama.chat(model='codegemma:7b', messages=[{'role': 'system', 'content': get_prompt()},
                                                                {'role': 'user', 'content': input('Command: ')}])
        command = response['message']['content']
        print(command)

        handle_command(command)
