# Multi-AI Aggregator (Gemini & OpenAI)

This application provides a simple web interface to query both the Google Gemini API and the OpenAI (ChatGPT) API with a single prompt. It then displays the responses from each AI side-by-side.

## Prerequisites

*   Python 3.7+
*   Access to the internet

## Setup Instructions

1.  **Clone the Repository (if you haven't already):**
    ```bash
    # If you're working with this project locally from a git clone
    # git clone <repository_url>
    # cd <repository_directory>
    ```

2.  **Obtain API Keys:**
    You will need API keys for both Google Gemini and OpenAI.

    *   **Google Gemini API Key:**
        *   Go to [Google AI Studio](https://aistudio.google.com/apikey).
        *   Sign in with your Google account if prompted.
        *   Click on "Create API key in new project" or use an existing project.
        *   Copy the generated API key.

    *   **OpenAI API Key:**
        *   Go to [OpenAI Platform - API Keys](https://platform.openai.com/account/api-keys).
        *   Sign up or log in to your OpenAI account.
        *   Navigate to the API keys section and create a new secret key.
        *   Copy the generated API key.
        *   **Note on Free Tier:** Check OpenAI's current free tier offerings when you sign up. New accounts often receive free credits suitable for testing with models like `gpt-3.5-turbo`.

3.  **Create a Python Virtual Environment (Recommended):**
    ```bash
    python -m venv venv
    # On Windows
    # venv\Scripts\activate
    # On macOS/Linux
    # source venv/bin/activate
    ```

4.  **Install Dependencies:**
    Install the required Python packages using the `requirements.txt` file:
    ```bash
    pip install -r requirements.txt
    ```

5.  **Configure API Keys:**

    *   **Gemini API Key:**
        *   Open the `gemini_client.py` file in a text editor.
        *   Locate the line: `API_KEY = 'YOUR_API_KEY'`
        *   Replace `'YOUR_API_KEY'` with your actual Gemini API key.
        *   Save the `gemini_client.py` file.

    *   **OpenAI API Key:**
        *   **Recommended Method (Environment Variable):**
            Set an environment variable named `OPENAI_API_KEY` to your OpenAI API key. The `openai_client.py` script will automatically use it.
            ```bash
            # On macOS/Linux
            # export OPENAI_API_KEY='your_openai_api_key_here' 
            # (add this to your .bashrc or .zshrc for persistence)

            # On Windows (PowerShell)
            # $Env:OPENAI_API_KEY='your_openai_api_key_here' 
            # (add to your PowerShell profile for persistence)
            ```
        *   **Alternative Method (Edit `openai_client.py`):**
            If you don't set the environment variable, you can directly edit `openai_client.py`:
            *   Open `openai_client.py`.
            *   Locate the line: `OPENAI_API_KEY_DIRECT = 'YOUR_OPENAI_API_KEY'`
            *   Replace `'YOUR_OPENAI_API_KEY'` with your actual OpenAI API key.
            *   Save the `openai_client.py` file.

    *   **Note on Security:** For simple local testing, editing the files or using environment variables is acceptable. For production, use more robust secret management.

## Running the Application

1.  **Ensure your virtual environment is activated (if you created one).**
2.  **Ensure API keys are configured as described above.**
3.  **Run the Flask web server:**
    ```bash
    python app.py
    ```

4.  **Open your web browser:**
    Navigate to `http://127.0.0.1:5000/` (or the URL shown in your terminal).

5.  **Use the App:**
    *   The page will show the configuration status for both Gemini and OpenAI API keys.
    *   Enter your common prompt in the text area.
    *   Click "Get Responses from AIs".
    *   Responses from both Gemini and OpenAI (if configured and successful) will be displayed.

## Project Structure

*   `app.py`: The Flask web server application.
*   `gemini_client.py`: Handles communication with the Google Gemini API.
*   `openai_client.py`: Handles communication with the OpenAI API.
*   `templates/index.html`: The HTML template for the web interface.
*   `requirements.txt`: Lists the Python dependencies.
*   `README.md`: This file.
