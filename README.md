# Mini RAG: Ollama + Local ChromaDB (Windows, no Docker/Anaconda)

**All model inference, embeddings, vector storage and the Python app run locally.** No Groq, API key, Docker, Anaconda, or cloud vector DB is required. Ollama model downloads and pip package installs need internet once; after installation the RAG can run offline.

It fulfills the three requirements:

1. **LLM access**: local Ollama installation with `llama3.2:1b` as the chat model.
2. **Vector DB**: ChromaDB embedded in the Python process, persisted at `chroma_db/`.
3. **Verification**: `python rag.py verify` checks `.env`, opens ChromaDB, confirms Ollama models are installed, and makes real embedding + chat calls.

Pipeline: `data/*.txt` -> text chunks -> Ollama `nomic-embed-text` -> local ChromaDB -> matching chunks -> Ollama `llama3.2:1b` -> grounded answer.

## 1. Install Python and Ollama (no Docker or Conda)

- Install 64-bit **Python 3.11** from https://www.python.org/downloads/ . Check `py -3.11 --version`.
- Install Ollama for Windows from https://ollama.com/download . Launch the Ollama app. It normally starts the server automatically on `http://127.0.0.1:11434`.
- Open a **new PowerShell** and verify `ollama --version`.

Pull both required models (internet required to download them once):

```powershell
ollama pull llama3.2:1b
ollama pull nomic-embed-text
ollama list
```

`llama3.2:1b` is a relatively small chat model; accuracy may be limited. `nomic-embed-text` is a separate embedding model. You need **both**. If the Ollama app is not serving, start it; alternatively run `ollama serve` in a separate terminal. Do not run a second server if one is already listening on port 11434.

## 2. Unzip the project and open PowerShell in the correct folder

Extract `windows_rag_ollama_chromadb.zip` and open its `windows_rag_ollama_chromadb` folder in File Explorer. Click the address bar, type `powershell`, and press Enter. Confirm the prompt is in the project directory, **not** `C:\WINDOWS\system32`.

```powershell
Get-Location
Get-ChildItem
```

You should see `rag.py`, `requirements.txt`, `data`, and `.env.example`.

## 3. Create virtual environment and install dependencies

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

This uses Windows' ordinary Python and `venv`; no `conda`, `Activate.ps1` or Docker needed. Note ChromaDB installs standard Python dependencies such as NumPy.

## 4. Create and confirm .env (NO API key)

```powershell
Copy-Item .env.example .env
notepad .env
```

The defaults are:

```env
OLLAMA_HOST=http://127.0.0.1:11434
OLLAMA_CHAT_MODEL=llama3.2:1b
OLLAMA_EMBED_MODEL=nomic-embed-text
CHROMA_PATH=./chroma_db
CHROMA_COLLECTION=company_knowledge_ollama
```

The `.env` file configures local endpoints/models, not secrets.

## 5. Verify the three required components

```powershell
.\.venv\Scripts\python.exe rag.py verify
```

On success the program reports the local `.env` configuration, persistent ChromaDB access, available Ollama models, a real embedding vector, a live chat response, and finally:

```text
PASS: .env, local ChromaDB, local embeddings and local LLM are working.
```

This is not simulated output; actual `verify` calls local Ollama. The chat response may vary.

## 6. Ingest documents and ask a question

```powershell
.\.venv\Scripts\python.exe rag.py ingest
.\.venv\Scripts\python.exe rag.py ask "How many days can employees work remotely?"
```

The sample document says employees may work remotely up to **two days per week, with manager approval**.

To use your own knowledge, add UTF-8 `.txt` files into `data/`, then run `ingest` again. This sample supports text files only; PDF loading can be added in a later version. If you change embedding models after ingestion, use a new `CHROMA_COLLECTION` (or delete `chroma_db` to reset) because embedding dimensions may differ. Re-ingestion updates existing chunk IDs for existing files; it does not delete chunks from files you removed.

## Troubleshooting

- **`PS C:\WINDOWS\system32>` / `.venv\Scripts\python.exe` not recognized**: you are in the wrong folder. Open PowerShell from the extracted project folder containing `rag.py` before running the commands.
- **`ollama` not recognized**: install Ollama, then reopen the terminal.
- **Cannot connect to Ollama / connection refused**: open the Ollama app; if necessary run `ollama serve` in a separate window and keep it running.
- **Model not installed**: `ollama pull llama3.2:1b` and `ollama pull nomic-embed-text`.
- **`py` not recognized**: install the Python launcher with Python 3.11 or replace `py -3.11` with `python` if it points to Python 3.11.
- **No module named `chromadb`/`dotenv`**: install requirements using the project's `.venv` Python and run commands using that same executable.
- **Ollama is too slow or out of memory**: close other memory-heavy apps; use the small `llama3.2:1b` model, which is intended to reduce hardware demands. CPU-only operation may be slow.
- **Ollama HTTP 404 / unknown endpoint**: update Ollama to a recent version supporting `/api/embed` and `/api/chat`.
- **Chroma dimension mismatch**: clear your old embedding collection or use a fresh project folder before re-ingesting.

## Note about the previous Groq project

This ZIP is a **new, separate project**. It removes `groq` from `requirements.txt`, uses local Ollama for *both* embeddings and chat, and no longer reads `GROQ_API_KEY`. Extract it to a new folder to avoid mixing old Groq embeddings with Ollama embeddings in the same vector collection.
