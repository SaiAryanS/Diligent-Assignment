/**
 * Jarvis AI Assistant - Frontend JavaScript
 */

// Generate a unique session ID
const sessionId = 'session_' + Math.random().toString(36).substr(2, 9);

// API base URL
const API_BASE = '';

// DOM Elements
const chatContainer = document.getElementById('chat-container');
const welcomeMessage = document.getElementById('welcome-message');
const messageInput = document.getElementById('message-input');
const sendBtn = document.getElementById('send-btn');
const statusIndicator = document.getElementById('status-indicator');
const chatView = document.getElementById('chat-view');
const knowledgeView = document.getElementById('knowledge-view');

// Check service health on load
document.addEventListener('DOMContentLoaded', checkHealth);

/**
 * Check the health of backend services
 */
async function checkHealth() {
    try {
        const response = await fetch(`${API_BASE}/api/health`);
        const data = await response.json();
        
        const statusDot = statusIndicator.querySelector('.status-dot');
        const statusText = statusIndicator.querySelector('.status-text');
        
        if (data.services.llm.status === 'connected') {
            statusDot.className = 'status-dot connected';
            statusText.textContent = 'LLM Connected';
        } else {
            statusDot.className = 'status-dot disconnected';
            statusText.textContent = 'LLM Disconnected';
        }
    } catch (error) {
        const statusDot = statusIndicator.querySelector('.status-dot');
        const statusText = statusIndicator.querySelector('.status-text');
        statusDot.className = 'status-dot disconnected';
        statusText.textContent = 'Server Offline';
    }
}

/**
 * Send a message to the assistant
 */
