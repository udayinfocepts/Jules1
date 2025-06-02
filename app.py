from flask import Flask, render_template, request
import os

# Import from our AI client modules
from gemini_client import get_gemini_response, list_gemini_models, API_KEY as GEMINI_API_KEY
DEFAULT_GEMINI_MODEL = 'models/gemini-1.5-flash-latest' # Using a specific, current "flash" model

from openai_client import get_openai_response, list_openai_models, OPENAI_API_KEY_DIRECT, MODEL_NAME as DEFAULT_OPENAI_MODEL
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

    # --- Gemini Model Selection Logic ---
    determined_gemini_model_id = DEFAULT_GEMINI_MODEL
    actual_gemini_models_for_dropdown = [{'id': DEFAULT_GEMINI_MODEL, 'display_name': f"Default: {DEFAULT_GEMINI_MODEL.split('/')[-1]}"}]
    current_gemini_list_error = None
    if gemini_configured:
        gemini_models_list_from_api = list_gemini_models()
        if gemini_models_list_from_api and isinstance(gemini_models_list_from_api, list) and \
           gemini_models_list_from_api[0]['id'] not in ['ERROR', 'NO_MODELS', 'API_KEY_NOT_CONFIGURED']:
            actual_gemini_models_for_dropdown = gemini_models_list_from_api
            pref_model_found = False
            if any(m['id'] == DEFAULT_GEMINI_MODEL for m in actual_gemini_models_for_dropdown):
                determined_gemini_model_id = DEFAULT_GEMINI_MODEL
                pref_model_found = True
            if not pref_model_found:
                for model in actual_gemini_models_for_dropdown:
                    model_id_lower = model['id'].lower()
                    if 'flash' in model_id_lower and not any(term in model_id_lower for term in ['legacy', 'alpha', 'beta', 'embed', 'vision']):
                        determined_gemini_model_id = model['id']
                        pref_model_found = True; break
            if not pref_model_found and actual_gemini_models_for_dropdown:
                determined_gemini_model_id = actual_gemini_models_for_dropdown[0]['id']
        elif gemini_models_list_from_api and isinstance(gemini_models_list_from_api, list):
            current_gemini_list_error = gemini_models_list_from_api[0]['display_name']
        else: current_gemini_list_error = "Could not retrieve Gemini model list."
    else: current_gemini_list_error = "Gemini API Key not configured."

    # --- OpenAI Model Selection Logic ---
    determined_openai_model_id = DEFAULT_OPENAI_MODEL
    actual_openai_models_for_dropdown = [{'id': DEFAULT_OPENAI_MODEL, 'display_name': DEFAULT_OPENAI_MODEL}]
    current_openai_list_error = None
    if openai_configured:
        openai_models_list_from_api = list_openai_models()
        if openai_models_list_from_api and isinstance(openai_models_list_from_api, list) and \
           openai_models_list_from_api[0]['id'] not in ['ERROR', 'NO_MODELS', 'AUTH_ERROR', 'API_KEY_NOT_CONFIGURED']:
            actual_openai_models_for_dropdown = openai_models_list_from_api
            pref_model_found = False
            if any(m['id'] == DEFAULT_OPENAI_MODEL for m in actual_openai_models_for_dropdown):
                determined_openai_model_id = DEFAULT_OPENAI_MODEL
                pref_model_found = True
            if not pref_model_found:
                for model in actual_openai_models_for_dropdown:
                    if 'gpt-4' in model['id']: determined_openai_model_id = model['id']; pref_model_found = True; break
            if not pref_model_found and actual_openai_models_for_dropdown:
                 determined_openai_model_id = actual_openai_models_for_dropdown[0]['id']
        elif openai_models_list_from_api and isinstance(openai_models_list_from_api, list):
            current_openai_list_error = openai_models_list_from_api[0]['display_name']
        else: current_openai_list_error = "Could not retrieve OpenAI model list."
    else: current_openai_list_error = "OpenAI API Key not configured."

    return render_template('index.html',
                           gemini_configured=gemini_configured, openai_configured=openai_configured, claude_configured=claude_configured,
                           gemini_models=actual_gemini_models_for_dropdown, current_gemini_model=determined_gemini_model_id, gemini_list_error=current_gemini_list_error, gemini_model_display=determined_gemini_model_id,
                           openai_models=actual_openai_models_for_dropdown, current_openai_model=determined_openai_model_id, openai_list_error=current_openai_list_error, openai_model_display=determined_openai_model_id,
                           claude_model_display=DEFAULT_CLAUDE_MODEL)

