"""
Vector Database Client using Pinecone for knowledge storage and retrieval
"""
from typing import List, Dict, Optional
import hashlib
from config import Config


class VectorDBClient:
    """Client for interacting with Pinecone vector database"""
    
    def __init__(self):
        """Initialize the vector database client"""
        self._embedding_model = None  # Lazy loaded
        self.index = None
        self.pinecone_client = None
        
        # Initialize Pinecone if API key is provided
        api_key = Config.PINECONE_API_KEY
        print(f"[VectorDB] Checking Pinecone API key: {'Set' if api_key and api_key != 'your-pinecone-api-key-here' else 'Not set'}", flush=True)
        
        if api_key and api_key != "your-pinecone-api-key-here":
            try:
                from pinecone import Pinecone
                print(f"[VectorDB] Initializing Pinecone client...", flush=True)
                self.pinecone_client = Pinecone(api_key=api_key)
                print(f"[VectorDB] Pinecone client created, initializing index...", flush=True)
                self._init_index()
                print(f"[VectorDB] Index initialized successfully: {self.index is not None}", flush=True)
            except Exception as e:
                import traceback
                print(f"Warning: Could not initialize Pinecone: {e}", flush=True)
                traceback.print_exc()
                self.pinecone_client = None
    
    @property
    def embedding_model(self):
        """Lazy load the embedding model"""
        if self._embedding_model is None:
            from sentence_transformers import SentenceTransformer
            print("Loading embedding model...")
            self._embedding_model = SentenceTransformer(Config.EMBEDDING_MODEL)
            print("Embedding model loaded.")
        return self._embedding_model
    
    def _init_index(self):
        """Initialize or create the Pinecone index"""
        from pinecone import ServerlessSpec
        index_name = Config.PINECONE_INDEX_NAME
        
        print(f"[VectorDB] Looking for index: {index_name}", flush=True)
        
        # Check if index exists, create if not
        existing_indexes = [idx.name for idx in self.pinecone_client.list_indexes()]
        print(f"[VectorDB] Existing indexes: {existing_indexes}", flush=True)
        
        if index_name not in existing_indexes:
            print(f"[VectorDB] Creating new index: {index_name}", flush=True)
            self.pinecone_client.create_index(
                name=index_name,
                dimension=Config.EMBEDDING_DIMENSION,
                metric="cosine",
                spec=ServerlessSpec(
                    cloud="aws",
                    region="us-east-1"
                )
            )
            print(f"[VectorDB] Index created, waiting for it to be ready...", flush=True)
        
        self.index = self.pinecone_client.Index(index_name)
        print(f"[VectorDB] Connected to index: {index_name}", flush=True)
    
    def _generate_id(self, text: str) -> str:
        """Generate a unique ID for a text chunk"""
        return hashlib.md5(text.encode()).hexdigest()
    
    def _get_embedding(self, text: str) -> List[float]:
        """Generate embedding for a text"""
        return self.embedding_model.encode(text).tolist()
    
    def add_knowledge(self, text: str, metadata: Optional[Dict] = None) -> bool:
        """
        Add a piece of knowledge to the vector database
        
        Args:
            text: The text content to store
            metadata: Optional metadata dict
            
        Returns:
            True if successful, False otherwise
        """
        if not self.index:
            print("Warning: Pinecone not configured. Knowledge not stored.")
            return False
        
        try:
            doc_id = self._generate_id(text)
            embedding = self._get_embedding(text)
            
            meta = metadata or {}
            meta["text"] = text
            
            self.index.upsert(vectors=[{
                "id": doc_id,
                "values": embedding,
                "metadata": meta
            }])
            return True
        except Exception as e:
            print(f"Error adding knowledge: {e}")
            return False
    
    def search(self, query: str, top_k: int = 3) -> List[str]:
        """
        Search for relevant knowledge based on a query
        
        Args:
            query: The search query
            top_k: Number of results to return
            
        Returns:
            List of relevant text chunks
        """
        if not self.index:
            return []
        
        try:
            query_embedding = self._get_embedding(query)
            results = self.index.query(
                vector=query_embedding,
                top_k=top_k,
                include_metadata=True
            )
            
            texts = []
            for match in results.matches:
                if match.score > 0.5:  # Only include relevant results
                    if "text" in match.metadata:
                        texts.append(match.metadata["text"])
            
            return texts
        except Exception as e:
            print(f"Error searching knowledge: {e}")
            return []
    
    def is_configured(self) -> bool:
        """Check if Pinecone is properly configured"""
        return self.index is not None


# Singleton instance
vector_db = VectorDBClient()
