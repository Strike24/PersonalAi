#Command: pc open [name]
#Command: pc sleep
#Command: pc restart
#Command: pc eval [command to run]
import os

def control_pc(command):
    if "open" in command:
        #get the application name
        words = command.split()
        index = words.index("open")
        app_name = words[index + 1]
        #open the application
        os.system(f"start {app_name}")
        print(f"Opening {app_name}.")

    elif "sleep" in command:
        os.system("shutdown /h")
        print("Sleeping computer.")
    elif "restart" in command:
        os.system("shutdown /r /t 0")
        print("Restarting computer.")
    elif "eval" in command:
        # Extract the command to run
        words = command.split()
        index = words.index("eval")
        command_to_run = " ".join(words[index + 1:])
        # Run the command
        os.system(command_to_run)
        print("Command executed.")
    else:
        print("PC command not recognized.")
