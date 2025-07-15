#Command: pc open [name]
#Command: pc sleep
#Command: pc restart
import os
import webbrowser

def execute(args):
    if args is None or len(args) == 0:
        return ("No command provided.")
    
    command = args.get("action", None).lower()  # Convert command to lowercase for case-insensitive matching

    if "open_website" in command:
        website_url = args.get("website_url", None)
        if website_url is not None:
            webbrowser.open(website_url)
            return(f"Opening website: {website_url}.")
        else:
            return("No website URL provided.")
    elif "open" in command:
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
