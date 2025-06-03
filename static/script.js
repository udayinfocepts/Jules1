// static/script.js

// --- Globally Scoped Variables ---
const UDAYS_AI_AGENTS_HISTORY_KEY = 'udaysAiAgentsHistory';
const MAX_HISTORY_ITEMS = 50;
const SIDEBAR_STATE_KEY = 'udaysAiAgentsSidebarState';
let currentHistory = []; // Shared history array
let recentlyDeletedSet = null; // Will store { item: qnaSet, originalIndex: index }
let undoDeleteTimer = null;    // To manage the undo timeout

// DOM Element Variables - to be initialized in DOMContentLoaded
let historySidebar = null;
let openHistorySidebarButton = null;
let closeHistorySidebarButton = null;
let historyListUl = null;
let clearHistoryButton = null;
let mainPromptTextarea = null;
// Add all visual and hidden select input elements here
let visualGeminiSelect = null, hiddenGeminiInput = null;
let visualOpenAISelect = null, hiddenOpenAIInput = null;
let visualClaudeSelect = null, hiddenClaudeInput = null;
let apiStatusModal = null, openApiStatusModalButton = null, closeModalButton = null; // For modal


// --- Core History Data Functions (Global) ---
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
            if (typeof showToast === 'function') { // Ensure showToast is available
                showToast('History storage limit reached. Oldest items may not be saved.', 'error');
            }
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

// --- Toast Notification Functionality (Global) ---
function showToast(message, type = 'error', duration = 5000, action = null) {
    // --- BEGIN ADDED LOGS ---
    console.log('showToast function called.');
    console.log('Message:', message, 'Type:', type, 'Duration:', duration);
    console.log('Received Action Object:', action); // Log the entire action object

    if (action) {
        console.log('Action object exists. action.text:', action.text, '| typeof action.callback:', typeof action.callback);
    } else {
        console.log('No action object was provided.');
    }
    // --- END ADDED LOGS ---

    const container = document.getElementById('toastContainer');
    if (!container) {
        console.error('Toast container not found!');
        return;
    }

    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;

    const messageSpan = document.createElement('span');
    messageSpan.textContent = message;
    toast.appendChild(messageSpan);

    let toastTimeoutId = null;

    // Condition to check if action link should be created
    if (action && typeof action.text === 'string' && typeof action.callback === 'function') {
        console.log('Condition MET: Creating action link for toast.'); // <-- ADD THIS LOG
        const actionLink = document.createElement('a');
        actionLink.href = '#';
        actionLink.className = 'toast-action-link';
        actionLink.textContent = action.text;

        actionLink.onclick = function(e) {
            e.preventDefault();
            if (toastTimeoutId) {
                clearTimeout(toastTimeoutId);
            }
            action.callback();
            toast.classList.remove('show');
            setTimeout(() => {
                if (toast.parentNode === container) {
                    container.removeChild(toast);
                }
            }, 500);
        };

        const spacer = document.createTextNode(' \u00A0 ');
        toast.appendChild(spacer);
        toast.appendChild(actionLink);
    } else {
        // --- ADDED LOG ---
        console.log('Condition NOT MET for creating action link.');
        // --- END ADDED LOG ---
    }

    container.appendChild(toast);
    // Trigger reflow for animation
    toast.offsetHeight;

    // Add class to make it visible and animate
    toast.classList.add('show');

    // Store the timeout ID when setting the auto-dismiss timeout
    toastTimeoutId = setTimeout(() => { // Assign to the previously declared toastTimeoutId
        toast.classList.remove('show');
        // Remove the element from DOM after animation
        setTimeout(() => {
            if (toast.parentNode === container) { // Check if still child before removing
                container.removeChild(toast);
            }
        }, 500); // Matches CSS transition time
    }, duration);
}

