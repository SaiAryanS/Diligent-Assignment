"""
LLM Client for connecting to LM Studio local LLM server
Uses OpenAI-compatible API
"""
from openai import OpenAI
from config import Config


class LLMClient:
    """Client for interacting with the local LLM via LM Studio"""
    
    def __init__(self):
        """Initialize the LLM client with LM Studio endpoint"""
        self.client = OpenAI(
            base_url=Config.LLM_BASE_URL,
            api_key="lm-studio"  # LM Studio doesn't require a real API key
        )
        self.model = Config.LLM_MODEL
        self.system_prompt = Config.SYSTEM_PROMPT
    
    def chat(self, user_message: str, context: str = None, conversation_history: list = None) -> str:
        """
        Send a message to the LLM and get a response
        
        Args:
            user_message: The user's input message
            context: Optional context from the knowledge base
            conversation_history: Optional list of previous messages
            
        Returns:
            The LLM's response as a string
        """
        messages = []
        
        # Build system prompt with optional context
        system_content = self.system_prompt
        if context:
            system_content += f"\n\nRelevant knowledge from the database:\n{context}"
        
        messages.append({"role": "system", "content": system_content})
        
        # Add conversation history if provided
        if conversation_history:
            messages.extend(conversation_history)
        
        # Add the current user message
        messages.append({"role": "user", "content": user_message})
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=2048,
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error communicating with LLM: {str(e)}"
    
    def is_available(self) -> bool:
        """Check if the LLM server is available"""
        try:
            self.client.models.list()
            return True
        except Exception:
            return False


# Singleton instance
llm_client = LLMClient()
