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


import os
import shutil


def execute(args):
    if args is None or len(args) == 0:
        return("No command provided.")
    
    command = args.get("action", None).lower()  # Convert command to lowercase for case-insensitive matching


    if "createdir" in command:
        path = args.get("path", None)  # Get the path from the arguments
        if path is None:
            return("No path provided for directory creation.")
        try:
            # Create the directory
            os.makedirs(path)
            return(f"Directory created at: {path}")
        except FileExistsError:
            return(f"Error: Directory '{path}' already exists.")
        except PermissionError:
            return(f"Error: Permission denied to create directory at '{path}'.")
        except Exception as e:
            return(f"An error occurred: {e}")

    elif "create" in command:
        path = args.get("path", None)  # Get the path from the arguments
        if path is None:
            return("No path provided for file creation.")
            return
        # Create the file
        open(f"{path}", "w").close()
        return(f"File created at {path}.")
        
    elif "write" in command:
        path = args.get("path", None)  # Get the path from the arguments
        if path is None:
            return("No path provided for file writing.")
        content  = args.get("content", None)  # Get the content from the arguments
        if content is None:
            return("No content provided for file writing.")
        
        # Write the content to the file
        with open(f"{path}", "w") as file:
            file.write(content)
        return(f"Content written to {path}.")

    elif "read" in command:
        path = args.get("path", None)  # Get the path from the arguments
        if path is None:
            return("No path provided for file reading.")
            return
        # Read the content of the file
        with open(f"{path}", "r") as file:
            content = file.read()
        return(f"Content of {path}:" f"\n{content}")

    elif "delete" in command:
       path = args.get("path", None)  # Get the path from the arguments
       if path is None:
            return("No path provided for file deletion.")
       # Delete the file
       try:
           os.remove(f"{path}")
       except FileNotFoundError:
            return(f"Error: File '{path}' not found.")
       except PermissionError:
            return(f"Error: Permission denied to delete file '{path}'.")
       return(f"File deleted from {path}.")

    elif "copy" in command:
        source_path = args.get("source_path", None)  # Get the source path from the arguments
        dest_path = args.get("destination_path", None)  # Get the destination path from the arguments
        if source_path is None or dest_path is None:
            return("Source or destination path not provided for file copying.")
        # Copy the file
        shutil.copy(f"{source_path}", f"{dest_path}")
        return(f"File copied from {source_path} to {dest_path}.")
    elif "move" in command:
        source_path = args.get("source_path", None)
        dest_path = args.get("destination_path", None)
        if source_path is None or dest_path is None:
            return("Source or destination path not provided for file moving.")        # Move the file
        shutil.move(f"{source_path}", f"{dest_path}")
        return(f"File moved from {source_path} to {dest_path}.")
    elif "rename" in command:
        path =  args.get("path", None)  # Get the path from the arguments
        old_name =  args.get("old_name", None)  # Get the old name from the arguments
        new_name =   args.get("new_name", None)  # Get the new name from the arguments
        if path is None or old_name is None or new_name is None:
            return("Path, old name or new name not provided for file renaming.")
        # Rename the file
        os.rename(f"{path}/{old_name}", f"{path}/{new_name}")
        return(f"File {old_name} renamed to {new_name} in {path}.")
    elif "list" in command:
        # Extract the path from the command
        path = args.get("path", None)
        if path is None:
            return("No path provided for listing files.")
        # List the files in the directory, make it look nice
        files = os.listdir(path)
        str = f"Files in {path}:"
        for file in files:
            str += f"\n- {file}"
        return str

    elif "search" in command:
        # Extract the path and file name from the command
        path = args.get("path", None)
        file_name = args.get("file_name", None)
        if path is None or file_name is None:
            return("Path or file name not provided for file searching.")
        # Search for the file in the directory, and its subdirectories
        # return the path of the file if found or a message if not found
        for root, dirs, files in os.walk(path):
            if file_name in files:
                return(f"File found at: {os.path.join(root, file_name)}")
        else:
            return(f"File '{file_name}' not found in '{path}' or its subdirectories.")
    else:
        return("Files command not recognized.")

