"""
Configuration settings for Jarvis AI Assistant
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Application configuration"""
    
    # LLM Settings (LM Studio)
    LLM_BASE_URL = os.getenv("LLM_BASE_URL", "http://192.168.0.104:1234/v1")
    LLM_MODEL = os.getenv("LLM_MODEL", "qwen2.5-coder-7b-instruct")
    
    # Pinecone Settings
    PINECONE_API_KEY = os.getenv("PINECONE_API_KEY", "")
    PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "jarvis-knowledge")
    
    # Flask Settings
    FLASK_DEBUG = os.getenv("FLASK_DEBUG", "True").lower() == "true"
    FLASK_PORT = int(os.getenv("FLASK_PORT", "5000"))
    
    # Embedding model for vector search
    EMBEDDING_MODEL = "all-MiniLM-L6-v2"  # Small, fast embedding model
    EMBEDDING_DIMENSION = 384  # Dimension for MiniLM
    
    # System prompt for the assistant
    SYSTEM_PROMPT = """You are Jarvis, an intelligent AI assistant created to help users with their questions and tasks.
You are helpful, harmless, and honest. You provide accurate, contextual responses.
When given context from the knowledge base, use it to provide more relevant answers.
If you don't know something, admit it rather than making things up."""
