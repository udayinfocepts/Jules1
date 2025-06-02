import anthropic
import os

# --- Configuration ---
# IMPORTANT: You need to set your Anthropic API key.
# Option 1: Set it as an environment variable named ANTHROPIC_API_KEY.
#             The script will automatically pick it up. This is recommended.
# Option 2: Replace 'YOUR_ANTHROPIC_API_KEY' below with your actual key.
# You can obtain an API key from: https://console.anthropic.com/account/keys
ANTHROPIC_API_KEY_DIRECT = 'YOUR_ANTHROPIC_API_KEY' # Replace if not using environment variable

# Using Claude 3 Haiku for cost-effectiveness and speed.
MODEL_NAME = 'claude-3-haiku-20240307' # Ensure this is one of the IDs from list_claude_models

def list_claude_models(api_key: str = None) -> list:
    """
    Returns a static list of recommended Anthropic Claude models.
    The api_key argument is included for consistency but not used in this static implementation.
    """
    # Static list of Claude models
    # Ensure these model IDs are valid and generally available.
    static_models = [
        {'id': 'claude-3-haiku-20240307', 'display_name': 'Claude 3 Haiku'},
        {'id': 'claude-3-sonnet-20240229', 'display_name': 'Claude 3 Sonnet'},
        {'id': 'claude-instant-1.2', 'display_name': 'Claude Instant 1.2'} 
        # Add claude-3-opus-20240229 if desired, but it's more expensive
    ]
    # To mimic the structure of dynamic listers in case of API key issues (though not applicable here for static)
    # This structure helps app.py handle it consistently if it expects an error dict.
    # For a static list, we assume API key configuration is not directly tied to listing.
    # However, if ANTHROPIC_API_KEY_DIRECT is not set, perhaps return an error indicator.
    
    # For simplicity with a static list, we'll just return the list directly.
    # If app.py needs to check configuration before showing even static models,
    # that logic would reside in app.py based on check_claude_config().
    return static_models

def get_claude_response(prompt: str, model_to_use: str, api_key: str = None) -> str:
    """
    Sends a prompt to the specified Anthropic Claude API model and returns the text response.

    Args:
        prompt: The text prompt to send to the model.
        model_to_use: The specific Claude model ID to use (e.g., 'claude-3-haiku-20240307').
        api_key: Optional. Your Anthropic API key. If not provided,
                 the function will try to use the ANTHROPIC_API_KEY environment
                 variable or the ANTHROPIC_API_KEY_DIRECT variable set in this file.

    Returns:
        The model's text response, or an error message if something went wrong.
    """
    client = None
    if not model_to_use:
        return "Error: No model specified for Claude."

    try:
        current_api_key = None # Determine API key to use
        if api_key:
            current_api_key = api_key
        elif os.getenv('ANTHROPIC_API_KEY'):
            current_api_key = os.getenv('ANTHROPIC_API_KEY')
        elif ANTHROPIC_API_KEY_DIRECT != 'YOUR_ANTHROPIC_API_KEY':
            current_api_key = ANTHROPIC_API_KEY_DIRECT
        
        if not current_api_key:
             return "Error: Anthropic API key not configured. Please set the ANTHROPIC_API_KEY environment variable or update ANTHROPIC_API_KEY_DIRECT in claude_client.py."

        client = anthropic.Anthropic(api_key=current_api_key)

        # Create a message request
        response = client.messages.create(
            model=model_to_use, # Use the passed model_to_use
            max_tokens=2048, # Max tokens for the response
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        # The response structure for Claude API provides content as a list of blocks.
        # We need to extract the text from the first text block if available.
        if response.content and isinstance(response.content, list) and len(response.content) > 0:
            first_block = response.content[0]
            if hasattr(first_block, 'text'):
                return first_block.text
            else:
                return "Error: No text content found in Claude's response block."
        else:
            return "Error: No content received from Claude or unexpected format."

    except anthropic.AuthenticationError as e:
        error_message = e.body.get('error', {}).get('message', 'Please check your Anthropic API key and account status.')
        return f"Anthropic AuthenticationError on model {model_to_use}: {error_message}"
    except anthropic.RateLimitError as e:
        error_message = e.body.get('error', {}).get('message', 'You have exceeded your current quota.')
        return f"Anthropic RateLimitError on model {model_to_use}: {error_message}"
    except anthropic.APIConnectionError as e:
        return f"Anthropic APIConnectionError on model {model_to_use}: Could not connect to Anthropic. Details: {e}"
    except Exception as e:
        return f"An unexpected error occurred with Anthropic model {model_to_use}: {e}"

if __name__ == '__main__':
    print("Welcome to the Anthropic Claude API Client!")
    print("-----------------------------------------")
    print("Important: Make sure you have configured your Anthropic API key.")
    print("You can set it as an environment variable 'ANTHROPIC_API_KEY' (recommended),")
    print("or directly edit the 'ANTHROPIC_API_KEY_DIRECT' variable in this script.")
    print(f"Get an API key from https://console.anthropic.com/account/keys")
    print("-----------------------------------------")

    configured_check = os.getenv('ANTHROPIC_API_KEY') or ANTHROPIC_API_KEY_DIRECT != 'YOUR_ANTHROPIC_API_KEY'

    if not configured_check:
        print("Please configure your Anthropic API key before running full tests.")
    else:
        print(f"--- Testing Model Listing (Claude) ---")
        available_models = list_claude_models()
        if available_models: # Should always be true for static list unless modified
            print("Available Claude models (static list):")
            for model_info in available_models:
                print(f"  ID: {model_info['id']}, Name: {model_info['display_name']}")
        else: # Should not happen with current static list logic
            print("Could not retrieve Claude model list.")
        print("------------------------------------")

        print(f"\n--- Testing Response Generation (Claude) ---")
        # Use the global MODEL_NAME (e.g., claude-3-haiku-20240307) as the default for this direct script test
        print(f"Using model (for get_claude_response test): {MODEL_NAME}") 
        test_prompt = "Explain the concept of 'emergence' in complex systems in a few sentences."
        print(f"Sending prompt: \"{test_prompt}\"")
        
        api_response = get_claude_response(test_prompt, model_to_use=MODEL_NAME) 
        
        print("\nResponse from Anthropic Claude:")
        print(api_response)
        print("--------------------------------------")

    print("\n--- Test Complete ---")
    print("You can now import functions from this client in your Flask app.")
