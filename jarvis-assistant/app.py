"""
Jarvis AI Assistant - Main Flask Application
A personal AI assistant powered by a self-hosted LLM with vector database knowledge retrieval
"""
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from llm_client import llm_client
from vector_db import vector_db
from config import Config
import os

# Initialize Flask app
app = Flask(__name__, static_folder='static')
CORS(app)  # Enable CORS for frontend

# Store conversation history (in-memory, per session)
# In production, use a database or session storage
conversations = {}


@app.route('/')
def index():
    """Serve the chat UI"""
    return send_from_directory('static', 'index.html')


@app.route('/static/<path:path>')
def serve_static(path):
    """Serve static files"""
    return send_from_directory('static', path)


@app.route('/api/health', methods=['GET'])
def health_check():
    """Check the health of all services"""
    llm_status = llm_client.is_available()
    vector_db_status = vector_db.is_configured()
    
    return jsonify({
        "status": "ok" if llm_status else "degraded",
        "services": {
            "llm": {
                "status": "connected" if llm_status else "disconnected",
                "url": Config.LLM_BASE_URL,
                "model": Config.LLM_MODEL
            },
            "vector_db": {
                "status": "connected" if vector_db_status else "not_configured",
                "index": Config.PINECONE_INDEX_NAME if vector_db_status else None
            }
        }
    })


@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Main chat endpoint
    
    Request body:
        - message: The user's message
        - session_id: Optional session ID for conversation history
        - use_knowledge: Whether to search the knowledge base (default: True)
    """
    data = request.json
    
    if not data or 'message' not in data:
        return jsonify({"error": "Message is required"}), 400
    
    user_message = data['message']
    session_id = data.get('session_id', 'default')
    use_knowledge = data.get('use_knowledge', True)
    
    # Get or create conversation history
    if session_id not in conversations:
        conversations[session_id] = []
    
    conversation_history = conversations[session_id]
    
    # Search for relevant context from knowledge base
    context = None
    if use_knowledge and vector_db.is_configured():
        relevant_docs = vector_db.search(user_message, top_k=3)
        if relevant_docs:
            context = "\n\n".join(relevant_docs)
    
    # Get response from LLM
    response = llm_client.chat(
        user_message=user_message,
        context=context,
        conversation_history=conversation_history[-10:]  # Last 10 messages
    )
    
    # Update conversation history
    conversation_history.append({"role": "user", "content": user_message})
    conversation_history.append({"role": "assistant", "content": response})
    
    # Keep only last 20 messages to prevent memory issues
    if len(conversation_history) > 20:
        conversations[session_id] = conversation_history[-20:]
    
    return jsonify({
        "response": response,
        "context_used": context is not None,
        "session_id": session_id
    })


@app.route('/api/knowledge', methods=['POST'])
def add_knowledge():
    """
    Add knowledge to the vector database
    
    Request body:
        - text: The text content to store
        - metadata: Optional metadata dict
    """
    data = request.json
    
    if not data or 'text' not in data:
        return jsonify({"error": "Text is required"}), 400
    
    if not vector_db.is_configured():
        return jsonify({
            "error": "Vector database not configured",
            "hint": "Please set your PINECONE_API_KEY in the .env file"
        }), 503
    
    text = data['text']
    metadata = data.get('metadata', {})
    
    success = vector_db.add_knowledge(text, metadata)
    
    if success:
        return jsonify({"status": "success", "message": "Knowledge added successfully"})
    else:
        return jsonify({"error": "Failed to add knowledge"}), 500


@app.route('/api/knowledge/search', methods=['POST'])
def search_knowledge():
    """
    Search the knowledge base
    
    Request body:
        - query: The search query
        - top_k: Number of results (default: 3)
    """
    data = request.json
    
    if not data or 'query' not in data:
        return jsonify({"error": "Query is required"}), 400
    
    if not vector_db.is_configured():
        return jsonify({
            "error": "Vector database not configured",
            "hint": "Please set your PINECONE_API_KEY in the .env file"
        }), 503
    
    query = data['query']
    top_k = data.get('top_k', 3)
    
    results = vector_db.search(query, top_k)
    
    return jsonify({
        "results": results,
        "count": len(results)
    })


@app.route('/api/session/clear', methods=['POST'])
def clear_session():
    """Clear conversation history for a session"""
    data = request.json
    session_id = data.get('session_id', 'default') if data else 'default'
    
    if session_id in conversations:
        del conversations[session_id]
    
    return jsonify({"status": "success", "message": "Session cleared"})


if __name__ == '__main__':
    import sys
    print("=" * 60, flush=True)
    print("  Jarvis AI Assistant", flush=True)
    print("=" * 60, flush=True)
    print(f"  LLM Server: {Config.LLM_BASE_URL}", flush=True)
    print(f"  Model: {Config.LLM_MODEL}", flush=True)
    print(f"  Vector DB: {'Configured' if vector_db.is_configured() else 'Not configured'}", flush=True)
    print("=" * 60, flush=True)
    print(f"  Starting server on http://localhost:{Config.FLASK_PORT}", flush=True)
    print("=" * 60, flush=True)
    sys.stdout.flush()
    
    app.run(
        host='0.0.0.0',
        port=Config.FLASK_PORT,
        debug=Config.FLASK_DEBUG
    )
