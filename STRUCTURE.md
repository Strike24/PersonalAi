# Codebase Structure

This document describes the code structure of the Personal AI Assistant.

## Directory Structure

```
src/
├── assistant.py              # Main entry point
├── gemini/                   # Gemini API integration
│   ├── client.py            # API client and configuration
│   └── function_declarations.py  # Function schemas for AI
├── core/                     # Core functionality modules
│   ├── history_manager.py   # Conversation history management
│   ├── image_handler.py     # Clipboard image handling
│   ├── function_handler.py  # Function call execution
│   └── message_processor.py # Message processing logic
├── modules/                  # Existing function modules
│   ├── media.py
│   ├── files.py
│   ├── pc.py
│   ├── spotify.py
│   ├── gmail.py
│   └── commandline.py
└── utils/                    # Utility functions
    ├── memory.py
    ├── prompt.txt
    └── windows_media.py
```

## Module Responsibilities

### assistant.py

- Main entry point and application loop
- User interface and input handling
- Coordinates between other modules

### gemini/

- **client.py**: Gemini API client initialization and configuration
- **function_declarations.py**: All function schemas that the AI can call

### core/

- **history_manager.py**: Load, save, and manage conversation history
- **image_handler.py**: Handle clipboard image paste functionality
- **function_handler.py**: Execute function calls by loading appropriate modules
- **message_processor.py**: Process messages to/from Gemini API
