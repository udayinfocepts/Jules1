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
        hiddenGeminiInput.value = visualGeminiSelect.value;
        visualGeminiSelect.addEventListener('change', function() {
            hiddenGeminiInput.value = this.value;
        });
    }
});

// --- OpenAI Model Selector Sync ---
document.addEventListener('DOMContentLoaded', function() {
    const visualOpenAISelect = document.getElementById('openai_model_select_visual');
    const hiddenOpenAIInput = document.getElementById('openai_model_select_hidden');

    if (visualOpenAISelect && hiddenOpenAIInput) {
        hiddenOpenAIInput.value = visualOpenAISelect.value;
        visualOpenAISelect.addEventListener('change', function() {
            hiddenOpenAIInput.value = this.value;
        });
    }
});

// --- Claude Model Selector Sync ---
document.addEventListener('DOMContentLoaded', function() {
    const visualClaudeSelect = document.getElementById('claude_model_select_visual');
    const hiddenClaudeInput = document.getElementById('claude_model_select_hidden');

    if (visualClaudeSelect && hiddenClaudeInput) {
        hiddenClaudeInput.value = visualClaudeSelect.value;
        visualClaudeSelect.addEventListener('change', function() {
            hiddenClaudeInput.value = this.value;
        });
    }
});


// --- History Sidebar UI Management ---
const SIDEBAR_STATE_KEY = 'udaysAiAgentsSidebarState';

document.addEventListener('DOMContentLoaded', function() {
    let currentHistory = []; // Correctly scoped for functions within this DOMContentLoaded

    const historySidebar = document.getElementById('historySidebar');
    const openHistorySidebarButton = document.getElementById('openHistorySidebar');
    const closeHistorySidebarButton = document.getElementById('closeHistorySidebar');
    const historyListUl = document.getElementById('historyList');
    const clearHistoryButton = document.getElementById('clearHistoryButton');

    // Load and Apply Initial Sidebar State
    if (historySidebar) {
        const savedSidebarState = localStorage.getItem(SIDEBAR_STATE_KEY);
        console.log('Loaded sidebar state:', savedSidebarState);
        if (savedSidebarState === 'open') {
            console.log('Applying open state from Local Storage.');
            historySidebar.classList.add('open');
            if (typeof renderHistorySidebar === 'function') {
                console.log('Calling renderHistorySidebar from DOMContentLoaded due to saved open state.');
                renderHistorySidebar(); 
            }
        } else {
            console.log('Applying closed state or default.');
            historySidebar.classList.remove('open'); 
        }
    }

    const mainPromptTextarea = document.getElementById('prompt');
    const visualGeminiSelect = document.getElementById('gemini_model_select_visual');
    const hiddenGeminiInput = document.getElementById('gemini_model_select_hidden');
    const visualOpenAISelect = document.getElementById('openai_model_select_visual');
    const hiddenOpenAIInput = document.getElementById('openai_model_select_hidden');
    const visualClaudeSelect = document.getElementById('claude_model_select_visual');
    const hiddenClaudeInput = document.getElementById('claude_model_select_hidden');

    function renderHistorySidebar() {
        console.log('renderHistorySidebar called.');
        if (!historyListUl) return;
        historyListUl.innerHTML = '';
        currentHistory = loadHistory(); // Assigns to the scoped currentHistory
        console.log('History data for rendering:', currentHistory);

        if (currentHistory.length === 0) {
            console.log('Rendering sidebar with "No history yet."');
            const li = document.createElement('li');
            li.textContent = 'No history yet.';
            li.style.fontStyle = 'italic';
            li.style.color = '#777777';
            historyListUl.appendChild(li);
            return;
        }

        currentHistory.forEach((qnaSet, index) => {
            const li = document.createElement('li');
            li.dataset.historyIndex = index;
            console.log('Rendering history item:', qnaSet);

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
                document.querySelectorAll('#historyList li').forEach(item => item.classList.remove('active-history-item'));
                this.classList.add('active-history-item');
            });
            historyListUl.appendChild(li);
        });
    }

