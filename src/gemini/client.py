"""
Gemini API client configuration and tool setup.

This module handles:
- Gemini API client initialization 
- Tool configuration with function declarations
- Content generation configuration
- System prompt loading

Extracted from assistant.py to improve code organization and maintainability.
"""
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from .function_declarations import get_all_function_declarations
from datetime import datetime


# Load environment variables
load_dotenv()


class GeminiClient:
    """Wrapper for Gemini API client with configured tools and settings."""
    
    def __init__(self):
        """Initialize the Gemini client with API key from environment."""
        self.api_key = os.getenv('GEMINI_API_KEY')
        self.client = genai.Client(api_key=self.api_key)
        
    def get_grounding_tool(self):
        """Returns the AI tool configuration with all function declarations."""
        return types.Tool(
            google_search=types.GoogleSearch(),
            function_declarations=get_all_function_declarations(),
        )

    def get_content_config(self, system_prompt):
        """Returns the content generation configuration for the AI model."""
        return types.GenerateContentConfig(
            tools=[self.get_grounding_tool()],
            system_instruction=system_prompt,
            thinking_config=types.ThinkingConfig(thinking_budget=1024),
            tool_config=types.ToolConfig(
                function_calling_config=types.FunctionCallingConfig(
                    mode='AUTO')
            ),
        )
    
    def generate_content(self, model_name, config, contents):
        """Generate content using the Gemini API with retry logic and error handling."""
        import time
        from google.genai.errors import ServerError, ClientError, APIError
        
        max_retries = 3
        retry_delay = 2  # seconds
        
        for attempt in range(max_retries):
            try:
                return self.client.models.generate_content(
                    model=model_name,
                    config=config,
                    contents=contents
                )
            except ServerError as e:
                if e.status_code == 500 and attempt < max_retries - 1:
                    print(f"⚠️  Gemini API server error (attempt {attempt + 1}/{max_retries}). Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff
                    continue
                else:
                    print(f"❌ Gemini API server error after {max_retries} attempts: {e.message}")
                    raise APIError(f"Gemini API is temporarily unavailable. Please try again later. (Error: {e.message})")
            except ClientError as e:
                print(f"❌ Gemini API client error: {e.message}")
                raise APIError(f"Invalid request to Gemini API: {e.message}")
            except Exception as e:
                print(f"❌ Unexpected error communicating with Gemini API: {str(e)}")
                raise APIError(f"Failed to communicate with Gemini API: {str(e)}")
        
        # This shouldn't be reached, but just in case
        raise APIError("Failed to generate content after multiple retries")


def load_system_prompt():
    """Load the system prompt from prompt.txt."""
    PROMPT_FILE = "src/utils/prompt.txt"
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    if os.path.exists(PROMPT_FILE):
        with open(PROMPT_FILE, "r", encoding="utf-8") as f:
            return f.read() + f"\n\nCurrent date: {current_date}, time: {datetime.now().strftime('%H:%M:%S')}"
    
    print("System prompt file not found! Using default prompt.\nCreate a prompt.txt file for customized instructions.")
    return "You are a helpful AI assistant."