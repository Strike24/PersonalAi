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
        """Generate content using the Gemini API."""
        return self.client.models.generate_content(
            model=model_name,
            config=config,
            contents=contents
        )


def load_system_prompt():
    """Load the system prompt from prompt.txt."""
    PROMPT_FILE = "src/utils/prompt.txt"
    current_date = datetime.now().strftime("%Y-%m-%d")
    
    if os.path.exists(PROMPT_FILE):
        with open(PROMPT_FILE, "r", encoding="utf-8") as f:
            return f.read() + f"\n\nCurrent date: {current_date}, time: {datetime.now().strftime('%H:%M:%S')}"
    
    print("System prompt file not found! Using default prompt.\nCreate a prompt.txt file for customized instructions.")
    return "You are a helpful AI assistant."