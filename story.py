from dotenv import load_dotenv
from openai import OpenAI
import os
import json

# Load API Key from environment variables
def load_api_key():
    """
    Load the OpenAI API key from the environment variables using dotenv.

    Returns:
        str: The OpenAI API key.
    """
    load_dotenv()  # Load variables from the .env file
    return os.getenv('OPENAI_API_KEY')  # Retrieve the API key

# Get response from OpenAI model
def get_openai_response(api_key: str, model: str, system_prompt: str, user_message: str, temperature: float = 1, max_tokens: int = 2000):
    """
    Generate a chat completion response from the OpenAI model.

    Args:
        api_key (str): The API key to authenticate with OpenAI.
        model (str): The model name (e.g., "gpt-4").
        system_prompt (str): Instructions provided to the model.
        user_message (str): The user's input message.
        temperature (float): Sampling temperature (higher values generate more randomness).
        max_tokens (int): Maximum number of tokens to include in the response.

    Returns:
        dict: The response object from the OpenAI model.
    """
    # Initialize OpenAI client with the provided API key
    client = OpenAI(api_key=api_key)

    # Generate a chat completion response
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": 'system', "content": system_prompt},  # Instructions for the model
            {"role": 'user', "content": user_message},    # User's message
        ],
        temperature=temperature,  # Control randomness
        max_tokens=max_tokens     # Limit on response length
    )
    return response

# Clean the response content from OpenAI
def clean_response_content(response_content: str):
    """
    Process and clean the response content from OpenAI. 
    Removes markdown formatting and ensures the content is valid JSON.

    Args:
        response_content (str): Raw response content from OpenAI.

    Returns:
        dict: Parsed and cleaned JSON content.
    """
    response_content = response_content.strip()  # Remove any extra whitespace

    # Remove markdown-style JSON delimiters if present
    if response_content.startswith("```json") and response_content.endswith("```"):
        response_content = response_content[7:-3].strip()  # Strip delimiters

    # Attempt to parse the response content as JSON
    try:
        return json.loads(response_content)  # Convert the string to JSON
    except json.JSONDecodeError as e:
        # If JSON decoding fails, provide raw content for debugging
        print("Error parsing JSON. Raw content:")
        print(response_content)  # Log the problematic content
        raise ValueError(f"Invalid JSON format: {e}")  # Raise a detailed error
