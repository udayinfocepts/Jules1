import google.generativeai as genai
import os

# --- Configuration ---
# IMPORTANT: Replace 'YOUR_API_KEY' with your actual Google AI Studio API key.
# You can obtain an API key from: https://aistudio.google.com/apikey
# For better security, consider using environment variables or a config file
# for production, but for this simple script, direct replacement is fine.
API_KEY = 'YOUR_API_KEY'

# You can also try 'gemini-1.5-flash-latest' if 'gemini-2.0-flash' gives issues
# or if you want to ensure you're using the latest flash model.
# Both have good free tier limits.
MODEL_NAME = 'gemini-2.0-flash' # This can remain as a default for __main__ testing

def get_gemini_response(prompt: str, model_to_use: str, api_key: str = None) -> str:
    """
    Sends a prompt to the specified Gemini API model and returns the text response.

    Args:
        prompt: The text prompt to send to the model.
        model_to_use: The specific Gemini model ID to use (e.g., 'models/gemini-pro').
        api_key: Optional. Your Google AI Studio API key. If not provided,
                 it will try to use the API_KEY constant set in this file.
    Returns:
        The model's text response, or an error message if something went wrong.
    """
    current_api_key = api_key if api_key else API_KEY
    if current_api_key == 'YOUR_API_KEY':
        return "Error: API_KEY has not been configured. Please edit gemini_client.py and replace 'YOUR_API_KEY' with your actual API key."

    if not model_to_use: # Basic check
        return "Error: No model specified for Gemini."

    try:
        genai.configure(api_key=current_api_key)
        model = genai.GenerativeModel(model_to_use) # Use the passed model_to_use
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"An error occurred with Gemini model {model_to_use}: {e}"

# New function to list models:
def list_gemini_models(api_key: str = None) -> list:
    """
    Lists available Gemini models that support 'generateContent'.

    Args:
        api_key: Optional. Your Google AI Studio API key. If not provided,
                 it will try to use the API_KEY constant set in this file.
    
    Returns:
        A list of dictionaries, where each dictionary has 'id' (model resource name)
        and 'display_name'. Returns an empty list if an error occurs or no suitable models are found.
    """
    models_list = []
    current_api_key = api_key if api_key else API_KEY

    if current_api_key == 'YOUR_API_KEY':
        print("Error in list_gemini_models: API_KEY has not been configured.")
        return [{'id': 'ERROR', 'display_name': 'API Key Not Configured'}] # Error indication

    try:
        genai.configure(api_key=current_api_key)
        
        # Iterate through all available models
        for model in genai.list_models():
            # Check if the model supports the 'generateContent' method (or similar)
            # The exact method name might be 'generateContent' or 'generate_content'
            # in supported_generation_methods. Let's check for common variations.
            if any(method in ['generateContent', 'generate_content', 'models.generateContent'] for method in model.supported_generation_methods):
                models_list.append({
                    'id': model.name,  # e.g., 'models/gemini-pro'
                    'display_name': model.display_name 
                })
        
        if not models_list:
             # This case could happen if the API returns models but none support generateContent,
             # or if the API returns no models at all.
             return [{'id': 'NO_MODELS', 'display_name': 'No suitable models found'}]

        return models_list
    except Exception as e:
        print(f"An error occurred while listing Gemini models: {e}")
        # Return a list with an error indicator that app.py can check
        return [{'id': 'ERROR', 'display_name': f'Error listing models: {str(e)}'}]

if __name__ == "__main__":
    print("Welcome to the Gemini API Client!")
    print("---------------------------------")
    # ... (existing __main__ content for get_gemini_response) ...
    print("Important: Make sure you have replaced 'YOUR_API_KEY' in this script with your actual API key.")
    print("You can get an API key from https://aistudio.google.com/apikey")
    print("---------------------------------")

    if API_KEY == 'YOUR_API_KEY':
        print("Please configure your API key in gemini_client.py before running get_gemini_response test.")
    else:
        print(f"Using model (for get_gemini_response test): {MODEL_NAME}")
        print("\nThis script will now send a test prompt to the Gemini API.")
        
        test_prompt = "Explain what a Large Language Model is in one sentence."
        print(f"\nSending prompt: \"{test_prompt}\"")
        
        # Get the response
        api_response = get_gemini_response(test_prompt, model_to_use=MODEL_NAME)
        
        print("\nResponse from Gemini:")
        print(api_response)

        print("\n--- Get Response Test Complete ---")
    
    print("\n--- Testing Model Listing ---")
    if API_KEY == 'YOUR_API_KEY':
        print("Skipping model listing test as API_KEY is not configured.")
    else:
        print("Attempting to list Gemini models...")
        available_models = list_gemini_models()
        if available_models:
            print("Available and suitable Gemini models:")
            for model_info in available_models:
                print(f"  ID: {model_info['id']}, Name: {model_info['display_name']}")
        else:
            print("Could not retrieve model list or no suitable models found.")
    print("-----------------------------")
    print("You can now import the 'get_gemini_response' and 'list_gemini_models' functions in your Flask app.")
