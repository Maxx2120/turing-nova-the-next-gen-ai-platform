# 🤖 AI Chat Application (Production-Grade)

A modern, full-stack AI chat application built with **FastAPI**, **React**, and **LangChain**. Designed to run locally with **Ollama** (Llama 3 / Mistral) but architected for production scalability.

## 🚀 Features

- **Brain**: Powered by open-source LLMs via Ollama (Llama 3 suggested).
- **Architecture**: Clean separation of concerns (Frontend, Backend, Database, LLM Layer).
- **Communication**: Real-time streaming via WebSockets.
- **Memory**: Persistent conversation history (SQLite + SQLAlchemy).
- **UI/UX**: "Startup-like" polished interface with Tailwind CSS, typing indicators, and markdown support.
- **Robustness**: Error handling, logging, and automatic reconnection logic.

---

## 🛠️ Tech Stack

### Backend
- **Python 3.9+**
- **FastAPI**: High-performance async API.
- **LangChain**: LLM orchestration and memory.
- **SQLAlchemy**: Database ORM.
- **WebSockets**: Real-time bi-directional communication.

### Frontend
- **React 18**: UI Library (Vite).
- **Tailwind CSS**: Utility-first styling.
- **Lucide React**: Beautiful icons.
- **React Markdown**: Messaging rendering.

---

## 📦 Installation & Setup

### Prerequisites
1.  **Python 3.9+** installed.
2.  **Node.js 16+** installed.
3.  **Ollama** installed and running.
    -   Download from [ollama.com](https://ollama.com).
    -   Run `ollama pull llama3` (or your preferred model).
    -   Ensure it's running: `ollama serve`.

### 1. Backend Setup

```bash
cd chat-app/backend

# Create virtual environment (optional but recommended)
python -m venv venv
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate

# Install dependencies
pip install fastapi uvicorn langchain langchain-community langchain-core sqlalchemy websockets

# Run the server
uvicorn main:app --reload
```
*Server runs on `http://localhost:8000`*

### 2. Frontend Setup

```bash
cd chat-app/frontend

# Install dependencies
npm install

# Start development server
npm run dev
```
*Frontend runs on `http://localhost:5173` (usually)*

---

## 🧠 System Architecture

### 1. Intent Understanding & Persona
The chatbot uses a **System Prompt** injected via LangChain to define its persona:
- **Friendly & Casual**: Uses emojis and informal language when appropriate.
- **Helpful**: Breaks down complex topics.
- **Context Aware**: Uses a sliding window of chat history from the SQL database to maintain context.

### 2. Real-Time Pipeline
1.  **User types message** -> Sent via WebSocket to Backend.
2.  **Backend** persists message to SQLite.
3.  **LangChain Chain** invokes Ollama with History + System Prompt + New Input.
4.  **LLM Token Stream** is captured and sent chunk-by-chunk back to Frontend via WebSocket.
5.  **Frontend** appends chunks to the active message bubble for that "typing" effect.

### 3. Folder Structure
```
chat-app/
├── backend/
│   ├── main.py              # Entry point
│   ├── websocket.py         # WS Connection Manager
│   ├── database/            # DB Models & CRUD
│   ├── llm/                 # Model Loader & Prompts
│   └── utils/               # Logger & Helpers
└── frontend/
    ├── src/
    │   ├── components/      # React Components (ChatBox, Message...)
    │   ├── hooks/           # Custom Hooks (useChatWebSocket)
    │   └── App.jsx
    └── tailwind.config.js
```

---

## 🛡️ Future Improvements
- **Dockerization**: Add `Dockerfile` and `docker-compose` for one-click deploy.
- **Authentication**: Add JWT auth to secure chat sessions per user.
- **Vector DB**: Use RAG (Retrieval Augmented Generation) to let the bot answer questions about specific documents.
- **Model Switching UI**: specialized admin panel to switch models (e.g., Llama 3 -> Mixtral) on the fly.

---

*Built with ❤️ by Antigravity*
