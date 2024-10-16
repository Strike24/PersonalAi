import os

def get_prompt():
    modules_folder = os.path.join(os.path.dirname(__file__), '..', 'modules')
    modules = [f for f in os.listdir(modules_folder) if os.path.isfile(os.path.join(modules_folder, f))]

    module_commands = []
    for module in modules:
        module_path = os.path.join(modules_folder, module)
        with open(module_path, 'r') as file:
            commands = file.readlines()
            command_names = []
            for line in commands:
                # Check for lines that define commands using a specific comment format
                if line.startswith("#Command:"):
                    command_name = line[len("#Command:"):].strip()  # Extract the command name
                    command_names.append(command_name)
            
            # Add to the module_commands list only if there are command names found
            if command_names:
                module_commands.append(f"{module[:-3]}: {', '.join(command_names)}")  # Remove .py from the module name

    return f"""Hello, You are a personal computer assistant. You can run specific commands on your computer. 
            Instructions:

            Please enter only the command using the following format:
            [module] [action] [parameters if needed]

            Examples:
            pc open browser
            media set volume 0.0
            media mute
            **Available Modules and Commands**:
            {chr(10).join(module_commands)}

            Important Notes:
            For the pc module, use the full path for directories and files. Windows user is: tomxc
            For the set volume command:
                Use a float between 0.0 (maximum volume) and -65.25 (minimum volume).
                If asked for 100% volume, set it to 0.0.
                If asked for 0% volume, set it to -65.25.
            Provide no feedback or extra text; only return the command.
            If command is chat, answer regularly as if you were chatting with a person. than return to the instructions.
            For any request that requires command execution (like downloading packages), use the eval command.
            You ARE NOT typing in markdown. Do not include any markdown syntax in your responses.
            If multiple commands are needed, separate them with a semicolon (;)."""

