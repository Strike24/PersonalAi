"""
Message processing for Gemini API interactions.
Handles building messages, processing responses, and managing the conversation flow.
"""
import os
from google.genai import types
from PIL import Image
from colorama import Fore, Style
from .history_manager import add_to_history, load_memory_content
from .function_handler import handle_function_call


def build_gemini_messages(history):
    """Convert history to Gemini API message format, with memory context at the start."""
    messages = []
    # Add memory context as the second message
    memory_context = load_memory_content()
    if memory_context.strip():
        messages.append(types.Content(role="user", parts=[types.Part(text=f"Here is my memory context, remember this about me and use it for all future responses:\n{memory_context}")]))
    # Add conversation history
    for msg in history:
        if msg["role"] == "user":
            messages.append(types.Content(role="user", parts=[types.Part(text=msg["content"])]))
        else:
            messages.append(types.Content(role="model", parts=[types.Part(text=msg["content"])]))
    return messages


def print_ai_response(response):
    """Prints the AI's text response."""
    print(Style.BRIGHT + Fore.WHITE + response + Style.RESET_ALL)


def process_user_input(user_input, history, gemini_client, config, image_handler):
    """Processes user input, sends it to Gemini, handles function calls, and lets the AI answer after function calls."""
    from google.genai.errors import APIError
    
    history = add_to_history(history, "user", user_input)
    messages = build_gemini_messages(history)
    
    # If an image is pasted, add it to the messages
    image_path = image_handler.get_current_image_path()
    if image_path is not None and os.path.exists(image_path):
        image = Image.open(image_path)
        messages.append(image)

    try:
        response = gemini_client.generate_content(
            model_name="gemini-2.5-flash",
            config=config,
            contents=messages
        )
    except APIError as e:
        error_msg = f"🚫 API Error: {str(e)}"
        print(Fore.RED + error_msg + Style.RESET_ALL)
        history = add_to_history(history, "assistant", "I'm sorry, but I'm having trouble connecting to my AI service right now. Please try your request again in a moment.")
        return history
    except Exception as e:
        error_msg = f"🚫 Unexpected error: {str(e)}"
        print(Fore.RED + error_msg + Style.RESET_ALL)
        history = add_to_history(history, "assistant", "I encountered an unexpected error. Please try your request again.")
        return history
    
    parts = response.candidates[0].content.parts
    function_called = False
    # Handle function calls
    if hasattr(parts[0], "function_call") and parts[0].function_call:
        for fn in parts:
            fn = fn.function_call
            function_name = fn.name
            function_args = fn.args
            print(Fore.LIGHTRED_EX + f"Function call detected: {function_name} with arguments {function_args}" + Style.RESET_ALL + "\n---------------------------------------------------------------")
            history = handle_function_call(function_name, function_args, history)
            function_called = True

    # After function call(s), let the AI respond with the updated history
    if function_called:
        messages = build_gemini_messages(history)
        try:
            response = gemini_client.generate_content(
                model_name="gemini-2.5-flash",
                config=config,
                contents=messages
            )
            parts = response.candidates[0].content.parts
            ai_text = parts[0].text
            if (ai_text is not None and ai_text.strip()) or len(parts) > 1:
                print_ai_response(ai_text)
                history = add_to_history(history, "assistant", ai_text)
        except APIError as e:
            error_msg = f"Function executed successfully, but I couldn't generate a follow-up response due to an API error: {str(e)}"
            print(Fore.YELLOW + error_msg + Style.RESET_ALL)
            fallback_response = "The function was executed successfully, but I'm having trouble generating a response right now."
            print_ai_response(fallback_response)
            history = add_to_history(history, "assistant", fallback_response)
        except Exception as e:
            # Handle various types of errors more gracefully
            try:
                error_details = str(e)
            except:
                error_details = repr(e)
            error_msg = f"Function executed successfully, but encountered an unexpected error: {error_details}"
            print(Fore.YELLOW + error_msg + Style.RESET_ALL)
            fallback_response = "The function was executed successfully."
            print_ai_response(fallback_response)
            history = add_to_history(history, "assistant", fallback_response)
    elif parts and hasattr(parts[0], "text"):
        ai_text = parts[0].text
        print_ai_response(ai_text)
        history = add_to_history(history, "assistant", ai_text)

    # Clean up the pasted image after processing
    if image_path is not None:
        image_handler.cleanup_image(image_path)
    
    return history