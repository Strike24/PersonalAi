
import json
import os
MEMORY_FILE = os.getenv('MEMORY_FILE', 'src/utils/memory.json')

def save_to_memory(topic, info):
    # Load existing memory
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            memory = json.load(f)
    else:
        memory = {}

    # Save or update memory
    memory[topic] = info

    # Write back to memory file
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=2)


def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    else:
        return {}
    
