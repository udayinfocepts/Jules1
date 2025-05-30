from flask import Flask, render_template, request
from gemini_client import get_gemini_response, API_KEY # Import API_KEY to check configuration

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    api_key_configured = API_KEY != 'YOUR_API_KEY'
    return render_template('index.html', api_key_not_configured=not api_key_configured)

@app.route('/get_response', methods=['POST'])
def get_response_route():
    api_key_configured = API_KEY != 'YOUR_API_KEY'
    if not api_key_configured:
        return render_template('index.html', 
                               error="API Key not configured on the server. Please ask the administrator to set it up.",
                               api_key_not_configured=True)

    prompt = request.form.get('prompt')
    if not prompt:
        return render_template('index.html', 
                               error="Prompt cannot be empty.", 
                               prompt_text=prompt,
                               api_key_not_configured=False)

    # Call the function from gemini_client.py
    gemini_response = get_gemini_response(prompt)

    # Check if the response indicates an API key configuration error from the client script itself
    if "Error: API_KEY has not been configured" in gemini_response:
         return render_template('index.html',
                               error=gemini_response, # Show the specific error from gemini_client
                               prompt_text=prompt,
                               api_key_not_configured=True) # Treat as not configured
    elif "An error occurred:" in gemini_response: # General error from gemini_client
        return render_template('index.html',
                               error=gemini_response,
                               prompt_text=prompt,
                               api_key_not_configured=False)
    
    return render_template('index.html', 
                           response=gemini_response, 
                           prompt_text=prompt,
                           api_key_not_configured=False)

if __name__ == '__main__':
    # Before running, ensure:
    # 1. You have installed Flask: pip install Flask
    # 2. You have configured your API_KEY in gemini_client.py
    print("Starting Flask server...")
    print("Open your browser and go to http://127.0.0.1:5000/")
    print("Make sure 'gemini_client.py' is in the same directory and API_KEY is set.")
    app.run(debug=True) # debug=True is helpful for development