@app.route('/get_response', methods=['POST'])
def get_response_route():
    gemini_configured = check_gemini_config()
    openai_configured = check_openai_config()
    claude_configured = check_claude_config()
    prompt = request.form.get('prompt')

    # --- Gemini Model Logic for POST ---
    _initial_gemini_model_id = DEFAULT_GEMINI_MODEL
    _actual_gemini_models_for_dropdown = [{'id': DEFAULT_GEMINI_MODEL, 'display_name': f"Default: {DEFAULT_GEMINI_MODEL.split('/')[-1]}"}]
    _current_gemini_list_error = None
    if gemini_configured:
        gemini_models_list_from_api = list_gemini_models()
        if gemini_models_list_from_api and isinstance(gemini_models_list_from_api, list) and \
           gemini_models_list_from_api[0]['id'] not in ['ERROR', 'NO_MODELS', 'API_KEY_NOT_CONFIGURED']:
            _actual_gemini_models_for_dropdown = gemini_models_list_from_api
            pref_model_found = any(m['id'] == DEFAULT_GEMINI_MODEL for m in _actual_gemini_models_for_dropdown)
            if pref_model_found: _initial_gemini_model_id = DEFAULT_GEMINI_MODEL
            else: # Simplified fallback
                if 'flash' in _actual_gemini_models_for_dropdown[0]['id'].lower() : _initial_gemini_model_id = _actual_gemini_models_for_dropdown[0]['id']
                # else stick with DEFAULT_GEMINI_MODEL if first in list is not flash (or add more specific selection)
        elif gemini_models_list_from_api: _current_gemini_list_error = gemini_models_list_from_api[0]['display_name']
        else: _current_gemini_list_error = "Could not retrieve Gemini model list."
    else: _current_gemini_list_error = "Gemini API Key not configured."
    selected_gemini_model = request.form.get('gemini_model_select', _initial_gemini_model_id)

    # --- OpenAI Model Logic for POST ---
    _initial_openai_model_id = DEFAULT_OPENAI_MODEL
    _actual_openai_models_for_dropdown = [{'id': DEFAULT_OPENAI_MODEL, 'display_name': DEFAULT_OPENAI_MODEL}]
    _current_openai_list_error = None
    if openai_configured:
        openai_models_list_from_api = list_openai_models()
        if openai_models_list_from_api and isinstance(openai_models_list_from_api, list) and \
           openai_models_list_from_api[0]['id'] not in ['ERROR', 'NO_MODELS', 'AUTH_ERROR', 'API_KEY_NOT_CONFIGURED']:
            _actual_openai_models_for_dropdown = openai_models_list_from_api
            pref_model_found = any(m['id'] == DEFAULT_OPENAI_MODEL for m in _actual_openai_models_for_dropdown)
            if pref_model_found: _initial_openai_model_id = DEFAULT_OPENAI_MODEL
            elif _actual_openai_models_for_dropdown: _initial_openai_model_id = _actual_openai_models_for_dropdown[0]['id']
        elif openai_models_list_from_api: _current_openai_list_error = openai_models_list_from_api[0]['display_name']
        else: _current_openai_list_error = "Could not retrieve OpenAI model list."
    else: _current_openai_list_error = "OpenAI API Key not configured."
    selected_openai_model = request.form.get('openai_model_select', _initial_openai_model_id)

    if not prompt:
        return render_template('index.html',
                               error="Prompt cannot be empty.", prompt_text=prompt,
                               gemini_configured=gemini_configured, openai_configured=openai_configured, claude_configured=claude_configured,
                               gemini_models=_actual_gemini_models_for_dropdown, current_gemini_model=selected_gemini_model, gemini_list_error=_current_gemini_list_error, gemini_model_display=selected_gemini_model,
                               openai_models=_actual_openai_models_for_dropdown, current_openai_model=selected_openai_model, openai_list_error=_current_openai_list_error, openai_model_display=selected_openai_model,
                               claude_model_display=DEFAULT_CLAUDE_MODEL)

    gemini_response_text = openai_response_text = claude_response_text = None
    error_messages = []

    if gemini_configured:
        gemini_response_text = get_gemini_response(prompt, model_to_use=selected_gemini_model)
        if "Error:" in gemini_response_text or "An error occurred:" in gemini_response_text:
            error_messages.append(f"Gemini ({selected_gemini_model.split('/')[-1]}): {gemini_response_text}")
    else: error_messages.append("Gemini: API key not configured.")

    if openai_configured:
        openai_response_text = get_openai_response(prompt, model_to_use=selected_openai_model)
        if "Error:" in openai_response_text or "An unexpected error occurred with OpenAI:" in openai_response_text or "OpenAI AuthenticationError:" in openai_response_text or "OpenAI RateLimitError:" in openai_response_text or "OpenAI APIConnectionError:" in openai_response_text or "OpenAI NotFoundError:" in openai_response_text :
            error_messages.append(f"OpenAI ({selected_openai_model}): {openai_response_text}")
    else: error_messages.append("OpenAI: API key not configured.")

    if claude_configured:
        # Assuming claude_client.get_claude_response will be updated to take model_to_use
        claude_response_text = get_claude_response(prompt, model_to_use=DEFAULT_CLAUDE_MODEL)
        if "Error:" in claude_response_text or "An unexpected error occurred with Anthropic:" in claude_response_text or "Anthropic AuthenticationError:" in claude_response_text or "Anthropic RateLimitError:" in claude_response_text or "Anthropic APIConnectionError:" in claude_response_text:
            error_messages.append(f"Claude ({DEFAULT_CLAUDE_MODEL.replace('claude-3-haiku-','c3-haiku-')}): {claude_response_text}")
    else: error_messages.append("Claude: API key not configured.")

    final_error_message = " | ".join(error_messages) if error_messages else None

    return render_template('index.html',
                           gemini_response=gemini_response_text, openai_response=openai_response_text, claude_response=claude_response_text,
                           prompt_text=prompt, error=final_error_message,
                           gemini_configured=gemini_configured, openai_configured=openai_configured, claude_configured=claude_configured,
                           gemini_models=_actual_gemini_models_for_dropdown, current_gemini_model=selected_gemini_model, gemini_list_error=_current_gemini_list_error, gemini_model_display=selected_gemini_model,
                           openai_models=_actual_openai_models_for_dropdown, current_openai_model=selected_openai_model, openai_list_error=_current_openai_list_error, openai_model_display=selected_openai_model,
                           claude_model_display=DEFAULT_CLAUDE_MODEL)

if __name__ == '__main__':
    print("Starting Flask server for Multi-AI Aggregator (Gemini, OpenAI, Claude)...")
    print("Open your browser and go to http://127.0.0.1:5000/")
    print("Ensure API keys are set in client files or as environment variables.")
    app.run(debug=True)
