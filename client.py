from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor, create_openai_functions_agent
from langchain_core.tools import tool
from langchain.prompts import ChatPromptTemplate
import httpx

load_dotenv()

# MCP 도구 정의
@tool(description="회의 내용을 요약하고 액션 아이템을 정리합니다.")
def generate_summary(room_id: str) -> str:
    response = httpx.post(
        "http://localhost:8000/summarize",
        json={"room_id": room_id},
        timeout=30.0
    )
    return response.json()["summary"]["summary"]

# LLM 설정
llm = ChatOpenAI(model="gpt-4o-mini")

# 프롬프트 구성
prompt = ChatPromptTemplate.from_messages([
    ("system", "당신은 회의 내용을 요약하고 액션 아이템을 추출하는 도우미입니다."),
    ("user", "{input}"),
    ("assistant", "{agent_scratchpad}")
])

# LangChain 에이전트 설정
tools = [generate_summary]
agent = create_openai_functions_agent(
    llm=llm,
    tools=tools,
    prompt=prompt
)
executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# 실행
response = executor.invoke({"input": "test-room 회의 내용을 요약하고 액션 아이템을 알려줘"})
print("📋 최종 요약:\n", response["output"])