function displayResponseInArea(responseAreaId, responseText) {
    const responseArea = document.getElementById(responseAreaId);
    if (!responseArea) {
        console.error(`Response area with ID '${responseAreaId}' not found.`);
        return;
    }

    const pResponseContent = responseArea.querySelector('.ai-response-content');
    const pErrorText = responseArea.querySelector('.ai-response-error-text'); // Specific class for AI errors
    const pPlaceholder = responseArea.querySelector('.placeholder-text');

    // Ensure all elements are found before proceeding
    if (!pResponseContent || !pErrorText || !pPlaceholder) {
        console.error(`One or more required p tags not found in '${responseAreaId}'. Structure: .ai-response-content, .ai-response-error-text, .placeholder-text`);
        return;
    }

    // Hide all paragraphs initially
    pResponseContent.classList.add('hidden');
    pErrorText.classList.add('hidden');
    pPlaceholder.classList.add('hidden');

    // Clear previous content to be safe
    pResponseContent.textContent = '';
    pErrorText.textContent = '';
    // Placeholder text is static, so no need to clear/reset its content unless it changes dynamically

    if (responseText && typeof responseText === 'string' && responseText.trim() !== "") {
        // Heuristic to check if the responseText is an error message from our clients
        // (These are the patterns used in the client .py files)
        const isError = responseText.startsWith("Error:") || 
                        responseText.includes("An error occurred") || 
                        responseText.includes("API key not configured") || 
                        responseText.includes("No model specified") ||
                        responseText.includes("AuthenticationError") ||
                        responseText.includes("RateLimitError") ||
                        responseText.includes("APIConnectionError") ||
                        responseText.includes("NotFoundError"); // Added from OpenAI client

        if (isError) {
            pErrorText.textContent = responseText;
            pErrorText.classList.remove('hidden');
        } else {
            pResponseContent.textContent = responseText;
            pResponseContent.classList.remove('hidden');
        }
    } else {
        // If responseText is null, undefined, or empty string, show placeholder
        pPlaceholder.textContent = `Response from ${responseAreaId.replace('ResponseArea','')} will appear here once a prompt is submitted.`; // Ensure placeholder text is fresh
        pPlaceholder.classList.remove('hidden');
    }
}

    function loadQASetIntoUI(index) {
        console.log('loadQASetIntoUI called with index:', index); // DEBUG
        if (index < 0 || index >= currentHistory.length) {
            console.error('Invalid index for loadQASetIntoUI:', index); // DEBUG
            return;
        }
        const qnaSet = currentHistory[index];
        console.log('Loading Q&A set from history:', qnaSet); // DEBUG

        if (mainPromptTextarea) mainPromptTextarea.value = qnaSet.prompt;
        
        displayResponseInArea('geminiResponseArea', qnaSet.gemini_response);
        displayResponseInArea('openaiResponseArea', qnaSet.openai_response);
        displayResponseInArea('claudeResponseArea', qnaSet.claude_response);

        if (visualGeminiSelect && hiddenGeminiInput) {
            visualGeminiSelect.value = qnaSet.gemini_model || visualGeminiSelect.options[0].value;
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
            displayModelId = modelId.split('/').pop();
            if (responseAreaId === 'claudeResponseArea') { 
                displayModelId = displayModelId.replace('claude-3-haiku-', 'c3-haiku-');
            }
        } // No complex fallback to visualSelectElement.options[0].text needed here for now
        
        if (aiLabelSpan && aiLabelSpan.nextSibling && aiLabelSpan.nextSibling.nodeType === Node.TEXT_NODE) {
            aiLabelSpan.nextSibling.textContent = ` (${displayModelId})`;
        } else if (aiLabelSpan && !aiLabelSpan.nextSibling) { // If text node doesn't exist, create it
             const textNode = document.createTextNode(` (${displayModelId})`);
             h3.appendChild(textNode);
        }
    }

    // Sidebar Toggle Logic
    if (openHistorySidebarButton && historySidebar) {
        openHistorySidebarButton.onclick = function() {
            console.log('Open sidebar button clicked.');
            historySidebar.classList.add('open');
            localStorage.setItem(SIDEBAR_STATE_KEY, 'open');
            console.log('Saved sidebar state: open');
            if (typeof renderHistorySidebar === 'function') { 
                renderHistorySidebar();
            }
        }
    }
    if (closeHistorySidebarButton && historySidebar) {
        closeHistorySidebarButton.onclick = function() {
            console.log('Close sidebar button clicked.');
            historySidebar.classList.remove('open');
            localStorage.setItem(SIDEBAR_STATE_KEY, 'closed');
            console.log('Saved sidebar state: closed');
        }
    }

    // Clear History Button Logic
    if (clearHistoryButton) {
        clearHistoryButton.onclick = function() {
            if (confirm("Are you sure you want to clear all Q&A history? This cannot be undone.")) {
                clearHistory(); 
                renderHistorySidebar(); 
                showToast("History cleared.", "success");
            }
        }
    }
});

// --- Q&A History Management --- (Core functions: loadHistory, saveQASet, clearHistory)
const UDAYS_AI_AGENTS_HISTORY_KEY = 'udaysAiAgentsHistory';
const MAX_HISTORY_ITEMS = 50; 

function loadHistory() {
    console.log('loadHistory called.'); 
    let historyToReturn = [];
    try {
        const historyJson = localStorage.getItem(UDAYS_AI_AGENTS_HISTORY_KEY);
        console.log('Loaded history JSON from Local Storage:', historyJson); 
        if (historyJson) {
            const parsedHistory = JSON.parse(historyJson);
            console.log('Parsed history:', parsedHistory); 
            if (Array.isArray(parsedHistory)) {
                historyToReturn = parsedHistory;
            }
        } else {
            console.log('No history found in Local Storage or historyJson is null/empty.'); 
        }
    } catch (error) {
        console.error('Failed to parse history JSON:', error); 
    }
    console.log('loadHistory returning:', historyToReturn); 
    return historyToReturn;
}

function saveQASet(qnaSet) {
    console.log('saveQASet called with:', qnaSet); 
    if (!qnaSet || typeof qnaSet.prompt === 'undefined') {
        console.error("Invalid Q&A set provided to saveQASet:", qnaSet);
        return;
    }
    try {
        let history = loadHistory();
        history.unshift(qnaSet); 
        if (history.length > MAX_HISTORY_ITEMS) {
            history = history.slice(0, MAX_HISTORY_ITEMS); 
        }
        console.log('Saving to Local Storage:', JSON.stringify(history)); 
        localStorage.setItem(UDAYS_AI_AGENTS_HISTORY_KEY, JSON.stringify(history));
    } catch (error) {
        console.error('Error in saveQASet:', error); 
        if (error.name === 'QuotaExceededError') {
            showToast('History storage limit reached. Oldest items may not be saved.', 'error');
        }
    }
}

function clearHistory() {
    try {
        localStorage.removeItem(UDAYS_AI_AGENTS_HISTORY_KEY);
        console.log("Q&A history cleared from Local Storage.");
    } catch (error) {
        console.error("Error clearing history from Local Storage:", error);
    }
}

/* Example QnaSet Structure (already present) */
// ...
