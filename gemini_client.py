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
MODEL_NAME = 'gemini-2.0-flash'

def get_gemini_response(prompt: str) -> str:
    """
    Sends a prompt to the Gemini API and returns the text response.

    Args:
        prompt: The text prompt to send to the model.

    Returns:
        The model's text response, or an error message if something went wrong.
    """
    if API_KEY == 'YOUR_API_KEY':
        return "Error: API_KEY has not been configured. Please edit gemini_client.py and replace 'YOUR_API_KEY' with your actual API key."

    try:
        genai.configure(api_key=API_KEY)

        # Create the model instance
        # GenerationConfig and SafetySettings can be customized if needed.
        # For a simple request, defaults are often fine.
        model = genai.GenerativeModel(MODEL_NAME)

        # Send the prompt and get the response
        response = model.generate_content(prompt)

        return response.text
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == "__main__":
    print("Welcome to the Gemini API Client!")
    print("---------------------------------")
    print("Important: Make sure you have replaced 'YOUR_API_KEY' in this script with your actual API key.")
    print("You can get an API key from https://aistudio.google.com/apikey")
    print("---------------------------------")

    if API_KEY == 'YOUR_API_KEY':
        print("Please configure your API key in gemini_client.py before running.")
    else:
        print(f"Using model: {MODEL_NAME}")
        print("\nThis script will now send a test prompt to the Gemini API.")
        
        test_prompt = "Explain what a Large Language Model is in one sentence."
        print(f"\nSending prompt: \"{test_prompt}\"")
        
        # Get the response
        api_response = get_gemini_response(test_prompt)
        
        print("\nResponse from Gemini:")
        print(api_response)

        print("\n--- Test Complete ---")
        print("You can now import the 'get_gemini_response' function in your Flask app.")
