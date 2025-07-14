<!-- # Personal AI Assistant

Welcome to the Personal AI Assistant project! This assistant is designed to help you control various aspects of your computer and perform tasks using voice or text commands. Built using Python and the Ollama library, this project is modular and easily expandable. I designed this project to be a fun and educational way to learn about AI and voice recognition (in the future 👀).
> ❗ Requires Ollama to work. uses Ollama ai models on your computer in order to identify commands. ❗

![Personal AI Assistant Demo](https://i.imgur.com/1mMf4UW.gif)

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Contributing](#contributing)
- [Adding New Modules](#adding-new-modules)

## Features

- Control media playback (e.g., Spotify).
- Manage files and folders (create, delete, rename, list, etc).
- Perform system commands (shutdown, restart, etc).
- Manage reminders and to-do lists. (coming soon)
- Retrieve weather information. (coming soon)
- And more!

## Installation

Coming soon!

## Contributing

Any contributions you make are **greatly appreciated**. If you have any suggestions, bug reports, or feature requests, please open an issue or create a pull request.

> I know this project is still in its early stages, so I'll be very greatful for any infrastructural changes in the codebase that you think would make it easier to work with!

Also, if you'd like to contribute a new module, please see the [Adding New Modules](#adding-new-modules) section.

## Adding New Modules

To contribute a new module, follow these steps:

- Create a new Python file in the `modules` directory. name it based on the module (e.g., `weather.py`).
- Implement the module using the following template:
  ```python
    def modulename_control(command):
        if "keyword" in command:
            # do something
        else:
            print("Module_name command not recognized.")
  ```

<!--
To get started with the Personal AI Assistant, follow these steps:

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/personal-ai-assistant.git
   cd personal-ai-assistant
   ``` -->

# Personal AI Assistant 💻

Simple AI assistant built with Python and Google's Gemini API. <br>
This assistant can perform various tasks on your computer using voice or text commands. It is modular and easily expandable, built for educational purposes.
Using Gemini's Function Calling feature, the assistant can execute Python functions to perform tasks like controlling media playback, managing files, and more.

### Current Modules

- **Media Control**: Control media playback.
- **File Management**: Create, delete, rename, list and search for files and folders.
- **System Commands**: Execute system commands like shutdown and restart.
- **Memory Management**: Remember and recall information.
- **Command Line**: Execute command line commands.
- **Spotify Integration**: Control spotify playback and play songs. (Premium Required)
  Coming soon: Reminders, weather information, smart home control, and more..
![Untitledvideo-MadewithClipchamp-ezgif com-video-to-gif-converter](https://github.com/user-attachments/assets/f97ebf02-e275-4e61-8568-1b0933acd6e6)

### Other Examples
<img width="1737" height="709" alt="image" src="https://github.com/user-attachments/assets/10853a67-9be4-4459-9421-d0fbb528c61c" />
Initalizing a javascript project in a directory

<img width="1743" height="449" alt="image" src="https://github.com/user-attachments/assets/296b74f3-3d2f-4062-9bc3-fd0321eb4d0b" />
Installing express package using npm

<img width="1750" height="458" alt="image" src="https://github.com/user-attachments/assets/f55a9970-7fd8-4418-9445-11c3fd6a23e5" />
Creating an index.js file with boilerplate express code that gemini geneterated

> All examples were on the same session. gemini used the history and memory system to get its context.
