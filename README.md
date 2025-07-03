# 🧠 MCP-Based Meeting Summary Service Example

This project is a sample implementation of an AI-powered meeting summarization service using **MCP (Model Context Protocol)**. Built with FastMCP, LangChain, PostgreSQL, and Notion. it demonstrates how to define and invoke MCP-compatible tools to generate summaries, extract keywords, and identify action items from transcribed meeting data.

## 🚀 Features

- Generate meeting summaries using LLMs
- Extract keywords and action items
- Modular MCP (Model Context Protocol) architecture
- Integration with Notion for storing summaries
- PostgreSQL for storing transcripts
- LangChain for LLM interactions
- FastMCP for tool management

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
NOTION_TOKEN=your_notion_token
NOTION_PAGE_ID=your_notion_page_id  # The ID of the Notion page
```

## 🐘 Start PostgreSQL (via Docker)
If you don’t have PostgreSQL running locally, use Docker Compose:
```bash
docker-compose up -d
```

## Notion Setup
this project uses Notion to store meeting summaries. You need to create a Notion integration and get your token and page ID.
1. Go to [notion-mcp-server](https://github.com/makenotion/notion-mcp-server)
2. Follow the instructions to create a Notion integration and get your token.
3. Share the Notion page with your integration to allow it to write data.

## ▶️ Run
To test the full MCP tool pipeline using LangChain function calling:
```bash
python3 client.py
```
This will send a prompt to the LLM asking it to summarize the meeting and generate action items using your local MCP tool server.

## 📁 Folder Structure

```
meeting_summary/
├── mcp_server.py          # FastMCP server with tool definitions
├── client.py              # LangChain client with tool calling
├── tools/                 # MCP-compatible tools (e.g., generate_summary)
├── requirements.txt
├── .env                   # Your local environment config
├── docker-compose.yml     # PostgreSQL setup
├── init.sql               # SQL initialization script
```
