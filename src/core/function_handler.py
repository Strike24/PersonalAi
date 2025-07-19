"""
Function call handling and module loading.
Manages the execution of function calls from the AI by loading appropriate modules.
"""
import importlib
from colorama import Fore, Style
from utils.memory import save_to_memory
from .history_manager import add_to_history


def load_module(module_name):
    """Dynamically loads a module from the 'modules' package."""
    try:
        return importlib.import_module(f'modules.{module_name}')
    except ModuleNotFoundError:
        print(f"Module {module_name} not found!")
        return None


def handle_memory_function(function_args):
    """Handles memory function calls: save or retrieve information."""
    topic = function_args.get("topic")
    info = function_args.get("info")
    if topic and info:
        save_to_memory(topic, info)
        print(f"Saved information under topic '{topic}'.")
    else:
        print("Invalid memory function call.")


def handle_function_call(function_name, function_args, history):
    """Handles dynamic function calls by loading and executing the appropriate module.
    Adds the function response to history so the AI remembers."""
    if function_name == "memory":
        handle_memory_function(function_args)
        return history

    module = load_module(function_name)
    if module and hasattr(module, 'execute'):
        res = module.execute(function_args)
        if res is None:
            print(Fore.RED + "No response from the function." + Style.RESET_ALL)
            return history
        print(Style.DIM + Fore.WHITE + str(res) + Style.RESET_ALL)
        # Add function response to history as assistant message
        history = add_to_history(history, "assistant", str(res))
        return history
    else:
        print(Fore.RED + f"No executable module found for '{function_name}'." + Style.RESET_ALL)
        return history