from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
import asyncio
import os
from contextlib import AsyncExitStack
from types import SimpleNamespace

load_dotenv()

notion_token = os.getenv("NOTION_TOKEN")

servers = [
    {
        "name": "meeting_summary_server",
        "params": StdioServerParameters(
            command="python",
            args=["mcp_server.py"]
        )
    },
    {
        "name": "notionApi",
        "params": SimpleNamespace(
            command="npx",
            args=["-y", "@notionhq/notion-mcp-server"],
            cwd=None,
            encoding="utf-8",
            encoding_error_handler="replace",
            env={
                "OPENAPI_MCP_HEADERS": f'{{"Authorization": "Bearer {notion_token}", "Notion-Version": "2022-06-28"}}'
            }
        )
    }
]


async def connect_to_server(server_config, stack: AsyncExitStack):
    """서버에 연결하고 MCP 세션 및 툴 로딩"""
    name = server_config["name"]
    params = server_config["params"]

    read, write = await stack.enter_async_context(stdio_client(params))
    session = await stack.enter_async_context(ClientSession(read, write))
    await session.initialize()
    tools = await load_mcp_tools(session)

    return {
        "name": name,
        "tools": tools,
    }


async def run_multi_server_agent():
    async with AsyncExitStack() as stack:
        connections = []
        for server in servers:
            conn = await connect_to_server(server, stack)
            connections.append(conn)

        all_tools = [tool for conn in connections for tool in conn["tools"]]
        llm = ChatOpenAI(model="gpt-4o-mini")
        agent = create_react_agent(llm, all_tools)

        room_id = "test-room"
        page_id = os.getenv("NOTION_PAGE_ID")

        return await agent.ainvoke({
            "messages": [
                ("system",
                    f"당신은 회의 내용을 요약하고 액션 아이템을 추출한 후, Notion에 저장하는 도우미입니다.\n"
                    f"Notion에 저장할 때는 다음 지침을 따르세요:\n"
                    f"- 지정된 `page_id`를 부모로 사용합니다. (page_id: {page_id})\n"
                    f"- 새 페이지의 제목은 회의 날짜(YYYY년 MM월 DD일)로 설정합니다.\n"
                    f"- 본문은 다음과 같이 구성합니다:\n"
                    f"  1. 요약(Summary) 섹션: 회의 내용을 간단히 요약한 텍스트 블록\n"
                    f"  2. 액션 아이템(Action Items) 섹션: 각 액션 아이템을 bullet 블록으로 정리\n"
                    f"모든 정보를 JSON 형식으로 MCP Tool에 전달해 저장을 요청하세요."
                ),
                ("user",
                f"{room_id} 회의 내용을 요약하고 액션 아이템을 추출해 주세요. 그리고 위 기준에 따라 Notion에 저장해 주세요.")
            ]
        })


# 비동기 함수 실행
if __name__ == "__main__":
    result = asyncio.run(run_multi_server_agent())
