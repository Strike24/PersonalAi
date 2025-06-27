#Command: pc open [name]
#Command: pc sleep
#Command: pc restart
import os

def execute(args):
    if args is None or len(args) == 0:
        return ("No command provided.")
    
    command = args.get("action", None).lower()  # Convert command to lowercase for case-insensitive matching

    if "open" in command:
        app_name = args.get("application_name", None)
        #open the application
        os.system(f"{app_name}")
        return(f"Opening {app_name}.")

    elif "sleep" in command:
        os.system("shutdown /h")
        return("Sleeping computer.")
    elif "restart" in command:
        os.system("shutdown /r /t 0")
        return("Restarting computer.")
    else:
        return("PC command not recognized.")
