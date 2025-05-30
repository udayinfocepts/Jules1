# Simple Gemini API Web Aggregator (Single AI)

This application provides a simple web interface to query the Google Gemini API. You can enter a text prompt, and the application will display the response from the Gemini model.

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

2.  **Obtain a Google Gemini API Key:**
    *   Go to [Google AI Studio](https://aistudio.google.com/apikey).
    *   Sign in with your Google account if prompted.
    *   Click on "Create API key in new project" or use an existing project to generate your API key.
    *   Copy the generated API key. You will need it in step 4.

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

5.  **Configure the API Key:**
    *   Open the `gemini_client.py` file in a text editor.
    *   Locate the line: `API_KEY = 'YOUR_API_KEY'`
    *   Replace `'YOUR_API_KEY'` with the actual API key you obtained from Google AI Studio.
    *   Save the `gemini_client.py` file.
    *   **Note:** For better security in production applications, consider using environment variables or a secure secrets management solution for your API key. For this simple research app, direct editing is used for simplicity.

## Running the Application

1.  **Ensure your virtual environment is activated (if you created one).**

2.  **Run the Flask web server:**
    ```bash
    python app.py
    ```

3.  **Open your web browser:**
    Navigate to `http://127.0.0.1:5000/` (or the URL shown in your terminal, usually localhost on port 5000).

4.  **Use the App:**
    *   If you see a warning about the API key not being configured, double-check step 5 in the "Setup Instructions".
    *   Enter your prompt in the text area.
    *   Click "Get Response".
    *   The response from Gemini will be displayed below the form.

## Project Structure

*   `app.py`: The Flask web server application.
*   `gemini_client.py`: Handles communication with the Google Gemini API.
*   `templates/index.html`: The HTML template for the web interface.
*   `requirements.txt`: Lists the Python dependencies.
*   `README.md`: This file.
