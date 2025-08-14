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
    
    # Handle compositional function calling with a loop
    max_function_calls = 10  # Prevent infinite loops
    function_call_count = 0
    
    while function_call_count < max_function_calls:
        parts = response.candidates[0].content.parts
        function_called = False
        text_content = ""
        
        # Process all parts in the response
        for part in parts:
            if hasattr(part, "function_call") and part.function_call:
                # Handle function call
                function_name = part.function_call.name
                function_args = part.function_call.args
                print(Fore.LIGHTRED_EX + f"Function call detected: {function_name} with arguments {function_args}" + Style.RESET_ALL + "\n---------------------------------------------------------------")
                
                # Execute the function and get the result
                history_before = len(history)
                history = handle_function_call(function_name, function_args, history)
                
                # Get the function result from the last added history entry
                function_result = ""
                if len(history) > history_before:
                    function_result = history[-1]["content"]
                
                # Add a message to history indicating the function was executed with its result
                # This helps Gemini understand that the function was called and what the result was
                function_execution_msg = f"Function '{function_name}' was executed with arguments {function_args}. Result: {function_result}"
                history = add_to_history(history, "user", function_execution_msg)
                
                function_called = True
                function_call_count += 1
            elif hasattr(part, "text") and part.text:
                # Collect text content but don't display it immediately if functions are being called
                text_content += part.text
        
        # If no function was called, display any text content and exit
        if not function_called:
            if text_content.strip():
                print_ai_response(text_content)
                history = add_to_history(history, "assistant", text_content)
            break  # Exit the loop since no more function calls are needed
        
        # If function(s) were called, don't display the text content (it might be hallucinated)
        # Instead, get the AI's next response based on the function results
        messages = build_gemini_messages(history)
        try:
            response = gemini_client.generate_content(
                model_name="gemini-2.5-flash",
                config=config,
                contents=messages
            )
        except APIError as e:
            error_msg = f"Function executed successfully, but I couldn't generate a follow-up response due to an API error: {str(e)}"
            print(Fore.YELLOW + error_msg + Style.RESET_ALL)
            fallback_response = "The function was executed successfully, but I'm having trouble generating a response right now."
            print_ai_response(fallback_response)
            history = add_to_history(history, "assistant", fallback_response)
            break
        except Exception as e:
            # Handle various types of errors more gracefully
            try:
                # Try to get error message safely
                if hasattr(e, 'message'):
                    error_details = e.message
                elif hasattr(e, 'args') and e.args:
                    error_details = str(e.args[0])
                else:
                    error_details = type(e).__name__
            except:
                error_details = type(e).__name__
            
            error_msg = f"Function executed successfully, but encountered an unexpected error: {error_details}"
            print(Fore.YELLOW + error_msg + Style.RESET_ALL)
            fallback_response = "The function was executed successfully."
            print_ai_response(fallback_response)
            history = add_to_history(history, "assistant", fallback_response)
            break
    
    # Safety check for maximum function calls reached
    if function_call_count >= max_function_calls:
        warning_msg = f"⚠️  Maximum function calls ({max_function_calls}) reached. Stopping to prevent infinite loops."
        print(Fore.YELLOW + warning_msg + Style.RESET_ALL)
        fallback_response = "I've completed multiple function calls but need to stop here to prevent excessive operations."
        print_ai_response(fallback_response)
        history = add_to_history(history, "assistant", fallback_response)

    # Clean up the pasted image after processing
    if image_path is not None:
        image_handler.cleanup_image(image_path)
    
    return history