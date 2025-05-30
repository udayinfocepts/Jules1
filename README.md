# Multi-AI Aggregator (Gemini, OpenAI & Anthropic Claude)

This application provides a simple web interface to query Google Gemini, OpenAI (ChatGPT), and Anthropic Claude APIs with a single prompt. It then displays the responses from each AI side-by-side.

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
    *   The page will show the configuration status for all three API keys.
    *   Enter your common prompt.
    *   Click "Get Responses from AIs".
    *   Responses from Gemini, OpenAI, and Claude (if configured and successful) will be displayed.

## Project Structure

*   `app.py`: Flask web server.
*   `gemini_client.py`: Client for Google Gemini API.
*   `openai_client.py`: Client for OpenAI API.
*   `claude_client.py`: Client for Anthropic Claude API.
*   `templates/index.html`: HTML template for the UI.
*   `requirements.txt`: Python dependencies.
*   `README.md`: This file.
