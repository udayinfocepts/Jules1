document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('apiStatusModal');
    const openModalButton = document.getElementById('openApiStatusModal');
    const closeModalButton = document.getElementsByClassName('close-modal-button')[0];

    if (openModalButton) {
        openModalButton.onclick = function() {
            if (modal) modal.style.display = 'block';
        }
    }

    if (closeModalButton) {
        closeModalButton.onclick = function() {
            if (modal) modal.style.display = 'none';
        }
    }

    // Optional: Close modal if user clicks outside of the modal content
    window.onclick = function(event) {
        if (event.target == modal) {
            if (modal) modal.style.display = 'none';
        }
    }
});

// --- Toast Notification Functionality ---
function showToast(message, type = 'error', duration = 5000) {
    const container = document.getElementById('toastContainer');
    if (!container) {
        console.error('Toast container not found!');
        return;
    }

    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`; // e.g., toast-error, toast-success
    toast.textContent = message;

    container.appendChild(toast);

    // Trigger reflow for animation
    toast.offsetHeight;

    // Add class to make it visible and animate
    toast.classList.add('show');

    // Remove toast after specified duration
    setTimeout(() => {
        toast.classList.remove('show');
        // Remove the element from DOM after animation
        setTimeout(() => {
            if (toast.parentNode === container) { // Check if still child before removing
                container.removeChild(toast);
            }
        }, 500); // Matches CSS transition time
    }, duration);
}

// --- Gemini Model Selector Sync ---
document.addEventListener('DOMContentLoaded', function() {
    const visualGeminiSelect = document.getElementById('gemini_model_select_visual');
    const hiddenGeminiInput = document.getElementById('gemini_model_select_hidden');

    if (visualGeminiSelect && hiddenGeminiInput) {
        // Initialize hidden field with the current value of the visual select
        // (which should be correctly pre-selected by Jinja via current_gemini_model)
        hiddenGeminiInput.value = visualGeminiSelect.value;

        // Add event listener for changes on the visual select
        visualGeminiSelect.addEventListener('change', function() {
            hiddenGeminiInput.value = this.value;
        });
    }
});

// --- History Sidebar UI Management ---
document.addEventListener('DOMContentLoaded', function() {
    const historySidebar = document.getElementById('historySidebar');
    const openHistorySidebarButton = document.getElementById('openHistorySidebar');
    const closeHistorySidebarButton = document.getElementById('closeHistorySidebar');
    const historyListUl = document.getElementById('historyList');
    const clearHistoryButton = document.getElementById('clearHistoryButton');

    // --- Elements for displaying loaded history ---
    const mainPromptTextarea = document.getElementById('prompt');
    // Assuming response <p> tags are identifiable. If not, we need specific IDs or classes.
    // Let's assume the <p> tags holding responses are the direct <p> children of their respective .response-area,
    // and are NOT the .error-text or .placeholder-text paragraphs.
    // This might need refinement if HTML structure for responses is more complex.
    // const geminiResponseP = document.querySelector('#geminiResponseAreaContainer .response-area > p:not(.error-text):not(.placeholder-text)'); // Needs IDs on response areas
    // const openaiResponseP = document.querySelector('#openaiResponseAreaContainer .response-area > p:not(.error-text):not(.placeholder-text)');
    // const claudeResponseP = document.querySelector('#claudeResponseAreaContainer .response-area > p:not(.error-text):not(.placeholder-text)');

    // Placeholders and error <p> tags (to hide/show them)
    // const geminiPlaceholderP = document.querySelector('#geminiResponseAreaContainer .response-area > p.placeholder-text');
    // const geminiErrorP = document.querySelector('#geminiResponseAreaContainer .response-area > p.error-text');
    // ... similar for openai and claude ...

    // Model selectors (visual and hidden)
    const visualGeminiSelect = document.getElementById('gemini_model_select_visual');
    const hiddenGeminiInput = document.getElementById('gemini_model_select_hidden');
    const visualOpenAISelect = document.getElementById('openai_model_select_visual');
    const hiddenOpenAIInput = document.getElementById('openai_model_select_hidden');
    const visualClaudeSelect = document.getElementById('claude_model_select_visual');
    const hiddenClaudeInput = document.getElementById('claude_model_select_hidden');

    // These constants would need to be passed from app.py if used as JS fallbacks here.
    // For now, relying on qnaSet.xxx_model being present or visualSelect.value.
    // const DEFAULT_GEMINI_MODEL = "{{ DEFAULT_GEMINI_MODEL }}"; // Example, would need proper injection
    // const DEFAULT_OPENAI_MODEL = "{{ DEFAULT_OPENAI_MODEL }}";
    // const DEFAULT_CLAUDE_MODEL = "{{ DEFAULT_CLAUDE_MODEL }}";


    let currentHistory = []; // In-memory copy of history for easier access

    function renderHistorySidebar() {
        if (!historyListUl) return;
        historyListUl.innerHTML = ''; // Clear existing items
        currentHistory = loadHistory(); // Load from Local Storage

        if (currentHistory.length === 0) {
            const li = document.createElement('li');
            li.textContent = 'No history yet.';
            li.style.fontStyle = 'italic';
            li.style.color = '#777777';
            historyListUl.appendChild(li);
            return;
        }

        currentHistory.forEach((qnaSet, index) => {
            const li = document.createElement('li');
            li.dataset.historyIndex = index; // Store index to retrieve full data

            const promptSnippet = document.createElement('span');
            promptSnippet.className = 'history-prompt-snippet';
            promptSnippet.textContent = qnaSet.prompt.substring(0, 30) + (qnaSet.prompt.length > 30 ? '...' : '');

            const timestamp = document.createElement('span');
            timestamp.className = 'history-timestamp';
            timestamp.textContent = new Date(qnaSet.timestamp).toLocaleString();

            li.appendChild(promptSnippet);
            li.appendChild(timestamp);

            li.addEventListener('click', function() {
                loadQASetIntoUI(parseInt(this.dataset.historyIndex));
                // Optionally close sidebar:
                // if (historySidebar) historySidebar.classList.remove('open');

                // Highlight active item
                document.querySelectorAll('#historyList li').forEach(item => item.classList.remove('active-history-item'));
                this.classList.add('active-history-item');
            });
            historyListUl.appendChild(li);
        });
    }

    function displayResponseInArea(responseAreaId, responseText) {
        const responseArea = document.getElementById(responseAreaId);
        if (!responseArea) { console.warn("Response area not found:", responseAreaId); return; }

        const pResponse = responseArea.querySelector('p:not(.placeholder-text):not(.error-text)');
        const pPlaceholder = responseArea.querySelector('p.placeholder-text');
        const pError = responseArea.querySelector('p.error-text');

        // Clear previous state
        if (pResponse) { pResponse.textContent = ''; pResponse.classList.remove('error-text'); } // Ensure error-text is removed if it was added
        if (pPlaceholder) pPlaceholder.style.display = 'none';
        if (pError) { pError.textContent = ''; pError.style.display = 'none'; }

        const isErrorResponse = typeof responseText === 'string' && (responseText.startsWith("Error:") || responseText.includes("An error occurred") || responseText.includes("API key not configured") || responseText.includes("Auth Error"));

        if (isErrorResponse) {
            if (pError) {
                pError.textContent = responseText;
                pError.style.display = 'block';
            } else if (pResponse) { // Fallback if dedicated error <p> not found
                pResponse.textContent = responseText;
                pResponse.classList.add('error-text');
            }
        } else if (responseText && typeof responseText === 'string') {
            if (pResponse) {
                pResponse.textContent = responseText;
            } else { console.warn("Main response <p> tag not found in", responseAreaId); }
        } else { // No response and not an error (e.g. AI was not called or responseText is null/undefined)
            if (pPlaceholder) {
                pPlaceholder.style.display = 'block';
            } else { console.warn("Placeholder <p> tag not found in", responseAreaId); }
        }
    }


    function loadQASetIntoUI(index) {
        if (index < 0 || index >= currentHistory.length) return;
        const qnaSet = currentHistory[index];

        if (mainPromptTextarea) mainPromptTextarea.value = qnaSet.prompt;

        displayResponseInArea('geminiResponseArea', qnaSet.gemini_response);
        displayResponseInArea('openaiResponseArea', qnaSet.openai_response);
        displayResponseInArea('claudeResponseArea', qnaSet.claude_response);

        // Update model selectors
        if (visualGeminiSelect && hiddenGeminiInput) {
            visualGeminiSelect.value = qnaSet.gemini_model || visualGeminiSelect.options[0].value; // Fallback to first option
            hiddenGeminiInput.value = visualGeminiSelect.value;
        }
        if (visualOpenAISelect && hiddenOpenAIInput) {
            visualOpenAISelect.value = qnaSet.openai_model || visualOpenAISelect.options[0].value;
            hiddenOpenAIInput.value = visualOpenAISelect.value;
        }
        if (visualClaudeSelect && hiddenClaudeInput) {
            visualClaudeSelect.value = qnaSet.claude_model || visualClaudeSelect.options[0].value;
            hiddenClaudeInput.value = visualClaudeSelect.value;
        }

        updateResponseHeaderModelName('geminiResponseArea', qnaSet.gemini_model, visualGeminiSelect);
        updateResponseHeaderModelName('openaiResponseArea', qnaSet.openai_model, visualOpenAISelect);
        updateResponseHeaderModelName('claudeResponseArea', qnaSet.claude_model, visualClaudeSelect);
    }

    function updateResponseHeaderModelName(responseAreaId, modelId, visualSelectElement) {
        const responseArea = document.getElementById(responseAreaId);
        if (!responseArea) return;
        const h3 = responseArea.querySelector('.response-header > h3');
        if (!h3) return;

        const aiLabelSpan = h3.querySelector('.ai-label');
        let displayModelId = "";

        if (modelId) {
            displayModelId = modelId.split('/').pop(); // e.g., gemini-1.5-flash-latest
            if (responseAreaId === 'claudeResponseArea') {
                displayModelId = displayModelId.replace('claude-3-haiku-', 'c3-haiku-');
            }
        } else if (visualSelectElement && visualSelectElement.options.length > 0) {
            // Fallback to current selected display text in the dropdown if modelId is missing in history
            // This is a bit more complex as option text includes display name and ID.
            // Simplification: just show nothing or a generic placeholder if modelId is truly missing.
            // For now, let's assume modelId will usually be there.
            // If not, the H3 will just show " ( )" if modelId is null/undefined.
        }


        if (aiLabelSpan && aiLabelSpan.nextSibling && aiLabelSpan.nextSibling.nodeType === Node.TEXT_NODE) {
            aiLabelSpan.nextSibling.textContent = ` (${displayModelId})`;
        } else if (aiLabelSpan) { // If no text node, create one (less likely with current HTML)
             const textNode = document.createTextNode(` (${displayModelId})`);
             h3.appendChild(textNode);
        }
    }


    // Sidebar Toggle Logic
    if (openHistorySidebarButton && historySidebar) {
        openHistorySidebarButton.onclick = function() {
            historySidebar.classList.add('open');
            renderHistorySidebar(); // Re-render history every time it's opened, in case of external changes
        }
    }
    if (closeHistorySidebarButton && historySidebar) {
        closeHistorySidebarButton.onclick = function() {
            historySidebar.classList.remove('open');
        }
    }

    // Clear History Button Logic
    if (clearHistoryButton) {
        clearHistoryButton.onclick = function() {
            if (confirm("Are you sure you want to clear all Q&A history? This cannot be undone.")) {
                clearHistory(); // Clears Local Storage
                renderHistorySidebar(); // Re-renders the (now empty) sidebar
                showToast("History cleared.", "success");
            }
        }
    }

    // Initial population of history sidebar (if it's not initially open, this could be deferred)
    // renderHistorySidebar(); // Call it if sidebar might be open on load, or on first open.
    // For now, let's populate it when the sidebar is opened.
});

// --- Q&A History Management ---
const UDAYS_AI_AGENTS_HISTORY_KEY = 'udaysAiAgentsHistory';
const MAX_HISTORY_ITEMS = 50; // Optional: Limit the number of history items

/**
 * Loads the Q&A history from Local Storage.
 * @returns {Array} An array of Q&A set objects, or an empty array if none exists or an error occurs.
 */
function loadHistory() {
    try {
        const historyJson = localStorage.getItem(UDAYS_AI_AGENTS_HISTORY_KEY);
        if (historyJson) {
            const history = JSON.parse(historyJson);
            // Basic validation if it's an array
            return Array.isArray(history) ? history : [];
        }
        return [];
    } catch (error) {
        console.error("Error loading history from Local Storage:", error);
        return []; // Return empty array on error
    }
}

/**
 * Saves a new Q&A set to the history in Local Storage.
 * @param {object} qnaSet - The Q&A set object to save.
 *                          Expected structure: { prompt: string, gemini_response: string, gemini_model: string,
 *                                                openai_response: string, openai_model: string,
 *                                                claude_response: string, claude_model: string,
 *                                                timestamp: string }
 */
function saveQASet(qnaSet) {
    if (!qnaSet || typeof qnaSet.prompt === 'undefined') {
        console.error("Invalid Q&A set provided to saveQASet:", qnaSet);
        return;
    }
    try {
        let history = loadHistory();

        // Add the new set to the beginning of the history (most recent first)
        history.unshift(qnaSet);

        // Optional: Limit history size
        if (history.length > MAX_HISTORY_ITEMS) {
            history = history.slice(0, MAX_HISTORY_ITEMS); // Keep only the newest MAX_HISTORY_ITEMS
        }

        localStorage.setItem(UDAYS_AI_AGENTS_HISTORY_KEY, JSON.stringify(history));
    } catch (error) {
        console.error("Error saving history to Local Storage:", error);
        // Potentially show a toast error to the user if storage is full
        if (error.name === 'QuotaExceededError') {
            showToast('History storage limit reached. Oldest items may not be saved.', 'error');
        }
    }
}

/**
 * Clears all Q&A history from Local Storage.
 */
function clearHistory() {
    try {
        localStorage.removeItem(UDAYS_AI_AGENTS_HISTORY_KEY);
        console.log("Q&A history cleared from Local Storage.");
        // Later, this will also need to update the UI (e.g., clear the sidebar)
    } catch (error) {
        console.error("Error clearing history from Local Storage:", error);
    }
}

// Example of how qnaSet might be structured (for documentation/testing purposes):
/*
const exampleQnaSet = {
    id: new Date().getTime(), // Or a UUID, for unique identification if needed for UI keys
    prompt: "What is the weather like?",
    gemini_response: "Gemini says it's sunny.",
    gemini_model: "models/gemini-1.5-flash-latest",
    openai_response: "OpenAI says it's partly cloudy.",
    openai_model: "gpt-3.5-turbo",
    claude_response: "Claude says rain is expected.",
    claude_model: "claude-3-haiku-20240307",
    timestamp: new Date().toISOString()
};
*/

// --- Claude Model Selector Sync ---
document.addEventListener('DOMContentLoaded', function() {
    const visualClaudeSelect = document.getElementById('claude_model_select_visual');
    const hiddenClaudeInput = document.getElementById('claude_model_select_hidden');

    if (visualClaudeSelect && hiddenClaudeInput) {
        // Initialize hidden field with the current value of the visual select
        // (which should be correctly pre-selected by Jinja via current_claude_model)
        hiddenClaudeInput.value = visualClaudeSelect.value;

        // Add event listener for changes on the visual select
        visualClaudeSelect.addEventListener('change', function() {
            hiddenClaudeInput.value = this.value;
        });
    }
});

// --- OpenAI Model Selector Sync ---
document.addEventListener('DOMContentLoaded', function() {
    const visualOpenAISelect = document.getElementById('openai_model_select_visual');
    const hiddenOpenAIInput = document.getElementById('openai_model_select_hidden');

    if (visualOpenAISelect && hiddenOpenAIInput) {
        // Initialize hidden field with the current value of the visual select
        // (which should be correctly pre-selected by Jinja via current_openai_model)
        hiddenOpenAIInput.value = visualOpenAISelect.value;

        // Add event listener for changes on the visual select
        visualOpenAISelect.addEventListener('change', function() {
            hiddenOpenAIInput.value = this.value;
        });
    }
});
