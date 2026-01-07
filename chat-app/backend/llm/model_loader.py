import os
from langchain_community.chat_models import ChatOllama
from langchain_core.language_models.chat_models import BaseChatModel
from utils.logger import logger

def clean_model_name(model_name: str) -> str:
    """
    Cleans the model name input to ensure compatibility.
    """
    return model_name.strip()

def get_llm(model_name: str = "llama3", base_url: str = "http://localhost:11434") -> BaseChatModel:
    """
    Initializes and returns the LangChain model instance depending on availability.
    Default preference: Ollama (local).
    
    Args:
        model_name (str): Name of the model to pull/use in Ollama.
        base_url (str): URL of the Ollama instance.
        
    Returns:
        BaseChatModel: Configured LangChain chat model.
    """
    logger.info(f"Initializing LLM: {model_name} at {base_url}")
    
    try:
        # Check if Ollama is reachable (basic check logic could go here, 
        # but LangChain handles connection errors gracefully usually)
        
        # We use ChatOllama as the primary driver
        llm = ChatOllama(
            model=model_name,
            base_url=base_url,
            temperature=0.7, # Balance creativity and coherence
            keep_alive="5m"  # Keep model loaded for 5 minutes
        )
        
        return llm
        
    except Exception as e:
        logger.error(f"Failed to initialize LLM: {e}")
        raise e
