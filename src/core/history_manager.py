"""
Conversation history management.
Handles loading, saving, and managing conversation history with the AI.
"""
import os
import json


# History configuration
HISTORY_FILE = "src/utils/history.json"
MAX_HISTORY = 100


def load_history():
    """Load conversation history from a JSON file."""
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except Exception:
                return []
    return []


def save_history(history):
    """Save conversation history to a JSON file."""
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history[-MAX_HISTORY:], f, ensure_ascii=False, indent=2)


def add_to_history(history, role, content):
    """Add a message to the history and trim to the last MAX_HISTORY messages."""
    history.append({"role": role, "content": content})
    if len(history) > MAX_HISTORY:
        history = history[-MAX_HISTORY:]
    save_history(history)
    return history


def clear_history():
    """Clear the conversation history (both in memory and on disk)."""
    if os.path.exists(HISTORY_FILE):
        os.remove(HISTORY_FILE)
    print("Conversation history cleared.")
    return []


def load_memory_content():
    """Load memory.json as a string for context injection."""
    MEMORY_FILE = "src/utils/memory.json"
    
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            try:
                memory = json.load(f)
                return json.dumps(memory, ensure_ascii=False, indent=2)
            except Exception:
                return ""
    return ""