// --- UI Update Functions (Global, will use global DOM element vars) ---
function displayResponseInArea(responseAreaId, responseText) {
    const responseArea = document.getElementById(responseAreaId);
    if (!responseArea) {
        console.error(`Response area with ID '${responseAreaId}' not found.`);
        return;
    }
    const pResponseContent = responseArea.querySelector('.ai-response-content');
    const pErrorText = responseArea.querySelector('.ai-response-error-text');
    const pPlaceholder = responseArea.querySelector('.placeholder-text');

    if (!pResponseContent || !pErrorText || !pPlaceholder) {
        console.error(`One or more required p tags not found in '${responseAreaId}'. Structure: .ai-response-content, .ai-response-error-text, .placeholder-text`);
        return;
    }

    pResponseContent.classList.add('hidden');
    pErrorText.classList.add('hidden');
    pPlaceholder.classList.add('hidden');
    pResponseContent.textContent = '';
    pErrorText.textContent = '';

    if (responseText && typeof responseText === 'string' && responseText.trim() !== "") {
        const isError = responseText.startsWith("Error:") ||
                        responseText.includes("An error occurred") ||
                        responseText.includes("API key not configured") ||
                        responseText.includes("No model specified") ||
                        responseText.includes("AuthenticationError") ||
                        responseText.includes("RateLimitError") ||
                        responseText.includes("APIConnectionError") ||
                        responseText.includes("NotFoundError");
        if (isError) {
            pErrorText.textContent = responseText;
            pErrorText.classList.remove('hidden');
        } else {
            pResponseContent.textContent = responseText;
            pResponseContent.classList.remove('hidden');
        }
    } else {
        pPlaceholder.textContent = `Response from ${responseAreaId.replace('ResponseArea','')} will appear here once a prompt is submitted.`;
        pPlaceholder.classList.remove('hidden');
    }
}

function updateResponseHeaderModelName(responseAreaId, modelId) {
    const responseArea = document.getElementById(responseAreaId);
    if (!responseArea ) return; // Removed modelId check here, as null modelId should clear it.
    const h3 = responseArea.querySelector('.response-header > h3');
    if (!h3) return;
    const aiLabelSpan = h3.querySelector('.ai-label');
    if (!aiLabelSpan) return;

    let displayModelId = "";
    if (modelId && typeof modelId === 'string') { // Ensure modelId is a string before splitting
        displayModelId = modelId.split('/').pop();
        if (responseAreaId === 'claudeResponseArea') {
            displayModelId = displayModelId.replace('claude-3-haiku-', 'c3-haiku-');
        }
    }

    let textNode = aiLabelSpan.nextSibling;
    if (!textNode || textNode.nodeType !== Node.TEXT_NODE) {
        textNode = document.createTextNode('');
        // h3.appendChild(textNode); // This might place it after model selector if selector is also in h3
        // Safer: insert after the span
        aiLabelSpan.parentNode.insertBefore(textNode, aiLabelSpan.nextSibling);
    }
    textNode.textContent = displayModelId ? ` (${displayModelId})` : ""; // Clear if no modelId
}


function renderHistorySidebar(makeFirstItemActive = false) {
    if (!historyListUl) {
        console.warn('renderHistorySidebar called before historyListUl is initialized.');
        return;
    }
    console.log('renderHistorySidebar called. makeFirstItemActive:', makeFirstItemActive);
    historyListUl.innerHTML = '';
    currentHistory = loadHistory(); // Uses global currentHistory
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

        const timestampSpan = document.createElement('span');
        timestampSpan.className = 'history-timestamp';
        timestampSpan.textContent = new Date(qnaSet.timestamp).toLocaleString();

        li.appendChild(promptSnippet);
        li.appendChild(timestampSpan);

        const deleteBtn = document.createElement('span');
        deleteBtn.className = 'delete-history-item-btn';
        deleteBtn.innerHTML = '&times;'; // HTML entity for '×' (multiplication sign)
        deleteBtn.title = 'Delete this item';
        // Event listener for delete will be added in a later step.

        li.appendChild(deleteBtn); // Append delete button to the list item

        deleteBtn.addEventListener('click', function(event) {
            event.stopPropagation(); // Prevent li's click listener from firing

            const itemIndex = parseInt(li.dataset.historyIndex); // Get index from parent li
            if (isNaN(itemIndex) || itemIndex < 0 || itemIndex >= currentHistory.length) {
                console.error('Invalid index for delete:', itemIndex);
                return;
            }

            console.log('Delete button clicked for history item index:', itemIndex);

            // Clear any pending undo from a previous deletion
            if (undoDeleteTimer) {
                clearTimeout(undoDeleteTimer);
            }
            recentlyDeletedSet = { item: { ...currentHistory[itemIndex] }, originalIndex: itemIndex }; // Store a copy

            currentHistory.splice(itemIndex, 1); // Remove from in-memory array

            try {
                localStorage.setItem(UDAYS_AI_AGENTS_HISTORY_KEY, JSON.stringify(currentHistory));
            } catch (error) {
                console.error("Error saving history to Local Storage after delete:", error);
                showToast('Error updating history. Storage may be full.', 'error');
                // If save fails, should we revert currentHistory? For now, UI will be out of sync with storage.
            }

            renderHistorySidebar(); // Re-render the sidebar immediately to show item removed

            showToast('Item deleted.', 'info', 7000, { // 7 second undo window
                text: 'Undo',
                callback: undoDeleteCallback
            });

            // Set a timer to clear the recentlyDeletedSet if Undo is not clicked
            undoDeleteTimer = setTimeout(() => {
                if (recentlyDeletedSet) { // Check if undo wasn't already called
                    console.log('Undo window expired for item:', recentlyDeletedSet.item.prompt.substring(0,20));
                    recentlyDeletedSet = null;
                }
            }, 7000); // Same as toast duration
        });

        li.addEventListener('click', function(event) {
            // Prevent click on delete button from also triggering loadQASetIntoUI
            if (event.target === deleteBtn) {
                return;
            }
            document.querySelectorAll('#historyList li').forEach(item => item.classList.remove('active-history-item'));
            this.classList.add('active-history-item');
            loadQASetIntoUI(parseInt(this.dataset.historyIndex));
        });
        historyListUl.appendChild(li);
    });

    const listItems = historyListUl.querySelectorAll('li');
    listItems.forEach(item => item.classList.remove('active-history-item'));

    if (makeFirstItemActive && listItems.length > 0) {
        listItems[0].classList.add('active-history-item');
        console.log('renderHistorySidebar: Made first item active.');
    }
}

