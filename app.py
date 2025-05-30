from flask import Flask, render_template, request
import os

# Import from our AI client modules
from gemini_client import get_gemini_response, list_gemini_models, API_KEY as GEMINI_API_KEY, MODEL_NAME as DEFAULT_GEMINI_MODEL
from openai_client import get_openai_response, OPENAI_API_KEY_DIRECT, MODEL_NAME as DEFAULT_OPENAI_MODEL
from claude_client import get_claude_response, ANTHROPIC_API_KEY_DIRECT, MODEL_NAME as DEFAULT_CLAUDE_MODEL

app = Flask(__name__)

def check_gemini_config():
    return GEMINI_API_KEY != 'YOUR_API_KEY'

def check_openai_config():
    return os.getenv('OPENAI_API_KEY') is not None or OPENAI_API_KEY_DIRECT != 'YOUR_OPENAI_API_KEY'

def check_claude_config():
    return os.getenv('ANTHROPIC_API_KEY') is not None or ANTHROPIC_API_KEY_DIRECT != 'YOUR_ANTHROPIC_API_KEY'

@app.route('/', methods=['GET'])
def index():
    gemini_configured = check_gemini_config()
    openai_configured = check_openai_config()
    claude_configured = check_claude_config()
    
    gemini_models_list = []
    gemini_list_error = None
    if gemini_configured:
        gemini_models_list_result = list_gemini_models() # Uses API_KEY from gemini_client
        # Check if the result indicates an error or no models
        if gemini_models_list_result and gemini_models_list_result[0]['id'] in ['ERROR', 'NO_MODELS', 'API_KEY_NOT_CONFIGURED']: # Corrected logic here
            gemini_list_error = gemini_models_list_result[0]['display_name']
            gemini_models_list = [{'id': DEFAULT_GEMINI_MODEL, 'display_name': f"Default: {DEFAULT_GEMINI_MODEL.replace('models/', '')}"}]
        else:
            gemini_models_list = gemini_models_list_result
    else:
        gemini_list_error = "Gemini API Key not configured."
        # Provide a default model for display even if not configured, so dropdown can exist
        gemini_models_list = [{'id': DEFAULT_GEMINI_MODEL, 'display_name': f"Default: {DEFAULT_GEMINI_MODEL.replace('models/', '')}"}]

    return render_template('index.html', 
                           gemini_configured=gemini_configured,
                           openai_configured=openai_configured,
                           claude_configured=claude_configured,
                           gemini_models=gemini_models_list,
                           current_gemini_model=DEFAULT_GEMINI_MODEL, # Default selected model on first load
                           gemini_list_error=gemini_list_error,
                           gemini_model_display=DEFAULT_GEMINI_MODEL, # For the API status modal initially
                           openai_model_display=DEFAULT_OPENAI_MODEL, # Renamed from openai_model for clarity
                           claude_model_display=DEFAULT_CLAUDE_MODEL) # Renamed from claude_model for clarity

