#Command: files create [path\file name]
#Command: files delete [path\file name]
#Command: files copy [source path] [destination path]
#Command: files move [source path] [destination path]
#Command: files rename [path] [old name] [new name]
#Command: files list [path]
#Command: files search [path] [file name]

import os
import shutil


def control_files(command):
    if "create" in command:
        # Extract the path
        words = command.split()
        index = words.index("create")
        path = words[index + 1]
        # Create the file
        open(f"{path}", "w").close()
        print(f"File created at {path}.")
        
    elif "delete" in command:
        # Extract the path
        words = command.split()
        index = words.index("delete")
        path = words[index + 1]
        # Delete the file
        os.remove(f"{path}")
        print(f"File deleted from {path}.")


    elif "copy" in command:
        # Extract the source and destination paths from the command
        words = command.split()
        index = words.index("copy")
        source_path = words[index + 1]
        dest_path = words[index + 2]
        # Copy the file
        shutil.copy(f"{source_path}", f"{dest_path}")
        print(f"File copied from {source_path} to {dest_path}.")
    elif "move" in command:
        # Extract the source and destination paths from the command
        words = command.split()
        index = words.index("move")
        source_path = words[index + 1]
        dest_path = words[index + 2]
        # Move the file
        shutil.move(f"{source_path}", f"{dest_path}")
        print(f"File moved from {source_path} to {dest_path}.")
    elif "rename" in command:
        # Extract the path, old name, and new name from the command
        words = command.split()
        index = words.index("rename")
        path = words[index + 1]
        old_name = words[index + 2]
        new_name = words[index + 3]
        # Rename the file
        os.rename(f"{path}/{old_name}", f"{path}/{new_name}")
        print(f"File {old_name} renamed to {new_name} in {path}.")
    elif "list" in command:
        # Extract the path from the command
        words = command.split()
        index = words.index("list")
        path = words[index + 1]
        # List the files in the directory, make it look nice
        files = os.listdir(path)
        print(f"Files in {path}:")
        for file in files:
            print(file)
            
    elif "search" in command:
        # Extract the path and file name from the command
        words = command.split()
        index = words.index("search")
        path = words[index + 1]
        file_name = words[index + 2]
        # Search for the file in the directory
        files = os.listdir(path)
        if file_name in files:
            print(f"File {file_name} found in {path}.")
        else:
            print(f"File {file_name} not found in {path}.")
    else:
        print("Files command not recognized.")

