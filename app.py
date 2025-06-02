from flask import Flask, render_template, request
import os

# Import from our AI client modules
from gemini_client import get_gemini_response, list_gemini_models, API_KEY as GEMINI_API_KEY
DEFAULT_GEMINI_MODEL = 'models/gemini-1.5-flash-latest' # Using a specific, current "flash" model
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

    # --- Smart Default Selection Logic for index() ---
    determined_default_model_id = DEFAULT_GEMINI_MODEL
    actual_models_for_dropdown = [{'id': DEFAULT_GEMINI_MODEL, 'display_name': f"Default: {DEFAULT_GEMINI_MODEL.split('/')[-1]}"}]
    current_gemini_list_error = None

    if gemini_configured:
        gemini_models_list_from_api = list_gemini_models()

        if gemini_models_list_from_api and isinstance(gemini_models_list_from_api, list) and \
           gemini_models_list_from_api[0]['id'] not in ['ERROR', 'NO_MODELS', 'API_KEY_NOT_CONFIGURED']:

            actual_models_for_dropdown = gemini_models_list_from_api

            preferred_model_found = False
            # 1. Check if DEFAULT_GEMINI_MODEL is in the fetched list
            for model in actual_models_for_dropdown:
                if model['id'] == DEFAULT_GEMINI_MODEL:
                    determined_default_model_id = DEFAULT_GEMINI_MODEL
                    preferred_model_found = True
                    break

            # 2. If not, look for other "flash" models (non-legacy, non-beta, non-vision, non-embed)
            if not preferred_model_found:
                for model in actual_models_for_dropdown:
                    model_id_lower = model['id'].lower()
                    if 'flash' in model_id_lower and not any(term in model_id_lower for term in ['legacy', 'alpha', 'beta', 'embed', 'vision']):
                        determined_default_model_id = model['id']
                        preferred_model_found = True
                        break

            # 3. If no preferred model found by now, use the first model from the valid dynamic list
            if not preferred_model_found and actual_models_for_dropdown:
                determined_default_model_id = actual_models_for_dropdown[0]['id']
            # If actual_models_for_dropdown was empty, determined_default_model_id remains DEFAULT_GEMINI_MODEL

        else: # Error fetching list or Gemini not configured (this inner else handles errors from list_gemini_models)
            if gemini_models_list_from_api and isinstance(gemini_models_list_from_api, list): # It's an error structure
                current_gemini_list_error = gemini_models_list_from_api[0]['display_name']
            # If gemini_models_list_from_api is None or not a list (unexpected), no specific error is set here, relies on outer else.
            # determined_default_model_id remains DEFAULT_GEMINI_MODEL
            # actual_models_for_dropdown remains the single-entry default list

    else: # Gemini not configured
        current_gemini_list_error = "Gemini API Key not configured."
        # determined_default_model_id remains DEFAULT_GEMINI_MODEL
        # actual_models_for_dropdown remains the single-entry default list
    # --- End Smart Default Selection Logic for index() ---

    return render_template('index.html',
                           gemini_configured=gemini_configured,
                           openai_configured=openai_configured,
                           claude_configured=claude_configured,
                           gemini_models=actual_models_for_dropdown,
                           current_gemini_model=determined_default_model_id,
                           gemini_list_error=current_gemini_list_error,
                           gemini_model_display=determined_default_model_id, # For API status modal initially
                           openai_model_display=DEFAULT_OPENAI_MODEL,
                           claude_model_display=DEFAULT_CLAUDE_MODEL)

@app.route('/get_response', methods=['POST'])
def get_response_route():
    gemini_configured = check_gemini_config()
    openai_configured = check_openai_config()
    claude_configured = check_claude_config()

    prompt = request.form.get('prompt')

    # --- Smart Default Selection Logic for get_response_route() (for re-rendering) ---
    _initial_default_gemini_model = DEFAULT_GEMINI_MODEL
    actual_models_for_dropdown_on_post = [{'id': DEFAULT_GEMINI_MODEL, 'display_name': f"Default: {DEFAULT_GEMINI_MODEL.split('/')[-1]}"}]
    current_gemini_list_error_on_post = None

    if gemini_configured:
        gemini_models_list_from_api = list_gemini_models()

        if gemini_models_list_from_api and isinstance(gemini_models_list_from_api, list) and \
           gemini_models_list_from_api[0]['id'] not in ['ERROR', 'NO_MODELS', 'API_KEY_NOT_CONFIGURED']:

            actual_models_for_dropdown_on_post = gemini_models_list_from_api

            preferred_model_found = False
            for model in actual_models_for_dropdown_on_post:
                if model['id'] == DEFAULT_GEMINI_MODEL:
                    _initial_default_gemini_model = DEFAULT_GEMINI_MODEL
                    preferred_model_found = True
                    break
            if not preferred_model_found:
                for model in actual_models_for_dropdown_on_post:
                    model_id_lower = model['id'].lower()
                    if 'flash' in model_id_lower and not any(term in model_id_lower for term in ['legacy', 'alpha', 'beta', 'embed', 'vision']):
                        _initial_default_gemini_model = model['id']
                        preferred_model_found = True
                        break
            if not preferred_model_found and actual_models_for_dropdown_on_post:
                _initial_default_gemini_model = actual_models_for_dropdown_on_post[0]['id']
        else:
            if gemini_models_list_from_api and isinstance(gemini_models_list_from_api, list):
                 current_gemini_list_error_on_post = gemini_models_list_from_api[0]['display_name']
            # No explicit else for "Could not retrieve..." here, covered by the initial value of current_gemini_list_error_on_post
    else:
        current_gemini_list_error_on_post = "Gemini API Key not configured."

    selected_gemini_model = request.form.get('gemini_model_select', _initial_default_gemini_model)
    # --- End Smart Default Selection Logic ---

    if not prompt:
        return render_template('index.html',
                               error="Prompt cannot be empty.",
                               prompt_text=prompt,
                               gemini_configured=gemini_configured,
                               openai_configured=openai_configured,
                               claude_configured=claude_configured,
                               gemini_models=actual_models_for_dropdown_on_post,
                               current_gemini_model=selected_gemini_model,
                               gemini_list_error=current_gemini_list_error_on_post,
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
                           gemini_models=actual_models_for_dropdown_on_post,
                           current_gemini_model=selected_gemini_model,
                           gemini_list_error=current_gemini_list_error_on_post,
                           gemini_model_display=selected_gemini_model, # Show selected model in modal
                           openai_model_display=DEFAULT_OPENAI_MODEL,
                           claude_model_display=DEFAULT_CLAUDE_MODEL)

if __name__ == '__main__':
    print("Starting Flask server for Multi-AI Aggregator (Gemini, OpenAI, Claude)...")
    print("Open your browser and go to http://127.0.0.1:5000/")
    print("Ensure API keys are set in client files or as environment variables.")
    app.run(debug=True)