function undoDeleteCallback() {
    if (undoDeleteTimer) {
        clearTimeout(undoDeleteTimer);
        undoDeleteTimer = null;
    }

    if (recentlyDeletedSet && recentlyDeletedSet.item) {
        console.log('Undo delete for:', recentlyDeletedSet.item);
        // Re-insert the item at its original position
        currentHistory.splice(recentlyDeletedSet.originalIndex, 0, recentlyDeletedSet.item);

        try {
            localStorage.setItem(UDAYS_AI_AGENTS_HISTORY_KEY, JSON.stringify(currentHistory));
            // Optionally, re-apply MAX_HISTORY_ITEMS limit if re-insertion could exceed it,
            // though splice should maintain correct length relative to limit if it was applied before delete.
        } catch (error) {
            console.error("Error saving history to Local Storage during undo:", error);
            showToast('Error restoring item. Storage may be full.', 'error');
            // Revert currentHistory change if save fails? Or leave as is for next attempt?
            // For now, let's assume save will work if it worked before delete.
        }

        renderHistorySidebar(); // Re-render to show the item back
        // Optionally highlight the restored item - renderHistorySidebar would need to support this
        // For now, just re-rendering will show it.

        showToast('Item restored to history.', 'success', 3000);
        recentlyDeletedSet = null; // Clear the stored item
    } else {
        console.log('No recently deleted item to undo or undo clicked too late.');
        // showToast('Nothing to undo or undo window expired.', 'info', 3000); // Optional feedback
    }
}

function loadQASetIntoUI(index) {
    console.log('loadQASetIntoUI called with index:', index);
    if (!mainPromptTextarea) { // Check if DOM elements are ready
        console.warn('loadQASetIntoUI called before DOM elements are initialized.');
        return;
    }
    if (index < 0 || index >= currentHistory.length) {
        console.error('Invalid index for loadQASetIntoUI:', index);
        return;
    }
    const qnaSet = currentHistory[index];
    console.log('Loading Q&A set from history:', qnaSet);

    mainPromptTextarea.value = qnaSet.prompt;

    displayResponseInArea('geminiResponseArea', qnaSet.gemini_response);
    displayResponseInArea('openaiResponseArea', qnaSet.openai_response);
    displayResponseInArea('claudeResponseArea', qnaSet.claude_response);

    if (visualGeminiSelect && hiddenGeminiInput) {
        visualGeminiSelect.value = qnaSet.gemini_model || '';
        hiddenGeminiInput.value = visualGeminiSelect.value;
        updateResponseHeaderModelName('geminiResponseArea', visualGeminiSelect.value);
    }
    if (visualOpenAISelect && hiddenOpenAIInput) {
        visualOpenAISelect.value = qnaSet.openai_model || '';
        hiddenOpenAIInput.value = visualOpenAISelect.value;
        updateResponseHeaderModelName('openaiResponseArea', visualOpenAISelect.value);
    }
    if (visualClaudeSelect && hiddenClaudeInput) {
        visualClaudeSelect.value = qnaSet.claude_model || '';
        hiddenClaudeInput.value = visualClaudeSelect.value;
        updateResponseHeaderModelName('claudeResponseArea', visualClaudeSelect.value);
    }
}

