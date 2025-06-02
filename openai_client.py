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

MODEL_NAME = 'gpt-3.5-turbo' # This will be the default for __main__ tests

# New function to list models:
def list_openai_models(api_key: str = None) -> list:
    """
    Lists available OpenAI GPT models suitable for chat completion.

    Args:
        api_key: Optional. Your OpenAI API key.
    
    Returns:
        A list of dictionaries, where each has 'id' and 'display_name' (which is also the id).
        Returns a list with an error indicator if an error occurs.
    """
    client = None
    try:
        if api_key:
            client = openai.OpenAI(api_key=api_key)
        elif os.getenv('OPENAI_API_KEY'):
            client = openai.OpenAI()
        elif OPENAI_API_KEY_DIRECT != 'YOUR_OPENAI_API_KEY':
            client = openai.OpenAI(api_key=OPENAI_API_KEY_DIRECT)
        else:
            return [{'id': 'ERROR', 'display_name': 'OpenAI API Key Not Configured'}]

        models_list_data = client.models.list()
        processed_models = []
        if models_list_data:
            for model in models_list_data.data: # .data contains the list of Model objects
                # Revised filter:
                model_id_lower = model.id.lower()
                is_likely_chat_model = model_id_lower.startswith('gpt-')

                # Terms that usually indicate non-chat or highly specialized models we might want to exclude
                # 'instruct' can sometimes be chat-like, but often refers to older completion models.
                # We'll keep 'instruct' in the blacklist for now to prefer pure chat models like gpt-3.5-turbo, gpt-4.
                # If too few models appear, 'instruct' could be removed from this blacklist.
                non_chat_terms = ['vision', 'image', 'audio', 'embed', 'instruct', 'davinci', 'babbage', 'curie', 'ada'] 

                is_not_specialized_non_chat = not any(term in model_id_lower for term in non_chat_terms)

                # Consider ownership if we want to primarily list base models from OpenAI,
                # but removing it might show more fine-tuned models if the user has them.
                # For now, let's try without the strict 'owned_by' check to be more inclusive.
                # is_openai_owned = 'openai' in model.owned_by.lower() or 'openai-org' in model.owned_by.lower()

                if is_likely_chat_model and is_not_specialized_non_chat:
                    processed_models.append({'id': model.id, 'display_name': model.id})
        
        if not processed_models:
            return [{'id': 'NO_MODELS', 'display_name': 'No suitable GPT models found'}]
            
        # Sort models, perhaps to put gpt-4 versions before gpt-3.5 if desired, or just alphabetically
        processed_models.sort(key=lambda x: x['id'], reverse=True) # Simple sort, gpt-4 often appears before gpt-3.5

        return processed_models
    except openai.AuthenticationError:
        return [{'id': 'AUTH_ERROR', 'display_name': 'OpenAI Auth Error (check key/billing)'}]
    except Exception as e:
        print(f"An error occurred while listing OpenAI models: {e}")
        return [{'id': 'ERROR', 'display_name': f'Error listing OpenAI models: {str(e)}'}]

# Modify existing get_openai_response function:
def get_openai_response(prompt: str, model_to_use: str, api_key: str = None) -> str:
    """
    Sends a prompt to the specified OpenAI API model and returns the text response.

    Args:
        prompt: The text prompt to send to the model.
        model_to_use: The specific OpenAI model ID to use (e.g., 'gpt-3.5-turbo').
        api_key: Optional. Your OpenAI API key.
    Returns:
        The model's text response, or an error message if something went wrong.
    """
    client = None
    if not model_to_use:
        return "Error: No model specified for OpenAI."
        
    try:
        if api_key:
            client = openai.OpenAI(api_key=api_key)
        elif os.getenv('OPENAI_API_KEY'):
            client = openai.OpenAI()
        elif OPENAI_API_KEY_DIRECT != 'YOUR_OPENAI_API_KEY':
            client = openai.OpenAI(api_key=OPENAI_API_KEY_DIRECT)
        else:
            return "Error: OpenAI API key not configured. Please set the OPENAI_API_KEY environment variable or update OPENAI_API_KEY_DIRECT in openai_client.py."

        response = client.chat.completions.create(
            model=model_to_use, # Use the passed model_to_use
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        if response.choices and len(response.choices) > 0:
            return response.choices[0].message.content.strip()
        else:
            return "Error: No response received from OpenAI."

    except openai.AuthenticationError:
        return f"OpenAI AuthenticationError on model {model_to_use}: Incorrect API key or billing issue."
    except openai.RateLimitError:
        return f"OpenAI RateLimitError on model {model_to_use}: You have exceeded your current quota."
    except openai.NotFoundError: # Specific error if model doesn't exist or user doesn't have access
         return f"OpenAI NotFoundError: The model '{model_to_use}' was not found or you do not have access."
    except openai.APIConnectionError as e:
        return f"OpenAI APIConnectionError on model {model_to_use}: Could not connect. Details: {e}"
    except Exception as e:
        return f"An unexpected error occurred with OpenAI model {model_to_use}: {e}"

# Update the __main__ block:
if __name__ == '__main__':
    print("Welcome to the OpenAI API Client!")
    print("---------------------------------")
    print("Important: Make sure you have configured your OpenAI API key.")
    # ... (rest of existing API key instructions) ...
    print("You can set it as an environment variable 'OPENAI_API_KEY' (recommended),")
    print("or directly edit the 'OPENAI_API_KEY_DIRECT' variable in this script.")
    print("Get an API key from https://platform.openai.com/account/api-keys")
    print("---------------------------------")

    configured_check = os.getenv('OPENAI_API_KEY') or OPENAI_API_KEY_DIRECT != 'YOUR_OPENAI_API_KEY'

    if not configured_check:
        print("Please configure your OpenAI API key before running tests.")
    else:
        print(f"--- Testing Model Listing (OpenAI) ---")
        available_models = list_openai_models()
        if available_models and available_models[0]['id'] not in ['ERROR', 'NO_MODELS', 'AUTH_ERROR', 'API_KEY_NOT_CONFIGURED']:
            print("Available and suitable OpenAI GPT models:")
            for model_info in available_models:
                print(f"  ID: {model_info['id']}")
        else:
            print(f"Could not retrieve OpenAI model list or no suitable models found. Reason: {available_models[0]['display_name'] if available_models else 'Unknown'}")
        print("------------------------------------")

        print(f"\n--- Testing Response Generation (OpenAI) ---")
        # Use the global MODEL_NAME as the default for this direct script test
        print(f"Using model (for get_openai_response test): {MODEL_NAME}") 
        test_prompt = "What is the capital of France?"
        print(f"Sending prompt: \"{test_prompt}\"")
        
        # Pass the model_to_use argument
        api_response = get_openai_response(test_prompt, model_to_use=MODEL_NAME) 
        
        print("\nResponse from OpenAI (ChatGPT):")
        print(api_response)
        print("--------------------------------------")

    print("\n--- Test Complete ---")
    print("You can now import functions from this client in your Flask app.")
