# Uday's AI Agents

This application, "Uday's AI Agents," provides a simple, dark-themed web interface to query Google Gemini, OpenAI (ChatGPT), and Anthropic Claude APIs with a single prompt. Users can also select from available Gemini models. It then displays the responses from each AI side-by-side in a clean, professional layout with a compact input header.

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
    You will need API keys for Google Gemini, OpenAI, and Anthropic Claude.

    *   **Google Gemini API Key:**
        *   Go to [Google AI Studio](https://aistudio.google.com/apikey).
        *   Sign in and create/use a project to generate your API key.
        *   Copy the key.

    *   **OpenAI API Key:**
        *   Go to [OpenAI Platform - API Keys](https://platform.openai.com/account/api-keys).
        *   Sign up/log in and create a new secret key.
        *   Copy the key.
        *   **Note on Free Tier (OpenAI):** Check OpenAI's current free tier/trial credit offerings.

    *   **Anthropic Claude API Key:**
        *   Go to the [Anthropic Console](https://console.anthropic.com/) and navigate to Account Settings -> API Keys (or similar path).
        *   Sign up/log in and generate a new API key.
        *   Copy the key.
        *   **Note on Free Tier (Anthropic):** Check your Anthropic account dashboard for any initial free credits. The API is generally pay-as-you-go. We recommend using a Haiku model (e.g., `claude-3-haiku-20240307`) for cost-effectiveness.

3.  **Create a Python Virtual Environment (Recommended):**
    ```bash
    python -m venv venv
    # On Windows: venv\Scripts\activate
    # On macOS/Linux: source venv/bin/activate
    ```

4.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Configure API Keys:**

    *   **Gemini API Key:**
        *   Edit `gemini_client.py`.
        *   Replace `'YOUR_API_KEY'` with your actual Gemini API key.

    *   **OpenAI API Key:**
        *   **Recommended:** Set an environment variable `OPENAI_API_KEY` to your OpenAI API key.
        *   **Alternative:** Edit `openai_client.py` and replace `'YOUR_OPENAI_API_KEY'` with your key.

    *   **Anthropic Claude API Key:**
        *   **Recommended:** Set an environment variable `ANTHROPIC_API_KEY` to your Anthropic API key.
        *   **Alternative:** Edit `claude_client.py` and replace `'YOUR_ANTHROPIC_API_KEY'` with your key.

    *   **Note on Security:** For local testing, these methods are acceptable. For production, use more secure secret management.

## Running the Application

1.  **Ensure your virtual environment is activated.**
2.  **Ensure all three API keys are configured as described above.**
3.  **Run the Flask web server:**
    ```bash
    python app.py
    ```

4.  **Open your web browser:**
    Navigate to `http://127.0.0.1:5000/`.

5.  **Use the App:**
    *   The application features a dark theme and a compact header for input.
    *   To check the status of your API key configurations, click the gear icon (⚙️) in the top-right. This will open a modal dialog.
    *   **Gemini Model Selection:** Below the main prompt area (within the input form section), you will find a dropdown menu labeled "Gemini Model:".
        *   This dropdown is populated dynamically with available Gemini models that support text generation, fetched when the page loads (if your Gemini API key is correctly configured).
        *   If there's an issue fetching the list (e.g., API key problem), an error message will appear next to the dropdown, and it may show a default model.
        *   Select your desired Gemini model from this list. The chosen model will be used for the next query you make.
        *   The header of the Gemini response box will display the name of the model that was used.
    *   Enter your common prompt in the text area. The "Ask my AIs" button is located to the right of this input area.
    *   Click "Ask my AIs".
    *   If there are errors (e.g., an API key issue for a specific service), they will appear as temporary toast notifications, typically at the bottom-right of the screen.
    *   Responses from Gemini (using the selected model), OpenAI, and Claude (if configured and successful) will be displayed in their respective static content boxes, each featuring a styled label.

## Project Structure

*   `app.py`: Flask web server.
*   `gemini_client.py`: Client for Google Gemini API (includes model listing).
*   `openai_client.py`: Client for OpenAI API.
*   `claude_client.py`: Client for Anthropic Claude API.
*   `templates/index.html`: HTML template for the UI.
*   `static/script.js`: JavaScript for UI interactions (modal, toast notifications).
*   `static/style.css`: CSS for styling the application.
*   `requirements.txt`: Python dependencies.
*   `README.md`: This file.