@app.route('/get_response', methods=['POST'])
def get_response_route():
    gemini_configured = check_gemini_config()
    openai_configured = check_openai_config()
    claude_configured = check_claude_config()
    
    prompt = request.form.get('prompt')
    selected_gemini_model = request.form.get('gemini_model_select', DEFAULT_GEMINI_MODEL) # Get selected model or default

    # Regenerate Gemini models list for the template context, in case of errors or if needed for re-render
    gemini_models_list_for_template = []
    gemini_list_error_for_template = None # Initialize error variable for this scope
    if gemini_configured:
        gemini_models_list_result = list_gemini_models()
        if gemini_models_list_result and gemini_models_list_result[0]['id'] in ['ERROR', 'NO_MODELS', 'API_KEY_NOT_CONFIGURED']: # Corrected logic here
            gemini_list_error_for_template = gemini_models_list_result[0]['display_name']
            gemini_models_list_for_template = [{'id': DEFAULT_GEMINI_MODEL, 'display_name': f"Default: {DEFAULT_GEMINI_MODEL.replace('models/', '')}"}]
        else:
            gemini_models_list_for_template = gemini_models_list_result
    else:
        gemini_list_error_for_template = "Gemini API Key not configured."
        gemini_models_list_for_template = [{'id': DEFAULT_GEMINI_MODEL, 'display_name': f"Default: {DEFAULT_GEMINI_MODEL.replace('models/', '')}"}]


    if not prompt:
        return render_template('index.html', 
                               error="Prompt cannot be empty.", 
                               prompt_text=prompt,
                               gemini_configured=gemini_configured,
                               openai_configured=openai_configured,
                               claude_configured=claude_configured,
                               gemini_models=gemini_models_list_for_template,
                               current_gemini_model=selected_gemini_model,
                               gemini_list_error=gemini_list_error_for_template,
                               gemini_model_display=selected_gemini_model,
                               openai_model_display=DEFAULT_OPENAI_MODEL,
                               claude_model_display=DEFAULT_CLAUDE_MODEL)

    gemini_response_text = None
    openai_response_text = None
    claude_response_text = None
    error_messages = []

    # Gemini
    if not gemini_configured:
        error_messages.append("Gemini: API key not configured in gemini_client.py.")
    else:
        gemini_response_text = get_gemini_response(prompt, model_to_use=selected_gemini_model) # Pass selected model
        if "Error:" in gemini_response_text or "An error occurred:" in gemini_response_text: # Check for errors from client
            error_messages.append(f"Gemini ({selected_gemini_model.replace('models/','')}): {gemini_response_text}")
    
    # OpenAI
    if not openai_configured:
        error_messages.append("OpenAI: API key not configured.")
    else:
        openai_response_text = get_openai_response(prompt) # Using default model from openai_client
        if "Error:" in openai_response_text or "An unexpected error occurred with OpenAI:" in openai_response_text or "OpenAI AuthenticationError:" in openai_response_text or "OpenAI RateLimitError:" in openai_response_text or "OpenAI APIConnectionError:" in openai_response_text:
            error_messages.append(f"OpenAI ({DEFAULT_OPENAI_MODEL}): {openai_response_text}")

    # Claude
    if not claude_configured:
        error_messages.append("Claude: API key not configured.")
    else:
        claude_response_text = get_claude_response(prompt) # Using default model from claude_client
        if "Error:" in claude_response_text or "An unexpected error occurred with Anthropic:" in claude_response_text or "Anthropic AuthenticationError:" in claude_response_text or "Anthropic RateLimitError:" in claude_response_text or "Anthropic APIConnectionError:" in claude_response_text :
            error_messages.append(f"Claude ({DEFAULT_CLAUDE_MODEL.replace('claude-3-haiku-','c3-haiku-')}): {claude_response_text}")


    final_error_message = " | ".join(error_messages) if error_messages else None
        
    return render_template('index.html', 
                           gemini_response=gemini_response_text,
                           openai_response=openai_response_text,
                           claude_response=claude_response_text,
                           prompt_text=prompt,
                           error=final_error_message,
                           gemini_configured=gemini_configured,
                           openai_configured=openai_configured,
                           claude_configured=claude_configured,
                           gemini_models=gemini_models_list_for_template,
                           current_gemini_model=selected_gemini_model,
                           gemini_list_error=gemini_list_error_for_template,
                           gemini_model_display=selected_gemini_model, # Show selected model in modal
                           openai_model_display=DEFAULT_OPENAI_MODEL,
                           claude_model_display=DEFAULT_CLAUDE_MODEL)

if __name__ == '__main__':
    print("Starting Flask server for Multi-AI Aggregator (Gemini, OpenAI, Claude)...")
    print("Open your browser and go to http://127.0.0.1:5000/")
    print("Ensure API keys are set in client files or as environment variables.")
    app.run(debug=True)
