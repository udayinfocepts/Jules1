import openai
import os

# --- Configuration ---
# IMPORTANT: You need to set your OpenAI API key.
# Option 1: Set it as an environment variable named OPENAI_API_KEY.
#             The script will automatically pick it up. This is recommended.
# Option 2: Replace 'YOUR_OPENAI_API_KEY' below with your actual key.
#             This is simpler for this script but less secure for larger projects.
# You can obtain an API key from: https://platform.openai.com/account/api-keys
OPENAI_API_KEY_DIRECT = 'YOUR_OPENAI_API_KEY' # Replace if not using environment variable

MODEL_NAME = 'gpt-3.5-turbo'

def get_openai_response(prompt: str, api_key: str = None) -> str:
    """
    Sends a prompt to the OpenAI API (ChatGPT) and returns the text response.

    Args:
        prompt: The text prompt to send to the model.
        api_key: Optional. Your OpenAI API key. If not provided,
                 the function will try to use the OPENAI_API_KEY environment
                 variable or the OPENAI_API_KEY_DIRECT variable set in this file.

    Returns:
        The model's text response, or an error message if something went wrong.
    """
    client = None
    try:
        if api_key:
            client = openai.OpenAI(api_key=api_key)
        elif os.getenv('OPENAI_API_KEY'):
            client = openai.OpenAI() # Uses environment variable OPENAI_API_KEY
        elif OPENAI_API_KEY_DIRECT != 'YOUR_OPENAI_API_KEY':
            client = openai.OpenAI(api_key=OPENAI_API_KEY_DIRECT)
        else:
            return "Error: OpenAI API key not configured. Please set the OPENAI_API_KEY environment variable or update OPENAI_API_KEY_DIRECT in openai_client.py."

        # Create a chat completion request
        # For gpt-3.5-turbo and similar models, the input is a list of messages
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        # The response structure for chat models provides choices, and the message content is nested.
        if response.choices and len(response.choices) > 0:
            return response.choices[0].message.content.strip()
        else:
            return "Error: No response received from OpenAI."

    except openai.AuthenticationError:
        return "OpenAI AuthenticationError: Incorrect API key or billing issue. Please check your OpenAI API key and account status."
    except openai.RateLimitError:
        return "OpenAI RateLimitError: You have exceeded your current quota. Please check your OpenAI plan and billing details."
    except openai.APIConnectionError as e:
        return f"OpenAI APIConnectionError: Could not connect to OpenAI. Details: {e}"
    except Exception as e:
        return f"An unexpected error occurred with OpenAI: {e}"

if __name__ == '__main__':
    print("Welcome to the OpenAI API Client!")
    print("---------------------------------")
    print("Important: Make sure you have configured your OpenAI API key.")
    print("You can set it as an environment variable 'OPENAI_API_KEY' (recommended),")
    print("or directly edit the 'OPENAI_API_KEY_DIRECT' variable in this script.")
    print("Get an API key from https://platform.openai.com/account/api-keys")
    print("---------------------------------")

    # Check if key might be configured
    configured_check = os.getenv('OPENAI_API_KEY') or OPENAI_API_KEY_DIRECT != 'YOUR_OPENAI_API_KEY'

    if not configured_check:
        print("Please configure your OpenAI API key before running.")
    else:
        print(f"Using model: {MODEL_NAME}")
        print("\nThis script will now send a test prompt to the OpenAI API.")
        
        test_prompt = "What is the capital of France?"
        print(f"\nSending prompt: \"{test_prompt}\"")
        
        # Get the response
        api_response = get_openai_response(test_prompt)
        
        print("\nResponse from OpenAI (ChatGPT):")
        print(api_response)

        print("\n--- Test Complete ---")
        print("You can now import the 'get_openai_response' function in your Flask app.")
