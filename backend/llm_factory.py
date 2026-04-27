import os

from groq import Groq

from backend.adapters.GroqAdapter import GroqAdapter
from backend.llm_client import LlmClient

def create_llm_client() -> LlmClient:
    provider = os.environ.get("AI_PROVIDER")
    if provider == "groq":
        return GroqAdapter(Groq(api_key=os.environ.get("GROQ_API_KEY")))
    else:
        raise ValueError(f"Unknown provider: {provider}")