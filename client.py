from openai import OpenAI
import os
import httpx
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# MCP Tool definition (like OpenAI's tools schema)
tools = [
    {
        "type": "function",
        "function": {
            "name": "generate_summary",
            "description": "회의 내용을 요약하고 액션 아이템을 정리합니다.",
            "parameters": {
                "type": "object",
                "properties": {
                    "room_id": {
                        "type": "string",
                        "description": "요약할 회의의 room ID"
                    }
                },
                "required": ["room_id"]
            }
        }
    }
]

# Function execution handling
def call_tool(tool_call):
    if tool_call.function.name == "generate_summary":
        args = eval(tool_call.function.arguments)  # or use json.loads()
        room_id = args["room_id"]
        response = httpx.post(
            "http://localhost:8000/summarize",
            json={"room_id": room_id},
            timeout=30.0  # wait up to 30 seconds
        )
        result = response.json()["summary"]["summary"]
        return {
            "tool_call_id": tool_call.id,
            "output": result
        }

# Send request to LLM
response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": "test-room 회의 내용을 요약하고 액션 아이템을 알려줘"}
    ],
    tools=tools,
    tool_choice="auto"
)

# Check if tool call is made
if response.choices[0].finish_reason == "tool_calls":
    tool_call = response.choices[0].message.tool_calls[0]
    tool_result = call_tool(tool_call)

    # Pass tool response to LLM to get final summary
    final = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "user", "content": "test-room 회의 내용을 요약하고 액션 아이템을 알려줘"},
            {
                "role": "assistant",
                "tool_calls": [tool_call]
            },
            {
                "role": "tool",
                "tool_call_id": tool_result["tool_call_id"],
                "content": tool_result["output"]
            }
        ]
    )
    print("📋 최종 요약:\n", final.choices[0].message.content)
else:
    print("🔹 요약 결과:\n", response.choices[0].message.content)