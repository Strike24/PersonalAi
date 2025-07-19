# Code Organization

This document describes the refactored code structure of the Personal AI Assistant.

## Directory Structure

```
src/
├── assistant.py              # Main entry point (82 lines)
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
- Reduced from 458 lines to 82 lines (82% reduction)

### gemini/
- **client.py**: Gemini API client initialization and configuration
- **function_declarations.py**: All function schemas that the AI can call

### core/
- **history_manager.py**: Load, save, and manage conversation history
- **image_handler.py**: Handle clipboard image paste functionality  
- **function_handler.py**: Execute function calls by loading appropriate modules
- **message_processor.py**: Process messages to/from Gemini API

## Benefits of Refactoring

1. **Separation of Concerns**: Each module has a single, clear responsibility
2. **Improved Maintainability**: Easier to modify and extend individual components
3. **Better Readability**: Smaller, focused files are easier to understand
4. **Enhanced Testability**: Individual modules can be tested in isolation
5. **Reduced Complexity**: Main assistant.py is now simple and focused

## Import Structure

The refactored code maintains all original functionality while providing a cleaner import structure:

```python
# Main imports in assistant.py
from gemini.client import GeminiClient, load_system_prompt
from core.history_manager import load_history, clear_history
from core.image_handler import ImageHandler
from core.message_processor import process_user_input
```

All existing functionality is preserved - this was purely a structural refactoring to improve code organization.