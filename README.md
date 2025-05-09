# Personal AI Assistant

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
