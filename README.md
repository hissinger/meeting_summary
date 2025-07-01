# 🧠 MCP-Based Meeting Summary Service Example

This project is a sample implementation of an AI-powered meeting summarization service using **MCP (Model Context Protocol)**. Built with FastAPI, LangChain and PostgreSQL, it demonstrates how to define and invoke MCP-compatible tools to generate summaries, extract keywords, and identify action items from transcribed meeting data.

## 🚀 Features

- Generate meeting summaries using LLMs
- Extract keywords and action items
- Modular MCP (Model Context Protocol) architecture
- REST API server with FastAPI
- PostgreSQL for storing transcripts
- LangChain for LLM interactions

---

## ⚙️ Initial Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/meeting_summary.git
cd meeting_summary
```

### 2. Create and Activate Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip3 install -r requirements.txt
```

## 🧪 .env Configuration
Create a .env file in the root directory with the following content:
```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/meeting_summary
OPENAI_API_KEY=your_openai_api_key
```

## 🐘 Start PostgreSQL (via Docker)
If you don’t have PostgreSQL running locally, use Docker Compose:
```bash
docker-compose up -d
```

## ▶️ Run the FastAPI Server
```bash
uvicorn mcp_server:app --reload
```

## 🧪 Test Client
To test the full MCP tool pipeline using LangChain function calling:
```bash
python3 client.py
```
This will send a prompt to the LLM asking it to summarize the meeting and generate action items using your local MCP tool server.

## 📁 Folder Structure

```
meeting_summary/
├── mcp_server.py          # FastAPI entry point
├── client.py              # LangChain client with tool calling
├── tools/                 # MCP-compatible tools (e.g., generate_summary)
├── requirements.txt
├── .env                   # Your local environment config
├── docker-compose.yml     # PostgreSQL setup
├── init.sql               # SQL initialization script
```
