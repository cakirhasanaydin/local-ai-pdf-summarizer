# 📁 Local AI Document Summarizer & Q&A Assistant

A privacy-focused, local document summarization and interactive Q&A web application powered by **Python**, **Streamlit**, **Ollama (Llama 3)**, and **scikit-learn (TF-IDF)**. Runs entirely on your local machine with zero data leakage.

## 🚀 Features
- **Multi-Format Summarization:** Generate Executive Summaries, Bullet Points, or Detailed Reports.
- **Local RAG (Retrieval-Augmented Generation):** Ask questions about your PDF documents using lightweight TF-IDF and cosine similarity without heavy vector databases.
- **100% Private:** Powered by local LLMs via Ollama. No cloud APIs or data sharing required.
- **Dockerized:** Easily deploy and run in an isolated container environment.

---

## 🛠️ Prerequisites & Setup

Before running the app, ensure you have the following installed on your machine:
1. **Docker Desktop** (Running in the background)
2. **Ollama** (Installed locally with the Llama 3 model pulled)

### 1. Pull the Model via Ollama
```bash
ollama run llama3