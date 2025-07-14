import subprocess
import os

def execute(args):
    """
    Executes a command in the system command line and returns the output.
    args: dict with keys:
        - command: the command to execute (required)
        - path: the working directory for the command execution (optional)
    """
    if not args or "command" not in args:
        return "No command provided."

    command = args.get("command")
    path = args.get("path", None)

    try:
        # Set working directory if provided
        if path and os.path.isdir(path):
            result = subprocess.run(command, shell=True, capture_output=True, text=True, cwd=path)
        else:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
        output = result.stdout.strip() if result.stdout else result.stderr.strip()
        return output if output else "Command executed, but there was no output."
    except Exception as e:
        return f"Error executing command: {str(e)}"
