from flask import Flask, render_template, request
import os

# Import from our AI client modules
from gemini_client import get_gemini_response, API_KEY as GEMINI_API_KEY, MODEL_NAME as GEMINI_MODEL_NAME
from openai_client import get_openai_response, OPENAI_API_KEY_DIRECT, MODEL_NAME as OPENAI_MODEL_NAME
from claude_client import get_claude_response, ANTHROPIC_API_KEY_DIRECT, MODEL_NAME as CLAUDE_MODEL_NAME

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
    return render_template('index.html', 
                           gemini_configured=gemini_configured,
                           openai_configured=openai_configured,
                           claude_configured=claude_configured,
                           gemini_model=GEMINI_MODEL_NAME,
                           openai_model=OPENAI_MODEL_NAME,
                           claude_model=CLAUDE_MODEL_NAME)

@app.route('/get_response', methods=['POST'])
def get_response_route():
    gemini_configured = check_gemini_config()
    openai_configured = check_openai_config()
    claude_configured = check_claude_config()
    
    prompt = request.form.get('prompt')
    if not prompt:
        return render_template('index.html', 
                               error="Prompt cannot be empty.", 
                               prompt_text=prompt,
                               gemini_configured=gemini_configured,
                               openai_configured=openai_configured,
                               claude_configured=claude_configured,
                               gemini_model=GEMINI_MODEL_NAME,
                               openai_model=OPENAI_MODEL_NAME,
                               claude_model=CLAUDE_MODEL_NAME)

    gemini_response_text = None
    openai_response_text = None
    claude_response_text = None
    error_messages = []

    # Gemini
    if not gemini_configured:
        error_messages.append("Gemini API key not configured in gemini_client.py.")
    else:
        gemini_response_text = get_gemini_response(prompt)
        if "Error:" in gemini_response_text or "An error occurred:" in gemini_response_text:
            error_messages.append(f"Gemini: {gemini_response_text}")
    
    # OpenAI
    if not openai_configured:
        error_messages.append("OpenAI API key not configured in openai_client.py or as ENV variable.")
    else:
        openai_response_text = get_openai_response(prompt)
        if "Error:" in openai_response_text or "An unexpected error occurred with OpenAI:" in openai_response_text or "OpenAI AuthenticationError:" in openai_response_text or "OpenAI RateLimitError:" in openai_response_text or "OpenAI APIConnectionError:" in openai_response_text:
            error_messages.append(f"OpenAI: {openai_response_text}")

    # Claude
    if not claude_configured:
        error_messages.append("Anthropic Claude API key not configured in claude_client.py or as ENV variable.")
    else:
        claude_response_text = get_claude_response(prompt)
        if "Error:" in claude_response_text or "An unexpected error occurred with Anthropic:" in claude_response_text or "Anthropic AuthenticationError:" in claude_response_text or "Anthropic RateLimitError:" in claude_response_text or "Anthropic APIConnectionError:" in claude_response_text :
            error_messages.append(f"Claude: {claude_response_text}")

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
                           gemini_model=GEMINI_MODEL_NAME,
                           openai_model=OPENAI_MODEL_NAME,
                           claude_model=CLAUDE_MODEL_NAME)

if __name__ == '__main__':
    print("Starting Flask server for Multi-AI Aggregator (Gemini, OpenAI, Claude)...")
    print("Open your browser and go to http://127.0.0.1:5000/")
    print("Ensure API keys are set in 'gemini_client.py', 'openai_client.py' (or env var), and 'claude_client.py' (or env var).")
    app.run(debug=True)
