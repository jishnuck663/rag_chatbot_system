
import os
from dotenv import load_dotenv
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_chroma import Chroma

load_dotenv()

HOST = os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434")
EMBED = os.getenv("OLLAMA_EMBED_MODEL", "nomic-embed-text")
CHAT = os.getenv("OLLAMA_CHAT_MODEL", "llama3.2:1b")

# Ollama connections
embeddings = OllamaEmbeddings(model=EMBED, base_url=HOST)
llm = ChatOllama(model=CHAT, base_url=HOST, temperature=0)

# ChromaDB connection
db = Chroma(
    collection_name="langchain_rag_demo",
    persist_directory="./chroma_langchain",
    embedding_function=embeddings
)