async function sendMessage() {
    const message = messageInput.value.trim();
    if (!message) return;
    
    // Hide welcome message
    if (welcomeMessage) {
        welcomeMessage.style.display = 'none';
    }
    
    // Add user message to chat
    addMessage(message, 'user');
    
    // Clear input
    messageInput.value = '';
    messageInput.style.height = 'auto';
    
    // Disable send button
    sendBtn.disabled = true;
    
    // Show typing indicator
    const typingId = showTypingIndicator();
    
    try {
        const response = await fetch(`${API_BASE}/api/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                message: message,
                session_id: sessionId,
                use_knowledge: true
            })
        });
        
        const data = await response.json();
        
        // Remove typing indicator
        removeTypingIndicator(typingId);
        
        if (data.error) {
            addMessage(`Error: ${data.error}`, 'assistant', true);
        } else {
            addMessage(data.response, 'assistant');
        }
    } catch (error) {
        removeTypingIndicator(typingId);
        addMessage(`Error: Could not connect to the server. Please make sure the backend is running.`, 'assistant', true);
    }
    
    // Re-enable send button
    sendBtn.disabled = false;
    messageInput.focus();
}

/**
 * Add a message to the chat container
 */
function addMessage(content, role, isError = false) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}`;
    
    const avatarIcon = role === 'user' 
        ? '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>'
        : '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/><path d="M2 12h20"/></svg>';
    
    messageDiv.innerHTML = `
        <div class="message-avatar">
            ${avatarIcon}
        </div>
        <div class="message-content ${isError ? 'error' : ''}">
            <p>${formatMessage(content)}</p>
        </div>
    `;
    
    chatContainer.appendChild(messageDiv);
    scrollToBottom();
}

/**
 * Format message content (basic markdown support)
 */
function formatMessage(content) {
    // Escape HTML
    content = content.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    
    // Code blocks
    content = content.replace(/```(\w*)\n([\s\S]*?)```/g, '<pre><code>$2</code></pre>');
    
    // Inline code
    content = content.replace(/`([^`]+)`/g, '<code>$1</code>');
    
    // Bold
    content = content.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
    
    // Italic
    content = content.replace(/\*([^*]+)\*/g, '<em>$1</em>');
    
    // Line breaks
    content = content.replace(/\n/g, '<br>');
    
    return content;
}

/**
 * Show typing indicator
 */
function showTypingIndicator() {
    const id = 'typing_' + Date.now();
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message assistant';
    typingDiv.id = id;
    
    typingDiv.innerHTML = `
        <div class="message-avatar">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"/>
                <path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/>
                <path d="M2 12h20"/>
            </svg>
        </div>
        <div class="message-content">
            <div class="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
            </div>
        </div>
    `;
    
    chatContainer.appendChild(typingDiv);
    scrollToBottom();
    
    return id;
}

/**
 * Remove typing indicator
 */
function removeTypingIndicator(id) {
    const element = document.getElementById(id);
    if (element) {
        element.remove();
    }
}

/**
 * Scroll chat to bottom
 */
function scrollToBottom() {
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

/**
 * Handle keyboard input
 */
function handleKeyDown(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
}

/**
 * Auto-resize textarea
 */
function autoResize(element) {
    element.style.height = 'auto';
    element.style.height = Math.min(element.scrollHeight, 120) + 'px';
}

/**
 * Send a suggestion chip message
 */
function sendSuggestion(text) {
    messageInput.value = text;
    sendMessage();
}

/**
 * Clear conversation
 */
async function clearConversation() {
    try {
        await fetch(`${API_BASE}/api/session/clear`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ session_id: sessionId })
        });
    } catch (error) {
        console.error('Error clearing session:', error);
    }
    
    // Clear chat UI
    chatContainer.innerHTML = '';
    
    // Show welcome message again
    chatContainer.innerHTML = `
        <div class="welcome-message" id="welcome-message">
            <div class="welcome-icon">
                <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                    <circle cx="12" cy="12" r="10"/>
                    <path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/>
                    <path d="M2 12h20"/>
                </svg>
            </div>
            <h1>Hello, I'm Jarvis</h1>
            <p>Your personal AI assistant. How can I help you today?</p>
            <div class="suggestion-chips">
                <button class="chip" onclick="sendSuggestion('What can you help me with?')">What can you help me with?</button>
                <button class="chip" onclick="sendSuggestion('Tell me about yourself')">Tell me about yourself</button>
                <button class="chip" onclick="sendSuggestion('How does this work?')">How does this work?</button>
            </div>
        </div>
    `;
}

/**
 * Show chat view
 */
function showChat() {
    document.getElementById('chat-view').style.display = 'flex';
    document.getElementById('chat-view').classList.remove('hidden');
    document.getElementById('knowledge-view').style.display = 'none';
    document.getElementById('knowledge-view').classList.add('hidden');
    
    // Update nav buttons
    document.querySelectorAll('.nav-btn').forEach(btn => btn.classList.remove('active'));
    document.querySelectorAll('.nav-btn')[0].classList.add('active');
}

/**
 * Show knowledge view
 */
function showKnowledge() {
    document.getElementById('chat-view').style.display = 'none';
    document.getElementById('chat-view').classList.add('hidden');
    document.getElementById('knowledge-view').style.display = 'flex';
    document.getElementById('knowledge-view').classList.remove('hidden');
    
    // Update nav buttons
    document.querySelectorAll('.nav-btn').forEach(btn => btn.classList.remove('active'));
    document.querySelectorAll('.nav-btn')[1].classList.add('active');
}

/**
 * Add knowledge to the database
 */
async function addKnowledge() {
    const knowledgeInput = document.getElementById('knowledge-input');
    const knowledgeStatus = document.getElementById('knowledge-status');
    const text = knowledgeInput.value.trim();
    
    if (!text) {
        showKnowledgeStatus('Please enter some text to add.', 'error');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/api/knowledge`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text: text })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showKnowledgeStatus('Knowledge added successfully!', 'success');
            knowledgeInput.value = '';
        } else {
            showKnowledgeStatus(data.error || 'Failed to add knowledge', 'error');
        }
    } catch (error) {
        showKnowledgeStatus('Error connecting to the server.', 'error');
    }
}

/**
 * Search the knowledge base
 */
async function searchKnowledge() {
    const searchInput = document.getElementById('search-input');
    const searchResults = document.getElementById('search-results');
    const query = searchInput.value.trim();
    
    if (!query) {
        searchResults.innerHTML = '';
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/api/knowledge/search`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ query: query })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            if (data.results.length === 0) {
                searchResults.innerHTML = '<p style="color: var(--text-secondary); text-align: center; padding: 20px;">No results found.</p>';
            } else {
                searchResults.innerHTML = data.results.map(result => `
                    <div class="search-result-item">
                        <p>${result}</p>
                    </div>
                `).join('');
            }
        } else {
            searchResults.innerHTML = `<p style="color: var(--error-color); text-align: center; padding: 20px;">${data.error || 'Search failed'}</p>`;
        }
    } catch (error) {
        searchResults.innerHTML = '<p style="color: var(--error-color); text-align: center; padding: 20px;">Error connecting to the server.</p>';
    }
}

/**
 * Show knowledge status message
 */
function showKnowledgeStatus(message, type) {
    const knowledgeStatus = document.getElementById('knowledge-status');
    knowledgeStatus.textContent = message;
    knowledgeStatus.className = `knowledge-status ${type}`;
    
    setTimeout(() => {
        knowledgeStatus.textContent = '';
        knowledgeStatus.className = 'knowledge-status';
    }, 3000);
}

// Periodically check health
setInterval(checkHealth, 30000);