// --- Consolidated DOMContentLoaded for all UI initializations ---
document.addEventListener('DOMContentLoaded', function() {
    // Initialize all global DOM Element Variables
    historySidebar = document.getElementById('historySidebar');
    openHistorySidebarButton = document.getElementById('openHistorySidebar');
    closeHistorySidebarButton = document.getElementById('closeHistorySidebar');
    historyListUl = document.getElementById('historyList');
    clearHistoryButton = document.getElementById('clearHistoryButton');
    mainPromptTextarea = document.getElementById('prompt');

    visualGeminiSelect = document.getElementById('gemini_model_select_visual');
    hiddenGeminiInput = document.getElementById('gemini_model_select_hidden');
    visualOpenAISelect = document.getElementById('openai_model_select_visual');
    hiddenOpenAIInput = document.getElementById('openai_model_select_hidden');
    visualClaudeSelect = document.getElementById('claude_model_select_visual');
    hiddenClaudeInput = document.getElementById('claude_model_select_hidden');

    apiStatusModal = document.getElementById('apiStatusModal');
    openApiStatusModalButton = document.getElementById('openApiStatusModal');
    // Corrected selector for modal's close button
    const modalCloseButtonElem = document.querySelector('#apiStatusModal .close-modal-button');


    // Modal Logic
    if (openApiStatusModalButton && apiStatusModal) {
        openApiStatusModalButton.onclick = function() { if (apiStatusModal) apiStatusModal.style.display = 'block'; }
    }
    if (modalCloseButtonElem && apiStatusModal) { // Use the new variable name
        modalCloseButtonElem.onclick = function() { if (apiStatusModal) apiStatusModal.style.display = 'none'; }
    }
    window.onclick = function(event) { // Close modal if click outside
        if (event.target == apiStatusModal) { if (apiStatusModal) apiStatusModal.style.display = 'none'; }
    }

    // History Sidebar: Load Initial State & Attach Listeners
    if (historySidebar) {
        const savedSidebarState = localStorage.getItem(SIDEBAR_STATE_KEY);
        console.log('Loaded sidebar state:', savedSidebarState);
        if (savedSidebarState === 'open') {
            historySidebar.classList.add('open');
            console.log('Applying open state from Local Storage.');
            renderHistorySidebar();
        } else {
            historySidebar.classList.remove('open');
            console.log('Applying closed state or default.');
        }
    }

    if (openHistorySidebarButton && historySidebar) {
        openHistorySidebarButton.onclick = function() {
            console.log('Open sidebar button clicked.');
            historySidebar.classList.add('open');
            localStorage.setItem(SIDEBAR_STATE_KEY, 'open');
            console.log('Saved sidebar state: open');
            renderHistorySidebar();
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
    if (clearHistoryButton) {
        clearHistoryButton.onclick = function() {
            if (confirm("Are you sure you want to clear all Q&A history? This cannot be undone.")) {
                clearHistory();
                renderHistorySidebar();
                showToast("History cleared.", "success");
            }
        }
    }

    // Model Selector Sync Logic (Gemini, OpenAI, Claude)
    function setupModelSync(visualSelect, hiddenInput) {
        if (visualSelect && hiddenInput) {
            hiddenInput.value = visualSelect.value;
            visualSelect.addEventListener('change', function() {
                hiddenInput.value = this.value;
            });
        }
    }
    setupModelSync(visualGeminiSelect, hiddenGeminiInput);
    setupModelSync(visualOpenAISelect, hiddenOpenAIInput);
    setupModelSync(visualClaudeSelect, hiddenClaudeInput);

    // Clear Active History Item on New Prompt Input
    if (mainPromptTextarea && historyListUl) {
        mainPromptTextarea.addEventListener('input', function() {
            console.log('Input detected in main prompt. Clearing active history item highlight.');
            const listItems = historyListUl.querySelectorAll('li.active-history-item');
            listItems.forEach(item => { item.classList.remove('active-history-item'); });
        });
    }
});
